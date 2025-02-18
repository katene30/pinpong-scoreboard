<template>
  <div id="app">
    <div class="scoreboard">
      <!-- Player 1 Section -->
      <div class="player-section left">
        <h1>Player 1</h1>
        <h2>{{ scorePlayer1 }}</h2>
        <div class="score-controls">
          <button @click="incrementScorePlayer1">+</button>
          <button @click="decrementScorePlayer1">-</button>
        </div>
      </div>

      <!-- Player 2 Section -->
      <div class="player-section right">
        <h1>Player 2</h1>
        <h2>{{ scorePlayer2 }}</h2>
        <div class="score-controls">
          <button @click="incrementScorePlayer2">+</button>
          <button @click="decrementScorePlayer2">-</button>
        </div>
      </div>
    </div>

    <!-- Clear Scores Button -->
    <div class="clear-button-container">
      <button class="clear-button" @click="clearScore">Clear Scores</button>
    </div>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      socket: null,
      scorePlayer1: 0,
      scorePlayer2: 0
    };
  },
  created() {
    // Connect to Flask WebSocket server
    this.socket = io('http://localhost:5000');
    
    // Listen for score updates from Flask server
    this.socket.on('score_update', (data) => {
      this.scorePlayer1 = data.player_1;
      this.scorePlayer2 = data.player_2;
    });
  },
  methods: {
    incrementScorePlayer1() {
      this.socket.emit('increment_score', { player: 1 });
    },
    decrementScorePlayer1() {
      this.socket.emit('decrement_score', { player: 1 });
    },
    incrementScorePlayer2() {
      this.socket.emit('increment_score', { player: 2 });
    },
    decrementScorePlayer2() {
      this.socket.emit('decrement_score', { player: 2 });
    },
    clearScore() {
      this.socket.emit('clear_score');
    }
  }
};
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

.scoreboard {
  display: flex;
  justify-content: space-between;
  width: 100%;
  max-width: 1200px; /* Optional, ensures max width on large screens */
  margin-bottom: 20px;
}

.player-section {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 48%;
  min-width: 250px; /* Ensures the sections don't get too narrow */
  margin: 0 10px; /* Adds space between the player cards */
  display: flex;
  flex-direction: column;
  justify-content: center; /* Vertically centers the content */
}

.left {
  text-align: left;
}

.right {
  text-align: right;
}

.player-section h1 {
  font-size: 24px;
  margin-bottom: 10px;
}

.player-section h2 {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin: 10px 0;
}

.score-controls {
  display: flex;
  justify-content: center;
  gap: 10px;
}

button {
  padding: 10px 20px;
  font-size: 18px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.clear-button-container {
  margin-top: 20px;
}

.clear-button {
  padding: 12px 30px;
  font-size: 20px;
  background-color: #dc3545;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.clear-button:hover {
  background-color: #c82333;
}
</style>
