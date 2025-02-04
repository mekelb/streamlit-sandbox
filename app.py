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
if 'bandar_confirmed' not in st.session_state:
    st.session_state['bandar_confirmed'] = False

# Bandar decides availability at 15:50
current_time = datetime.datetime.now().time()
decision_time = datetime.time(15, 50)  # Changed to 3:50 PM

# Tailwind styles for custom layout and animation
st.markdown("""
    <style>
        body {background-color: #fef9c3; font-family: 'Comic Sans MS', cursive;}
        .stButton>button {border-radius: 12px; background-color: #f87171; color: white; font-size: 20px; padding: 10px;}
        .stDataFrame {border: 3px dashed #facc15;}
        
        /* Left and right animation */
        .left-animation, .right-animation {
            position: fixed;
            top: 10%;
            width: 400px;  /* Increased width */
            z-index: 999;
        }
        
        .left-animation {
            left: 0;
        }
        
        .right-animation {
            right: 0;
        }
    </style>
""", unsafe_allow_html=True)

# Add the images for the animations with larger size
st.markdown("""
    <div class="left-animation">
        <img src="https://media.istockphoto.com/id/1221449346/id/foto/gadis-berpakaian-merah-menampilkan-chip-berpose-dengan-latar-belakang-gelap-roulette-bermain.jpg?s=2048x2048&w=is&k=20&c=K21JFnyFBiGV0cJCaHtm8F6YXe0w853lCrVP09xsJSw=" width="400" />  <!-- Larger width -->
    </div>
    <div class="right-animation">
        <img src="https://media.istockphoto.com/id/1190168811/id/foto/gadis-bermain-poker-di-kasino-memegang-segelas-sampanye-dua-ace-berpose-di-meja-dengan-keripik.jpg?s=2048x2048&w=is&k=20&c=iq0oYaBUiyQU4_wgBiPtxRMaTHeKdDDL13MlEElVv5g=" width="400" />  <!-- Larger width -->
    </div>
""", unsafe_allow_html=True)

st.title("🎲 Cuno Masuk Hari Ini? Bet Now! 🎲")

st.write("Place your bet before 15:50! Do you think Cuno masuk hari ini? Earn points and climb the leaderboard!")

player_name = st.text_input("Masukin nama lu dulu nih:")

bet = st.radio("Bet lu:", ["Eh tumbenn masuuk", "Gaa masuk bre", "Masuk jam 10", "Jam 1 naruh tas","cerita soal macet" , "ngeeluh soal kerjaan pagi2","ngerjain reza" ])
wager = st.number_input("Mau bet berapa poin?", min_value=1, max_value=st.session_state['points'], step=1)

if st.button("Gas Bet!"):
    if player_name:
        st.session_state['bets'].append({'Player': player_name, 'Bet': bet, 'Wager': wager})
        st.success(f"{player_name}, bet lu udah masuk bro!")
    else:
        st.error("Masukin nama lu dulu bre!")

# Bandar Panel to Set the Result
st.subheader("🛠️ Bandar Panel 🛠️")
bandar_code = st.text_input("Masukin kode bandar (biar ga sembarang orang edit)", type="password")
if bandar_code == "bandar123":  # Change this to your preferred bandar code
    result_choice = st.radio("Set hasil Cuno:", ["Eh tumbenn masuuk", "Gaa masuk bre", "Masuk jam 10", "Jam 1 naruh tas"])
    if st.button("Konfirmasi Hasil"):
        st.session_state['is_available'] = result_choice
        st.session_state['bandar_confirmed'] = True
        st.success("Hasil berhasil diset! Sekarang semua bisa lihat hasilnya!")

# Show results after 15:50
if current_time >= decision_time and st.session_state['bandar_confirmed']:
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
