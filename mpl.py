import requests

mock_api = "https://sandbox.api.sap.com"
mock_api_key = "tEDvfAhpREXAcCDwNAOpWGoUHla8BFCh"
mock_url = f"{mock_api}/cpi/api/v1/MessageProcessingLogs?$inlinecount=allpages&$filter=Status eq 'FAILED'"

def get_mpls():
    try:
        response = requests.get(mock_url, headers={
            # "Authorization": "Basic " + b64encode(b"username:password").decode("ascii"),
            "APIKey": mock_api_key,
            "DataServiceVersion": "2.0",
            "Accept": "application/json"
        })

        response.raise_for_status()

        responseData = response.json()
        return responseData['d']

    except requests.exceptions.RequestException as e:
        print("Error fetching message processing logs:", e)
        raise e