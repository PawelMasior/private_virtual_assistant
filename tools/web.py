import os
import re
import json
from tavily import TavilyClient, MissingAPIKeyError
from typing import Annotated, Literal
from firecrawl import FirecrawlApp

set_search = {
    'method': 'detailed',
    'search_depth': 'basic',
    'topic': 'general',
    'days': 7,
    'max_results': 3,
    'include_images': False,
    'include_answer': False,
    'include_raw_content': False,
    'include_domains': None,
    'exclude_domains': None,
}

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
try:
    tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
except MissingAPIKeyError:
    print("API key is missing. Please provide a valid API key.")
    
def web_search(
        query: Annotated[str, "The query string to search for."],
        method: Annotated[str, f"Choose 'concise' for a brief answer or 'detailed' for comprehensive content. Default '{set_search['method']}'."] = set_search['method'],
        topic: Annotated[str, f"The category of the search. Choose between 'general' or 'news'. Default '{set_search['topic']}'."] = set_search['topic'],
        days: Annotated[int, f"The number of days back from today to include in the search results. Only relevant for 'news' topic. Default {set_search['days']}."] = set_search['days'],
        max_results: Annotated[int, f"The maximum number of search results to return. Default {set_search['max_results']}."] = set_search['max_results'],
    ) -> str:
    if method == 'concise':
        result = tavily_client.qna_search(query, topic=topic, days=days, max_results=max_results)
    elif method == 'detailed':
        result = tavily_client.get_search_context(query, topic=topic, days=days, max_results=max_results)
        result_str = f"""{result}""".replace("\\","")
        result_re = re.compile(r'\{.*?\}').findall(result_str)
        result = '\n'.join(result_re)
    else:
        result = 'Wrong method input'
    return result

# =============================================================================
# include_images: Annotated[bool, "Include a list of query-related images in the response. Defaults to False."] = set_search['include_images'],
# include_answer: Annotated[bool, "Include a short answer to the original query. Defaults to False."] = set_search['include_answer'],
# include_raw_content: Annotated[bool, "Include the cleaned and parsed HTML content of each search result. Defaults to False."] = set_search['include_raw_content'],
# include_domains: Annotated[Optional[List[str]], "A list of domains to specifically include in the search results. Defaults to None, which includes all domains."] = set_search['include_domains'],
# exclude_domains: Annotated[Optional[List[str]], "A list of domains to specifically exclude from the search results. Defaults to None, which excludes no domains."] = set_search['exclude_domains']
# search_depth: Annotated[str, "The depth of the search. 'basic' for basic results or 'advanced' for more detailed results. Defaults to 'basic'."] = set_search['search_depth'],
# =============================================================================

firecrawl = FirecrawlApp(api_key=os.environ['FIRECRAWL_API_KEY'])

def web_page(
        url: Annotated[str, "Url"],
        context: Annotated[str, "Information you want to identify."],
    ) -> str:
    
    page_content = firecrawl.scrape_url(
        url=url,
        params={
            "pageOptions":{
                "onlyMainContent": True
            }
        })
    msg = page_content['markdown']
    # to trimm with chat if tokens too much
    return msg


# =============================================================================
# def func to review specific web for query information
# import requests
# from bs4 import BeautifulSoup
# import markdownify
# def fetch_html_content(url):
#     try:
#         # Set headers to mimic a browser visit
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         # Make a GET request to fetch the raw HTML content
#         response = requests.get(url, headers=headers)
#         response.raise_for_status()  # Check if the request was successful
        
#         # Return the HTML content
#         return response.text
    
#     except requests.exceptions.RequestException as e:
#         return f"An error occurred: {e}"

# def convert_html_to_markdown(html_content):
#     # Parse the HTML with BeautifulSoup
#     soup = BeautifulSoup(html_content, 'html.parser')
    
#     # Use markdownify to convert the HTML to Markdown
#     markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")
#     return markdown_content

# # Example usage
# html_content = fetch_html_content(url)

# if 'An error occurred' not in html_content:
#     markdown_content = convert_html_to_markdown(html_content)
#     print(markdown_content)
# else:
#     print(html_content)