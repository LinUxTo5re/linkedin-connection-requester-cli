import requests
import json
import credentials

from linkedin_api import Linkedin

api = Linkedin(credentials.emailID_Chaitanya, credentials.password_Chaitanya)
Hr_Pune_List = api.search_people(keywords='HR Pune IT')

with open('HR_Pune.json', 'r') as file:
    HR_Pune = json.load(file)

urn_ids = [urn_id['urn_id'] for urn_id in HR_Pune]
print(len(urn_ids), '\n', urn_ids)
