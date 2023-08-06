import os
from datetime import datetime
from gitlabexporter.groupexport import ExportGroups
from gitlabexporter.projectexport import ExportProjects


if __name__ == "__main__":
    MAIN_GROUP_ID = 1234567
    GITLAB_PRIVATE_KEY = 'ABC'
    GITLAB_URL = 'https://gitlab.com'
    EXPORT_TIME_GROUP = 60  # seconds
    EXPORT_TIMEOUT_PROJECT = 3600  # seconds
    EXPORT_PATH_GROUP = os.environ['HOME'] + "/gitlab-backups/" + \
        datetime.today().strftime('%Y%m%d') + "/groups/"
    EXPORT_PATH_PROJECT = os.environ['HOME'] + "/gitlab-backups/" + \
        datetime.today().strftime('%Y%m%d') + "/projects/"

    p = ExportProjects(GITLAB_PRIVATE_KEY, GITLAB_URL)
    project_ids = p.get_all_projects(MAIN_GROUP_ID)
    p.export_all_projects(
        project_ids, EXPORT_TIMEOUT_PROJECT, EXPORT_PATH_PROJECT)

    g = ExportGroups(GITLAB_PRIVATE_KEY, GITLAB_URL)
    group_ids = g.get_all_groups(MAIN_GROUP_ID)
    g.export_all_groups(group_ids, EXPORT_TIME_GROUP, EXPORT_PATH_GROUP)
