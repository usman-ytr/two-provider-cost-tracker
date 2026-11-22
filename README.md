# Two Provider Cost Tracker
Two provider cost tracker is python script that accepts prompt from terminal,sends prompt to two different LLMs and gets response,input and output tokens and total cost in USD.It also shows comparison table and saves results in a separate json output file.

# Steps :
First make repo on github and then clone
   git clone "https://github.com/usman-ytr/two-provider-cost-tracker.git"

Initialize python project
   uv init
 
Generate API keys for gemini,groq providers.
Make .gitignore file and write following content into it.
    .env
   .venv/
   __pycache__/
   *.pyc

This file will not push API keys on github.

Commit gitignore file on github using commands
   git add .gitignore
   git commit -m "Add gitignore to protect secrets"
   git push

Install python packages using
  uv add google-genai groq python-dotenv

Make a secret file .env to hold provider API keys,model id,input and output price.

Create tracker.py file and write python script into it.
Open terminal and runs below command
  uv run tracker.py "Hi"
Output will be response,input and output token,total cost in usd,two provider comparison table and  a json file "result.json" will be automatically created on project that will hold two provider results.
Then commit and push to repo.type these commands.
  git add tracker.py,README.md,results.json
  git commit -m "last commit"
  git push origin main
