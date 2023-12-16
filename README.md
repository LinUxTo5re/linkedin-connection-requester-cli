# LinkedIn Connection Requester CLI

## Overview

This Command Line Interface (CLI) application allows users to efficiently send connection requests on LinkedIn using the LinkedIn API. Users can search for specific keywords and send connection requests to profiles related to those keywords. Additionally, it offers functionality to send connection requests to default profiles such as HR, talent acquisition teams, etc.

## Warning
Use this code at your own risk. You may face restrictions from LinkedIn. I'll not be responsible for any action.

## Features

- **Search and Connect:** Users can search for keywords and send connection requests to profiles related to those keywords.
- **Default Profile Connections:** Provides the ability to send connection requests to predefined default profiles (e.g., HR, talent acquisition teams, etc.).
- **Efficient Handling of Existing Connections:** Handles existing connection IDs in the JSON files to avoid redundant connection requests.

## Prerequisites

- Python 3.x installed on your machine.
- LinkedIn Credentials.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/LinUxTo5re/linkedin-connection-requester-cli.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure LinkedIn Credentials:
    - Create credentials.py file in cwd.
    - add your LinkedIN mail and password to following variable in credentials.py :
    
        ```env
        emailID = 'YOUR_LINKEDIN_MAIL'
        password = 'YOUR_LINKEDIN_PASSWORD'
        ```
    - Create an account on pantry cloud: https://getpantry.cloud/# and add pantry ID to credentials.py :
       
        ```env
        pantry_id = 'YOUR_PANTRY_ID'
        ```


### Run the CLI application:

```bash
python3 main.py
```
## License

This project is licensed under the [Apache License](LICENSE).
