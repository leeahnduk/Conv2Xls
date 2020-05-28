# Conversation2Xls
This application helps to quickly convert Tetration Conversation JSON file in Tetration Policies workspace from a Tetration Cluster and convert it into Excel XLS file for reporting purpose. 

## Table of contents
* [Installation](#Installation)
* [Screenshots](#screenshots)
* [How to Use](#UserGuide)
* [Files](#Files)
* [Steps to run](#Steps)
* [Feedback and Author](#Feedback)

## Installation

From sources

Download the sources from [Github](https://github.com/leeahnduk/Conv2xls.git), extract and execute the following commands

```
$ pip3 install -r requirements.txt

```

## Screenshots
![Run screenshot](https://github.com/leeahnduk/Conv2xls/blob/master/Run.jpg)
![Run screenshot](https://github.com/leeahnduk/Conv2xls/blob/master/Result.jpg)

## UserGuide
How to use this application:
To access to the cluster you need to get the API Credentials with the following permissions
* `sensor_management` - option: SW sensor management: API to configure and monitor status of SW sensors
* `hw_sensor_management` - option: HW sensor management: API to configure and monitor status of HW sensors
* `flow_inventory_query` - option: Flow and inventory search: API to query flows and inventory items in Tetration cluster
* `user_role_scope_management` - option: Users, roles and scope management: API for root scope owners to read/add/modify/remove users, roles and scopes
* `app_policy_management` - option: 
 Applications and policy management: API to manage applications and enforce policies

Download the api_credentials.json locally and have it ready to get the information required for the setup.

A quick look for the help will list the current available options.
* To start the script, just use: `python3 conv2xls.py --url https://Cluster-IP --credential api_credentials.json --conversation conversations-all.json`


## Files
Need to prepare Tetration Policies JSON file. The sample Tetration Policies JSON file is in the github folder.
If don't have the conversation file, the script will connect to Tetration cluster to download it.
Need to prepare Tetration Conversation JSON file. The sample Tetration Conversation JSON file is in the github folder.


## Steps

Step 1: Issue `$ pip3 install -r requirements.txt` to install all required packages.

Step 2: To run the apps:
* Download Conversation from Tet Cluster: `python3 conv2xls.py --url https://Cluster-IP --credential api_credentials.json`
* Already had the conversation JSON file: `python3 conv2xls.py --url https://Cluster-IP --credential api_credentials.json --conversation conversations.json`

Step 3: Answer all the questions about the application name in your cluster to download the conversation JSON file if any.

Step 4: Open Conversation.csv to see all conversation



## Feedback
Any feedback can send to me: Le Anh Duc (leeahnduk@yahoo.com or anhde@cisco.com)
