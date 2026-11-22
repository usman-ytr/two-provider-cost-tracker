
import os
import json
import sys
from dotenv import load_dotenv
from google import genai
from groq import Groq

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GEMINI_MODEL = os.getenv("GEMINI_MODEL")
GROQ_MODEL = os.getenv("GROQ_MODEL")

GEMINI_INPUT_PRICE = float(os.getenv("GEMINI_INPUT_PRICE_PER_M"))
GEMINI_OUTPUT_PRICE = float(os.getenv("GEMINI_OUTPUT_PRICE_PER_M"))

GROQ_INPUT_PRICE = float(os.getenv("GROQ_INPUT_PRICE_PER_M"))
GROQ_OUTPUT_PRICE = float(os.getenv("GROQ_OUTPUT_PRICE_PER_M"))

def getProviderResponse(client,model,prompt):
    if model == GEMINI_MODEL:
        providerResponse = client.models.generate_content(model=model,contents=prompt)
        reply = providerResponse.text
        inputTokens = providerResponse.usage_metadata.prompt_token_count
        outputTokens = providerResponse.usage_metadata.candidates_token_count
        inputPrice = GEMINI_INPUT_PRICE
        outputPrice = GEMINI_OUTPUT_PRICE
    else:
        providerResponse = client.chat.completions.create(model=model,messages=[{"role": "user", "content": prompt}])
        reply = providerResponse.choices[0].message.content
        inputTokens = providerResponse.usage.prompt_tokens
        outputTokens = providerResponse.usage.completion_tokens
        inputPrice = GROQ_INPUT_PRICE
        outputPrice = GROQ_OUTPUT_PRICE
    return reply,inputTokens,outputTokens,inputPrice,outputPrice

def getCost(inputTokens,outputTokens,inputPrice,outputPrice):
    return ((inputTokens * inputPrice) +(outputTokens * outputPrice)) / 1_000_000

def printResponse(name,reply,input_tokens,output_tokens,input_price,output_price):
    print(f"\n========== {name} RESPONSE ==========")
    print(reply)
    cost = getCost(input_tokens,output_tokens,input_price,output_price)
    print("Input Tokens:", input_tokens)
    print("Output Tokens:", output_tokens)
    print(f"Cost: ${cost:.8f}\n")
    return cost


# Create API clients
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY)

prompt = sys.argv[1]

gemini_reply,gemini_input_tokens,gemini_output_tokens,gemini_input_price,gemini_output_price = getProviderResponse(gemini_client,GEMINI_MODEL,prompt)
gemini_cost = printResponse("Gemini",gemini_reply,gemini_input_tokens,gemini_output_tokens,gemini_input_price,gemini_output_price)
groq_reply,groq_input_tokens,groq_output_tokens,groq_input_price,groq_output_price = getProviderResponse(groq_client,GROQ_MODEL,prompt)
groq_cost = printResponse("Groq",groq_reply,groq_input_tokens,groq_output_tokens,groq_input_price,groq_output_price)


print("\n========== COST COMPARISON ==========")
print(f"{'Provider':<12} {'Input':<10} {'Output':<10} {'Cost (USD)':<15}")
print("-" * 60)
print(f"{'Gemini':<12} {gemini_input_tokens:<10} {gemini_output_tokens:<10} ${gemini_cost:<14.8f}")
print(f"{'Groq':<12} {groq_input_tokens:<10} {groq_output_tokens:<10} ${groq_cost:<14.8f}")

results = [
    {
        "provider": "Gemini",
        "model": GEMINI_MODEL,
        "reply": gemini_reply,
        "input_tokens": gemini_input_tokens,
        "output_tokens": gemini_output_tokens,
        "input_price_per_m": gemini_input_price,
        "output_price_per_m": gemini_output_price,
        "cost_usd": f"{gemini_cost:.10f}"
    },
    {
        "provider": "Groq",
        "model": GROQ_MODEL,
        "reply": groq_reply,
        "input_tokens": groq_input_tokens,
        "output_tokens": groq_output_tokens,
        "input_price_per_m": groq_input_price,
        "output_price_per_m": groq_output_price,
        "cost_usd": f"{groq_cost:.10f}"
    }
]

with open("results.json", "w", encoding="utf-8") as file:
    json.dump(results, file, indent=4, ensure_ascii=False)

print("\nResults saved successfully in results.json")



