import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OWNER = os.getenv("GH_OWNER")
REPO = os.getenv("GH_REPO")
TOKEN = os.getenv("GH_TOKEN")
BRANCH = os.getenv("GH_BRANCH", "main") 

def upload_folder_to_github(local_folder, repo_path, commit_message):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    for root, _, files in os.walk(local_folder):
        for file_name in files:
            local_file_path = os.path.join(root, file_name)
            with open(local_file_path, "rb") as f:
                content = base64.b64encode(f.read()).decode()

            relative_path = os.path.relpath(local_file_path, local_folder).replace("\\", "/")
            github_file_path = f"{repo_path}/{relative_path}".strip("/")

            url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{github_file_path}"

            # Get file SHA if it exists
            response = requests.get(url, headers=headers)
            sha = response.json().get("sha") if response.status_code == 200 else None

            data = {
                "message": commit_message,
                "content": content,
                "branch": BRANCH
            }
            if sha:
                data["sha"] = sha

            put_response = requests.put(url, headers=headers, data=json.dumps(data))
            if put_response.status_code in [200, 201]:
                print(f"✅ Uploaded: {github_file_path}")
            else:
                print(f"❌ Failed to upload: {github_file_path}")
                print(f"    Error: {put_response.status_code}, {put_response.text}")


upload_folder_to_github(local_folder="downloaded_project", repo_path="", commit_message="Upload via script")