import os
import shutil
import subprocess

SOURCE_FILE = "~/repos/cleantrace/azure-pipelines.yml"
SUBDIRS_DIRECTORY = "~/repos/cleantrace"

# set source file path
source_path = os.path.expanduser(SOURCE_FILE)

# set destination directory path
destination_dir = os.path.expanduser(SUBDIRS_DIRECTORY)

# get a list of all subdirectories in the destination directory that start with "cleantrace-cloud"
subdirs = [os.path.join(destination_dir, subdir) for subdir in os.listdir(destination_dir) if os.path.isdir(
    os.path.join(destination_dir, subdir)) and subdir.startswith("cleantrace-cloud-lambda")]

# copy the source file to each subdirectory
for subdir in subdirs:
    destination_path = os.path.join(subdir, "azure-pipelines.yml")

    try:
        shutil.copy2(source_path, destination_path, follow_symlinks=True)
        os.chdir(subdir)
        print(f"File copied to {subdir}. Pushing changes now.")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error copying file to {subdir}: {e}")

    # pushing the latest changes to their respective GH repos
    try:
        subprocess.run(["git", "checkout", "dev"])
        subprocess.run(["git", "config", "pull.rebase", "false"])
        subprocess.run(["git", "pull"])
        subprocess.run(["git", "add", "."])
        subprocess.run(
            ["git", "commit", "-m", "updated azure pipeline template"])
        subprocess.run(["git", "push"])
    except subprocess.CalledProcessError as e:
        print(e)
