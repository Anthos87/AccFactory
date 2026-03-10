import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('GITHUB_TOKEN')
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
REPO = "Anthos87/AccFactory"
URL = f"https://api.github.com/repos/{REPO}/issues"

def create_issue(title, body):
    res = requests.post(URL, headers=HEADERS, json={"title": title, "body": body})
    if res.status_code == 201:
        print(f"Issue created: {res.json()['html_url']}")
    else:
        print(f"Error: {res.status_code} - {res.text}")

print("Creating Backend Task...")
create_issue(
    "Task Backend: Sviluppo endpoint e Unit Test",
    "**Assegnato a:** backend_agent\n\nTask:\n- Sviluppare endpoint in `/server` basandosi su `api_contract.md`.\n- Creare unit test per ogni endpoint."
)

print("Creating Frontend Task...")
create_issue(
    "Task Frontend: Sviluppo Interfacce React",
    "**Assegnato a:** frontend_agent\n\nTask:\n- Sviluppare interfacce in `/client`.\n- Consumare le API definite dall'Architect."
)
