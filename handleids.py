import os
import json
from datetime import datetime


# exclude common urn ids
def handle_existing_connection(total_req_existed_list, urn_ids):
    common_users = set(total_req_existed_list).intersection(urn_ids)
    for user in common_users:
        urn_ids.remove(user)
    return total_req_existed_list.extend(common_users), urn_ids


# write json file on local disk
def write_file(filename, keyword_searched, is_ToCheck=False):
    output_directory = os.path.join(os.getcwd(), 'JSON_files')
    file_path = os.path.join(output_directory, filename)
    if os.path.exists(file_path) and not is_ToCheck:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name, file_extension = os.path.splitext(filename)
        file_name = f"{file_name}_{timestamp}{file_extension}"
        file_path = os.path.join(output_directory, file_name)

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(file_path, 'a') as file:
        json.dump(keyword_searched, file, indent=2)
