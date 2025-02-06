import re
import pandas as pd

def clean_text(text):
    return re.sub(r'[^\x00-\x7F\s,;.!?":\(\)\-\[\]\'”’—–]', '', text)

def reverse_name(name):
    parts = name.split(', ')
    if len(parts) == 2:
        return f"{parts[1]} {parts[0]}"
    return "Author Not Found"

def remove_kindle_comments(text):
    return re.sub(r'- Your (Note|Highlight)[^\n]*\d{2}:\d{2}:\d{2}\s*', '', text)

with open("My Clippings.txt", "r", encoding="utf-8", errors="ignore") as f:
    content = f.read()

entries = content.split("==========")

data = []

for entry in entries:
    if not entry.strip():
        continue

    print(f"Processing entry:\n{entry}\n")

    match = re.match(r"(.*?)\s*(?:\(([^)]+)\))?\n- Your (Note|Highlight)[^\n]*\n\n(.*)", entry, re.DOTALL)

    if match:
        book = match.group(1).strip()
        author = match.group(2)
        quote = match.group(4).strip()
        
        if author:
            author = reverse_name(author.strip())
        else:
            author = "Author Not Found"

        book = clean_text(book)
        quote = clean_text(remove_kindle_comments(quote))

        if quote:
            data.append({"book": book, "author": author, "quote": quote})
        else:
            print("Skipped empty quote.")
    else:
        print("No match found for entry.")

if not data:
    print("No valid entries were found to save.")

if data:
    df = pd.DataFrame(data)
    df.to_csv("kindle_notes.csv", index=False)
    print("Converted Kindle notes to kindle_notes.csv successfully!")
else:
    print("No data to save to CSV.")
