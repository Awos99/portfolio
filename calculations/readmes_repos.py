import requests
import os
import base64
import pandas as pd
import asyncio
from app import app

try:
    os.environ["GITHUB_KEY"] = ""
except:
    print("Please set the GITHUB_KEY environment variable.")


headers = {
    "Authorization": "Bearer " + os.environ["GITHUB_KEY"],
}

def get_readme(url):
    url = f"{url}/readme"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        encoded_content = data.get('content')
        if encoded_content:
            decoded_content = base64.b64decode(encoded_content).decode('utf-8')
            return decoded_content
        else:
            return "Content not found"
    else:
        return f"Failed to fetch README: {response.status_code}"

def get_all_readmes(df_repos):
    df_repos["readme"] = df_repos["url"].apply(get_readme)
    return df_repos

def get_number_of_commits(repo, owner='Awos99'):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, headers=headers)
    data = response.json()
    df_data = pd.DataFrame(data)
    commits = pd.DataFrame(pd.DataFrame(df_data['commit'].values.tolist())['committer'].values.tolist())
    commits = commits[commits['name']==owner]
    commits['date'] = pd.to_datetime(commits['date']).apply(lambda x: x.strftime('%d-%m-%Y'))
    return commits['date'].tolist()

def get_repos(username="Awos99"):
    url = f"https://api.github.com/user/repos"
    response = requests.get(url, headers=headers)
    df_repos = pd.DataFrame(response.json())
    df_repos_filtered = df_repos[df_repos["owner"].apply(lambda x: x["login"] == "Awos99")]
    columns_selected = ["name", "full_name", "private", "owner", "html_url", "url", "description", "html_url", "created_at", "updated_at", "homepage", "language", "stargazers_count", "watchers_count", "topics", "watchers"]
    df_repos = get_all_readmes(df_repos_filtered)[columns_selected]
    df_repos["commits"] = df_repos["name"].apply(get_number_of_commits)
    return df_repos



async def get_repos_5h():
    while True:
        # Your code here
        get_repos().to_csv("static/repos.csv")
        await asyncio.sleep(5 * 60 * 60)  # Sleep for 5 hours

if __name__ == '__main__':
    app.run(debug=True)