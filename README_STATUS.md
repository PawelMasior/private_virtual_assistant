# Autogen Agents with Selenium Browser 🚀

This repository contains a deep dive into using Autogen with Selenium Browser techniques.

### ✅ Tested Use Cases

Working use cases in development:

- Login to linkedin.com and send a message to Pawel Masior saying 'Nice to connect with you.'
- Login to linkedin.com and follow Pawel Masior.
- Login to linkedin and post you are happy to be on the platform.'
- Login to linkedin.com and get my linkeding profile url
- Login to gmail.com.
- Login to gmail.com and send email to pawel.masior@geekforce.io.'
- Login to woodpecker.co.'
- (too complicated yet) Login to woodpecker.co.' and start a sample campaign
- Login to x.com.'
- Login to x.com and post 'Hello world.'
- Login to x.com and post something interesting.
- Go to olx.pl and search for newest Audi.'
- Go to otomoto.pl and search for newest Audi - get the phone number to the seller.'
- Go to google.com and search Donald Trump.'
- Go to google maps and find best pizzeria in Wroclaw - give me a number of the best one.'
- (too complicated yet) Go to google maps and write a positive comment under Hotel Podkowa in Wroclaw.'
- (too complicated yet) Find Audi for sale on otomoto - provide phone number to the seller.'
- (too complicated yet) Find Audi for sale on olx - provide phone number to the seller.'
- (too complicated yet) Find Audi for sale on allegro.pl - provide phone number to the seller.'
- Find phone number to pizzeria 'Piec Na Szewskiej' in Wroclaw.'
- Find the phone number of the best pizzeria in Wroclaw - use only Reasearcher and Planner (do not use Browser!).

## 🔮 Future work

### 📈 Development direction

General development direction

- **Browser Elements:**
  - extend review information to betterr identify key fixes.
- **Agent Framework**
  - buildup eviewing, hiring and plan-self improvement functionality,
  - tools ex. gmail access, phone calls etc.

### 💼 Business features

Future work to enhance the functionality and features of this project:

- **Implement removing pyCaptcha from Selenium:** Simplify the automation process by removing pyCaptcha.
- **Implement Phone-Based 2FA:** Enhance security with phone-based two-factor authentication.
- **Double-Check Email Verification:** Ensure accuracy in email verification processes.
- **Develop Agent Credentials Database:** Store and manage agent credentials securely.
- **Enable Meta Creation of Agents:** Facilitate the automatic generation of agent profiles.
- **Manage Extra Pop-Up Windows:** Handle additional pop-up windows during login and registration.
- **Accept Cookies Using OCR:** Use Optical Character Recognition (OCR) to accept cookies from pop-ups inside nestested functions.
- **Navigate to Specific Articles:** Directly identify and navigate to specific articles.
- **Integrate Local AI Models:** Incorporate local AI models for better performance and cost efficiency.
- **Handle Various Selenium Pop-Ups:** Improve Selenium to manage different types of pop-ups effectively.
- **Enhance Human Verification:** Improve the system’s ability to handle human verification steps, including pyCaptcha to overcome.
- **Tinder bot:**

### Competition

- [**AgentOps:**](https://www.agentops.ai) platform for developing, testing, and debugging AI agents, featuring robust monitoring, replay analytics, and cost management​.
- [**Agen.cy:**](https://www.agen.cy/) platform for building autonomous agents with a focus on customization and scalability for various applications.
- [**MultiOn:**](https://www.multion.ai/) to coordinating multiple AI agents, MultiOn excels in managing complex, collaborative tasks with real-time monitoring.
- [**SuperAGI:**](https://superagi.com/) platform for building scalable, high-performance AI agents, with strong support for multi-agent frameworks and integrations.
- [**Apify:**](https://apify.com/) platform where developers build, deploy, and publish web scraping, data extraction, and web automation tools.

## 📋 Detailed development steps

Next steps for development are available here [Excel Spreadsheet](https://docs.google.com/spreadsheets/d/18ZzaDf_gbfA0RlouF8LXv613WxEiO7HKEWkgQnpUpfc/edit?pli=1&gid=1450364081#gid=1450364081)

## 💡 Business Ideas

Here are potential implementation areas:

- **PowerBI AI Analyst:** Automate data analysis and reporting instead of PowerBI.
- **Mail Assistant:** Streamline email management tasks through automation.
- **People Screener:** Automatically find and verify email addresses.
- **Fiverr Automation:** Automate bidding and task execution on Fiverr.
- **Email Marketer:** Automate email campaign creation, tracking, and optimization.
- **Data Scraping:** Extract and analyze data from various sources.
- **LinkedIn Analytics:** Create visualizations and analytics from LinkedIn data.
- **YouTube Sentiment Analysis:** Analyze sentiment from YouTube videos.
- **Paid Reviews:** Sell out good reviews on google maps.
- **Market Sentiment:** Gauge market trends by analyzing social media sentiment.
- **Hotel Management:** Automate booking, customer service, and other hotel tasks.
- **Web Scraping Tools:** Enhance tools for data scraping and interaction with web platforms ex. [firecrawl](https://www.firecrawl.dev/)

## 🛠️ Best Practices

### Here are key notes on practices for development for encountered problems:

| **Encountered Problem**                      | **Solution**                                                                                             |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Hallucinations                               | Optimize tools output                                                                                    |
| Losing track                                 | Use sequential chats                                                                                     |
| Dynamic elements                             | Slow down browser loading time                                                                           |
| Conversation lengthy                         | Improve elements filtering                                                                               |
| Agents do not see when task is completed     | Enhance planning and prompts                                                                             |
| PyCaptcha appears                            | Add appropriate scripts                                                                                  |
| Register via Gmail POP-UP                    | Enrich Selenium functionalities                                                                          |
| Driver missing info in Selenium inheritance  | Consult and research                                                                                     |
| Inefficient conversation exchange            | Improve prompts and hiring                                                                               |
| Timely testing                               | Run all use cases simultaneously                                                                         |
| High LLM costs                               | Implement local models                                                                                   |
| High API costs                               | Implement local tools                                                                                    |
| Agents referencing outdated URLs             | Verify with updated OpenAI documentation                                                                 |
| Too many agents complicate processes         | Optimize agent use to the minimum, ex. hiring                                                            |
| Account registration framework               | Develop a separate framework with tools                                                                  |
| Agents not noticing correct steps            | Use vision for better guidance                                                                           |
| Agents going around the problem              | Use sequential chats                                                                                     |
| Too many agents confusing tools              | Optimize agents hiring and tools                                                                         |
| Overlapping skills in Researcher and Browser | Optimize agents hiring and tools                                                                         |
| Infinite loop with chat_manager              | ?introduce randomness/review autogen source code [link](https://github.com/microsoft/autogen/issues/108) |
| Agents are lying                             | ?add verifications agent, get autogen logs?                                                              |
| Cloudflare overcome                          | blocked on [https://nomadlist.com/](https://nomadlist.com/)                                              |

### Agents 🤖

1. **Planner**: overseeing the progress of the task and coordinating with other agents.
2. **Browser**: applying actions on browser with your tools to complete the task.
3. **Researcher**: doing research directly in the web (not in browser) to collect information for the task.
4. **Nothing**: keep up for now just to keep group chat framework.
