import streamlit as st
import plotly.express as px
import pandas as pd
from measures import *
#import seaborn as sns
###from scipy.stats import ttest_ind




    

   

selected_measurement = st.selectbox("Choose a measurement", measurements)
data = pd.read_csv("Reference_Prototype.csv")
phase_id = data['Phase'].unique()
unit_id = data['Unit'].unique()

#selected_phase = st.multiselect('Select tower(s)', options = phase_id, default=phase_id)
#selected_unit = st.multiselect('Select tower(s)', options = unit_id, default=unit_id)


average = data[selected_measurement].mean()
stdev = data[selected_measurement].std()

Reference = data[data["Unit"] == "Reference"]
Prototype = data[data["Unit"] == "Prototype"]
##t_test = ttest_ind(Reference[selected_measurement], Prototype[selected_measurement])

st.write(t_test)

UCL = average + (3*stdev)
LCL = average - (3*stdev)

control = data[(data[selected_measurement] >= LCL) & (data[selected_measurement] <= UCL)]
outside = data[(data[selected_measurement] < LCL) | (data[selected_measurement] > UCL)]

dfg = data.groupby(['Unit'])[selected_measurement].mean()

stdev = data.groupby(['Unit'])[selected_measurement].std()

#bar = dfg.plot(kind='bar', title=f'Prototype vs Reference Mean of {selected_measurement}', ylabel=f'Mean of {selected_measurement}',
         #xlabel='Unit', figsize=(6, 5))


fig = px.box(data, x='Unit', y=selected_measurement, title=f"{selected_measurement} Box Plot", color='Unit',)


#st.plotly_chart(bar, use_container_width=True)


bar = px.bar(dfg, title=f"Mean of {selected_measurement}, Prototype vs Reference")
bar2 = px.bar(stdev, title=f"Standard Deviation of {selected_measurement}, Prototype vs Reference")
st.plotly_chart(bar, use_container_width=True)
st.plotly_chart(bar2, use_container_width=True)

st.plotly_chart(fig, use_container_width=True)
