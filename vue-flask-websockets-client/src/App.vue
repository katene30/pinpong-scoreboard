<template>
  <div id="app">
    <h1>Score: {{ score }}</h1>
    <button @click="incrementScore">Increment</button>
    <button @click="decrementScore">Decrement</button>
  </div>
</template>

<script>
import io from 'socket.io-client';

export default {
  data() {
    return {
      socket: null,
      score: 0
    };
  },
  created() {
    // Connect to Flask WebSocket server
    this.socket = io('http://localhost:5000');
    
    // Listen for score updates from Flask server
    this.socket.on('score_update', (data) => {
      this.score = data.score;
    });
  },
  methods: {
    incrementScore() {
      this.socket.emit('increment_score');
    },
    decrementScore() {
      this.socket.emit('decrement_score');
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
