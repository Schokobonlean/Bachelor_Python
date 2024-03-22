import msal
import requests
import secret_file

TENANT_ID = secret_file.mail_tenant_id
CLIENT_ID = secret_file.mail_client_id
CLIENT_SECRET = secret_file.mail_client_secret
AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'

RESOURCE = 'https://graph.microsoft.com'

app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

scopes = ["https://graph.microsoft.com/.default"]

def send_mail(to, body, flow_name):

    result = app.acquire_token_silent(scopes, account=None)

    if not result:
        result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        userId = secret_file.mail_user_id
        endpoint = f'https://graph.microsoft.com/v1.0/users/{userId}/sendMail'
        
        email_msg = {'Message': {
                        'Subject': "Error in Integration Flow "+flow_name+"!",
                        'Body': {
                            'ContentType': 'Text',
                            'Content': body
                            },
                        'ToRecipients': [{
                            'EmailAddress': {
                                'Address': to
                                }
                            }]
                        },
                    'SaveToSentItems': 'true'}
        
        r = requests.post(endpoint, headers={'Authorization': 'Bearer ' + result['access_token']}, json=email_msg)
        
        if r.ok:
            print('Sent email successfully')
        else:
            print(r.json())

    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))