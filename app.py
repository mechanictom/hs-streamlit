import streamlit as st
import pandas as pd

df = st.cache_data(pd.read_csv)("Fleet Data.csv")

def clean(val):
    val = str(val)
    val = val.replace("$", "").replace(",", "")
    if val != "nan":
        val = int(val)
    return val

df[["Current", "Future", "Historic", "Total", "Orders"]] = df[[
    "Current", "Future", "Historic", "Total", "Orders"]].fillna(0)
df["Unit Cost"] = df["Unit Cost"].apply(clean)
df["Total Cost (Current)"] = df["Total Cost (Current)"].apply(clean)
df.drop(columns = "Airline", inplace = True)
df.rename(columns = {"Parent Airline" : "Airline"}, inplace = True)

df['Unit Cost'] = df['Unit Cost'].replace(to_replace={'nan': '0'})
df['Total Cost (Current)'] = df['Total Cost (Current)'].replace(to_replace={'nan': '0'})
df['Unit Cost'] = df['Unit Cost'].astype('int')
df['Total Cost (Current)'] = df['Total Cost (Current)'].astype('int')
df['Average Age'] = df['Average Age'].fillna(value=0)

# for historic fleets average age means nothing - and is nan (converted to 0)

selected = st.sidebar.multiselect('What data you need to show?',
                       ['Current', 'Future', 'Historic'])

airline = 'Aeroflot'
airline = st.sidebar.selectbox('What airline', df['Airline'].unique())

st.dataframe(df.query('Airline == @airline')[['Aircraft Type'] + selected])

st.write('Showing ' + ' '.join(selected) + ' fleet for ' + airline)

st.bar_chart(data=df, x='Aircraft Type', y=selected, color=None, width=0, height=0, use_container_width=True)
