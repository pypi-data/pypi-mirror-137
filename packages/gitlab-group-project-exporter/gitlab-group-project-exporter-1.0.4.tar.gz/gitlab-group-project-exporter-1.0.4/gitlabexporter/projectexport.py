import os
import time
import gitlab
import logging


class ExportProjects():
    def __init__(self, gitlab_private_key, gitlab_private_url):
        self.gl = gitlab.Gitlab(gitlab_private_url, gitlab_private_key)

    def get_all_projects(self, main_group_id):
        group = self.gl.groups.get(main_group_id)
        projects = group.projects.list(include_subgroups=True, all=True)
        project_ids = []
        for project in projects:
            project_ids.append((project.path_with_namespace, project.id))
        return project_ids

    def export_all_projects(self, project_ids, export_timeout_project, export_path_project):
        for i, (project_name, project_id) in enumerate(project_ids):
            print(
                f"Starting to export project {i+1}/{len(project_ids)} - {project_name}")

            # Create export
            p = self.gl.projects.get(project_id)
            export = p.exports.create()

            # Wait for finished status
            export.refresh()
            t1 = time.time()
            while export.export_status != 'finished':
                if round(time.time()-t1) >= export_timeout_project:
                    break
                print(
                    f"Project {i+1}/{len(project_ids)} exporting since {round(time.time()-t1)} seconds...")
                time.sleep(1)
                export.refresh()

            # Download export
            filename = export_path_project + \
                str(project_name) + '-export.tar.gz'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            try:
                with open(filename, 'wb') as f:
                    export.download(streamed=True, action=f.write)
            except:
                logging.error(
                    f"Error exporting project {i+1}/{len(project_ids)} - {project_name}")
