import requests
import json
import credentials
from tqdm import tqdm
import csv
import os
import glob
from linkedin_api import Linkedin
import time

total_req_sent = 0
total_req_existed = 0
total_req_excluded = 0

total_req_sent_list = []
total_req_existed_list = []
total_req_excluded_list = []

api = Linkedin(credentials.emailID_Chaitanya, credentials.password_Chaitanya)
keywords = input("Search Keywords: ")
name_of_file = keywords.replace(' ', '_').lower()

if len(keywords) == 0:
    current_directory = os.getcwd()
    json_pattern = '*.json'
    search_path = os.path.join(current_directory, json_pattern)
    json_files = glob.glob(search_path)
    for file in json_files:
        with open(file, 'r') as f:
            file_loaded = json.load(f)
            print(f'{file} loaded successfully')
else:
    keyword_searched = api.search_people(keywords='HR Pune IT')


file_name_to_load = ''
urn_ids = [urn_id['urn_id'] for urn_id in file_name_to_load]


# print(len(urn_ids), '\n', urn_ids)
def read_csv_file(filename):
    if os.path.exists(filename):
        data = []
        with open(filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data


total_req_existed_list = read_csv_file('existing_connection.csv')
total_req_excluded_list = read_csv_file('excluded_connection.csv')

# added 1, total sent- 21
# print(api.add_connection(urn_ids[0])) # single connection (urn_id - id of host)
# host-LinkedIn user

progress_bar_all = tqdm(urn_ids, desc='Processing URN IDs', total=len(urn_ids), colour='red')
for i in progress_bar_all:
    progress_bar_all.set_postfix({'Processing': i})
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

total_req_existed.append
print(f'\n total_req_send: {total_req_sent} \n total_req_existed: {total_req_existed} '
      f'\n total_req_excluded: {total_req_excluded}')


def write_list_to_file(lst, filename):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(lst)


write_list_to_file(total_req_existed_list, 'existing_connection.csv')
write_list_to_file(total_req_excluded_list, 'excluded_connection.csv')
