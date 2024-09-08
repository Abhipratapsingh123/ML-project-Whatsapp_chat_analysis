from urlextract import URLExtract
extractor = URLExtract()
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



