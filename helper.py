from urlextract import URLExtract
extractor = URLExtract()
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch number of messages
    num_messages = df.shape[0]
    # fetch number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())
    # fetch number of media messages

    num_media_messages = df[df['messages'].str.contains('<Media omitted>\n', regex=False)].shape[0]

    # fetching links

    links =[]
    for messages in df['messages']:
        links.extend(extractor.find_urls(messages))



    return num_messages, len(words),num_media_messages,len(links)



# function to find the busiest user
def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={"users": "name", "count": "percent"})
    return x,df


def create_word_cloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))

    return df_wc



def most_common_words(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Filter out group notifications and "<Media omitted>" messages
    temp = df[df['users'] != 'group_notification']
    temp['messages'] = temp['messages'].str.strip()  # Strip leading/trailing whitespace

    # Remove all messages containing "<Media omitted>" (case insensitive)
    temp = temp[~temp['messages'].str.contains(r'<media omitted>', case=False, regex=True)]

    # Most used words in chats
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()  # Read stopwords as a list

    words_2 = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words_2.append(word)

    # Top 20 most used words

    most_common_df = pd.DataFrame(Counter(words_2).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df



# showing timeline

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['messages'].reset_index()

    time =[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+ str(timeline['year'][i]))
    timeline['time'] = time
    return timeline


# weekly activity
def week_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['day_name'].value_counts()

# monthly activity
def month_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]
    return df['month'].value_counts()










