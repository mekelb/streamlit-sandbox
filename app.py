from pymongo import MongoClient
import datetime

# MongoDB Atlas connection (replace with your own connection string)
# Access the Mongo URI from Streamlit secrets
MONGO_URI = st.secrets["mongo"]["MONGO_URI"]
client = MongoClient(MONGO_URI)

# Access the database
db = client['streamlitdb']  # Replace with your database name

# Check and create collections if they don't exist
bets_collection = db.get_collection('bets')  # Access or create the 'bets' collection
leaderboard_collection = db.get_collection('leaderboard')  # Access or create the 'leaderboard' collection

# Initialize session state variables
import streamlit as st
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
        # Save to MongoDB
        bet_entry = {
            "player_name": player_name,
            "bet": bet,
            "wager": wager,
            "timestamp": datetime.datetime.now()
        }
        bets_collection.insert_one(bet_entry)  # Insert bet into MongoDB
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
        
        # Update leaderboard in MongoDB
        player = leaderboard_collection.find_one({"player_name": bet['player_name']})
        if player:
            new_points = player['points'] + change
            leaderboard_collection.update_one(
                {"player_name": bet['player_name']}, 
                {"$set": {"points": new_points}}
            )
        else:
            leaderboard_collection.insert_one({
                "player_name": bet['player_name'],
                "points": change
            })
        
        st.write(f"{bet['player_name']} {result}! ({actual}).")

# Display Leaderboard
st.subheader("🏆 Leaderboard 🏆")
leaderboard_data = leaderboard_collection.find().sort("points", -1)
leaderboard_df = pd.DataFrame(list(leaderboard_data))
st.dataframe(leaderboard_df)
