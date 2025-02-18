<template>
  <div id="app">
    <h1>Player 1 Score: {{ scorePlayer1 }}</h1>
    <h1>Player 2 Score: {{ scorePlayer2 }}</h1>

    <div>
      <button @click="incrementScorePlayer1">Increment Player 1</button>
      <button @click="decrementScorePlayer1">Decrement Player 1</button>
    </div>

    <div>
      <button @click="incrementScorePlayer2">Increment Player 2</button>
      <button @click="decrementScorePlayer2">Decrement Player 2</button>
    </div>

    <div>
      <button @click="clearScore">Clear Scores</button>
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
  text-align: center;
  margin-top: 100px;
}

button {
  margin: 10px;
  padding: 10px 20px;
  font-size: 16px;
}
</style>
