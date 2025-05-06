import requests
import os
from collections import Counter

USERNAME = "Shimu-I"  # Replace with your GitHub username
EVENTS_URL = f"https://api.github.com/users/{USERNAME}/events/public"
EXTENSION_MAP = {
    ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java",
    ".c": "C", ".cpp": "C++", ".html": "HTML", ".css": "CSS", ".php": "PHP",
    ".rb": "Ruby", ".go": "Go", ".rs": "Rust", ".sh": "Shell"
}

def fetch_recent_commits():
    resp = requests.get(EVENTS_URL, headers={"Accept": "application/vnd.github.v3+json"})
    events = resp.json()
    commit_urls = []

    for event in events:
        if event.get("type") == "PushEvent":
            for commit in event["payload"]["commits"]:
                commit_urls.append(commit["url"])
    
    return commit_urls[:15]  # Limit to 15 commits

def detect_languages(commit_urls):
    lang_counter = Counter()
    for url in commit_urls:
        resp = requests.get(url)
        files_url = url.replace("/commits/", "/commits/")  # Stay same
        commit_data = resp.json()
        for file in commit_data.get("files", []):
            filename = file.get("filename", "")
            ext = os.path.splitext(filename)[1]
            lang = EXTENSION_MAP.get(ext)
            if lang:
                lang_counter[lang] += 1
    return lang_counter.most_common(5)

def write_output(langs):
    with open("RECENT_LANGUAGES.md", "w") as f:
        f.write("### 🧠 Recently Committed Languages\n\n")
        for lang, count in langs:
            f.write(f"- {lang} ({count} files)\n")

if __name__ == "__main__":
    commits = fetch_recent_commits()
    langs = detect_languages(commits)
    write_output(langs)
