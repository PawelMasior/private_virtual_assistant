- github actions runner
- (crontab -l 2>/dev/null; echo "@reboot cd ~/actions-runner && RUNNER_ALLOW_RUNASROOT=1 ./run.sh") | crontab -

# Autogen Agents with Selenium Browser 🌐

This repository contains a deep dive into using Autogen with Selenium Browser techniques.

## Table of Contents 📋

- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Running](#running)
- [License](#license)

## Project Structure 📋

```markdown
- .env
- .gitignore
- Dockerfile
- initialize.py
- main.py
- plan.py
- pyproject.toml
- README.md
- README_STATUS.md
- requirements.txt
- run.py
- run_overnight.py
- agents\agents.py
- review\DBautogen.md
- review\func.py
- review\logs.db
- settings\ai-agents-project-key.json
- settings\func.py
- settings\gcp.py
- settings\modules.txt
- settings\plot.py
- settings\Comfortaa\Comfortaa-Bold.ttf
- settings\Comfortaa\Comfortaa-Light.ttf
- settings\Comfortaa\Comfortaa-Medium.ttf
- settings\Comfortaa\Comfortaa-Regular.ttf
- settings\Comfortaa\Comfortaa-SemiBold.ttf
- settings\fonts\Comfortaa-Regular.ttf
- settings\fonts\DejaVuSans.ttf
- tools\browser_plt.py
- tools\browser_selenium.py
- tools\gmail.py
- tools\info.py
- tools\langchain.py
- tools\twilio.py
- tools\vapi.py
- tools\web.py
```

## Setup and Installation 🛠️

0. **Install Python**

Recommended to use Anaconda distribution [Conda](https://conda.io/projects/conda/en/latest/index.html)

1. **Clone the repository**:

   ```bash
   git clone https://github.com/PawelMasior/backend_GenAI_RPA.git
   cd backend_GenAI_RPA
   ```

2. **Install dependencies**:

   2.1 **Poetry**: Option 1

   Ensure you have [Poetry](https://python-poetry.org/docs/#installation) installed.

   ```bash
   pip install poetry
   ```

   and next:

   ```bash
   poetry install --no-root
   ```

   2.2 **Requirements**: Option 2

   Preprate Python enviroment 3.11.3 using sample instruction:

   - [Python website](https://docs.python.org/3/library/venv.html)
   - [Conda (recommended)](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)

   Install all packages with single commend

   ```bash
   pip install -r requirements.txt
   ```

   2.3 **Enviroment** Option 3

   Get ready-to-use python enviroment from [GCP STORAGE](https://console.cloud.google.com/storage/browser/ai-agents-env;tab=objects?authuser=0&project=ai-agents-project-431615&prefix=&forceOnObjectsSortingFiltering=false)
   All you need is to set up new python interpreter now.

3. **Set up environment variables**:

   - **Enviroment** Create a `.env` file in the root directory and in relevant subdirectories with your API keys and other configurations.
     Get ready-to-use .env file from [GCP STORAGE](https://console.cloud.google.com/storage/browser/ai-agents-env;tab=objects?authuser=0&project=ai-agents-project-431615&prefix=&forceOnObjectsSortingFiltering=false)

   ````env
   YOUTUBE_API_KEY=your_youtube_api_key
   OPENAI_API_KEY=your_openai_api_key
   # Add other necessary environment variables
   ``

   - **Key** Create a key file to connect to GCP platform.
     Get ready-to-use .json file from [GCP STORAGE](https://console.cloud.google.com/storage/browser/ai-agents-env;tab=objects?authuser=0&project=ai-agents-project-431615&prefix=&forceOnObjectsSortingFiltering=false)

   ```env
   settings/ai-agents-project-key.json
   ````

## Running 🚀

```bash
python main.py
```

Nex, got to [http://localhost:5000/docs](http://localhost:5000/docs)

### API Setup 📜

To use owm API keys for this project, follow these steps:

- **GCP**: Go to the [IAM](https://console.cloud.google.com/iam-admin/iam?authuser=0&project=ai-agents-project-431615) name it **ai-agents-project-key.json** in keys/.
- **OpenAI**: Go to the [OpenAI page](https://platform.openai.com/docs/overview) name it **OPENAI_API_KEY**.
- **Twilio**: Go to the [Twilio page](https://www.twilio.com/en-us) name it **twilioAccountSid** and **twilioAuthToken**.
- **Tavily**: Go to the [Tavily page](https://tavily.com/) name it **TAVILY_API_KEY**.
- **Vapi**: Go to the [Vapi page](https://vapi.ai/) name it **TAVILY_API_KEY**.
- **Firecrawl**: Go to the [Firecrawl page](https://www.firecrawl.dev/) name it **FIRECRAWL_API_KEY**.
- **Gmail**: To define instructions **<not_applicable_yet>**.
- **Langchain**: Go to the [Langchain page](https://www.langchain.com/) name it **<not_applicable_yet>**.

Copy the generated API key and add it to your `.env` file as ex. `YOUTUBE_API_KEY`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
