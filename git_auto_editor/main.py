import argparse
import os
from git_utils import checkout_branch, commit_changes
from file_updater import load_template, update_files

def main(repo_path, branch, template_file):
    print(f"Checking out branch: {branch}")
    checkout_branch(repo_path, branch)

    print(f"Loading template: {template_file}")
    rules = load_template(template_file)

    print("Updating files...")
    update_files(repo_path, rules)

    print("Committing changes...")
    commit_changes(repo_path, f"Applied template: {os.path.basename(template_file)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="Path to Git repo")
    parser.add_argument("--branch", required=True, help="Branch to checkout")
    parser.add_argument("--template", required=True, help="Path to template file")

    args = parser.parse_args()
    main(args.repo, args.branch, args.template)