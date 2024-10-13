import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt



st.title("Earthquakes")
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

# Припустимо, що магнітуда міститься у стовпці 'magnitude'
# Якщо назва інша, змініть 'magnitude' на відповідну
#magnitudes = df[['magnitude']]

# Побудова гістограми з Altair
#hist = alt.Chart(magnitudes).mark_bar().encode(
#    alt.X('magnitude:Q', bin=alt.Bin(maxbins=30), title='Магнітуда'),
#    alt.Y('count()', title='Кількість землетрусів'),
 #   tooltip=['magnitude', 'count()']
#).properties(
#    title='Розподіл магнітуд землетрусів',
#    width=600,
#    height=400
#).interactive()  # Додає можливість масштабування та взаємодії

# Відображення графіка
#hist.show()

#chart_data = df, columns=["magnitude", "b", "c"])

#c = (
#   alt.Chart(chart_data)
#   .mark_circle()
#   .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
#)

#st.altair_chart(c, use_container_width=True)

magnitude_counts = data['magnitude'].round().value_counts().sort_index()

# Побудова кругової діаграми
plt.figure(figsize=(8, 8))
plt.pie(
    magnitude_counts,
    labels=magnitude_counts.index,            # Підписи для кожного сектора
    autopct='%1.1f%%',                        # Відсоткове значення в кожному секторі
    startangle=140,                           # Початковий кут для розвороту діаграми
    colors=plt.cm.viridis_r(magnitude_counts.index / magnitude_counts.max())  # Кольорова палітра
)

plt.title("Distribution of Earthquake Magnitudes (1995-2023)")  # Заголовок
plt.show()  # Показ діаграми