import csv
import os
import json
from datetime import datetime


def handle_existing_connection(total_req_existed_list, urn_ids):
    common_users = set(total_req_existed_list).intersection(urn_ids)

    for user in common_users:
        urn_ids.remove(user)

    return total_req_existed_list.extend(common_users), urn_ids


def read_csv_file(filename):
    if os.path.exists(filename):
        data = []
        with open(filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                data.append(row)
        return data


def write_list_to_file(lst, filename):
    with open(filename, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(lst)


def write_json_file(filename):
    pass
    output_directory = os.path.join(os.getcwd(), 'JSON_files')
    file_path = os.path.join(output_directory, filename)
    if os.path.exists(file_path):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name, file_extension = os.path.splitext(filename)
        file_name = f"{file_name}_{timestamp}{file_extension}"
        file_path = os.path.join(output_directory, file_name)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(file_path, 'w') as file:
        json.dump(filename, file, indent=2)
