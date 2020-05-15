import tetpyclient
import json
import requests.packages.urllib3
import sys
import os
import xlsxwriter
import argparse
import time
import csv

from argparse import ArgumentParser
from collections import defaultdict
from datetime import datetime
from builtins import input
from columnar import columnar
import pandas as pd


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
# python3 conversation2xls.py --url https://192.168.30.4 --credential dmz_api_credentials.json --conversation conversations.json
# feedback: Le Anh Duc - anhdle@cisco.com
# =================================================================================
requests.packages.urllib3.disable_warnings()


parser = argparse.ArgumentParser(description='Tetration Create Policy under Apps')
parser.add_argument('--url', help='Tetration URL', required=True)
parser.add_argument('--credential', help='Path to Tetration json credential file', required=True)
parser.add_argument('--conversation',  help='Path to JSON Conversation file', required=True)
args = parser.parse_args()


def ShowConversation(convs):
    """
        Show All conversation and export to Excel file
        Source IP | Source Filter Name | Destination IP | Destination Filter Name | Protocol | Port | Bytes | Packets
        """
    data_list = []
    headers = ['Source IP', 'Source Filter Name', 'Destination IP', 'Destination Filter Name', 'Protocol', 'Port', 'Bytes', 'Packets']
    for x in convs: 
        data_list.append([x['src_ip'], x['src_filter_name'], x['dst_ip'], x['dst_filter_name'], x['proto_name'], x['port'], x['byte_count'], x['packet_count']]) 
    table = columnar(data_list, headers, no_borders=False)
    print(table)
    with open('conversation.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(i for i in headers)
        for row in data_list:
            writer.writerow(row)
    print ("conversation.csv created!!!")


def main():
    with open(args.conversation) as config_file:
                ShowConversation(json.load(config_file))


				

if __name__ == "__main__":
	main()