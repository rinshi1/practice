import os
import requests

from dotenv import load_dotenv

load_dotenv()

OWNER = os.getenv("GH_OWNER")
REPO = os.getenv("GH_REPO")
TOKEN = os.getenv("GH_TOKEN")
BRANCH = os.getenv("GH_BRANCH", "main") 

def download_github_folder(folder_path, local_dir):
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    def download_recursive(api_url, base_folder):
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        items = response.json()

        if not isinstance(items, list):
            items = [items]

        for item in items:
            item_path = item["path"]
            local_path = os.path.join(base_folder, os.path.relpath(item_path, folder_path))

            if item["type"] == "dir":
                os.makedirs(local_path, exist_ok=True)
                download_recursive(item["url"], base_folder)
            elif item["type"] == "file":
                file_data = requests.get(item["download_url"], headers=headers).content
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, "wb") as f:
                    f.write(file_data)
                print(f"✅ Downloaded: {item_path}")
            else:
                print(f"⚠️ Skipping unsupported type: {item['type']} at {item_path}")

    os.makedirs(local_dir, exist_ok=True)
    api_url = f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{folder_path}?ref={BRANCH}"
    download_recursive(api_url, local_dir)

# Upload local folder 'my_local_folder' to GitHub under 'project/' directory
# upload_folder_to_github(local_folder="my_local_folder", repo_path="project", commit_message="Upload via script")

# Download 'project/' folder from GitHub repo to local folder 'downloaded_project'
download_github_folder(folder_path="", local_dir="project")
