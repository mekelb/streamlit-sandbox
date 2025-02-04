import streamlit as st
import random
import datetime
import pandas as pd
from pymongo import MongoClient
import requests

# MongoDB Atlas connection (replace with your own connection string)
# Access the Mongo URI from Streamlit secrets
MONGO_API_KEY = st.secrets["mongo"]["API_KEY"]
MONGO_CLUSTER_URL = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-hsbur/endpoint/data/v1"

def insert_data_to_mongo(collection, data):
    url = MONGO_CLUSTER_URL + f"insertOne"
    headers = {
        "Content-Type": "application/json",
        "Api-Key": MONGO_API_KEY
    }
    payload = {
        "dataSource": "Cluster0",  # Replace with your actual data source
        "database": "streamlitdb",  # Replace with your database name
        "collection": "streamlitdb",  # Collection name (bets or leaderboard)
        "document": data
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error inserting data: {response.text}")
        return None

# Function to fetch data from MongoDB collection
def fetch_data_from_mongo(collection):
    url = MONGO_CLUSTER_URL + f"find"
    headers = {
        "Content-Type": "application/json",
        "Api-Key": MONGO_API_KEY
    }
    payload = {
        "dataSource": "Cluster0",  # Replace with your actual data source
        "database": "streamlitdb",  # Replace with your database name
        "collection": collection  # Collection name (bets or leaderboard)
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()['documents']
    else:
        st.error(f"Error fetching data: {response.text}")
        return []

# Initialize session state variables
if 'points' not in st.session_state:
    st.session_state['points'] = 100
if 'bets' not in st.session_state:
    st.session_state['bets'] = []

# Title and description
st.title("🎲 Cuno Masuk Hari Ini? Bet Now! 🎲")
st.write("Place your bet before 15:50! Do you think Cuno masuk hari ini? Earn points and climb the leaderboard!")

# User input for bet and name
player_name = st.text_input("Masukin nama lu dulu nih:")

bet = st.radio("Bet lu:", ["Eh tumbenn masuuk", "Gaa masuk bre", "Masuk jam 10", "Jam 1 naruh tas"])
wager = st.number_input("Mau bet berapa poin?", min_value=1, max_value=st.session_state['points'], step=1)

# Add bet to database and session state
if st.button("Gas Bet!"):
    if player_name:
        bet_entry = {
            "player_name": player_name,
            "bet": bet,
            "wager": wager,
            "timestamp": datetime.datetime.now().isoformat()  # Use ISO format for timestamp
        }
        insert_data_to_mongo("bets", bet_entry)  # Insert bet into MongoDB
        st.session_state['bets'].append(bet_entry)
        st.success(f"{player_name}, bet lu udah masuk bro!")
    else:
        st.error("Masukin nama lu dulu bre!")

# Show results after 15:50 (similar to previous logic)
current_time = datetime.datetime.now().time()
decision_time = datetime.time(15, 50)

if current_time >= decision_time:
    st.subheader("🔔 Hasil Udah Keluar Bre! 🔔")
    actual = "Eh tumbenn masuuk"  # Example result
    st.write(f"Cuno hari ini: **{actual}**")
    
    # Update points based on bets and save leaderboard to MongoDB
    updated_leaderboard = []
    for bet in st.session_state['bets']:
        result = "Win" if bet['bet'] == actual else "Lose"
        change = bet['wager'] if result == "Win" else -bet['wager']
        
        # Check if player exists in leaderboard
        leaderboard_data = fetch_data_from_mongo("leaderboard")
        player = next((entry for entry in leaderboard_data if entry['player_name'] == bet['player_name']), None)
        
        if player:
            new_points = player['points'] + change
            # Update leaderboard in MongoDB
            update_payload = {
                "filter": {"player_name": bet['player_name']},
                "update": {"$set": {"points": new_points}},
                "upsert": True  # Insert if not exists
            }
            url = MONGO_CLUSTER_URL + "updateOne"
            response = requests.post(url, headers={"Api-Key": MONGO_API_KEY}, json=update_payload)
            if response.status_code == 200:
                st.write(f"{bet['player_name']} {result}! ({actual}).")
            else:
                st.error(f"Error updating leaderboard: {response.text}")
        else:
            leaderboard_entry = {
                "player_name": bet['player_name'],
                "points": change
            }
            insert_data_to_mongo("leaderboard", leaderboard_entry)
            st.write(f"{bet['player_name']} {result}! ({actual}).")

# Display Leaderboard
st.subheader("🏆 Leaderboard 🏆")
leaderboard_data = fetch_data_from_mongo("leaderboard")
leaderboard_df = pd.DataFrame(leaderboard_data)
st.dataframe(leaderboard_df)