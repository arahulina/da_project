import streamlit as st
import pandas as pd


st.title("earthquakes")
st.write(
    "Let's start!"
)

# Завантаження даних з файлу CSV 
df = pd.read_csv('data/earthquake_1995-2023.csv')

# Відображення заголовку
st.title("Моя карта на основі даних")

# Відображення DataFrame
#st.write("Набір даних:")
#st.write(df)

# Відображення карти на основі даних про широту і довготу
st.map(df[['latitude', 'longitude']])