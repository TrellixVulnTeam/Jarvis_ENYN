import os
import git
import json
import subprocess
import shutil

# open versions
relPath = str(Path(__file__).parent) + "/"
with open(relPath + "versions.json", "r") as old_versions_file:
    old_version = json.load(old_versions_file)

os.mkdir(relPath + 'temp')

git_url = 'https://github.com/JakobPrie/Jarvis'
download_path = relPath + 'temp/'
git.Git(download_path).clone(git_url)

with open(download_path + 'versions.json', 'r') as new_versions_file:
    new_versions = json.load(new_versions_file)

if new_versions.get('version') != old_version.get('version'):
    # this version is not up-to-date
    last_versions = new_versions.get('last versions')
    for version in last_versions:
        if verion.get('version') == old_version.get('version'):
            break
        for item in new_versions.get('shellcommands for update'):
            subprocess.call(item.split(' '))

    os.remove(relPath + 'modules')
    try:
        shutil.copytree(download_path + 'modules/', relPath + 'modules/')
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(download_path + 'modules/', relPath + 'modules/')
        else:
            raise


os.remove(relPath + 'temp')
