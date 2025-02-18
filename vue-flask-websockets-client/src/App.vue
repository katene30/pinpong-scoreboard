<template>
  <div id="app" class="bg-gray-900 text-white flex flex-col items-center justify-center h-screen w-screen">
    <h1 class="text-6xl font-bold mb-6">🏓 Ping Pong Scoreboard</h1>
        <!-- Pick Who Starts Serving -->
        <div class="mb-4 flex gap-4 text-2xl">
      <span>Who serves first?</span>
      <select v-model="selectedServer" @change="setInitialServer" class="px-4 py-2 bg-gray-700 text-white rounded-lg">
        <option :value="1">Player 1</option>
        <option :value="2">Player 2</option>
      </select>
    </div>

    <div class="flex justify-center w-full h-3/4 items-center gap-20">
      <!-- Player 1 -->
      <div class="text-center flex flex-col items-center w-1/3 p-6 rounded-xl bg-gray-800" :class="{ 'border-8 border-yellow-500 shadow-xl': server === 1  }">
        <h2 class="text-4xl font-semibold">Player 1</h2>
        <p class="text-[12rem] font-bold my-6">{{ scorePlayer1 }}</p>
        <div class="flex gap-4">
          <button @click="incrementScorePlayer1"
                  class="px-10 py-6 bg-green-500 hover:bg-green-600 rounded-lg text-4xl font-semibold">+1</button>
          <button @click="decrementScorePlayer1"
                  class="px-10 py-6 bg-red-500 hover:bg-red-600 rounded-lg text-4xl font-semibold">-1</button>
        </div>
      </div>

      <!-- Player 2 -->
      <div class="text-center flex flex-col items-center w-1/3 p-6 rounded-xl bg-gray-800" :class="{ 'border-8 border-yellow-500 shadow-xl': server === 2  }">
        <h2 class="text-4xl font-semibold">Player 2</h2>
        <p class="text-[12rem] font-bold my-6">{{ scorePlayer2 }}</p>
        <div class="flex gap-4">
          <button @click="incrementScorePlayer2"
                  class="px-10 py-6 bg-green-500 hover:bg-green-600 rounded-lg text-4xl font-semibold">+1</button>
          <button @click="decrementScorePlayer2"
                  class="px-10 py-6 bg-red-500 hover:bg-red-600 rounded-lg text-4xl font-semibold">-1</button>
        </div>
      </div>
    </div>

    <!-- Clear Scores Button -->
    <div class="mt-8 text-4xl font-semibold">
      <button @click="clearScore"
              class="px-12 py-6 bg-yellow-500 hover:bg-yellow-600 text-4xl font-bold rounded-lg">Clear Scores</button>
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
      scorePlayer2: 0,
      server: 1,  // Track the current server
      selectedServer: 1,  // Default selected server


    };
  },
  created() {
    // Connect to Flask WebSocket server
    this.socket = io('http://10.0.0.14:5000');
    
    // Listen for score updates from Flask server
    this.socket.on('score_update', (data) => {
      this.scorePlayer1 = data.player_1;
      this.scorePlayer2 = data.player_2;
      this.server = data.server;
      this.selectedServer = data.server;  // Keep dropdown in sync!


    });
  },
  methods: {
    setInitialServer() {
      this.socket.emit('set_server', { player: this.selectedServer });
    },
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

<style scoped>
#app {
  font-family: 'Arial', sans-serif;
}

button {
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}
</style>
