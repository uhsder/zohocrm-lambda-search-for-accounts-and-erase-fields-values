from botocore.vendored import requests
import boto3
import json
import os

def lambda_handler(event, context):
    
    
    # S3 bucket information
    # Using paint text file to store valid token
    s3 = boto3.resource('s3')
    object = s3.Object(os.environ['s3_bucket'], os.environ['file_with_zoho_token'])
    
    # Getting previous token from S3 bucket and sending test request just to get status code 200 or 401
    latestToken = object.get()['Body'].read().decode('utf-8')
    print("Retrieved last token: "+latestToken)
    testRequest = requests.get('https://www.zohoapis.com/crm/v2/Leads', headers={"Authorization": "Zoho-oauthtoken "+latestToken})
    
    # It it is not 200, then generating new token using refresh token and overwriting previous one in S3 bucket
    if testRequest.status_code != 200:
        testAuth = (requests.post(
            os.environ['refresh_token'])).json()
        latestToken = testAuth['access_token']
        object.put(Body=latestToken)
        print ("Previous token expired, overwriting with new one: " + latestToken)
    
    ## Fetching accounts which are matched with the criteria
    
    parameterToSort=event['payload']
    
    try:
        actualRequest = (requests.get('https://www.zohoapis.com/crm/v2/Accounts/search?criteria=(Issues:equals:'+parameterToSort+')', headers={"Authorization": "Zoho-oauthtoken "+latestToken}).json())
    
        ## Defining accounts array to change

        accountsArray=[]
        for account in range(0, len(actualRequest)):
            issues = []
            id = actualRequest['data'][account]['id']
            for issue in actualRequest['data'][account]['Issues']:
                if issue != parameterToSort:
                    issues.append(issue)
            accountsArray.append({'id':id, 'Issues':issues})
    
        print(json.dumps(accountsArray, indent=4, sort_keys=True))
    
        dataToSend = {"data":accountsArray}
        print dataToSend

        # Exaple of valid payload = {"data":[{"id":"2110967000043729001", "Issues":["Compliance", "Features", "TestOne"]}]}

        updateRequest = requests.put('https://www.zohoapis.com/crm/v2/Accounts', data=json.dumps(dataToSend), headers={"Authorization": "Zoho-oauthtoken "+latestToken, "Content-Type": "application/json"})
    
        print(updateRequest.json())
    except ValueError:
        print "\n"+"Dude, value which you are looking for seems to be missing, kindly try another one, cheers!"
