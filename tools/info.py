import json
import os
from typing import Annotated, Literal

def user_info(
    ) -> str:
    agent_info = {
        'name': 'John Smith',
        'birth_date': '12th January 2001',    
        'company': 'Agent Company',
        'email': 'john.smith.agentai@gmail.com',
        'password': 'StrongPassword123!123',
        'describtion': 'You are regular user',
        'twitter_user_name': 'smith_john56714',
        }
    agent_details = {k.replace('_',' '): agent_info[k] for k in [
        'name', 'birth_date', 'company', 'email', 'password', 'twitter_user_name']}

    return json.dumps(agent_details)

def user_phone_nr(
    ) -> str: 
    return '+48732096499'

def gcp_agent_folder(
    ) -> str: 
    return 'agent-johnsmith'

folder = 'temporary'
report_name = 'report.md'
def save_report(
        markdown_content: Annotated[str, "Markdown content of report"],
        ) -> str:
    try:
      with open(os.path.join(folder, report_name), 'w') as f:
          f.write(markdown_content)
      return f"Success: saved report to '{report_name}'"
    except Exception as e:
        return f"Error: {str(e)[:200]}"
# print(save_report(markdown_content))

def read_report(
        report_name: Annotated[str, "Markdown content of report"] = report_name,        
        ) -> str:
    try:
        folder = 'temporary'
        report_name = 'report.md'
        with open(os.path.join(folder, report_name), 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)[:200]}"
# print(read_report(report_name))