from tetpyclient import RestClient
from builtins import input
import tetpyclient
import json
import requests.packages.urllib3
import sys
import os
import argparse
import time
import csv
import re
from columnar import columnar


CEND = "\33[0m"     #End
CGREEN = "\33[32m"  #Information
CYELLOW = "\33[33m" #Request Input
CRED = "\33[31m"    #Error
URED = "\33[4;31m" 
Cyan = "\33[0;36m"  #Return

# =================================================================================
# See reason below -- why verify=False param is used
# python3 downloadAppsConv.py --url https://192.168.30.4 --credential dmz_api_credentials.json
# feedback: Le Anh Duc - anhdle@cisco.com
# =================================================================================
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser(description='Tetration Get an App detail and create JSON file for the detail')
parser.add_argument('--url', help='Tetration URL', required=True)
parser.add_argument('--credential', help='Path to Tetration json credential file', required=True)
args = parser.parse_args()


def CreateRestClient():
    """create REST API connection to Tetration cluster
    Returns:
        REST Client
    """
    rc = RestClient(args.url,
                    credentials_file=args.credential, verify=False)
    return rc

def GetApps(rc):
    resp = rc.get('/applications')

    if resp.status_code != 200:
        print(URED + "Failed to retrieve Apps list" + CEND)
        print(resp.status_code)
        print(resp.text)
    else:
        return resp.json()


def ShowApps(Apps):
    AppsList = []
    headers = ['Number', 'App Name', 'Author', 'App ID', 'Primary?']
    for i,app in enumerate(Apps): AppsList.append([i+1,app["name"] , app['author'], app["id"], app['primary']])
    table = columnar(AppsList, headers, no_borders=False)
    print(table)

def GetAppVersions(rc, appid):
    resp = rc.get('/applications/' + appid + '/versions')

    if resp.status_code != 200:
        print(URED + "Failed to retrieve Apps list" + CEND)
        print(resp.status_code)
        print(resp.text)
    else:
        return resp.json()

def GetLatestVersion(app_versions):
    try:
        for vers in app_versions: 
            if "v" in vers["version"]: return vers["version"]
    except:
        print(URED + "Failed to retrieve latest app version"+ CEND)

def GetLatestEnforcedVersion(app_versions):
    try:
        for vers in app_versions: 
            if "p" in vers["version"]: return vers["version"]
    except:
        print(URED + "Failed to retrieve latest app version"+ CEND)

def selectTetApps(apps):
    # Return App IDa for one or many Tetration Apps that we choose
    print (Cyan + "\nHere are all Application workspaces in your cluster: " + CEND)
    ShowApps(apps)
    choice = input('\nSelect which Tetration Apps (Number, Number) above you want to download polices: ')

    choice = choice.split(',')
    appIDs = []
    for app in choice:
        if '-' in app:
            for app in range(int(app.split('-')[0])-1,int(app.split('-')[1])):
                appIDs.append(resp.json()[int(app)-1]['id'])
        else:
            appIDs.append(apps[int(app)-1]['id'])
    return appIDs

def downloadConvs(rc,appIDs):
    # Download Apps Conversation JSON files from Apps workspace
    apps = []
    for appID in appIDs:
        print('Downloading app details for '+appID + "into json file")
        versions = GetAppVersions(rc,appID)
        version = int(re.search(r'\d+', GetLatestVersion(versions)).group(0))
        req_payload = {"version": version,
               "limit": 100000
               }
        resp = rc.post('/openapi/v1/conversations/%s'%appID, json_body=json.dumps(req_payload))
        if resp.status_code == 200:
            parsed_resp = json.loads(resp.content)
            apps.append(parsed_resp)
    
    with open('all-conversations.json', "w") as config_file:
                json.dump(apps, config_file, indent=4)
                print("all-conversations.json created")


def main():
    rc = CreateRestClient()
    apps = GetApps(rc)
    appIDs = selectTetApps(apps)
    downloadConvs(rc, appIDs)


if __name__ == "__main__":
    main()