from mega import Mega
from credentials import emailID_mega, password_mega

mega = Mega()
usr = mega.login(emailID_mega, password_mega)

root_nodes = usr.get_files()


def create_folders(new_folder_name):
    folder_exists = any(node['type'] == 'folder' and node['name'] == new_folder_name for node in root_nodes.values())

    if not folder_exists:
        folder = usr.create_folder(new_folder_name)


create_folders('JSON_files')
create_folders('CSV_files')


def upload_file(filename, folder_name):
    folder = usr.find(folder_name)
    usr.upload(filename, folder[0])


def download_file(filename):
    file = usr.find(filename)
    usr.download(file)


def search_files(extension):
    files = [node for node in root_nodes.values()
             if node['type'] == 'file' and node['name'].lower().endswith(extension)]

