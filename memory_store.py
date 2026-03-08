import json
import os

MEMORY_FILE = "memory/chat_memory.json"

def load_memory():

    if not os.path.exists(MEMORY_FILE):
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory[-20:], f, indent=2)