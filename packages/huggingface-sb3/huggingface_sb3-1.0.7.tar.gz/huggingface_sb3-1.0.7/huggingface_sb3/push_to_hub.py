import logging
import os

import shutil

from pathlib import Path

from huggingface_hub import HfApi, HfFolder, Repository

README_TEMPLATE = """---
tags:
- deep-reinforcement-learning
- reinforcement-learning
- stable-baselines3
---
# TODO: Fill this model card
"""

def _create_model_card(repo_dir: Path):
    """
    Creates a model card for the repository.
    :param repo_dir:
    """
    readme_path = repo_dir / "README.md"
    readme = ""
    if readme_path.exists():
      with readme_path.open("r", encoding="utf8") as f:
          readme = f.read()
    else:
      readme = README_TEMPLATE
    with readme_path.open("w", encoding="utf-8") as f:
        f.write(readme)

def _copy_file(filepath: Path, dst_directory: Path):
    """
    Copy the file to the correct directory
    :param filepath: path of the file
    :param dst_directory: destination directory
    """
    dst = dst_directory / filepath.name
    shutil.copy(str(filepath.name), str(dst))


def push_to_hub(repo_id: str,
               filename: str,
               commit_message: str,
               use_auth_token=True,
               local_repo_path="hub"):
    """
      Upload a model to Hugging Face Hub.
      :param repo_id: repo_id: id of the model repository from the Hugging Face Hub
      :param filename: name of the model zip or mp4 file from the repository
      :param commit_message: commit message
      :param use_auth_token
      :param local_repo_path: local repository path
      """
    huggingface_token = HfFolder.get_token()

    temp = repo_id.split('/')
    organization = temp[0]
    repo_name = temp[1]
    print("REPO NAME: ", repo_name)
    print("ORGANIZATION: ", organization)

    # Step 1: Clone or create the repo
    # Create the repo (or clone its content if it's nonempty)
    api = HfApi()
    repo_url = api.create_repo(
        name=repo_name,
        token=huggingface_token,
        organization=organization,
        private=False,
        exist_ok=True, )

    # Git pull
    repo_local_path = Path(local_repo_path) / repo_name
    repo = Repository(repo_local_path, clone_from=repo_url, use_auth_token=use_auth_token)
    repo.git_pull(rebase=True)

    # Add the model
    filename_path = os.path.abspath(filename)
    _copy_file(Path(filename_path), repo_local_path)
    _create_model_card(repo_local_path)

    logging.info(f"Pushing repo {repo_name} to the Hugging Face Hub")
    repo.push_to_hub(commit_message=commit_message)

    logging.info(f"View your model in {repo_url}")

    # Todo: I need to have a feedback like:
    # You can see your model here "https://huggingface.co/repo_url"
    print("Your model has been uploaded to the Hub, you can find it here: ", repo_url)
    return repo_url



