import pandas as pd
import os
import datetime

hey = datetime.datetime.strptime("12/21/2008", "%m/%d/%Y").strftime("%Y-%m-%d")
print(hey)
# df = pd.read_excel("Example_Testing.xlsx")
# LIST = [(0, 'ETQT-25228'), (1, 'ETQT-25229'), (2, 'No Key')]
# JUST_KEY_LIST = [l[1] for l in LIST]
#
# df.insert(29, "Jira Keys4",JUST_KEY_LIST)
# df.to_excel("Example_Testing.xlsx", index=False)
#
# print(df)
"""
from jira import JIRA
def start_connection():
    '''Jira Server Connection'''
    jiraOptions = {'server': "https://jira-corelogic.valiantys.net"}
    jira = JIRA(options=jiraOptions, basic_auth=('Internal-EDG-SA-BulkDefects', 'iXyM*8W!s84&'))
    return jira

jira = start_connection()
allfields = jira.fields()

# Fetch all fields


# Make a map from field name -> field id
name_map = {field['name']:field['id'] for field in allfields}
# print(name_map)
issue = jira.issue('ETQA-110726')
print(issue.raw['fields'])
# for field_name in issue.raw['fields']:
#     print ("Field:", field_name, "Value:", issue.raw['fields'][field_name])


def format_the_date(value):
    try:
        er = value.split(" ")[0]
        return er
    except AttributeError:
        return None



# df = pd.read_excel("ass.xlsb",parse_dates=["Detected Date"],
#                    date_parser=lambda x: pd.to_datetime(x,format='%Y-%m-%d %I:%M:%S'))
df=pd.read_excel("ass.xlsb")
#df['BatchDate']= pd.to_datetime(pd.to_numeric(df['BatchDate'],errors='coerce'),errors='coerce',origin='1899-12-30',unit='D')
df["Detected Date"] = pd.to_datetime(df['Detected Date'], unit='D', origin='1899-12-30')

df['Detected Date'] = df['Detected Date'].astype(str)
# print(df['Detected Date'])
print(df)
#print(df['Detected By'])
#df['BatchDate'] = df['BatchDate'].astype(str)
# df['BatchDate'] = df['BatchDate'].replace("/", "-")
# df['Detected Date'] = df['Detected Date'].replace("/", "-")
#print(df.dtypes)
for index, row in df.iterrows():
    pass
    #print(str(row['BatchDate']))
    #print(str(row['Detected Date']))



    #print(pd.isna(row['Deed Category']))

    #print(type(row['Detected Date']))
# df['Detected Date'].apply(lambda x: x.split)
# for index, row in df.iterrows():
#     print(row["Detected Date"])

#df['Detected Date']= pd.to_datetime(pd.to_numeric(df['Detected Date'],errors='coerce'),errors='coerce',origin='1899-12-30',unit='D')
"""