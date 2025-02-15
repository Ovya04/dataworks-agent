import os
import json
import subprocess
import sqlite3
import requests
from api.utils import call_llm, parse_dates, sort_contacts, extract_headings

DATA_DIR = "/data"

def execute_task(task: str):
    """Executes a plain-English task."""
    if "prettier" in task:
        return format_markdown()
    elif "count Wednesdays" in task:
        return count_wednesdays()
    elif "sort contacts" in task:
        return sort_contacts()
    else:
        raise ValueError("Unsupported task")

def format_markdown():
    """Format Markdown using Prettier."""
    file_path = os.path.join(DATA_DIR, "format.md")
    subprocess.run(["npx", "prettier", "--write", file_path], check=True)
    return f"Formatted {file_path}"

def count_wednesdays():
    """Count Wednesdays in a date file."""
    file_path = os.path.join(DATA_DIR, "dates.txt")
    output_path = os.path.join(DATA_DIR, "dates-wednesdays.txt")
    count = parse_dates(file_path)
    with open(output_path, "w") as f:
        f.write(str(count))
    return f"Wednesdays counted: {count}"

def read_file(path):
    """Reads a file's contents."""
    try:
        with open(path, "r") as file:
            return {"content": file.read()}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
