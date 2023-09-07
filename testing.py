import pandas as pd
df = pd.read_excel("Example_Testing.xlsx")
LIST = [(0, 'ETQT-25228'), (1, 'ETQT-25229'), (2, 'No Key')]
JUST_KEY_LIST = [l[1] for l in LIST]

df.insert(29, "Jira Keys4",JUST_KEY_LIST)
df.to_excel("Example_Testing.xlsx", index=False)

print(df)