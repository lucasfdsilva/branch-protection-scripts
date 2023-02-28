import os
import shutil
import subprocess

# Path to the parent directory containing the subdirectories to search for DIRECTORY_TO_BE_DELETED
PARENT_DIR = ""
DIRECTORY_TO_BE_DELETED = ""

# Loop over all directories inside the parent directory
for subdir in os.listdir(PARENT_DIR):
    subdir_path = os.path.join(PARENT_DIR, subdir)
    if os.path.isdir(subdir_path):
        aws_account_dir = os.path.join(subdir_path, DIRECTORY_TO_BE_DELETED)
        if os.path.isdir(aws_account_dir):
            # Delete the "aws_account" directory
            try:
                shutil.rmtree(aws_account_dir)
                print(f"Deleted {aws_account_dir}")
            except Exception as e:
                print(f"Error deleting {aws_account_dir}: {e}")

            # Push the changes to the GitHub repository
            commit_msg = "removed the aws_directory altogether to centralize the main.tf configuration"
            cleantrace_dir = subdir_path
            try:
                os.chdir(subdir_path)
                subprocess.run(["git", "checkout", "dev"])
                subprocess.run(["git", "config", "pull.rebase", "false"])
                subprocess.run(["git", "pull"])
                subprocess.run(["git", "add", "."])
                subprocess.run(
                    ["git", "commit", "-m", "updated azure pipeline template"])
                subprocess.run(["git", "push"])
                print(f"Pushed changes in {cleantrace_dir} to GitHub")
            except Exception as e:
                print(
                    f"Error pushing changes in {cleantrace_dir} to GitHub: {e}")
        else:
            print(f"{aws_account_dir} does not exist in {subdir_path}")
