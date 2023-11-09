import streamlit as st
import plotly.express as px
import pandas as pd
from measures import *
#import seaborn as sns
from scipy.stats import ttest_ind

selected_measurement = st.selectbox("Choose a measurement", measurements)
data = pd.read_csv("Reference_Prototype.csv")
phase_id = data['Phase'].unique()
unit_id = data['Unit'].unique()

selected_phase = st.multiselect('Select Phase(s)', options = phase_id, default=phase_id)

average = data[selected_measurement].mean()
stdev = data[selected_measurement].std()

Reference = data[data["Unit"] == "Reference"]
Prototype = data[data["Unit"] == "Prototype"]

Reference = Reference[Reference['Phase'].isin(selected_phase)]
Prototype = Prototype[Prototype['Phase'].isin(selected_phase)]
data = data[data['Phase'].isin(selected_phase)]

t_test = ttest_ind(Reference[selected_measurement], Prototype[selected_measurement], equal_var=False)


pvalue = t_test[1]
st.write(pvalue)
if pvalue >= 0.05:
    st.write(f"The P value is {pvalue} and greater than 0.05 and the Prototype and References are likely the same")
else:
    st.write(f"The P value is {pvalue} and less than 0.05 and the Prototype and References are likely different")

fig = px.box(data, x='Unit', y=selected_measurement, title=f"{selected_measurement} Box Plot of the Selected Phase(s)", color='Unit',)
st.plotly_chart(fig, use_container_width=True)
