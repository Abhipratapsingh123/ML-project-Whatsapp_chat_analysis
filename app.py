import streamlit as st
import preprocessor
import helper
import warnings
warnings.filterwarnings(action='ignore')

st.sidebar.title("Whatspp Chat Analyzer")

# File uploader widget
uploaded_file = st.sidebar.file_uploader("Choose a file")

# Check if a file has been uploaded
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df= preprocessor.preprocess(data)

    st.dataframe(df)

    # fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # adding button
    if st.sidebar.button("Show analysis"):
        num_messages, words, num_media_messages,links = helper.fetch_stats(selected_user,df)


        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Links Shared")
            st.title(links)







