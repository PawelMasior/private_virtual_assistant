import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join('keys',f'ai-agents-project-431615-da1ce680b550.json')
import numpy as np
import pandas as pd
import re
import time
import random
from copy import deepcopy
# from json import loads, dumps
# from PIL import Image, ImageDraw, ImageFont
import openai
from openai import OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
client_openai = OpenAI()
from agents.agents import *

# =============================================================================
# task = 'Go to otomoto.pl and find newest Audi and provide me a phone number to the seller'
# task = 'Go to google maps and find best pizzeria in Wroclaw and provide me a phone number'
# task = 'Login to gmail.com'
# task = 'Login to x.com and write some positive comments under Donald Trump post'
# task = 'Go to google maps and find best pizzeria in Wroclaw and provide me a phone number'
# =============================================================================
def plan_agents(group_agents):
    prompt_agents = ''
    if len(group_agents):
        prompt_agents = f"""## Agents describtion:"""
        for a in group_agents: 
            prompt_agents += f"\n###{a.__dict__.get('_name')}"
            prompt_agents += f"\n{a.__dict__.get('_description')}"
    return prompt_agents

def plan_init(task='', group_agents=[]):
    prompt = f"""
    # Generate a detailed milestones plan in Markdown for the task:
    **{task}**

    You may create one or more milestones based on the task's complexity.

    ## Each Milestone contains:
    - **Start** Each starts with triple hashes (###) with title.
    - **Goal:** Clearly defined objectives and simple verification.
    - **Hire:** Define agents to use with responsibilities.
    - **Complexity:** Group milestones with similar complexity levels.
        - Example of a single milestone: 
            - Login to Gmail, 
            - Search on Google, 
            - Verify task completion,
            - etc..
    - **Context:** Focus on the current task only.
    - **End** Each milestone ends with by tripple equations in new line (===).

    ## Milestone constrains:
    - A milestone must reflect levels of achievement rather than one or two actions.

    {plan_agents(group_agents)}
    """
    # print(prompt)
    response = client_openai.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
         {
          "role": "user",
          "content": [{ "type": "text", "text": prompt,},],
          }
      ],
      max_tokens=1000,
      temperature=0.
    )
    plan = response.choices[0].message.content
    # print(plan)
    pattern = re.compile(r'### (.*?)(?====)', re.DOTALL)
    plan_list = pattern.findall(plan)
    # print('# ====================\n'.join(plan_list))
    # print('\n'.join(plan_list))
    return plan_list   
    
# =============================================================================
#     name_plan = "plan.md"
#     print(plan)
#     with open(name_plan, 'w') as file:
#         file.write(plan)
#     with open(name_plan, 'r') as file:
#         markdown_text = file.read()
# =============================================================================
# =============================================================================
# agent_browser.llm_config["tools"]
# =============================================================================