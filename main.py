import json
import credentials
from tqdm import tqdm
import os
import glob
from linkedin_api import Linkedin
import handleids
from time import sleep
from random import uniform
import pantry_cloud

# count
total_req_sent = 0
total_req_existed = 0
total_req_excluded = 0

# add id's to list
total_req_sent_list = []
total_req_existed_list = []
total_req_excluded_list = []
is_dataToCheck = False

# LinkedIn instances
api = Linkedin(credentials.emailID_ln, credentials.password_ln)


# Ask for usr input or continue with existing json files
def start_point_():
    global is_dataToCheck
    is_input = input("Do You Want To Search (Y/N): ")
    if is_input == 'Y' or is_input == 'y':
        keywords = input("Search Keywords: ")
        name_of_file = keywords.replace(' ', '_').lower()
        keyword_searched = api.search_people(keywords=keywords)
        if len(keyword_searched) != 0:
            handleids.write_file(name_of_file, keyword_searched)
            urn_ids = [urn_id['urn_id'] for urn_id in keyword_searched]
            handling_connection(urn_ids)
    else:
        current_directory = os.getcwd()
        json_pattern = '*.json'
        search_path = os.path.join(current_directory, 'JSON_files', json_pattern)
        json_files = glob.glob(search_path)
        is_dataToCheck = 'dataToCheck.json' in json_files
        json_files = [file for file in json_files if not file == 'dataToCheck.json']  # exclude dataToCheck with purpose
        for file in json_files:
            with open(file, 'r') as f:
                file_loaded = json.load(f)
                urn_ids = list(file_loaded.keys())
            handling_connection(urn_ids)


# load dataToCheck and find common ids b/w dataToCheck and loaded json
def handling_connection(urn_ids):
    global total_req_excluded_list, total_req_existed_list
    total_req_existed_list = []
    total_req_excluded_list = []
    # load existing files

    if is_dataToCheck:
        with open('dataToCheck.json', 'r') as f:
            total_req_existed_list = json.load(f)

    if len(urn_ids) == 0:
        print("NO DATA")
        return 0
    if total_req_existed_list is not None:  # excluding common values
        total_req_existed_list, urn_ids = handleids.handle_existing_connection(total_req_existed_list, urn_ids)
    if total_req_excluded_list is not None:
        urn_ids.extend(total_req_excluded_list)
        total_req_excluded_list.clear()

    total_req_existed_list = progress_status(urn_ids)
    # write data to json files
    total_req_existed_list = {str(element): index for index, element in enumerate(total_req_existed_list)}
    handleids.write_file('dataToCheck.json', keyword_searched=total_req_existed_list, is_ToCheck=True)


# progress of connection requests
def progress_status(urn_ids):
    global total_req_excluded_list, total_req_existed_list, total_req_sent_list, total_req_existed, total_req_sent, total_req_excluded
    # total_req_existed_list = total_req_excluded_list = total_req_sent_list = []
    total_req_sent = total_req_existed = total_req_excluded = 0
    if total_req_existed_list is None:
        total_req_existed_list = []

    if total_req_excluded_list is None:
        total_req_excluded_list = []

    if total_req_sent_list is None:
        total_req_sent_list = []

    progress_bar_all = tqdm(urn_ids, desc='Processing URN IDs', total=len(urn_ids), colour='red')

    for urn_id in progress_bar_all:
        progress_bar_all.set_postfix({'Processing': urn_id})  # Update progress bar
        sleep(int(uniform(15, 30)))  # hibernating to avoid any action by LinkedIn
        try:
            if api.add_connection(urn_id):
                total_req_existed_list.append(urn_id)  # Existing connection
                total_req_existed += 1
            else:
                total_req_sent_list.append(urn_id)  # New connection
                total_req_sent += 1
        except Exception as ex:
            print("Skipped...", ex)
            total_req_excluded_list.append(urn_id)  # Exception for current connection
            total_req_excluded += 1

    progress_bar_all.close()

    total_req_existed_list = total_req_existed_list + total_req_sent_list

    print(f'\n total_req_send: {total_req_sent} \n total_req_existed: {total_req_existed} '
          f'\n total_req_excluded: {total_req_excluded}')
    return total_req_existed_list


# download files from pantry_cloud
def init():
    folder_name = 'JSON_files'
    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):  # if not exists, create new
        os.makedirs(folder_path)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files_in_folder = os.listdir(folder_path)
        print("Cleaning of local files has been initiated......")
        for file_name in files_in_folder:  # delete existing files from json_files
            file_path = os.path.join(folder_path, file_name)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except Exception as e:
                pass
        else:
            details = pantry_cloud.get_account_details(pantry_id=credentials.pantry_id)
            baskets = details['baskets']
            print("download from pantry cloud has been initiated.....")
            for basket in baskets:
                json_data = pantry_cloud.create_replace_basket(credentials.pantry_id, basket_name=basket['name'],
                                                               is_download=True)
                json_name = basket['name']
                with open(os.path.join(folder_path, f'{json_name}.json'), 'w') as file:  # adding new files to
                    # json_files from pantry cloud
                    json.dump(json_data.json(), file, indent=2)
    print("initialization completed....")


# upload files to pantry_cloud
def catchup():
    folder_name = 'JSON_files'
    folder_path = os.path.join(os.getcwd(), folder_name)
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        files_in_folder = os.listdir(folder_path)
    print("uploading from local to pantry cloud has been started")
    for file_name in files_in_folder:  # list of files in json_files
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                json_data = json.load(file)
            # uploading all files to pantry cloud
            pantry_cloud.create_replace_basket(pantry_id=credentials.pantry_id, basket_name=file_name,
                                               json_data=json_data)
    print("catchup completed.....")


if __name__ == "__main__":
    init()  # download files from pantry cloud
    start_point_()  # perform linkedin operations
    catchup()  # upload files to pantry cloud
