import re
import pandas as pd
import numpy as np
def preprocess(data):
    pattern= pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages, 'message_date':dates})
#convert message_date type
#df['message_date']=pd.to_datetime(df['message_date'], format='%d%m%y, %H:%M - ')#errors='coerce')

#df.rename(columns={'message_date': 'date'},inplace=True)
    df.head()
    df['message_date'] = df['message_date'].astype(str)##str mae connvert kia because message_dtae mae kuch values nan hai aur kuch datetime aur str string par lagta sirf islia str mae convert kia 
    df['message_date'] = (
        df['message_date']
        .str.replace(',', '', regex=False)
        .str.replace(' -', '', regex=False)
        .str.strip()
    )
    df.rename(columns={'user_message':'message','message_date':'date'},inplace=True)
    df.rename(columns={'message':'user_message','message_date':'date'},inplace=True)
    users=[]
    messages=[]
    for message in df['user_message']:
        entry = re.split(r'([^:]+):\s', message)
        if entry[1:]:#user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)
    a=df['date']
    y=[]
    for i in a:
        y.append(i[6:8])
    df['year']=y
    m=[]
    for i in a:
        if i[3:5]== '01':
            m.append('January')
        elif i[3:5]== '02':
            m.append('February')
        elif i[3:5]== '03':
            m.append('March')
        elif i[3:5]== '04':
            m.append('April')
        elif i[3:5]== '05':
            m.append('May')
        elif i[3:5]== '06':
            m.append('June')
        elif i[3:5]== '07':
            m.append('July')
        elif i[3:5]== '08':
            m.append('August')
        elif i[3:5]== '09':
            m.append('September')
        elif i[3:5]== '10':
            m.append('October')
        elif i[3:5]== '11':
            m.append('November')
        elif i[3:5]== '12':
            m.append('December')    
    df['month']=m
    d=[]
    for i in a:
        d.append(i[0:2])
    df['day']=d

    h=[]
    for i in a:
        h.append(i[9:11])
    df['hour']=h

    s=[]
    for i in a:
        s.append(i[12:14])
    df['minute']=s

    mn=[]
    for i in df['date']:
        mn.append(i[3:5])
    df['month_num']=mn

    odl=[]
    for i in df['date']:
        odl.append(i[0:8])
    df['only_date']=odl

    df['date']=pd.to_datetime(df['date'],dayfirst=True)
    df['day_name']=df['date'].dt.day_name()

    period = []

    for hour in df[['day_name','hour']]['hour'].astype(int):
        if hour == 23:
            period.append(str(hour) + '-' + str(0))
        elif hour == 0:
            period.append(str(0) + '-' + str(hour+1))
        else:
            period.append(str(hour) + '-' + str(hour+1))
    df['period']=period

    
    return df
     
