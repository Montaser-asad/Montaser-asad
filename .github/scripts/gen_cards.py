"""Generate profile cards from GitHub data, keeping images available during outages."""

import json
import os
from pathlib import Path
import textwrap
import urllib.request
from xml.sax.saxutils import escape

USER = "Montaser-asad"
ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ("minishell", "Philosophers", "NetPractice", "2D-game")


def get(path):
    headers = {"User-Agent": "profile-card-generator"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/{path}", headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def text(x, y, value, color="#dbeafe", size=16):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}">'
            f'{escape(str(value))}</text>')


def card(title, lines, height):
    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" width="495" height="{height}" '
        f'viewBox="0 0 495 {height}" role="img" aria-labelledby="title">',
        f'<title id="title">{escape(title)}</title>',
        '<style>text{font-family:-apple-system,Segoe UI,Arial,sans-serif}</style>',
        f'<rect x="1" y="1" width="493" height="{height - 2}" rx="12" '
        'fill="#0b1220" stroke="#28476b" stroke-width="2"/>',
        text(24, 36, title, "#60a5fa", 21),
        *lines,
        '</svg>',
    ]) + '\n'


def generate():
    user = get(f"users/{USER}")
    repos = []
    page = 1
    while True:
        batch = get(f"users/{USER}/repos?per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    by_name = {repo["name"]: repo for repo in repos}
    output = {}
    for name in PROJECTS:
        repo = by_name[name]
        description = repo["description"] or "View the project on GitHub."
        wrapped = textwrap.wrap(description, width=55)
        if len(wrapped) > 3:
            wrapped = wrapped[:3]
            wrapped[-1] = wrapped[-1].rstrip(" .") + "…"
        lines = [text(24, 66 + i * 22, line) for i, line in enumerate(wrapped)]
        details = []
        if repo["language"]:
            details.append(repo["language"])
        details.extend([f'Stars: {repo["stargazers_count"]}', f'Forks: {repo["forks_count"]}'])
        lines.append(text(24, 151, "   ·   ".join(details), "#93c5fd", 14))
        output[f"project-{name}.svg"] = card(name, lines, 174)
    stats = [
        ("Public repositories", user["public_repos"]),
        ("Followers", user["followers"]),
        ("Stars earned", sum(repo["stargazers_count"] for repo in repos)),
        ("Repository forks", sum(repo["forks_count"] for repo in repos)),
    ]
    lines = []
    for i, (label, value) in enumerate(stats):
        y = 69 + i * 32
        lines.extend([text(24, y, label), text(420, y, value, "#7dd3fc")])
    output["github-stats.svg"] = card("GitHub stats", lines, 195)
    # Fetch and build every card before replacing any existing images.
    for name, svg in output.items():
        (ROOT / "assets" / name).write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    generate()
