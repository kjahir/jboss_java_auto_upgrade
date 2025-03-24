import subprocess

def run_command(command, cwd=None):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout

def checkout_branch(repo_path, branch_name):
    run_command(["git", "checkout", branch_name], cwd=repo_path)

def commit_changes(repo_path, commit_message):
    run_command(["git", "add", "."], cwd=repo_path)
    run_command(["git", "commit", "-m", commit_message], cwd=repo_path)