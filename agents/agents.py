import os
import autogen

llm_config={
    "cache_seed": 44,
    "temperature": 0,
    # "config_list": [{"model": "gpt-3.5-turbo", "api_key": os.environ["OPENAI_API_KEY"]}],
    # "config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}],
    # "config_list": autogen.config_list_from_dotenv(".env", {"gpt-4o": "OPENAI_API_KEY"}), #gpt-4o-mini
    # "config_list": autogen.config_list_from_dotenv(".env", {"gpt-3.5-turbo": "OPENAI_API_KEY"}),
    # "config_list": autogen.config_list_from_dotenv(".env", {"gpt-4o-mini": "OPENAI_API_KEY"}),
    # "config_list": [{"model": "gpt-4o-mini", "api_key": os.environ["OPENAI_API_KEY"]}],
    "config_list": [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}],
    "timeout": 120,
    }

executor = autogen.ConversableAgent(
    name="tool_executor",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    default_auto_reply="TERMINATE",
    human_input_mode="NEVER",
)

agent_human = autogen.ConversableAgent(
    name="HumanProxy",
    system_message="""
    ## You are agent connectint to human user for additional actions in the browser like fill pycatcha etc.
    Maybe secretary can do this?? or some tool??
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=10,
    human_input_mode="NEVER",
)

agent_planner = autogen.ConversableAgent(
    name="Planner",
    system_message = """
    ## You are the Planner responsible for overseeing the progress of the task and coordinating with other agents.
    
    ### Goal
    - Create a plan to complete the given task.
    - Verify if the task is completed.
    
    ### Responsibilities
    **Plan Development and Execution:**
    - **Create Plan:** Outline specific steps needed to complete the task with responsible agents.
    - **Coordinate Agents:** Ensure agents and their tools are aligned with the plan.
    - **Monitor Progress:** Track the progress of each step and verify completion or if additional steps are required.
    - **Make Decisions:** Make high-level decisions based on info from agents.
    **Error Handling:**
    - **Handle Errors:** Develop a new plan or adjust actions if errors occur or if responses are incorrect.
    - **Guide Adjustments:** Direct agents on necessary changes to achieve task goals.

    ### Reply 'TERMINATE' when the whole task is completed.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=3,
    human_input_mode="NEVER",
)

agent_secretary = autogen.ConversableAgent(
    name="Secretary",
    system_message = """
    ## You are Secretary.

    ### Responsibilities
    - **Wrap up final information into raport.md**

    ### Reply 'TERMINATE' when the task is complete.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=3,
    human_input_mode="NEVER",
)
# - **Send and read SMS.**
# - **Provide user information**

agent_browser = autogen.ConversableAgent(
    name="Browser",
    system_message = """
    # You are Browser assistant applying actions in already opened browser with your tools to complete the task. 
    
    ### Your Role
    - **Interact with the Browser** Use your Tools to apply actions.
    - **Provide Tools Output:** Return the results from the executed tools and what has been achieved to other agents.
    - **Provide Results:** Return the information what has been acieved with tools to other agents.
    
    **Tools Guidelines:**
    - Navigate to link.
    - Enter text into box.
    - Click on button.
    - Scroll the page only if you need to identify more search results.
    - Use vision tools for deeper inspection aor verification of current page window and its elements.

    **Action Guidelines:**
    - **Cookies:** Always suggest to accept cookies first (e.g., "Allow All," "Accept Cookies") to ensure full page visibility.
    - **Pop-up windows:** Always close the window or make sure it doesnt appear any longer  to ensure full page visibility.
    - **Interactions:** Only interact with existing text boxes, links and buttons. You can scroll page if necessary.
    - **Avoid:** Avoid buttons for login or registration via Google, Apple, Facebook, etc.
    - **Exit Loop or Repeating Action:** Request other agents for help.

    ### Reply 'TERMINATE' when the whole task is completed.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
)

agent_researcher = autogen.ConversableAgent(
    name="Researcher",
    system_message="""
    # You are the Researcher collecting information directly from the web. (not in browser).

    ### Your Role
    - **Provide Tools Output:** Return results from executed tools to other agents.
    - **Provide Results:** Report findings to other agents.
    - **Deep dive:** Adjust research to gather precise information as needed.

    ### Reply 'TERMINATE' when the whole task is completed.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=5,
    human_input_mode="NEVER",
)

agent_assistant = autogen.ConversableAgent(
    name="Assistant",
    system_message="""
    ## You are Assistant.
    """,
    llm_config=llm_config,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    max_consecutive_auto_reply=2,
    human_input_mode="NEVER",
)
