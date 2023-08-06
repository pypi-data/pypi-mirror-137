# gitlab-group-project-exporter

This project can be used to export GitLab groups and projects inside a main group. This repo can be used for regularly backing up content from Gitlab.com server to a private storage.

## Install

Download and install directly from PyPi using ```pip install gitlab-group-project-exporter``` or download source from this git and install using ```sudo python3 setup.py install```.

## Usage

The main script to be run for exporting groups and projects is ```bin/main.py```. The parameters to be configured in this script are:

| Parameter | Explanation |
| :---: | :---: |
| MAIN_GROUP_ID | The ID of the main group. All the subgroups and projects of this group will be backed up. |
| GITLAB_PRIVATE_KEY | GitLab private key/personal token with api access. Can be obtained after logging into your account from https://gitlab.com/-/profile/personal_access_tokens. |
| GITLAB_URL | The URL where GitLab instance is installed. Should be ```https://gitlab.com``` for GitLab.com installation. |
| EXPORT_TIME_GROUP | Maximum amount in seconds till a group export is awaited to be prepared. |
| EXPORT_TIMEOUT_PROJECT | Maximum amount in seconds till a project export is awaited to be prepared. |
| EXPORT_PATH_GROUP | The path where backup of main group and all subgroups inside the main group will be expored. |
| EXPORT_PATH_PROJECT | The path where all projects inside the main group will be exported. |
