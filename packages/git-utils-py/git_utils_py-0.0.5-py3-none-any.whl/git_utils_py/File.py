import gitlab


def download_file(host,
                  token,
                  project_name,
                  project_id,
                  file_search_path,
                  file_search_name,
                  file_search_extension,
                  file_output_path,
                  file_output_name=None,
                  branch_name='master'):
    try:
        gl = gitlab.Gitlab(url=host, private_token=token)
        project = None

        if project_name is not None:
            project = gl.projects.get(project_name)

        if project_id is not None:
            project = gl.projects.get(project_id)

        if project is None:
            return None

        if file_output_name is None:
            file_output_name = file_search_name

        with open(file_output_path + '/' + file_output_name + '.' + file_search_extension, 'wb') as f:
            project.files.raw(file_path=file_search_path + '/' + file_search_name + '.' + file_search_extension,
                              ref=branch_name,
                              streamed=True,
                              action=f.write)
    except Exception as e:
        print("Error:", e)
