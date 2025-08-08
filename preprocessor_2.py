import re
import pandas as pd

def preprocess(data):
    # replacing blank character with a space
    data = data.replace('\u202f',' ')

    # Extracting messages
    pattern = r'\d{1,2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern,data)[1:]
    
    # extracting dates
    pattern2 = r'\d{1,2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m'
    dates = re.findall(pattern2,data)

    # converting to dataframe
    df = pd.DataFrame({'message':messages,'dates':dates})
    df['dates'] = pd.to_datetime(df['dates'],format='%d/%m/%y, %I:%M %p')

    # separating user-names and messages
    users =[]
    messages=[]
    for message in df['message']:
        entry= re.split(r'^(.*?):\s(.*)',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
            
    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['message'],inplace=True)

    # extrating year, month, day, hour and minute from date
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['month_num'] = df['dates'].dt.month
    df['day_name'] = df['dates'].dt.day_name
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute

    return df
