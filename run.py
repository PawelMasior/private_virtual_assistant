# %reset -f
from dotenv import load_dotenv
load_dotenv()
import os
from review.func import dbname, log_report
from plan import plan_init
from agents.agents import *
agents_const = [agent_planner, agent_secretary]
agents_hire = [agent_browser, agent_researcher]
agents_all = agents_const + agents_hire

# =============================================================================
# # Apply your task here and Planning information
# =============================================================================
Tasks = [
    "Go to https://2captcha.com/demo/recaptcha-v3 and solve the puzzle - finish once done.",
    # "Prepare a report what to do during Winobranie Zielona Gora 2024: music concerts, restaurants etc.; and save all info in the report. DONT USE BROWSER AGENT.",
]
for task in Tasks: 0
bool_plan = False

Plan = plan_init(task, agents_all) if bool_plan else [task]

# Plan = ['Login to gmail.com',
#         'Send email to pawel.masior@geekforce.io']

print(f'\n# Plan for task: {task}')
print(''.join(['=']*60))
print(f"""\n{''.join(['=']*60)}\n""".join(Plan))
print('\n')

print('Running Conversation:')
print('# '+''.join(['=']*20))
with open(os.path.join(os.getcwd(), 'initialize.py')) as f:
    exec(f.read(), globals())

agents_tool = agents_hire #filter here
#agents_tool = [agent_researcher] #filter here
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
for i, agent in enumerate(agents_chat): 
    if agent.name == 'Planner': pass
    else:
        agents_other = [a for i_a, a in enumerate(agents_chat) if i!=i_a]
        queue=[
            {"recipient": agent, "sender": executor, "summary_method": "last_msg"},
            {"recipient": group_chat_manager, "sender": agent, "summary_method": "reflection_with_llm"},
            ] + [{"recipient": a, "sender": agent, "summary_method": "reflection_with_llm"} for a in agents_other]
        agent.register_nested_chats(trigger=group_chat_manager, chat_queue=queue)

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
            "max_round": 60,
            "summary_method": "reflection_with_llm",
        } for t in Plan])
autogen.runtime_logging.stop()

# if not 'chat_results' in globals(): chat_results = [[]]
log_report(dbname, logging_session_id, task, Plan, chat_results)

# browser_driver.quit()
# clean_memory()


