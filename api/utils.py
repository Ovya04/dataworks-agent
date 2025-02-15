import datetime
import json
import openai

def parse_dates(file_path):
    """Count the number of Wednesdays."""
    with open(file_path, "r") as f:
        dates = [line.strip() for line in f.readlines()]
    return sum(1 for date in dates if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 2)

def sort_contacts():
    """Sort contacts JSON file."""
    with open("/data/contacts.json", "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda x: (x["last_name"], x["first_name"]))
    with open("/data/contacts-sorted.json", "w") as f:
        json.dump(sorted_contacts, f, indent=4)
    return "Contacts sorted."

def call_llm(prompt):
    """Call OpenAI GPT-4o-Mini for LLM processing."""
    openai.api_key = os.getenv("eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDEwMjhAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.aI5bnxxhoxRxp5AiLLErQfm1XCvcBGV8WW9QJPeQhgY")
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

def extract_headings(text):
    # Sample function, modify as needed
    return [line for line in text.split("\n") if line.strip().startswith("#")]

