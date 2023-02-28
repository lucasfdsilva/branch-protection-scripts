import os
import shutil
import subprocess

# Path to the parent directory containing the subdirectories to search for DIRECTORY_TO_BE_DELETED
PARENT_DIR = ""
DIRECTORY_TO_BE_DELETED_NAME = ""

# Loop over all directories inside the parent directory
for subdir in os.listdir(PARENT_DIR):
    subdir_path = os.path.join(PARENT_DIR, subdir)
    if os.path.isdir(subdir_path):
        dir_to_be_deleted = os.path.join(
            subdir_path, DIRECTORY_TO_BE_DELETED_NAME)
        if os.path.isdir(dir_to_be_deleted):
            # Delete the "aws_account" directory
            try:
                shutil.rmtree(dir_to_be_deleted)
                print(f"Deleted {dir_to_be_deleted}")
            except Exception as e:
                print(f"Error deleting {dir_to_be_deleted}: {e}")

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
            print(f"{dir_to_be_deleted} does not exist in {subdir_path}")
