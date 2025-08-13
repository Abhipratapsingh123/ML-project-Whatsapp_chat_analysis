import re
import pandas as pd

def preprocess(data):
    # Replace non-breaking space with normal space
    data = data.replace('\u202f', ' ')

    # Pattern for 12-hour format WhatsApp export (example: 12/05/23, 9:15 pm - )
    pattern = r'\d{1,2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    messages = re.split(pattern, data)[1:]  # Skip the first split (empty)
    
    # Extract dates in 12-hour format
    pattern2 = r'\d{1,2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m'
    dates = re.findall(pattern2, data)

    # Create DataFrame
    df = pd.DataFrame({'message': messages, 'date': dates})
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%y, %I:%M %p')

    # Separate usernames and messages
    users = []
    msgs = []
    for message in df['message']:
        # Split only on the first occurrence of ": "
        entry = re.split(r'^([^:]+):\s', message, maxsplit=1)
        if len(entry) >= 3:
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('group_notification')
            msgs.append(entry[0])

    df['users'] = users
    df['messages'] = msgs

    # Drop original combined column
    df.drop(columns=['message'], inplace=True)

    # Ensure messages are strings (prevents .str errors later)
    df['messages'] = df['messages'].astype(str)

    # Extract datetime components
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day_name'] = df['date'].dt.day_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
