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
# =============================================================================
bool_plan = True
Tasks = [
    "Login to linkedin.com and find and connect with Łukasz Kwiatkowski Tar Heel Capital.",
    "Login to linkedin.com and send a message to Pawel Masior saying 'Nice to connect with you.'",
    "Login to linkedin and post you are happy to be on the platform.'",
    "Login to linkedin.com and get my linkeding profile url",
    "Login to gmail.com.",
    "Login to gmail.com and send email to pawel.masior@geekforce.io.'",
    "Login to gmail.com and compose an email to pawel.masior@geekforce.io.. Keep in the email information on weather in Wroclaw for next 7 days.",
    "Login to gmail.com. and send email to lukasz.kwiatkowski@geekforce.io saying you are excited to meet today at 3pm",
    "Login to woodpecker.co.'",
    "Login to woodpecker.co.' and start a sample campaign",
    "Login to x.com.'",
    "Login to x.com and post 'Hello world.'",
    "Login to x.com and post something interesting.",
    "Go to olx.pl and search for newest Audi.'",
    "Go to otomoto.pl and search for newest Audi - get the phone number to the seller.'",
    "Go to google.com and search Banana trees",
    "Go to google.com and search Donald Trump.'",
    "Go to google maps and find best pizzeria in Wroclaw - give me a number of the best one.'",
    "Go to google maps and write a positive comment under Hotel Podkowa in Wroclaw.'",
    "Find Audi for sale on otomoto - provide phone number to the seller.'",
    "Find Audi for sale on olx - provide phone number to the seller.'",
    "Find Audi for sale on allegro.pl - provide phone number to the seller.'",
    "Find phone number to pizzeria 'Piec Na Szewskiej' in Wroclaw.'",
    "Find the phone number of the best pizzeria in Wroclaw - use only Reasearcher and Planner (do not use Browser!).",
    "Prepare a report what to do during Winobranie Zielona Gora 2024: music concerts, restaurants etc.; and save all info in the report. DONT USE BROWSER AGENT.",
    "Use Secretary: Send SMS to +48665937049 'how are you' and verify if sent. Dont use Researcher or Browser.",
]

for task in Tasks:
    Plan = plan_init(task, agents_all) if bool_plan else [task]
    
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

