# vue-flask-websockets
A real-time scorekeeping web app using Vue.js, Flask, and WebSockets for multiplayer game tracking.

## Project Setup
### Frontend Setup (Vue.js)
Install dependencies:

`npm install`

Run in development mode:

`npm run serve`

Build for production:

`npm run build`

### Backend Setup (Flask Server)
Install dependencies:

`pip3 install -r requirements.txt`

Run the Flask WebSocket server:

`python app.py`

## Features
- Change player names 📝
- Switch names (used for switching sides) 🔄
- Set the score manually 🔢
- Adjust the service interval (default: every 5 points, changes based on input and deuce) 🎾
- Select who serves first 🏓
- Real-time WebSocket updates → Others can connect and see live scores 🌍
- Clear Scores & Clear Names buttons (for quick resets) 🧹
## Planned Improvements
### MVP (Minimum Viable Product)
- ✅ Basic score tracking

- ✅ Real-time updates with WebSockets

- ✅ Service interval adjustments

- ✅ Name and side switching

### Upcoming Enhancements
- 🔧 Settings Modal → Move score/service interval settings to a dedicated settings modal
- 🗣️ Audio Commentary (Stretch Goal) → If there’s a big points difference, use AI voice (e.g., ElevenLabs) to throw trash talk/insults at the losing player 😈