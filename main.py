import requests
import json
import credentials
from tqdm import tqdm
import csv
import os
import glob
from linkedin_api import Linkedin
import handleids

# count
total_req_sent = 0
total_req_existed = 0
total_req_excluded = 0

# add id's to list
total_req_sent_list = []
total_req_existed_list = []
total_req_excluded_list = []

api = Linkedin(credentials.emailID_Chaitanya, credentials.password_Chaitanya)


def start_point_():
    is_input = input("Do You Want To Search (Y/N): ")
    if is_input == 'Y' or is_input == 'y':
        keywords = input("Search Keywords: ")
        name_of_file = keywords.replace(' ', '_').lower()
        keyword_searched = api.search_people(keywords=keywords)
        handleids.write_json_file(keyword_searched)
        urn_ids = [urn_id['urn_id'] for urn_id in keyword_searched]
        handling_connection(urn_ids)
    else:
        current_directory = os.getcwd()
        json_pattern = '*.json'
        search_path = os.path.join(current_directory + '/JSON_files', json_pattern)
        json_files = glob.glob(search_path)
        for file in json_files:
            with open(file, 'r') as f:
                file_loaded = json.load(f)
                urn_ids = [urn_id['urn_id'] for urn_id in file_loaded]
            handling_connection(urn_ids)


def handling_connection(urn_ids):
    global total_req_excluded_list, total_req_existed_list
    # load csv files
    total_req_existed_list = handleids.read_csv_file('existing_connection.csv')
    total_req_excluded_list = handleids.read_csv_file('excluded_connection.csv')

    total_req_existed_list, urn_ids = handleids.handle_existing_connection(total_req_existed_list, urn_ids)
    urn_ids.extend(total_req_excluded_list)
    total_req_excluded_list.clear()

    progress_status(urn_ids)
    # write data to csv files
    handleids.write_list_to_file(total_req_existed_list, 'existing_connection.csv')
    handleids.write_list_to_file(total_req_excluded_list, 'excluded_connection.csv')


def progress_status(urn_ids):
    global total_req_excluded_list, total_req_existed_list, total_req_existed_list, total_req_existed, total_req_sent, total_req_excluded
    progress_bar_all = tqdm(urn_ids, desc='Processing URN IDs', total=len(urn_ids), colour='red')
    for i in progress_bar_all:
        progress_bar_all.set_postfix({'Processing': i})  # host-LinkedIn user
        for urn_id in urn_ids:
            try:
                if api.add_connection(urn_id):
                    print("Already Connected with host")
                    total_req_existed_list.append(urn_id)
                    total_req_existed += 1
                else:
                    print("successfully connected")
                    total_req_sent_list.append(urn_id)
                    total_req_sent += 1

            except Exception as ex:
                print("Skipped...")
                total_req_excluded_list.append(urn_id)
                total_req_excluded += 1
        progress_bar_all.close()

        total_req_existed_list = total_req_existed_list + total_req_sent_list

    print(f'\n total_req_send: {total_req_sent} \n total_req_existed: {total_req_existed} '
          f'\n total_req_excluded: {total_req_excluded}')


if __name__ == "__main__":
    start_point_()
