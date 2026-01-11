import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp App Analyzer")

uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")
    
    df=preprocessor.preprocess(data)

    #st.dataframe(df)#to display dataframe on streamlit aplication 

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")


    selected_users= st.sidebar.selectbox("Show Analysis with respect ",user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages,words,number_of_media_messages,number_of_links= helper.fetch_stats(selected_users,df)

        st.title('Top Statistics')
        col1,col2,col3,col4= st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        
        with col3:
            st.header("No.of Media messages")
            st.title(number_of_media_messages)


        with col4:
            st.header("No.of Links")
            st.title(number_of_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_users,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['y-m'],timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline_df=helper.daily_timeline(selected_users,df)
        fig,ax=plt.subplots()
        plt.figure(figsize=(25,15))
        ax.plot(daily_timeline_df['only_date'],daily_timeline_df['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #weekday timeline
        st.title('Activity Map')
        weekday_df=helper.weekday_timeline(selected_users,df)

        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            fig,ax=plt.subplots()
            ax.bar(weekday_df['day_name'],weekday_df['message'])
            st.pyplot(fig)

        with col2:
            month_bar=helper.monthly_bar_graph(selected_users,df)
            st.header("Monthly Timeline Bar Graph")
            #timeline=helper.monthly_timeline(selected_users,df)
            fig,ax=plt.subplots()
            ax.bar(month_bar.index,month_bar.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        


        #weekday_df=helper.weekday_timeline(selected_users,df)


        # finding the busiest users in the group(Group level)
        if selected_users=='Overall':
            st.title('Most Busy Users')
            x,af=helper.most_busy_users(df)
            fig,ax=plt.subplots()
            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(af)

        # #WordCloud
        # st.title('Word Cloud')
        # df_wc=helper.create_wordcloud(selected_users,df)
        # fig,ax=plt.subplots()
        # ax.imshow(df_wc)
        # st.pyplot(fig)

        # most common words
        st.title("Most Common Words")
        most_common_df=helper.most_common_words(selected_users,df)
        fig,ax=plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')

        st.pyplot(fig) 

        #Emoji
        emoji_df=helper.emoji_helper(selected_users,df)
        st.title('Emoji Analysis')

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1],labels=emoji_df[1])
            st.pyplot(fig)

        
        #Heatmap
        st.title("Activity Heatmap")
        activity=helper.activity_heatmap(selected_users,df)
        plt.figure(figsize=(20,6))
        fig,ax=plt.subplots()
        ax=sns.heatmap(activity)
        st.pyplot(fig)





