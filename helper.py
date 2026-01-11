from urlextract import URLExtract #URLExtract is a class
extract=URLExtract() #extract is a object
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


def fetch_stats(selected_users,df):
    
    if selected_users!="Overall":
        df=df[df['user']==selected_users]
    num_messages=df.shape[0]

    words=[]
    for message in df['message']:
        words.extend(message.split())


    #fetch number of media
    number_of_media_messages=df[df['message']== '<Media omitted>\n'].shape[0]
    

    #fetch number of links
    links=[]
    for message in df['message']:
        links.extend(extract.find_urls(message))


    return num_messages,len(words),number_of_media_messages,len(links)


def most_busy_users(df):
    x=df['user'].value_counts().head()
    af=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'user':'name','count':'percent'})      
    return x,af


# def create_wordcloud(selected_users,df):
#     if selected_users != 'Overall':
#         df=df[df['user'] == selected_users]

#     wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
#     df_wc=wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc

def most_common_words(selected_users,df):
    f=open("stop_hinglish.txt",'r')
    stop_words=f.read().split('\n')

    if selected_users!="Overall":
        df=df[df['user']==selected_users]

    temp=df[df['user']!='group_notification']
    temp=temp[~temp['message'].str.contains('<Media omitted>',na=False)]

    wordss=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                wordss.append(word)
    from collections import Counter
    Counter(wordss)
    most_common_df=pd.DataFrame(Counter(wordss).most_common(20))
    return most_common_df

def emoji_helper(selected_users, df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]

    emojis = []
    for message in df['message']:
        emojis.extend(c for c in message if emoji.is_emoji(c))

    from collections import Counter
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    return emoji_df

def monthly_timeline(selected_users,df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]

    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    timeline['y-m']=timeline['month']+'-'+timeline['year']
    return timeline

def daily_timeline(selected_users,df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]
    daily_timeline_df=df.groupby(['only_date']).count()['message'].reset_index()
    return daily_timeline_df

def weekday_timeline(selected_users,df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]
    weekday_df=df.groupby('day_name').count()['message'].reset_index()
    return weekday_df

def monthly_bar_graph(selected_users,df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]
    month_bar=df['month'].value_counts()
    return month_bar

def activity_heatmap(selected_users,df):
    if selected_users != "Overall":
        df = df[df['user'] == selected_users]
    
    activity=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return activity