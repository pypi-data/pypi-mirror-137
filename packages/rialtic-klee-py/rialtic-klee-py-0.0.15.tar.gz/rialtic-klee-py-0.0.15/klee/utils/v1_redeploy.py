from github import Github
import os

g = Github(os.getenv("RIALTIC_DEV_PAT"))

WORKFLOW_NAME = 'relock_redeploy.yml'
ORG_NAME = 'rialtic-community'
BRANCH = 'develop'

def get_repo(line: str):
    if f'{ORG_NAME}/' in line:
        repo_string = line
    else:
        repo_string = f'{ORG_NAME}/{line.strip()}'
    return g.get_repo(repo_string)

def run(repo_name):
    repo = get_repo(repo_name)
    workflow = repo.get_workflow(WORKFLOW_NAME)
    print(workflow.name)
    workflow.create_dispatch(BRANCH)
