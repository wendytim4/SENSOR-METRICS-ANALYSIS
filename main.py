import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

@st.cache(suppress_st_warning=True)
def get_fvalue(val):
    feature_dict = {"No":1,"Yes":2}
    for key,value in feature_dict.items():
        if val == key:
            return value

def get_value(val,my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

app_mode = st.sidebar.selectbox('Select Page',['Sensors','Lineplot of sensors','Status of sensors']) #three pages


st.title("Sensor Metrics Analysis\n")
st.markdown("We will analyse the decibel level of noise sensors recorded in a particular period\n")

data_path = 'data/sensor_metrics.csv'
df = pd.read_csv(data_path)
newdb_level=df[df.field == "db_level"]


def __lineplot(deviceid):
    new_dfdevice_id = newdb_level[newdb_level['device_id'] == deviceid]
    new_dfdevice_id['date']=pd.to_datetime(new_dfdevice_id['date'])
    return new_dfdevice_id

sB1007=__lineplot('SB1007')
sB1005=__lineplot('SB1005')
sB1001=__lineplot('SB1001')
sB1012=__lineplot('SB1012')
sB1006=__lineplot('SB1006')
sB1002=__lineplot('SB1002')
sB1013=__lineplot('SB1013')
sB1008=__lineplot('SB1008')



if app_mode=='Sensors':
    st.header('General Information about sensors ')  
    st.markdown('Dataset: ')
    st.write(df.head())
    sensors=newdb_level['device_id'].value_counts()
    st.markdown('Number of records each sensor contains')
    st.write(sensors)
    st.markdown('Barplot of each sensor versus its number of records')
    fig,ax = plt.subplots()
    st.bar_chart(sensors)

elif app_mode == 'Lineplot of sensors':
    st.header('Lineplot of each sensors') 

    st.markdown('Lineplot of SB1007')
    First = pd.DataFrame({'date': list(sB1007['date']),  'value':list(sB1007['value'])})
    First = First.set_index('date')
    st.line_chart(First)

    st.markdown('Lineplot of SB1005')
    Second= pd.DataFrame({'date': list(sB1005['date']),  'value':list(sB1005['value'])})
    Second = Second.set_index('date')
    st.line_chart(Second)

    st.markdown('Lineplot of sB1001')
    Third = pd.DataFrame({'date': list(sB1001['date']),  'value':list(sB1001['value'])})
    Third = Third.set_index('date')
    st.line_chart(Third)

    st.markdown('Lineplot of sB1012')
    Fourth = pd.DataFrame({'date': list(sB1012['date']),  'value':list(sB1012['value'])})
    Fourth = Fourth.set_index('date')
    st.line_chart(Fourth)

    st.markdown('Lineplot of sB1006')
    Fifth = pd.DataFrame({'date': list(sB1006['date']),  'value':list(sB1006['value'])})
    Fifth = Fifth.set_index('date')
    st.line_chart(Fifth)

    st.markdown('Lineplot of SB1002')
    Sixth = pd.DataFrame({'date': list(sB1002['date']),  'value':list(sB1002['value'])})
    Sixth  =  Sixth .set_index('date')
    st.line_chart( Sixth )

    st.markdown('Lineplot of SB1013')
    Seventh = pd.DataFrame({'date': list(sB1013['date']),  'value':list(sB1013['value'])})
    Seventh= Seventh.set_index('date')
    st.line_chart(Seventh)

    st.markdown('Lineplot of SB1008')
    Eigtht = pd.DataFrame({'date': list(sB1008['date']),  'value':list(sB1008['value'])})
    Eigtht  =Eigtht .set_index('date')
    st.line_chart(Eigtht )

elif app_mode == 'Status of sensors':

    st.subheader('Percentage of exceedances for day-time and night-time for each sensor.')

    def day_night_records(id):
        id  =id.set_index('date')
        daytime = id.between_time('6:00','22:00')
        nighttime = id.between_time('22:00','6:00')
        return daytime, nighttime


    def exceedances(new_df, limit):
        return len(new_df[new_df['value'] >= limit])

    def records(sensor_name, data, day_limit, night_limit):
        day, night = day_night_records(data)
        day_exc = exceedances(day, day_limit)  
        day_percent = 0 if len(day) == 0 else (day_exc/len(day)) * 100
        night_exc = exceedances(night, night_limit)
        night_percent = 0 if len(night) == 0 else (night_exc/len(night)) * 100
        return [sensor_name, len(data), len(day), day_exc, day_percent, len(night), night_exc, night_percent]

    sensors = [('SB1005', sB1005, 60, 50), ('SB1006', sB1006, 60, 50), ('SB1007', sB1007, 55, 45),('SB1002', sB1002, 55, 45) ,
    ('SB1001', sB1001, 55, 45),('SB1008', sB1008, 55, 45), ('SB1012', sB1012, 55, 45), ('SB1013', sB1013, 60, 50)]
    newdf = [records(name, sensor_data, dl, nl) for name, sensor_data, dl, nl in sensors]
    sensor_df = pd.DataFrame.from_records(newdf, columns=["Sensor", "Total records", "Total Daytime Records", "Daytime Exceedances", "Daytime Exceedance Percentage", "Total Night Records", "Nighttime Exceedances", "Nighttime Exceedance Percentage"])
    sensor_df = sensor_df.set_index('Sensor')
    st.write(sensor_df)

