import urllib.request
import json
import re

url = "https://api.github.com/users/Hajmehrad"
req = urllib.request.Request(url, headers={"User-Agent": "readme-bot"})
data = json.loads(urllib.request.urlopen(req).read())

repos_url = "https://api.github.com/users/Hajmehrad/repos?per_page=100"
req2 = urllib.request.Request(repos_url, headers={"User-Agent": "readme-bot"})
repos = json.loads(urllib.request.urlopen(req2).read())

total_stars = sum(r["stargazers_count"] for r in repos)
total_forks = sum(r["forks_count"] for r in repos)

langs = {}
for r in repos:
    if r["language"]:
        langs[r["language"]] = langs.get(r["language"], 0) + 1
top_lang = max(langs, key=langs.get) if langs else "Python"

new_stats = f"""<!-- STATS:START -->
| | |
|---|---|
| 🗂 Public Repos | {data['public_repos']} |
| ⭐ Total Stars | {total_stars} |
| 🐍 Main Language | {top_lang} |
| 👥 Followers | {data['followers']} |
| 🔀 Forks | {total_forks} |
<!-- STATS:END -->"""

with open("README.md", "r", encoding="utf-8") as f:
    content = f.read()

content = re.sub(
    r"<!-- STATS:START -->.*?<!-- STATS:END -->",
    new_stats,
    content,
    flags=re.DOTALL
)

with open("README.md", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Stats updated!")
