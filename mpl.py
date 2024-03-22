import requests
import xml.etree.ElementTree as ET
import secret_file
import re

class Entry:
    def __init__(self, message_guid = None, iflow_name = None, error_text = None, ki_response = None, in_charge = None, in_charge_mail = None):
        self.message_guid = message_guid
        self.iflow_name = iflow_name
        self.error_text = error_text
        self.ki_response = ki_response
        self.in_charge = in_charge
        self.in_charge_mail = in_charge_mail

"""
home_host = "https://cbsintegration.it-cpi001.cfapps.eu10.hana.ondemand.com"
client_host = "https://l100956-tmn.hci.eu1.hana.ondemand.com"
client_host_prod = "https://l100957-tmn.hci.eu1.hana.ondemand.com"
"""

username = secret_file.client_username
password = secret_file.client_password

def get_mpls(host, beginning_period, end_period):

    mpl_url = f"{host}/api/v1/MessageProcessingLogs?$inlinecount=allpages&$filter=Status eq 'FAILED'"# and LogStart gt datetime'{beginning_period}' and LogEnd lt datetime'{end_period}'&$select=MessageGuid,IntegrationFlowName"
    session = requests.Session()

    try:
        response = session.get(mpl_url,auth=(username, password))
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise e
    
    root = ET.fromstring(response.text)
    entries = []
    for entry_elem in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        message_guid = entry_elem.find(".//{http://schemas.microsoft.com/ado/2007/08/dataservices}MessageGuid").text
        iflow_name = entry_elem.find(".//{http://schemas.microsoft.com/ado/2007/08/dataservices}IntegrationFlowName").text
        entries.append(Entry(message_guid, iflow_name))
    for entry in entries:
        error_url = f"{host}/api/v1/MessageProcessingLogs('{entry.message_guid}')/ErrorInformation/$value"
        try:
            response = session.get(error_url,auth=(username, password))
            response.raise_for_status()
            entry.error_text = response.text
        except requests.exceptions.RequestException as e:
            raise e
    return entries

def write_to_file(entries):
    mesages = set()
    for entry in entries:
        mpl_id_pattern = r'The MPL ID for the failed message is : .+'
        inner_error_pattern = r',? *("innerError":{.*?})'
        message = re.sub(mpl_id_pattern, '', entry.error_text)
        message = re.sub(inner_error_pattern, '', message)
        mesages.add(message.replace("\n", ""))
    with open("mpls_cient_prod.txt", "w") as file:
        for message in mesages: 
            file.write(message)
            file.write("\n")