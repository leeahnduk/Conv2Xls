import tetpyclient
import json
import requests.packages.urllib3
import sys
import os
import xlsxwriter
import argparse
import time
import csv
import re

from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from builtins import input
from columnar import columnar
import xlsxwriter
from openpyxl import Workbook


from tetpyclient import RestClient
from tqdm import tqdm as progress
from terminaltables import AsciiTable
import urllib3

CEND = "\33[0m"     #End
CGREEN = "\33[32m"  #Information
CYELLOW = "\33[33m" #Request Input
CRED = "\33[31m"    #Error
URED = "\33[4;31m" 
Cyan = "\33[0;36m"  #Return
# =================================================================================
# See reason below -- why verify=False param is used
# Download Conversation from Tet Cluster: python3 appsConv2xls.py --url https://10.71.129.30/ --credential Japan_api_credentials.json
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
    version =[]
    try:
        for vers in app_versions: 
            if 'v' in vers["version"]: version.append(vers['version'])
        return version[0]
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
    limit = int(input ("How many conversation you want to download? "))
    for appID in appIDs:
        print('Downloading app details for '+appID + "into json file")
        versions = GetAppVersions(rc,appID)
        version = int(re.search(r'\d+', GetLatestVersion(versions)).group(0))
        req_payload = {"version": version,
               "limit": limit
               }
        resp = rc.post('/openapi/v1/conversations/%s'%appID, json_body=json.dumps(req_payload))
        if resp.status_code == 200:
            parsed_resp = json.loads(resp.content)
            apps.append(parsed_resp)
    
    with open('all-conversations.json', "w") as config_file:
                json.dump(apps, config_file, indent=4)
                print("all-conversations.json created")



def ShowConversationTet(convs):
    """
        Show All conversation and export to Excel file
        Source IP | Source Filter Name | Destination IP | Destination Filter Name | Protocol | Port | Bytes | Packets
        """
    data_list = []
    headers = ['Source IP', 'Destination IP', 'Protocol', 'Port', 'Bytes', 'Packets']
    listconv = convs[0]
    for x in listconv['results']:
        data_list.append([x['src_ip'], x['dst_ip'], x['protocol'], x['port'], x['byte_count'], x['packet_count']]) 
    table = columnar(data_list, headers, no_borders=False)
    print(table)
    with open('conversation.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(i for i in headers)
        for row in data_list:
            writer.writerow(row)
    
    export_xlsfile = 'Apps_Conversation.xlsx'
    workbook = xlsxwriter.Workbook(export_xlsfile)
    bold = workbook.add_format({'bold': True})
    worksheet = workbook.add_worksheet(name='Apps Conversation')
    header_format = workbook.add_format()
    header_format.set_bg_color('cyan')
    header_format.set_bold()
    header_format.set_font_size(13)
    header_format.set_font_color('black')
    worksheet.set_row(0, None)
    worksheet.write_row(0,0,headers,header_format)
    i=1
    firstline = True
    with open('conversation.csv', 'r') as f:
        for row in csv.reader(f):
            if firstline:    #skip first line
                firstline = False
                continue
            worksheet.write_row(i,0,row)
            i += 1
    worksheet.set_column(0, 0, 20)
    worksheet.set_column(1, 1, 20)
    i =2
    while i < 6:
        worksheet.set_column(i, i, 15)
        i += 1
    workbook.close()
    print ('Writing csv file to %s with %d columns' % (export_xlsfile, len(headers)))
    os.remove('conversation.csv')


def main():
    rc = CreateRestClient()
    AllApps = GetApps(rc)
    appIDs = selectTetApps(AllApps)
    downloadConvs(rc, appIDs)
    with open('all-conversations.json') as config_file:
        ShowConversationTet(json.load(config_file))
				

if __name__ == "__main__":
	main()