# Two Provider Cost Tracker

A Python-based tool that compares Google Gemini and Groq AI models based on response time, token usage, and API cost.

## Features

- Send the same prompt to Gemini and Groq.
- Measure API response time.
- Track input and output tokens using API usage data.
- Calculate API costs based on per-million-token pricing.
- Display a side-by-side comparison table.
- Save results automatically in `results.json`.
- Accept prompts through command-line arguments.

## Requirements

- Python
- uv package manager
- Google Gemini API key
- Groq API key

## Installation

1. Clone the repository:

   `git clone YOUR_GITHUB_REPOSITORY_URL`

2. Navigate to the project folder.

3. Install dependencies:

   `uv sync`

4. Create a `.env` file using `.env.example` as a template.

5. Add your Gemini and Groq API keys to `.env`.

## Usage

Run the tracker with a prompt:

`uv run tracker.py "Explain Agentic AI in simple words."`

## Output

The program displays:

- Gemini response
- Groq response
- Input and output tokens
- Response time
- Estimated API cost in USD
- Side-by-side comparison table

Results are also saved in `results.json`.

## Technologies Used

- Python
- Google Gemini API
- Groq API
- python-dotenv
- uv

## Security

API keys are stored in `.env`. The `.env` file is excluded from Git using `.gitignore`. Never commit real API keys to GitHub.# two-provider-cost-tracker