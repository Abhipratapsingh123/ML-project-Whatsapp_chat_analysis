from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

extractor = URLExtract()  # URL Extractor


def fetch_stats(selected_user, df):
    """Fetches statistics like message count, word count, media messages, and links shared."""
    
    if df.empty or 'messages' not in df.columns:
        return 0, 0, 0, 0  # Return zeros if df is empty or missing columns

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Fetch number of messages
    num_messages = df.shape[0]

    # Fetch number of words
    words = sum(len(str(message).split()) for message in df['messages'])

    # Fetch number of media messages
    num_media_messages = df[df['messages'].astype(str).str.contains('<Media omitted>', regex=False)].shape[0]

    # Fetching links
    links = [extractor.find_urls(str(message)) for message in df['messages']]
    num_links = sum(len(link_list) for link_list in links)  # Count total links

    return num_messages, words, num_media_messages, num_links


def most_busy_users(df):
    """Finds the most active users in the chat."""
    
    if df.empty or 'users' not in df.columns:
        return pd.Series(), pd.DataFrame()

    x = df['users'].value_counts().head()
    percentage_df = (df['users'].value_counts(normalize=True) * 100).reset_index()
    percentage_df.columns = ["name", "percent"]
    return x, percentage_df


def create_word_cloud(selected_user, df):
    """Generates a WordCloud from chat messages."""
    
    if df.empty or 'messages' not in df.columns:
        return WordCloud(width=500, height=500, min_font_size=10, background_color='white').generate("")

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    text = ' '.join(df['messages'].astype(str))
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    return wc.generate(text)


def most_common_words(selected_user, df):
    """Finds the most commonly used words in chats, excluding stopwords."""
    
    if df.empty or 'messages' not in df.columns:
        return pd.DataFrame(columns=["Word", "Count"])

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # Remove "<Media omitted>" messages
    df = df[~df['messages'].str.contains(r'<media omitted>', case=False, regex=True)]

    # Load stopwords
    try:
        with open('stop_hinglish.txt', 'r', encoding='utf-8') as f:
            stop_words = set(f.read().splitlines())
    except FileNotFoundError:
        stop_words = {"aap", "hai", "ko", "ka", "ki", "ke", "or", "par", "se", "yeh"}  # Default stopwords

    # Tokenize and filter words
    words = []
    for message in df['messages'].dropna():
        words.extend([word.lower() for word in message.split() if word.lower() not in stop_words])

    # Get top 20 most common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=["Word", "Count"])
    return most_common_df


def emoji_helper(selected_user, df):
    """Extracts and counts emoji usage."""
    
    if df.empty or 'messages' not in df.columns:
        return pd.DataFrame(columns=["Emoji", "Count"])

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = [char for message in df['messages'].astype(str) for char in message if char in emoji.EMOJI_DATA]

    if not emojis:  # If no emojis found, return empty DataFrame
        return pd.DataFrame(columns=["Emoji", "Count"])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=["Emoji", "Count"])
    return emoji_df


def monthly_timeline(selected_user, df):
    """Generates a monthly timeline of message activity."""
    
    if df.empty or 'messages' not in df.columns:
        return pd.DataFrame(columns=["time", "messages"])

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month'])['messages'].count().reset_index()
    timeline['time'] = timeline['month'] + '-' + timeline['year'].astype(str)
    return timeline


def week_activity(selected_user, df):
    """Finds the number of messages sent per day of the week."""
    
    if df.empty or 'day_name' not in df.columns:
        return pd.Series()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts().sort_index()


def month_activity(selected_user, df):
    """Finds the number of messages sent per month."""
    
    if df.empty or 'month' not in df.columns:
        return pd.Series()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts().sort_index()
