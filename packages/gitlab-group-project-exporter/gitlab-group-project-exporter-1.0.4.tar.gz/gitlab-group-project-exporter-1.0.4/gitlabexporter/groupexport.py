import os
import time
import gitlab
import logging


class ExportGroups():
    def __init__(self, gitlab_private_key, gitlab_private_url):
        self.gl = gitlab.Gitlab(gitlab_private_url, gitlab_private_key)

    def get_all_groups(self, main_group_id):
        main_group = self.gl.groups.get(main_group_id)
        main_group_name = main_group.full_path
        group_ids = [(main_group_name, main_group_id)]
        for (_, group_id) in group_ids:
            group = self.gl.groups.get(group_id)
            subgroups = group.subgroups.list()
            for sub in subgroups:
                group_ids.append((sub.full_path, sub.id))
        return group_ids

    def export_all_groups(self, group_ids, export_time_group, export_path_group):
        for i, (group_name, group_id) in enumerate(group_ids):
            print(
                f"Starting to export group {i+1}/{len(group_ids)} - {group_name}")

            # Create export
            g = self.gl.groups.get(group_id)
            export = g.exports.create()

            # Wait for finished status
            time.sleep(export_time_group)

            # Download export
            filename = export_path_group + \
                str(group_name) + '-export.tar.gz'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            try:
                with open(filename, 'wb') as f:
                    export.download(streamed=True, action=f.write)
            except:
                logging.error(
                    f"Error exporting group {i+1}/{len(group_ids)} - {group_name}")
