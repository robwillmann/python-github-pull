import os
import requests
from git import Repo, GitCommandError

# Set constants
LOCAL_REPO_PATH = "R:/tester/subfolder"  # my local repo path
REMOTE_URL = "https://github.com/robwillmann/python-github-pull.git"  # GitHub remote repo
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1358699156029571144/pmvpRHKy8Ny5Wo08tRw-dIOLbNAHCo9gaHqDbYA_VwumbrfECSmA2R-o-n9ZSZSkE8V7"  # Discord webhook URL so I can verify if process works

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def send_discord_message(message: str):
    timestamp = get_timestamp()
    data = {
        "content": f"{message}\n🕒 `{timestamp}`"
    }
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("Discord message sent successfully.")
        else:
            print(f"Failed to send Discord message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending Discord message: {e}")

def update_repo():
    if os.path.exists(LOCAL_REPO_PATH):
        try:
            print(f"Opening local repo at {LOCAL_REPO_PATH}")
            repo = Repo(LOCAL_REPO_PATH)
            origin = repo.remotes.origin
            print("Pulling latest changes...")
            pull_info = origin.pull()
            summary = "\n".join([f"{info.ref.name} - {info.commit.hexsha[:7]}" for info in pull_info])
            message = f"✅ Pulled latest changes for `{repo.working_dir}`:\n```\n{summary}\n```"
            send_discord_message(message)
        except GitCommandError as e:
            error_msg = f"❌ Git error while pulling repo: {e}"
            print(error_msg)
            send_discord_message(error_msg)
    else:
        try:
            print(f"Cloning repository from {REMOTE_URL} to {LOCAL_REPO_PATH}")
            repo = Repo.clone_from(REMOTE_URL, LOCAL_REPO_PATH)
            message = f"📥 Repository cloned successfully to `{LOCAL_REPO_PATH}`."
            send_discord_message(message)
        except GitCommandError as e:
            error_msg = f"❌ Failed to clone repo: {e}"
            print(error_msg)
            send_discord_message(error_msg)

if __name__ == "__main__":
    update_repo()
