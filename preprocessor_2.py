import re
import pandas as pd

def preprocess(data):
    # Adjusted pattern to match your chat format correctly
    pattern = r'\[\d{2}/\d{2}/\d{2,4},\s\d{2}:\d{2}:\d{2}\]\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Convert extracted dates to datetime format
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = df['date'].str.strip("[]")  # Remove square brackets
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S',errors='coerce')

    # Separate users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\s\+]+?):\s', message, maxsplit=1)
        if len(entry) > 1:
            users.append(entry[1].strip())
            messages.append(entry[2].strip())
        else:
            users.append('group_notification')
            messages.append(entry[0].strip())

    df['users'] = users
    df['messages'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Remove system messages like "Messages and calls are end-to-end encrypted."
    df = df[~df['messages'].str.contains('Messages and calls are end-to-end encrypted', na=False)]
    
    # Identifying media messages
    df['media_message'] = df['messages'].apply(lambda x: True if "<Media omitted>" in x else False)

    # Extracting more date components
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
