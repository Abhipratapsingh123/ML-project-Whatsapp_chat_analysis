import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
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

    # st.dataframe(df)

    # fetching unique users
    user_list = df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    # adding button
    if st.sidebar.button("Show analysis"):

        # stats area
        num_messages, words, num_media_messages,links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")

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

        # timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color = 'green')
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)

        # activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1 :
            st.header("Most Busy Month")
            busy_month = helper.month_activity(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index.astype(str), busy_month.values)
            plt.xticks(rotation=90)  # Rotate labels by 90 degrees for vertical
            st.pyplot(fig)

        # with col2:
        #     st.header("Most Busy Day")
        #     busy_day = helper.week_activity(selected_user, df)
        #     fig, ax = plt.subplots()
        #     # Convert index and values to lists
        #     x_values = busy_day.index.astype(str).tolist()
        #     y_values = busy_day.values
        #
        #     ax.bar(x_values, y_values)
        #     plt.xticks(rotation=90)  # Rotate labels by 90 degrees for vertical
        #     st.pyplot(fig)





        # finding the busiest user in the group
        if selected_user == "Overall":
            st.title('Most busy Users')
            x, new_df = helper.most_busy_users(df)
            fig,ax= plt.subplots()
            col1,col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
               st.dataframe(new_df)


        # word cloud
        st.title("Word Cloud")
        df_wc = helper.create_word_cloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        ax.axis("off")
        st.pyplot(fig)

        # most common words
        st.title("Most Used Words in Chats")
        most_common_df = helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels= emoji_df[0].head(), autopct="%.2f")
            st.pyplot(fig)









