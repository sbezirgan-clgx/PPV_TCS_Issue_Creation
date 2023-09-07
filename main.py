import time
from threezero_lookup import LookUp
from jira import JIRA, JIRAError
import os
import csv
import pandas as pd
import math
import datetime
import custom_fields
from custom_fields import Customfield
from openpyxl import load_workbook
FILE_NAME = 'PPV_Second_Format.xlsx'
FOLDER_PATH = rf'\\filer-diablo-prd\data_acquisition\QA\EagleQC\Daily defects upload\{FILE_NAME}'
KEY_LIST = []
STAT_LIST = []
INDEX_LIST = []
PROBLEM_INDEX_LIST = []
PROBLEM_ROWS = []
PROB_TEXT = []
HEADERS=['Num_of_Records','Keys','Stat']
JIRA_USERNAME = os.getenv("JIRA_USERNAME")
JIRA_PASSWORD = os.getenv("JIRA_PASSWORD")
EDG_PMO_PROJECTS_NAME = 'EDG PMO Projects'
EDG_PMO_PROJECTS_ID = '16901'
EDG_QA_PROJECTS_NAME = 'EDG - QA Projects'
EDG_QA_PROJECTS_ID = '22400'
EDG_QA_TCS = 'EDG - QA Transaction TCS'
EDG_QA_TCS_ID = '21900'
EDG_QA_CTS_NAME = 'EDG - Transactions QA CTS'
EDG_QA_CTS_ID = '21300'
BEGIN_DATE_STRING = 'T12:05:00.000-0700'
LookUp.thirtyseventytwo_Values
def start_connection():
    '''Jira Server Connection'''
    jiraOptions = {'server': "https://jira-corelogic.valiantys.net"}
    jira = JIRA(options=jiraOptions, basic_auth=(JIRA_USERNAME, JIRA_PASSWORD))
    return jira


def get_transition_id_by_name(jira: JIRA, issue, name: str):
    transitions = jira.transitions(issue)
    transition_list = [(t['id'], t['name']) for t in transitions]
    print(transition_list)
    transition_list_iterator = filter(lambda x: (x[1] == name), transition_list)
    filtered_transition_list = list(transition_list_iterator)
    print(filtered_transition_list)
    return filtered_transition_list[0][0]


def get_transition_name_list(jira:JIRA, issue):
    transitions = jira.transitions(issue)
    transition_list = [t['name'] for t in transitions]
    return transition_list


def set_issue_statuses_by_name(jira:JIRA,keys_list,name):
    for key in keys_list:
        iss = jira.issue(key)
        if name.lower() == 'open':
            jira.transition_issue(iss,transition='OPEN')
        elif name.lower() == 'closed':
            jira.transition_issue(iss,transition='Closed')

def format_the_date(value: str):
    try:
        new_date = value.split("/")
        if not new_date[0].startswith("0"):
            new_date[0] = '0' + new_date[0] if int(new_date[0]) < 10 and not "0" in new_date[0] else new_date[0]
        if not new_date[1].startswith("0"):
            new_date[1] = '0' + new_date[1] if int(new_date[1]) < 10 and not "0" in new_date[1] else new_date[1]
        strr = new_date[2] + "-" + new_date[0] + "-" + new_date[1]
        return strr
    except AttributeError:
        return None



def create_status_csv(header_list,key_list,status_list):
    len_list = int(len(key_list))
    num_list = []
    for i in range(len_list):
        num_list.append(i + 1)

    zipped_list = list(zip(num_list, key_list, status_list))
    with open('out2.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(header_list)
        write.writerows(zipped_list)

def create_problem_csv(header_list,index_list,dataframe):
    with open('problem.csv','w') as d:
        write = csv.writer(d)
        write.writerow(header_list)
        for index in index_list:
            pass


def create_bulk_issues(jira:JIRA,issue_value_list):
    new_issues = jira.create_issues(field_list=issue_value_list)
    global KEY_LIST
    num_of_errors=0
    num_of_issues = 1
    for issue in new_issues:
        if issue['status'] == 'Success':
            KEY_LIST.append(issue['issue'].key)
        else:
            print(f"Row number: {num_of_issues} has an error. Error is : {issue['error']}")
            num_of_errors +=1
        num_of_issues += 1
    print(f"Number of errors while creating the jira issues are:{num_of_errors} ")
    print(f"List of issues created successfully:{KEY_LIST}")
    return KEY_LIST


jira = start_connection()
df = pd.read_excel(FOLDER_PATH)
df = df.reset_index()
print(df)
format_list = []
num_of_errors = 0
num_of_issues = 0

for index, row in df.iterrows():
    lookup_key = str(row['3072 Field Name']).split("_")[0]
    my_val = 'mgundluru@corelogic.com' if row['Assignee '] != 'varssingh@corelogic.com' else 'varssingh@corelogic.com'
    QA_Regular_Format1_3072 = {
        'project': {'id': '21900'},#'EDG - QA Transaction TCS'
        'summary': row['Summary'],  #Summary
        'description': row['Description'],#Description
        'issuetype': {'name': row['Issue Type']},#IssueType
        #'customfield_24512': {'value': row['3072 Field Name']},  # 3072-------------
        'customfield_24512': {'value': LookUp.thirtyseventytwo_Values[lookup_key]},#3072
        'customfield_29815': ' ' if math.isnan(row['Record ID']) else str(row['Record ID']),  # RecordID
        'customfield_24502': {'value': row['Project']},  # Project
        'customfield_24513': {'value': row['Vendor Name']},  # Vendor
        'customfield_18909': {'value': row['State']},  # State
        'customfield_25100': {'value': row['County'].upper()},  # County
        'customfield_24519': ' ' if math.isnan(row['Doc Number']) else str(row['Doc Number']),  # Doc Number
        'customfield_26900': ' ' if math.isnan(row['Recording Book']) else str(row['Recording Book']),  # Recording Book
        'customfield_27309': ' ' if math.isnan(row['Recording Page']) else str(row['Recording Page']),  # Recording Page
        'customfield_24526': format_the_date(row['Recording date']),  # Recording Date
        'customfield_26002': str(row['Doc Year']),  # DocYear
        'customfield_24501': {'value': row['Deed Category']},  # DeedCategory
        'customfield_24511': {'value': row['DAMAR Code']},  # DAMAR
        # 'customfield_24508' : {'value' : ''},#ADC
        'customfield_24505': {'value': row['Type of Error']},  # TypeofError
        'customfield_24517': {'name': row['Detected By']},  # DetectedBy
        'customfield_24529': format_the_date(row['Detected Date']),  #Detected Date
        'customfield_24528': row['Sample date '],  # Sample Date
        'customfield_24506': {'value': row['Critical/Non-Critical']},  # Critical
        'customfield_24515': format_the_date(row['BatchDate']), # Batch Date
        'customfield_26003': str(row["Batch Seq"]), #Batch Seq
        'customfield_26004': str(row["FIPS"]),#FIPS Code
        'customfield_26015': str(row["Layout"]),#Layout
        'assignee': {'name': my_val}, #Assignee
        'customfield_25506': ' ' if math.isnan(row['FilmID']) else str(row['FilmID']),#FilmID
        'customfield_17716' : format_the_date(row['Begin date']), #Begin Date
        'customfield_25900' : str(row["Remarks"]) #Remarks
    }

    try:
        new_issue = jira.create_issue(fields=QA_Regular_Format1_3072)

    except JIRAError as e:
        print(f"Error in row #{index+2}")
        print(e.response.text)
        error_list =  e.response.text.split(",")[1:]
        error_str = " ".join(error_list)
        PROB_TEXT.append(error_str)
        num_of_errors +=1
        PROBLEM_INDEX_LIST.append(index)


    else:
        num_of_issues += 1
        print(f"Row #{index+2}: created with the key\t" +new_issue.key)
        KEY_LIST.append(str(new_issue.key))
        STAT_LIST.append(df.loc[index,"Status"])
        INDEX_LIST.append(index)




    format_list.append(QA_Regular_Format1_3072)
print(f"Total number of errors encountered: {num_of_errors}")
print(f"Total number of issues have created:{num_of_issues}")
print(f"Total number of records in the excel sheet:{len(df.index)}")
print(PROB_TEXT)
#df['Error Description'] = PROB_TEXT

zipped_list = list(zip(INDEX_LIST, KEY_LIST, STAT_LIST))
zipped_list_short = list(zip(INDEX_LIST, KEY_LIST))
print(len(df.index))
print(zipped_list)
print(PROBLEM_INDEX_LIST)
NO_KEY_LIST = []

for _ in range(len(PROBLEM_INDEX_LIST)):
    NO_KEY_LIST.append('No Key')
NO_LIST = list(zip(PROBLEM_INDEX_LIST,NO_KEY_LIST)) + zipped_list_short
LLT = NO_LIST.sort(key=lambda x : x[0]) #Full List of indexes with Jira keys and No keys
JUST_KEY_LIST = [l[1] for l in NO_LIST]
with open('out2.csv', 'w') as f:
    write = csv.writer(f)
    write.writerow(HEADERS)
    write.writerows(zipped_list)

time.sleep(2)
with open('out2.csv', "r") as my_file:
    # pass the file object to reader()
    file_reader = csv.reader(my_file)
    # do this for all the rows
    for i in file_reader:
        if i == [] or i == ['Num_of_Records', 'Keys', 'Stat']:
            continue
        iss = jira.issue(str(i[1]))
        if i[2].lower() == 'open':
            jira.transition_issue(iss,transition='OPEN')
        elif i[2].lower() == 'closed':
            jira.transition_issue(iss, transition='Closed')


prob_df = df.loc[PROBLEM_INDEX_LIST]
print("------------")
print(prob_df)
print(len(PROB_TEXT))
PROB_LIST = []
for prob in PROB_TEXT:
    new_list = prob.split('"')
    WOW_LIST = []
    for item in new_list:
        if "custom" not in item:
            new_list.remove(item)
    for item1 in new_list:
        if "custom" in item1:
            WOW_LIST.append(item1)
    PROB_LIST.append(WOW_LIST)
print(PROB_LIST)
for i in PROB_LIST:
    length = 0
    for a in i:
        if a in Customfield.cust_field_dic.keys():
            new_str = str(a.replace(a,Customfield.cust_field_dic[a]))
            i[length] = new_str
        length += 1
print(PROB_LIST)
print('---------------')
prb_lst = pd.Series(PROB_TEXT)
prob_df['Defected Fields'] = PROB_LIST
prob_df.to_csv('prob.csv',encoding='utf-8', index=False)
time.sleep(2)

prob = pd.read_csv('prob.csv')
prob.to_excel("Defected_File.xlsx",sheet_name='Defected records', index=False)
field_code_df = pd.DataFrame.from_dict(Customfield.custom_field_dictt)
time.sleep(2)
writer = pd.ExcelWriter('Defected_File.xlsx', engine='openpyxl', mode='a')
field_code_df.to_excel(writer,sheet_name='Code Table')
writer.close()
df.insert(32, "Jira Keys",JUST_KEY_LIST)
df.to_excel(FOLDER_PATH, index=False)
print(field_code_df)
#issue = jira.issue('ETQT-22807')
#read_csv_line_by_line(filename='out2.csv',jira=jira)
#create_bulk_issues(jira=jira,issue_value_list=format_list)
# str = '5/31/2023'
# print(strr)




