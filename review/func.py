#%reset -f

import os 
# =============================================================================
# dbname = os.path.join('review',f"logs copy.db")
# =============================================================================
dbname = os.path.join('review',f"logs.db")
from PIL import Image, ImageDraw, ImageFont
import json
import numpy as np
import pandas as pd
import copy
import sqlite3
from pprint import pprint
from types import SimpleNamespace
from datetime import datetime, timedelta
from fpdf import FPDF
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import matplotlib.image as image
import matplotlib.ticker as mtick
import matplotlib.dates as mdates
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.ticker as ticker
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D
from settings.plot import _style, _bytes, plt_c, _ffont
import textwrap

# =============================================================================
# logging_session_id='f53e51b8-1ac5-4736-9446-0aff8e60e0fe'
# logging_session_id = '5db38f4f-4c06-47d2-8a06-039c8354acf9'
# =============================================================================
json_group = {'source_name': 'Agents','idx': 'Conversation',}
json_measure = {
    'time_sec': 'Time sec',
    'cost': 'Cost',
    #'total_tokens': 'Tokens total',
    }    

def tbl_data(dbname = dbname, tbl="chat_completions", filter_col='session_id', filter_val=''):
    con = sqlite3.connect(dbname)
    query = f"""SELECT * FROM {tbl} WHERE {filter_col}='{filter_val}'""" #
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data

def tbl_data_t(dbname = dbname, tbl="events", time_min_str='', time_max_str=''):
    con = sqlite3.connect(dbname)
    query = f"""SELECT * FROM {tbl} WHERE timestamp>='{time_min_str}' AND timestamp>='{time_min_str}'""" #
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data

def db_data(dbname, logging_session_id):
    # agents
    agents = tbl_data(dbname = dbname, tbl="agents", filter_col='session_id', filter_val=logging_session_id)
    agents_data = []
    for i,d in enumerate(agents[:]):
        d_init_args = json.loads(d['init_args'])    
        chat_messages_count = 0
        chat_messages = d_init_args['chat_messages']
        if chat_messages:
            for k,v in chat_messages.items(): 
                chat_messages_count += len(v)
        out = {k: v for k,v in d.items() if k not in ['init_args','chat_messages']}
        out['system_message'+'_count'] = len(d_init_args['system_message'])
        out['chat_messages'+'_count'] = chat_messages_count
        agents_data += [out]
    df_a = pd.DataFrame(agents_data)
    df_a['id_session'] = 1*(1==df_a['chat_messages'+'_count'])
    df_a['id_session'] = df_a['id_session'].cumsum().clip(lower=1)
    df_a['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_a['timestamp']]
    df_a['end_time'] = df_a['timestamp']
    # print('df_a', df_a['timestamp'].min(), df_a['timestamp'].max())
    
    # conversations
    chat_completions = tbl_data(dbname = dbname, tbl="chat_completions", filter_col='session_id', filter_val=logging_session_id)
    chat_completions_data = []
    for i,d in enumerate(chat_completions[:]):
        out = {k: v for k,v in d.items() if k not in ['request','response']}
        
        d_request = json.loads(d['request'])    
        out['messages'+'_count'] = len(d_request['messages'])
        out['message_start'] = d_request['messages'][1]['content']
        d_response = json.loads(d['response'])
        if 'usage' in d_response.keys():
            out = {**out,**d_response['usage']}
        if 'choices' in d_response.keys():
            out['message_end'] = d_response['choices'][0]['message']['content']
            out['finish_reason'] = d_response['choices'][0]['finish_reason']
        chat_completions_data += [out]
    df_c_c = pd.DataFrame(chat_completions_data)
    df_c_c['start_time'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_c_c['start_time']]
    df_c_c['end_time'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_c_c['end_time']]
    df_c_c['time_sec'] = (df_c_c['end_time'] - df_c_c['start_time']).dt.total_seconds()
    df_c_c = df_c_c.sort_values(by=['end_time']).reset_index(drop=True)
    # print('df_c_c', df_c_c['start_time'].min(), df_c_c['end_time'].max())
    
    # sequential
    df_s = df_a.groupby(['id_session']).agg({'timestamp': 'first',
        }).reset_index(drop=False).sort_values(by=['timestamp'], ascending=[True])
    df_s['idx'] = [df_c_c[df_c_c['start_time'] >= t].index.min() for t in df_s['timestamp']]
    df_s['end'] = list(df_s['idx'][1:]) + [df_c_c.shape[0]-1]
    df_s['message_start'] = [df_c_c.iloc[i]['message_start'] for i in df_s['idx']]
    df_s['message_end'] = [df_c_c.iloc[i]['message_end'] for i in df_s['end']]
    
    time_min_str = (df_a['timestamp'].min()-timedelta(seconds=2)).strftime('%Y-%m-%d %H:%M:%S.%f')
    time_max_str = (df_c_c['end_time'].max()+timedelta(seconds=2)).strftime('%Y-%m-%d %H:%M:%S.%f')

    # events
    data_events = tbl_data_t(dbname, "events", time_min_str, time_max_str)
    for i,d in enumerate(data_events):
        d_new = {**d, **json.loads(d['json_state'])}
        d_new.pop('json_state')
        data_events[i] = d_new
    df_ev = pd.DataFrame(data_events)
    df_ev['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_ev['timestamp']]
    id_step_event = [1] 
    for i,r_0 in df_ev.iloc[1:,:].iterrows():
        r_1 = df_ev.iloc[i-1]
        if r_1['source_name'] == r_0['source_name']: id_step_event += [id_step_event[-1]]
        else: id_step_event += [id_step_event[-1]+1]
    df_ev['id_step_event'] = id_step_event
        
    # function_calls
    data_function_calls = []
    for source_name in df_ev['source_name'].unique()[:]:
        e = tbl_data(dbname = dbname, tbl="function_calls", filter_col='source_name', filter_val=source_name)
        data_function_calls += e
    df_f_c = pd.DataFrame(data_function_calls)
    df_f_c['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_f_c['timestamp']]
    return df_a, df_c_c, df_s, df_ev, df_f_c

# =============================================================================
#     data, go, i, d, data_json_state = [], True, 1, [0],[]
#     while len(d):
#         d = tbl_data(dbname = dbname, tbl="events", filter_col='id', filter_val=i)
#         if len(d): 
#             data_json_state += [json.loads(d[0].pop('json_state'))]
#             data += d
#         i+=1
#     df_ev = pd.DataFrame(data)
#     df_ev = df_ev.merge(pd.DataFrame(data_json_state), left_index=True, right_index=True, how='left')
#     df_ev['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_ev['timestamp']]
#     id_step_event = [1] 
#     for i,r_0 in df_ev.iloc[1:,:].iterrows():
#         r_1 = df_ev.iloc[i-1]
#         if r_1['source_name'] == r_0['source_name']:
#             id_step_event += [id_step_event[-1]]
#         else: id_step_event += [id_step_event[-1]+1]
#     df_ev['id_step_event'] = id_step_event
#     print('df_ev', df_ev['timestamp'].min(), df_ev['timestamp'].max())
# =============================================================================


    
# =============================================================================
#     df_o_c = pd.DataFrame(tbl_data(tbl="oai_clients", filter_col='session_id', filter_val=logging_session_id))
#     df_o_c['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_o_c['timestamp']]
#     print('df_o_c', df_o_c['timestamp'].min(), df_o_c['timestamp'].max())
# 
#     df_o_w = pd.DataFrame(tbl_data(tbl="oai_wrappers", filter_col='session_id', filter_val=logging_session_id))
#     df_o_w['timestamp'] = [datetime.strptime(t, '%Y-%m-%d %H:%M:%S.%f') for t in df_o_w['timestamp']]
#     print('df_o_w', df_o_w['timestamp'].min(), df_o_w['timestamp'].max())
# =============================================================================
# =============================================================================
#     # version
#     data, go, i, d = [], True, 1, [0]
#     while len(d):
#         d = tbl_data(dbname = dbname, tbl="version", filter_col='id', filter_val=i)
#         if len(d): data += d
#         i+=1
#     df_v = pd.DataFrame(data)
# =============================================================================
def plt_bar(df_c_c, df_s, color_map, group='idx', measure='cost'):
    df_l = df_c_c
    df_l['color'] = df_l['source_name'].map(color_map)    
    df_l['idx'] = df_l.index
    df_l['Steps'] = df_l.index
    df_l['Agents'] = df_l['source_name']
    df = df_l.groupby([group]).agg({
        'time_sec': 'sum',
        'cost': 'sum',
        'prompt_tokens': 'sum',
        'completion_tokens': 'sum',
        'total_tokens': 'sum',
        'color': 'last',
        'Steps': 'last',
        # 'Tools': 'last',
        'Agents': 'last',
        }).reset_index(drop=False).sort_values(by=[group], ascending=[True])
    

    _style()
    fig, ax = plt.subplots(figsize=(16, 9))
    if df_s.shape[0] > 1 and group == 'idx':
        fig.text(0.77, 0.88, '(Seqetial Chat)', ha='left', color=plt_c['stone-800'], fontproperties=_ffont(24))  
        for i,r in df_s.iterrows():
            ax.axvline(x=r['idx']-.5, ymin=0, ymax=df[f'{measure}'].max()*10e9, color=plt_c['stone-700'],alpha=.5)
    ax.bar(df[group], df[measure], color=df['color'])
    ax.set_xlabel(f"{json_group[group]}", fontproperties=_ffont(32))
    ax.set_ylabel(f'{json_measure[measure]}', fontproperties=_ffont(32))
    ax.set_title(f'{json_measure[measure]}', fontproperties=_ffont(44))
    ax.set_xticks(df[f'{group}'])
    ax.set_xticklabels(df[f'{group}'], rotation=30, fontproperties=_ffont(20))
    ax.grid(axis='y', linewidth=4, color=plt_c['stone-100'])
    handles = [plt.Line2D([0], [0], color=color_map[source], lw=4) for source in df_l['Agents'].unique()]
    legend  = ax.legend(handles, df_l['Agents'].unique(), loc='upper left', prop=_ffont(24), frameon=True)
    legend.get_frame().set_alpha(0.6) 
    fig.tight_layout(rect=[0.025, 0.025, .975, .975])
    name = f'{json_group[group]}_{json_measure[measure]}.png'
    fig.savefig(os.path.join('review',name),dpi=200)
    return name


def plt_timeline_conversation(df_ev, df_s, color_map):
    df = df_ev.groupby(['id_step_event', 'source_name']).agg({
        'timestamp': ['min','max'],
        'reply_func_name': ['first','last'],
        }).reset_index(drop=False)#.sort_values(by=[group], ascending=[True])
    df.columns = [c[0]+c[1] for c in df.columns]
    df = df.rename(columns={'timestampmin':'start_time','timestampmax':'end_time'})
    df['color'] = df['source_name'].map(color_map)    
    
    y_label = {lbl: i for i, lbl in enumerate(np.sort(df['source_name'].unique()))}
    _style()
    fig, ax = plt.subplots(figsize=(32, 9))
    for _, r in df.iterrows():
        y = y_label[r['source_name']]
        ax.barh(y, 
                (r['end_time'] - r['start_time']),#.total_seconds()/100000, 
                left=r['start_time'],
                color=r['color'])
    if df_s.shape[0]>0:
        for t in df_s['timestamp']: 
            ax.axvline(x=t, ymin=0, ymax=len(y_label), color=plt_c['stone-700'],alpha=.5)
    time_b = (df['end_time'].max()-df['start_time'].min())*.1
    ax.set_xlim((df['start_time'].min()-time_b,df['end_time'].max()+time_b))
    ax.set_yticks(list(y_label.values()))
    ax.set_yticklabels(list(y_label.keys()))
    ax.grid(linewidth=4, color=plt_c['stone-100'])
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontproperties=_ffont(20), color=plt_c['stone-900'])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontproperties=_ffont(20), color=plt_c['stone-900'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d%b %H:%M:%S'))
    ax.set_title(f'Timeline Conversation', fontproperties=_ffont(44))
    fig.tight_layout(rect=[0.025, 0.025, .975, .975])
    name = f'Timeline_Conversation.png'
    fig.savefig(os.path.join('review',name),dpi=200)
    return name
    

def plt_timeline_functions(df_f_c, df_ev, df_s):
    palette_f = sns.color_palette("viridis", n_colors=df_f_c['function_name'].nunique())
    color_map_f = dict(zip(df_f_c['function_name'].unique(), palette_f))
    
    df_ev_f = df_ev.groupby(['id_step_event', 'source_name']).agg({
        'timestamp': ['min','max'],
        'reply_func_name': ['first','last'],
        }).reset_index(drop=False)#.sort_values(by=[group], ascending=[True])
    df_ev_f.columns = [c[0]+c[1] for c in df_ev_f.columns]
    df_ev_f = df_ev_f.rename(columns={'timestampmin':'start_time',
                                      'timestampmax':'end_time'})
    
    start_time = []
    for _,r in df_f_c[:].iterrows(): 
        t = r['timestamp']
        i = np.argmin(np.abs(df_ev_f['end_time'] - t))
        d = df_ev_f.iloc[i]
        start_time += [d['start_time']]
    df_f_c['start_time'] = start_time
    df_f_c['end_time'] = df_f_c['timestamp']
    df_f_c['color'] = df_f_c['function_name'].map(color_map_f)    
    df = copy.deepcopy(df_f_c)
    
    y_label = {lbl: i for i, lbl in enumerate(np.sort(df['function_name'].unique()))}
    _style()
    fig, ax = plt.subplots(figsize=(32, 9))
    for _, r in df.iterrows():
        y = y_label[r['function_name']]
        ax.barh(y, 
                (r['end_time'] - r['start_time']),#.total_seconds()/100000, 
                left=r['start_time'],
                color=r['color'])
    if df_s.shape[0]>0:
        for t in df_s['timestamp']: 
            ax.axvline(x=t, ymin=0, ymax=len(y_label), color=plt_c['stone-700'],alpha=.5)
    time_b = (df['end_time'].max()-df['start_time'].min())*.1
    ax.set_xlim((df['start_time'].min()-time_b,df['end_time'].max()+time_b))
    ax.set_yticks(list(y_label.values()))
    ax.set_yticklabels(list(y_label.keys()))
    ax.grid(linewidth=4, color=plt_c['stone-100'])
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontproperties=_ffont(20), color=plt_c['stone-900'])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, fontproperties=_ffont(20), color=plt_c['stone-900'])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d%b %H:%M:%S'))
    ax.set_title(f'Timeline Functions', fontproperties=_ffont(44))
    fig.tight_layout(rect=[0.025, 0.025, .975, .975])
    name = f'Timeline_Functions.png'
    fig.savefig(os.path.join('review',name),dpi=200)
    return name


def plt_all(df_a, df_c_c, df_s, df_ev, df_f_c):

    palette = sns.color_palette("husl", n_colors=df_ev['source_name'].nunique())
    color_map = dict(zip(df_ev['source_name'].unique(), palette))
    
    data_name_bar = []
    for group in json_group.keys():
        for measure in json_measure.keys():
            data_name_bar += [plt_bar(df_c_c, df_s, color_map, group, measure)]
    
    name_timeline_conversation = plt_timeline_conversation(df_ev, df_s, color_map)
    name_timeline_functions = plt_timeline_functions(df_f_c, df_ev, df_s)
    
    _style()
    fig, ax = plt.subplots(figsize=(16*2,9*4))
    fig.patch.set_facecolor('lightgrey')
    ax.axis('off')
    fig.figimage(Image.open(os.path.join('review',data_name_bar[0])), xo=1600*0, yo=900*6, alpha=1.)
    fig.figimage(Image.open(os.path.join('review',data_name_bar[1])), xo=1600*2, yo=900*6, alpha=1.)
    fig.figimage(Image.open(os.path.join('review',data_name_bar[2])), xo=1600*0, yo=900*4, alpha=1.)
    fig.figimage(Image.open(os.path.join('review',data_name_bar[3])), xo=1600*2, yo=900*4, alpha=1.)
    fig.figimage(Image.open(os.path.join('review',name_timeline_conversation)), xo=1600*0, yo=900*2, alpha=1.)
    fig.figimage(Image.open(os.path.join('review',name_timeline_functions)), xo=1600*0, yo=900*0, alpha=1.)
    fig.savefig(os.path.join('review','Summary'),dpi=200)
    
    for n in data_name_bar + [name_timeline_conversation, name_timeline_functions]: 
        try: os.remove(os.path.join('review',n))
        except: print(f'Error: unable to delete {n}')

def markdown_report(task, Plan, chat_results):
    name_task = task.replace(' ','_')
    for s in ['.','!','-','(','[',')',']']:
        name_task = name_task.replace(s,'')
        
    markdown_name = os.path.join("review","report.md")
    markdown_text = f"""
    # Task: 
    **{name_task}**
    
    # Milestones:
        
    """
    for milestone, cr in zip(Plan, chat_results): 
        markdown_text += f"""
    ## Milestone: {milestone}
    ## Summary: {cr.summary}
        
    """
    markdown_text += f"""
    # Logs
    ![image]({os.path.join(os.getcwd(),'review','Summary.png')})
    """
    with open(markdown_name, 'w') as file:
        file.write(markdown_text)
       
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    tuple_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return tuple_color

def _ttl(pdf, ttl, x=10, w=190, y=44, f='', s=12, a='C', h=6, c=plt_c['stone-900']):
    pdf.set_fill_color(hex_to_rgb('#ffffff'))
    pdf.set_text_color(hex_to_rgb(c))
    pdf.set_font('CustomFont', f, size=s)
    pdf.set_left_margin(x)
    pdf.set_y(y)
    pdf.multi_cell(w, h, ttl, 0, align=a)
    return pdf

def pdf_compose(task, Plan, chat_results):
    #print(f"chat_results {chat_results}")
    now = f'{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    now_str = f'{datetime.now().strftime("%H:%M:%S, %d %b%Y")}'
    
    pdf = FPDF()
    pdf.set_line_width(.4)
    pdf.set_text_color(*hex_to_rgb('#666666'))  # Assuming plt_c['stone-800'] is '#666666'
    pdf.add_font('CustomFont', '', os.path.join(os.getcwd(), 'settings', 'Comfortaa', 'Comfortaa-Regular.ttf'))
    pdf.add_font('CustomFont', 'B', os.path.join(os.getcwd(), 'settings', 'Comfortaa', 'Comfortaa-Bold.ttf'))
    pdf.set_font('CustomFont', '', size=10)
    
    pdf.add_page()
    y_set = 20
    pdf = _ttl(pdf, f"""Task""", x=15, s=20, a='L', y=y_set, f='B')
    pdf = _ttl(pdf, f"""{now_str}""", x=0, w=195, s=12, a='R', y=y_set, f='B')
    pdf = _ttl(pdf, f"""{task}""", 
         x=15, y=y_set+10, f='B', s=12, a='L', w=170)
    y_set = min(72, pdf.get_y()+10)
    pdf.image(os.path.join('review','Summary.png'), 10, y_set, 190, 190*(9*4/32), "", "")
    
    if len(chat_results):
        pdf.add_page()
        y_set = 25
        pdf = _ttl(pdf, f"""Milestones""", s=20, y=y_set, f='B')
        
        y_set += 20
        pdf.set_y(y_set)
        for milestone, cr in zip(Plan, chat_results):
            try:
                summary = cr.summary
                _ttl(pdf, f"""Milestone: {milestone}""", s=12, x=15, y=pdf.get_y(), a='L', f='B')
                pdf.set_y(pdf.get_y()+2)
                #_ttl(pdf, f"""Summary""", s=12, x=15, y=pdf.get_y(), a='L', f='B')
                _ttl(pdf, f"""{summary}""", s=12, x=15, y=pdf.get_y(), a='L', f='')        
                pdf.set_y(pdf.get_y()+10)
            except: 0
    
    name_task = task.replace(' ','_')
    for s in ['.','!','-','(','[',')',']',':','/']:name_task = name_task.replace(s,'')
    pdf.output(os.path.join("review","reports", f"Report_{name_task}.pdf"))
       
def log_report(dbname, logging_session_id, task, Plan, chat_results):
       
    df_a, df_c_c, df_s, df_ev, df_f_c = db_data(dbname = dbname, 
                                                logging_session_id=logging_session_id)
    plt_all(df_a, df_c_c, df_s, df_ev, df_f_c)
    pdf_compose(task, Plan, chat_results)
    os.remove(os.path.join('review','Summary.png'))
