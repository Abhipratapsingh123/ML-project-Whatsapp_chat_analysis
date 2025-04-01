import re
import pandas as pd

def preprocess(data):
    # Adjusted pattern to match your chat format correctly
    pattern = r'\[\d{2}/\d{2}/\d{2,4},\s\d{2}:\d{2}:\d{2}\]\s'
    
    # Splitting messages and dates based on the pattern
    messages = re.split(pattern, data)[1:]  # Skip the first empty part due to initial split
    dates = re.findall(pattern, data)

    # Convert extracted dates to datetime format
    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = df['date'].str.strip("[]")  # Remove square brackets
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %H:%M:%S')

    # Separate users and messages
    users = []
    message_texts = []

    for message in df['user_message']:
        entry = re.split(r'([\w\s\+]+?):\s', message, maxsplit=1)
        if len(entry) > 1:
            users.append(entry[1].strip())
            message_texts.append(entry[2].strip() if len(entry) > 2 else '')  # Handle empty messages
        else:
            users.append('group_notification')
            message_texts.append(entry[0].strip())

    df['users'] = users
    df['messages'] = message_texts
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
