import requests
import json
from bs4 import BeautifulSoup
import re

beginning_period = "2024-02-01T00:00:00"
end_period = "2024-02-14T00:00:00"

host = "https://cbsintegration.it-cpi001.cfapps.eu10.hana.ondemand.com"
username = "S0019518955"
password = "80W{}>ER"

def get_mpls():

    host_url = f"{host}/api/v1/MessageProcessingLogs?$inlinecount=allpages&$filter=Status eq 'FAILED' and LogStart gt datetime'{beginning_period}' and LogEnd lt datetime'{end_period}'"
    session = requests.Session()

    try:
        response = session.get(host_url, headers={
            #"DataServiceVersion": "2.0",
            #"Accept": "application/json"
        },auth=(username, password))

        response.raise_for_status()

        print(response.text)

    except requests.exceptions.RequestException as e:
        print(e)
        raise e
    

mock_api = "https://sandbox.api.sap.com"
mock_api_key = "tEDvfAhpREXAcCDwNAOpWGoUHla8BFCh"

def get_mpls_mock():

    mock_url = f"{mock_api}/cpi/api/v1/MessageProcessingLogs?$inlinecount=allpages&$filter=Status eq 'FAILED' and LogStart gt datetime'{beginning_period}' and LogEnd lt datetime'{end_period}'"
    
    try:
        response = requests.get(mock_url, headers={
            "APIKey": mock_api_key,
            "DataServiceVersion": "2.0",
            "Accept": "application/json"
        })

        response.raise_for_status()
        responseData = response.json()['d']

        print(json.dumps(responseData, indent=4))

        return responseData

    except requests.exceptions.RequestException as e:
        print("Error fetching message processing logs:", e)
        raise e

get_mpls()


"""

notes
 - if i need to access the custom header properties: https://<host address>/api/v1/MessageProcessingLogs('ABCD-1234-XYZ')​/CustomHeaderProperties'

 response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        redirection_script = soup.find('script').get_text()
        url_pattern = r"location=['\"]([^'\"]+)['\"]"
        matching_url = re.search(url_pattern, redirection_script).group(1)

        response = session.get(matching_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        auth_url = soup.find_all('a', class_='saml-login-link')[0].get('href')

        response = session.get(auth_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        login_form = soup.find('form', id='logOnForm')
        form_data = {}
        for input_tag in login_form.find_all('input'):
            if input_tag.get('name'):
                form_data[input_tag['name']] = input_tag.get('value', '')
        form_data['j_username'] = username

        response = session.post(auth_url, data=form_data)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        login_form = soup.find('form', id='logOnForm')
        form_data = {}
        for input_tag in login_form.find_all('input'):
            if input_tag.get('name'):
                form_data[input_tag['name']] = input_tag.get('value', '')
        form_data['j_password'] = password

        response = session.post(auth_url, data=form_data)
        response.raise_for_status()

"""