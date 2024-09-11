from uvicorn import run
from fastapi import FastAPI, Query, BackgroundTasks, HTTPException, File, UploadFile  # , Depends, Body
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('settings',f'ai-agents-project-key.json')
from dotenv import load_dotenv
load_dotenv()
import autogen
import numpy as np
import random
import json
import shutil
from typing import Annotated, Literal

from tools.selenium import *
from tools.web import web_search, web_page
from tools.twilio import sms_send
from tools.info import *

from agents.agents import *
agents_const = [agent_planner, agent_secretary]
agents_hire = [agent_browser, agent_researcher]
agents_all = agents_const + agents_hire

from settings.func import *
from plan import *
from review.func import dbname, log_report

import warnings
seed = 123
np.random.seed(seed)
random.seed(seed)
warnings.filterwarnings("ignore")
clean_memory()

# =============================================================================
# Browser functions
# =============================================================================
agent_details = user_info()
browser_driver = init_driver()
browser_driver_el = init_elements(None, None, gcp_agent_folder())

set_browser = {
    'step': "Describe the specific action being taken with general context and task goals",
    'sleep_link': 4,
    'sleep_click': 4,
    'sleep_box_fill': 2,
    'scrollBy': 900,
    'scroll_limit': 3000,
    }

def browser_link_goto(
        step: Annotated[str, set_browser['step']],        
        url: Annotated[str, "URL to navigate page to."],        
        sleep: Annotated[int, f"Time in seconds to wait for the page to fully load, default is {set_browser['sleep_link']} seconds"] = set_browser['sleep_link']
        ) -> str:
    return link_goto(browser_driver, browser_driver_el, step, sleep, url)

def browser_button_click(
        step: Annotated[str, set_browser['step']],        
        button: Annotated[str, "Name of the button to click."],        
        sleep: Annotated[int, f"Time in seconds to wait for the page to fully load, default is {set_browser['sleep_click']} seconds."] = set_browser['sleep_click'],        
        ) -> str:
    return button_click(browser_driver, browser_driver_el, step, sleep, button)

def browser_box_fill(
        step: Annotated[str, set_browser['step']],        
        box: Annotated[str, "Box name to send text to."],        
        text: Annotated[str, "Text to send to box."],        
        hit_return: Annotated[bool, f"Press RETURN after input, default is False."] = False,        
        sleep: Annotated[int, f"Wait time in seconds after RETURN, default is {set_browser['sleep_box_fill']} seconds."] = set_browser['sleep_box_fill'],        
        ) -> str:
    return box_fill(browser_driver, browser_driver_el, step, sleep, box, text, hit_return) 

def browser_scroll(
        step: Annotated[str, set_browser['step']],        
        scrollBy: Annotated[int, f"Scroll by browser in pixels, default around {set_browser['scrollBy']}."] = set_browser['scrollBy'],
        direction: Annotated[str, f"Direction of scrolling: 'up' or 'down', default 'down'."] = 'down',
        ) -> str:
    return page_scroll(browser_driver, browser_driver_el, step, scrollBy, set_browser['scroll_limit'], direction)

def browser_vision(
        step: Annotated[str, set_browser['step']],        
        task: Annotated[str, "Describe remaining steps of the plan to realize the task."],                
        ) -> str:
    return page_vision(browser_driver, browser_driver_el, step, task)

def phone_sms_send(
        body_msg: Annotated[str, "Message body"],
        to_nr: Annotated[str, "Receipient phone number, ex. +48665937049"],
        ) -> str:
    return sms_send(body_msg, to_nr, user_phone_nr())



# =============================================================================
# Tools register
# =============================================================================
autogen.register_function(browser_link_goto, caller=agent_browser, executor=executor,
    name="browser_link_goto", 
    description="""
    Navigates to a specified link (optinally to url with https).
    Outputs actionable elements of the page.
    """
)

autogen.register_function(browser_button_click, caller=agent_browser, executor=executor,
    name="browser_button_click", 
    description="""
    Clicks on a button specified by name.
    Outputs actionable elements of the page.
    """
)

autogen.register_function(browser_box_fill, caller=agent_browser, executor=executor,
    name="browser_box_fill", 
    description="""
    Sends text to box specified by name.
    Outputs actionable elements of the page.
    """
)

autogen.register_function(browser_scroll, caller=agent_browser, executor=executor,
    name="browser_scroll", 
    description="""
    Scrolls the page up or down by a specified number of pixels.
    Outputs actionable elements of the page.
    """
)

autogen.register_function(browser_vision, caller=agent_browser, executor=executor,
    name="browser_vision", 
    description="""
    Provides suggestions on actions and page general info (based on page elements and a screenshot). 
    Useful for troubleshooting and next steps.
    """
)

autogen.register_function(user_info, caller=agent_browser, executor=executor,
    name="user_info",
    description="""
    Retrieves my user info to apply in the browser: emails, passwords, usernames etc.
    """
)

autogen.register_function(web_search, caller=agent_researcher, executor=executor,
    name="web_search",
    description="""
    Searches internet with query, providing concise or detailed content as needed.
    """
)

autogen.register_function(web_page, caller=agent_researcher, executor=executor,
    name="web_page",
    description="""
    Retrieves website content by scraping URL. 
    Efficient and effective to collect public information.
    """
)

# =============================================================================
# FastAPI
# =============================================================================
app = FastAPI(
    title="Autogen Agents with Selenium Browser API",
    description='Following details API enlist methods',
    version="0.0.1",
    terms_of_service="<link>",
    contact={
        "name": "Pawel",
        "url": "https://geekforce.io",
        "email": "pawel.masior@geekforce.io",
    },
    license_info={
        "name": "Samlpe licence",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

origins = [
    #"https://domain.com",
    "http://localhost",
    "http://localhost:5000",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home(): return 'hello'
            
@app.get("/job/")#, tags=["APIs"], response_model=str)
def _stream(
        task: str = Query("Login to gmail.com and send sample email to pawel.masior@geekforce.io."),
        bool_plan: bool = Query(True),
        ):
    Plan = plan_init(task, agents_all) if bool_plan else [task]

    print(f'\n# Plan for task: {task}')
    print(''.join(['=']*60))
    print(f"""\n{''.join(['=']*60)}\n""".join(Plan))
    print('\n')

    print('Running Conversation:')
    print('# '+''.join(['=']*20))
    agents_tool = agents_hire # to apply filter here
    agents_chat = agents_const + agents_tool
    group_chat = autogen.GroupChat(
        agents=agents_chat,
        messages=[],
        max_round=20,
    )
    group_chat_manager = autogen.GroupChatManager(
        groupchat=group_chat,
        llm_config={"config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}]},
    )
    for agent in agents_tool:
        agent.register_nested_chats(
            trigger=group_chat_manager,
            chat_queue=[
                {"recipient": agent, "sender": executor, "summary_method": "last_msg"},
                {"recipient": group_chat_manager, "sender": agent, "summary_method": "reflection_with_llm"},
                {"recipient": agent_planner, "sender": agent, "summary_method": "reflection_with_llm"},
                {"recipient": agent_secretary, "sender": agent, "summary_method": "reflection_with_llm"},
                ],)
    for agent in [agent_secretary]:
        agent.register_nested_chats(
            trigger=group_chat_manager,
            chat_queue=[
                {"recipient": agent, "sender": executor, "summary_method": "last_msg"},
                {"recipient": group_chat_manager, "sender": agent, "summary_method": "reflection_with_llm"},
                {"recipient": agent_planner, "sender": agent, "summary_method": "reflection_with_llm"},
                ],)  

    logging_session_id = autogen.runtime_logging.start(config={"dbname": dbname})
    chat_results = agent_planner.initiate_chats([{
                "recipient": group_chat_manager,
                "message": f"""
                Complete Milestone: {t}

                # Use my info:
                    {user_info()}

                # Additional intructions:
                    - Focuse on the Milestone and perform only necessary steps.                
                    - Go to next Milestone when previous Milestone is completed.
                    - Continue work untill Milestone goal is completed. 
                """,
                "max_turns": 20,
                "max_round": 48,
                "summary_method": "reflection_with_llm",
            } for t in Plan])
    autogen.runtime_logging.stop()

    if not 'chat_results' in globals(): chat_results = [[]]
    log_report(dbname, logging_session_id, task, Plan, chat_results)

    browser_driver.quit()
    clean_memory()
    return 'Check conversation report'


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5001))
    run(app, host="0.0.0.0", port=port)

