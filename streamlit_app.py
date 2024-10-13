import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
#import matplotlib.pyplot as plt



st.title("Earthquakes")
st.write(
    "Let's start!"
)

# Завантаження даних з файлу CSV 
df = pd.read_csv('data/earthquake_1995-2023.csv')

# Відображення заголовку
st.title("Моя карта на основі даних")
# Відображення DataFrame
st.write("Набір даних:")
st.write(df)

# Відображення карти на основі даних про широту і довготу
st.map(df[['latitude', 'longitude']])

import folium
from streamlit_folium import st_folium

# Завантаження даних
data = pd.read_csv('data/earthquake_1995-2023.csv')

# Заголовок додатка
st.title("Інтерактивна мапа землетрусів (1995-2023)")

# Налаштування початкової мапи
map_center = [0, 0]  # Центр карти для глобального огляду
m = folium.Map(location=map_center, zoom_start=2)

# Нормалізація магнітуд для маркерів
magnitude_min = data['magnitude'].min()
magnitude_max = data['magnitude'].max()

# Функція для вибору кольору залежно від магнітуди
def get_color(magnitude):
    if magnitude < 5:
        return 'green'
    elif 5 <= magnitude < 6:
        return 'orange'
    elif 6 <= magnitude < 7:
        return 'red'
    else:
        return 'darkred'

# Додавання маркерів на мапу
for _, row in data.iterrows():
    location = [row['latitude'], row['longitude']]
    magnitude = row['magnitude']
    
    # Розмір маркера залежно від магнітуди
    radius = (magnitude - magnitude_min) / (magnitude_max - magnitude_min) * 10 + 3

    # Додавання маркера з кольором та інформацією
    folium.CircleMarker(
        location=location,
        radius=radius,
        color=get_color(magnitude),
        fill=True,
        fill_color=get_color(magnitude),
        fill_opacity=0.7,
        tooltip=f"{row['location']}, Magnitude: {magnitude}"
    ).add_to(m)

# Відображення інтерактивної мапи у Streamlit
st_folium(m, width=700, height=500)

# Легенда для кольорів
st.markdown("""
### Легенда кольорів магнітуд:
- <span style="color:green;">**Зелений**</span>: Магнітуда < 5  
- <span style="color:orange;">**Помаранчевий**</span>: 5 ≤ Магнітуда < 6  
- <span style="color:red;">**Червоний**</span>: 6 ≤ Магнітуда < 7  
- <span style="color:darkred;">**Темно-червоний**</span>: Магнітуда ≥ 7  
""", unsafe_allow_html=True)