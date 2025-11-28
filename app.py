import streamlit as st
import requests
import datetime
import pandas as pd

API_URL = 'https://taxifare.lewagon.ai/predict'

st.markdown('''
#  NYC CAB
''')

with st.form(key='params_form'):
    st.subheader("Paramètres de la course")

    col1, col2 = st.columns(2)
    with col1:
        pickup_date = st.date_input("Date de prise en charge", datetime.date(2013, 7, 6))
    with col2:
        pickup_time = st.time_input("Heure de prise en charge", datetime.time(17, 18))

    pickup_datetime_dt = datetime.datetime.combine(pickup_date, pickup_time)
    pickup_datetime = pickup_datetime_dt.strftime("%Y-%m-%d %H:%M:%S")

    st.subheader("Prise en charge")
    col3, col4 = st.columns(2)
    with col3:
        pickup_latitude = st.number_input("Latitude", value=40.783282, format="%f")
    with col4:
        pickup_longitude = st.number_input("Longitude", value=-73.950655, format="%f")

    st.subheader("Lieu de dépose")
    col5, col6 = st.columns(2)
    with col5:
        dropoff_latitude = st.number_input("Latitude", value=40.769802, format="%f")
    with col6:
        dropoff_longitude = st.number_input("Longitude", value=-73.984365, format="%f")

    passenger_count = st.slider("Nombre de passagers", 1, 8, 1)

    submitted = st.form_submit_button("Calculer le prix 💰")


if submitted:
    params = dict(
        pickup_datetime=pickup_datetime,
        pickup_longitude=pickup_longitude,
        pickup_latitude=pickup_latitude,
        dropoff_longitude=dropoff_longitude,
        dropoff_latitude=dropoff_latitude,
        passenger_count=passenger_count
    )

    with st.spinner('Envoi de la requête à l\'API...'):
        response = requests.get(API_URL, params=params)

    if response.status_code == 200:
        prediction = response.json()
        fare = round(prediction.get('fare', 0), 2)
        st.success(f"✅ Le prix prédit de la course est de **{fare} $**")

        st.subheader("Localisation de la course")
        map_data = pd.DataFrame({
            'lat': [pickup_latitude, dropoff_latitude],
            'lon': [pickup_longitude, dropoff_longitude]
        })
        st.map(map_data, zoom=11)

    else:
        st.error(f"❌ Erreur lors de l'appel à l'API. Statut: {response.status_code}. Vérifiez l'URL: {API_URL}")
