import os


def create_folders(new_folder_name, usr):
    root_nodes = usr.get_files()
    folder_exists = any(node['type'] == 'folder' and node['name'] == new_folder_name for node in root_nodes.values())

    if not folder_exists:
        usr.create_folder(new_folder_name)


def upload_file(folder_name, usr):
    mega_folder = usr.find(folder_name, exclude_deleted=True)
    create_folders(folder_name, usr)  # create folder if it doesn't exist
    if mega_folder:
        mega_folder_id = mega_folder[0]

        # delete existing files from folder
        existing_files = usr.get_files_in_node(mega_folder_id)
        if existing_files:
            for file_info in existing_files:
                file_id = file_info['h']
                usr.delete(file_id)
        local_folder_path = os.path.join(os.getcwd(), folder_name)

        if os.path.exists(local_folder_path) and os.path.isdir(local_folder_path):
            files_to_upload = os.listdir(local_folder_path)

            # uploading files to folder
            for file_name in files_to_upload:
                file_path = os.path.join(local_folder_path, file_name)
                if os.path.isfile(file_path):
                    usr.upload(file_path, mega_folder_id)


def download_file(folder_name, usr):
    create_folders(folder_name, usr)  # create folder if it doesn't exist
    extension = '.json' if folder_name == 'JSON_files' else '.csv'
    folder_node = usr.find(folder_name, exclude_deleted=True)
    if folder_node:
        folder_id = folder_node[0]
        files_in_folder = usr.get_files_in_node(folder_id)

        # downloading files from folder
        for file_info in files_in_folder:
            file_name = file_info['a']['n']
            if file_name.lower().endswith(extension):
                file_id = file_info['h']
                usr.download_from_node(file_id, os.path.join(folder_name, file_name))
