
import os
import time
import json
import sys
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

GEMINI_INPUT_PRICE = float(os.getenv("GEMINI_INPUT_PRICE_PER_M"))
GEMINI_OUTPUT_PRICE = float(os.getenv("GEMINI_OUTPUT_PRICE_PER_M"))

GROQ_INPUT_PRICE = float(os.getenv("GROQ_INPUT_PRICE_PER_M"))
GROQ_OUTPUT_PRICE = float(os.getenv("GROQ_OUTPUT_PRICE_PER_M"))


# Create API clients
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

prompt = sys.argv[1]

# Gemini API call
start_time = time.perf_counter()

gemini_response = gemini_client.models.generate_content(
    model=GEMINI_MODEL,
    contents=prompt
)

gemini_seconds = time.perf_counter() - start_time

gemini_input_tokens = gemini_response.usage_metadata.prompt_token_count
gemini_output_tokens = gemini_response.usage_metadata.candidates_token_count

gemini_cost = (
    (gemini_input_tokens * GEMINI_INPUT_PRICE) +
    (gemini_output_tokens * GEMINI_OUTPUT_PRICE)
) / 1_000_000

print("\n========== GEMINI RESPONSE ==========")
print(gemini_response.text)
print("Input Tokens:", gemini_input_tokens)
print("Output Tokens:", gemini_output_tokens)
print("Response Time:", round(gemini_seconds, 2), "seconds")
print(f"Cost: ${gemini_cost:.8f}")


# Groq API call
start_time = time.perf_counter()

groq_response = groq_client.chat.completions.create(
    model=GROQ_MODEL,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

groq_seconds = time.perf_counter() - start_time

groq_input_tokens = groq_response.usage.prompt_tokens
groq_output_tokens = groq_response.usage.completion_tokens

groq_cost = (
    (groq_input_tokens * GROQ_INPUT_PRICE) +
    (groq_output_tokens * GROQ_OUTPUT_PRICE)
) / 1_000_000

print("\n========== GROQ RESPONSE ==========")
print(groq_response.choices[0].message.content)
print("Input Tokens:", groq_input_tokens)
print("Output Tokens:", groq_output_tokens)
print("Response Time:", round(groq_seconds, 2), "seconds")
print(f"Cost: ${groq_cost:.8f}")


print("\n========== COST COMPARISON ==========")

print(f"{'Provider':<12} {'Input':<10} {'Output':<10} {'Time':<10} {'Cost (USD)':<15}")
print("-" * 60)

print(f"{'Gemini':<12} {gemini_input_tokens:<10} {gemini_output_tokens:<10} {gemini_seconds:<10.2f} ${gemini_cost:<14.8f}")

print(f"{'Groq':<12} {groq_input_tokens:<10} {groq_output_tokens:<10} {groq_seconds:<10.2f} ${groq_cost:<14.8f}")

results = [
    {
        "provider": "Gemini",
        "model": GEMINI_MODEL,
        "reply": gemini_response.text,
        "input_tokens": gemini_input_tokens,
        "output_tokens": gemini_output_tokens,
        "input_price_per_m": GEMINI_INPUT_PRICE,
        "output_price_per_m": GEMINI_OUTPUT_PRICE,
        "cost_usd": f"{gemini_cost:.10f}"
    },
    {
        "provider": "Groq",
        "model": GROQ_MODEL,
        "reply": groq_response.choices[0].message.content,
        "input_tokens": groq_input_tokens,
        "output_tokens": groq_output_tokens,
        "input_price_per_m": GROQ_INPUT_PRICE,
        "output_price_per_m": GROQ_OUTPUT_PRICE,
        "cost_usd": f"{groq_cost:.10f}"
    }
]

with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("\nResults saved successfully in results.json")



