import streamlit as st
import random
import datetime
import pandas as pd
import os

# Set up session state
if 'points' not in st.session_state:
    st.session_state['points'] = 100
if 'leaderboard' not in st.session_state:
    st.session_state['leaderboard'] = pd.DataFrame(columns=['Player', 'Points'])
if 'is_available' not in st.session_state:
    st.session_state['is_available'] = None
if 'bets' not in st.session_state:
    st.session_state['bets'] = []
if 'admin_confirmed' not in st.session_state:
    st.session_state['admin_confirmed'] = False

# Admin decides availability at 11:00 AM
current_time = datetime.datetime.now().time()
decision_time = datetime.time(11, 0)

# Tailwind styles
st.markdown("""
    <style>
        body {background-color: #fef9c3; font-family: 'Comic Sans MS', cursive;}
        .stButton>button {border-radius: 12px; background-color: #f87171; color: white; font-size: 20px; padding: 10px;}
        .stDataFrame {border: 3px dashed #facc15;}
    </style>
""", unsafe_allow_html=True)

st.title("🎲 Cuno Masuk Hari Ini? Bet Now! 🎲")

st.write("Place your bet before 11:00 AM! Do you think Cuno masuk hari ini? Earn points and climb the leaderboard!")

player_name = st.text_input("Masukin nama lu dulu nih:")

bet = st.radio("Bet lu:", ["Eh tumbenn masuuk", "Gaa masuk bre", "Masuk jam 10", "Jam 1 naruh tas","cerita soal macet" , "ngeeluh soal kerjaan pagi2","ngerjain reza" ])
wager = st.number_input("Mau bet berapa poin?", min_value=1, max_value=st.session_state['points'], step=1)

if st.button("Gas Bet!"):
    if player_name:
        st.session_state['bets'].append({'Player': player_name, 'Bet': bet, 'Wager': wager})
        st.success(f"{player_name}, bet lu udah masuk bro!")
    else:
        st.error("Masukin nama lu dulu bre!")

# Admin Panel to Set the Result
st.subheader("🛠️ Admin Panel 🛠️")
admin_code = st.text_input("Masukin kode admin (biar ga sembarang orang edit)", type="password")
if admin_code == "admin123":  # Change this to your preferred admin code
    result_choice = st.radio("Set hasil Cuno:", ["Eh tumbenn masuuk", "Gaa masuk bre", "Masuk jam 10", "Jam 1 naruh tas"])
    if st.button("Konfirmasi Hasil"):
        st.session_state['is_available'] = result_choice
        st.session_state['admin_confirmed'] = True
        st.success("Hasil berhasil diset! Sekarang semua bisa lihat hasilnya!")

# Show results after 11:00 AM
if current_time >= decision_time and st.session_state['admin_confirmed']:
    st.subheader("🔔 Hasil Udah Keluar Bre! 🔔")
    if st.session_state['is_available'] is not None:
        actual = st.session_state['is_available']
        st.write(f"Cuno hari ini: **{actual}**")
        
        # Update points
        updated_leaderboard = []
        for bet in st.session_state['bets']:
            result = "Win" if bet['Bet'] == actual else "Lose"
            change = bet['Wager'] if result == "Win" else -bet['Wager']
            player_entry = next((entry for entry in updated_leaderboard if entry['Player'] == bet['Player']), None)
            if player_entry:
                player_entry['Points'] += change
            else:
                updated_leaderboard.append({'Player': bet['Player'], 'Points': st.session_state['points'] + change})
            st.write(f"{bet['Player']} {result}! ({actual}).")
        
        # Save leaderboard
        st.session_state['leaderboard'] = pd.DataFrame(updated_leaderboard)

st.subheader("🏆 Leaderboard 🏆")
st.dataframe(st.session_state['leaderboard'].sort_values(by='Points', ascending=False))

# Add image at the bottom
st.image("https://d1tgyzt3mf06m9.cloudfront.net/v3-staging/2019/03/858e0fcf66cb938706481b861d586083ff37e50a.jpg")
