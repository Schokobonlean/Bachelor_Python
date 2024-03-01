import requests
import xml.etree.ElementTree as ET
import secret_file

class Entry:
    def __init__(self, message_guid, iflow_name, error_text, ki_response):
        self.message_guid = message_guid
        self.iflow_name = iflow_name
        self.error_text = error_text
        self.ki_response = ki_response

beginning_period = "2024-02-01T00:00:00"
end_period = "2024-02-01T00:05:00"
host = "https://cbsintegration.it-cpi001.cfapps.eu10.hana.ondemand.com"
username = secret_file.username
password = secret_file.password

def get_mpls():

    mpl_url = f"{host}/api/v1/MessageProcessingLogs?$inlinecount=allpages&$filter=Status eq 'FAILED' and LogStart gt datetime'{beginning_period}' and LogEnd lt datetime'{end_period}'&$select=MessageGuid,IntegrationFlowName"
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
        entries.append(Entry(message_guid, iflow_name, None, None))

    for entry in entries:
        error_url = f"{host}/api/v1/MessageProcessingLogs('{entry.message_guid}')/ErrorInformation/$value"
        try:
            response = session.get(error_url,auth=(username, password))
            response.raise_for_status()
            entry.error_text = response.text
        except requests.exceptions.RequestException as e:
            raise e
        print("Name: "+entry.iflow_name+"\nGUID`: "+entry.message_guid+"\nError Text:\n"+entry.error_text+"\n\n")
get_mpls()