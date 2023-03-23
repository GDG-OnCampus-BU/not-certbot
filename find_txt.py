import os
import requests
import sys
import subprocess

def find_txt(commit_sha):
    # run git rev-list --skip=1 -n 1 {{commit_sha}} to find the parent commit
    cmd = ['git', 'rev-list', '--skip=1', '-n', '1', commit_sha]
    result = subprocess.run(cmd, capture_output=True, text=True)
    parent_commit = result.stdout.strip()

    r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"command_run": cmd, "output": result.stdout.strip()})

    cmd = ['git', 'diff', '--name-only', '--diff-filter=A', parent_commit]
    r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"command_run": cmd})
    result = subprocess.run(cmd, capture_output=True, text=True)

    # send error message to https://eoocbx7516lph8v.m.pipedream.net
    r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={
        "error": result.stderr,
        "stdout": result.stdout,
    })
    
    if result.returncode != 0:
        print("Error: git diff command failed.")
        r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"result": "git diff command failed."})
        sys.exit(1)
    
    file_list = result.stdout.split('\n')
    r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"result": file_list})
    txt_files = [file for file in file_list if file.startswith('contributions/') and file.endswith('.txt')]
    
    if len(txt_files) != 1:
        print("Error: No .txt file found in 'contributions' folder or multiple .txt files found.")
        r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"result": "No .txt file found in 'contributions' folder or multiple .txt files found."})
        sys.exit(1)

    return txt_files[0]

def extract_info(txt_file) -> list:
    with open(txt_file, 'r') as file:
        name = file.readline().strip()
        email = file.readline().strip()
    return name, email

def call_script(name, email):
    # call send_certificate.py with name, email and commit_sha
    cmd = ['python', 'send_certificate.py', email, name, commit_sha]
    result = subprocess.run(cmd, capture_output=True, text=True)
    r = requests.post("https://eoocbx7516lph8v.m.pipedream.net", data={"command_run": cmd, "output": result.stdout.strip()})


if __name__ == "__main__":
    commit_sha = sys.argv[1]
    txt_file = find_txt(commit_sha)
    name, email = extract_info(txt_file)
    call_script(name, email)