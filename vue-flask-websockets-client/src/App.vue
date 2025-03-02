<template>
  <div id="app" class="bg-gray-900 text-white flex flex-col items-center justify-center min-h-screen py-10 max-w-full">
    <h1 class="text-6xl font-bold mb-6">🏓 Ping Pong Scoreboard</h1>

    <!-- Cog Icon Button in the Top Right -->
    <div class="absolute top-5 right-5">
      <button @click="openSettings" class="bg-gray-700 hover:bg-gray-600 p-3 rounded-full shadow-md text-white focus:outline-none">
        <PhGear :size="32" color="white" weight="fill" />
      </button>
    </div>

    <!-- Modal for Settings -->
    <div v-if="showSettings" @click.self="closeSettings" class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
      <div class="bg-gray-900 p-8 rounded-lg w-96 shadow-xl relative">
        <!-- Close "X" Button -->
        <button @click="closeSettings" class="absolute top-2 right-2 bg-gray-800 hover:bg-gray-700 text-white rounded-full p-2">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
        
        <h2 class="text-2xl font-semibold text-white mb-4">Game Settings</h2>
        
        <div class="mb-4 flex gap-4 text-xl text-white">
          <span>Winning Score:</span>
          <input type="number" v-model="winningScore" @change="updateWinningScore" min="1" class="px-4 py-2 bg-gray-700 text-white rounded-lg w-20">
        </div>
        
        <div class="mb-4 flex gap-4 text-xl text-white">
          <span>Service Interval:</span>
          <input type="number" v-model="serviceInterval" @change="updateServiceInterval" min="1" class="px-4 py-2 bg-gray-700 text-white rounded-lg w-20">
        </div>
      </div>
    </div>

    
    
    <!-- Pick player names -->
    <div class="mb-4 flex flex-wrap gap-4 text-2xl items-center justify-center w-full px-4">
      <span class="whitespace-nowrap">Player Names:</span>
      <input v-model="player1Name" placeholder="Enter Player 1 Name"
        class="px-4 py-2 bg-gray-700 text-white rounded-lg w-full sm:w-64 md:w-80 text-center">
      <input v-model="player2Name" placeholder="Enter Player 2 Name"
        class="px-4 py-2 bg-gray-700 text-white rounded-lg w-full sm:w-64 md:w-80 text-center">
    </div>

    
    <h2 v-if="gameState === 'deuce'" class="text-6xl font-bold text-white animate-pulse uppercase mb-4">🔥 DEUCE 🔥</h2>
    <h2 v-if="gameState === 'win'" class="text-6xl font-bold text-green-500 animate-pulse uppercase mb-4">{{winnerName}} WINS!</h2>
    
    <div class="flex flex-col md:flex-row justify-center w-full h-auto items-center gap-6">
      <!-- Player 1 -->
      <div class="text-center flex flex-col items-center w-full md:w-1/3 p-6 rounded-xl bg-gray-800 relative" 
            :class="{
              'border-8 border-yellow-500 shadow-xl': server === 1, 
              'border-8 border-green-500 shadow-xl': winnerName === player1Name 
              }">
        <div v-if="server === 1" class="absolute top-4 left-4 flex flex-col items-center space-y-1"
            :class="{
              'server-pulse': isFinalServe(),
            }">
          <PhPingPong :size="64" color="#F59E0B" weight="fill" />
        </div>

        <h2 class="text-4xl font-semibold">{{ player1Name }}</h2>
        <p class="text-[12rem] font-bold my-6">{{ scorePlayer1 }}</p>
        <div class="flex gap-4">
          <button @click="incrementScorePlayer1" class="px-10 py-6 bg-green-500 hover:bg-green-600 rounded-lg text-4xl font-semibold"><PhPlus :size="64" /></button>
          <button @click="decrementScorePlayer1" class="px-10 py-6 bg-red-500 hover:bg-red-600 rounded-lg text-4xl font-semibold"><PhMinus :size="64" /></button>
        </div>
      </div>
      
      <div class="flex-wrap grid grid-rows-2 grid-flow-col gap-4">
        
        <!-- Swap Service Button -->
        <button @click="swapService"
        class="bg-yellow-500 hover:bg-yellow-600 px-6 py-4 rounded-full text-2xl font-bold flex items-center gap-3">
        <!-- Icon in Circle -->
        <div class="bg-white rounded-full p-2 flex items-center justify-center w-16 h-16">
          <PhPingPong :size="64" color="#F59E0B" weight="fill" />
          <PhArrowCounterClockwise :size="38" color="#F59E0B" weight="fill" />
        </div>
        <!-- Button Text -->
            <span class="text-white">Swap Service</span>
        </button>


        <!-- Switch Sides Button -->
        <button @click="switchSides"
                class="bg-blue-500 hover:bg-blue-600 px-6 py-4 rounded-full text-2xl font-bold flex items-center gap-3">
            <!-- Icon in Circle -->
            
            <div class="bg-white rounded-full p-2 flex items-center justify-center w-12 h-12">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-8 h-8 text-blue-500">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7.5 21 3 16.5m0 0L7.5 12M3 16.5h13.5m0-13.5L21 7.5m0 0L16.5 12M21 7.5H7.5" />
              </svg>
            </div>
            
            <!-- Button Text -->
            <span class="text-white">Switch Sides</span>
        </button>
      </div>

      <!-- Player 2 -->
      <div class="text-center flex flex-col items-center w-full md:w-1/3 p-6 rounded-xl bg-gray-800 relative" 
            :class="{
              'border-8 border-yellow-500 shadow-xl': server === 2, 
              'border-8 border-green-500 shadow-xl': winnerName === player2Name 
              }">
        <div v-if="server === 2" class="absolute top-4 left-4 flex flex-col items-center space-y-1"
            :class="{
              'server-pulse': isFinalServe(),
            }">
          <PhPingPong :size="64" color="#F59E0B" weight="fill" />
        </div>

        <h2 class="text-4xl font-semibold">{{ player2Name }}</h2>
        <p class="text-[12rem] font-bold my-6">{{ scorePlayer2 }}</p>
        <div class="flex gap-4">
          <button @click="incrementScorePlayer2"
                  class="px-10 py-6 bg-green-500 hover:bg-green-600 rounded-lg text-4xl font-semibold"><PhPlus :size="64" /></button>
          <button @click="decrementScorePlayer2"
                  class="px-10 py-6 bg-red-500 hover:bg-red-600 rounded-lg text-4xl font-semibold"><PhMinus :size="64" /></button>
        </div>
      </div>
    </div>

    <!-- Clear Scores and Clear Names Buttons (Side by Side) -->
    <div class="mt-8 text-4xl font-semibold flex gap-4 justify-center flex-wrap">
      <button @click="clearScore" class="px-12 py-6 bg-red-500 hover:bg-red-600 text-4xl font-bold rounded-lg w-full sm:w-auto">
        Clear Scores
      </button>

      <button @click="clearNames" class="px-12 py-6 bg-red-500 hover:bg-red-600 text-4xl font-bold rounded-lg w-full sm:w-auto">
        Clear Names
      </button>
    </div>

  </div>
</template>

<script>
import io from 'socket.io-client';
import confetti from "canvas-confetti"; // Import confetti
import { PhPingPong, PhArrowCounterClockwise, PhGear, PhPlus, PhMinus, } from "@phosphor-icons/vue";

export default {
  name: 'App',
  components: {
    PhPingPong,
    PhArrowCounterClockwise,
    PhGear,
    PhPlus,
    PhMinus,
  },
  data() {
    return {
      socket: null,
      player1Name: "Player 1",
      player2Name: "Player 2",
      scorePlayer1: 0,
      scorePlayer2: 0,
      server: 1,
      selectedServer: 1,
      sounds: {
        beep: new Audio('/beep.wav'),  // Player 1 scores
        boop: new Audio('/boop.wav'),  // Player 2 scores
        finalServe: new Audio('/final-serve.mp3'),
        serviceChange: new Audio('/service-change.wav'),
      },
      gameState: "active",
      winningScore: 21,
      gamePoint: this.winningScore - 1,
      serviceInterval: 5,
      showSettings: false,
    };
  },
  created() {
    // Connect to Flask WebSocket server
    this.socket = io('http://10.0.0.14:5000');

    // Listen for name updates
    this.socket.on('name_update', (data) => {
      this.player1Name = data.player1;
      this.player2Name = data.player2;
    });
    
    // Listen for score updates from Flask server
    this.socket.on('score_update', (data) => {

      const previousScorePlayer1 = this.scorePlayer1;
      const previousScorePlayer2 = this.scorePlayer2;
      // Store the old server before updating
      const previousServer = this.server;  

      // Update scores and server
      this.scorePlayer1 = data.player_1;
      this.scorePlayer2 = data.player_2;
      this.server = data.server;

      // Play service change sound
      if (previousServer !== data.server) {
        this.playSound("serviceChange");
      }

      
      // Check if the score has incremented (for Player 1)
      if (this.scorePlayer1 > previousScorePlayer1) {
        // Only play beep sound if it's not a service change
        if (previousServer === data.server) {
          if (this.isFinalServe()) {
            this.playSound("finalServe");
          } else {
            this.playSound("beep");  // Play beep sound for Player 1
          }
        }
      }

      // Check if the score has incremented (for Player 2)
      if (this.scorePlayer2 > previousScorePlayer2) {
        // Only play boop sound if it's not a service change
        if (previousServer === data.server) {
          if (this.isFinalServe()) {
            this.playSound("finalServe");
          } else {
            this.playSound("boop");  // Play boop sound for Player 2
          }
        }
      }

      
    });

    this.socket.on("game_state_update", (data) => {
      this.gameState = data.gameState;
      this.serviceInterval = data.serviceInterval;
      this.winningScore = data.winningScore;

      // Only override serviceInterval if the game is in deuce
      if (this.gameState === "deuce") {
        this.serviceInterval = data.serviceInterval;
      }
    });


  },
  computed: {
    winnerName() {
        if (this.gameState === "win") {
          const winner = this.scorePlayer1 > this.scorePlayer2 ? this.player1Name : this.player2Name;
          this.triggerConfetti(winner === this.player1Name ? "left" : "right");
          return winner
        }
        return "";
      },
  },

  methods: {
    isFinalServe() {
      const totalPoints = this.scorePlayer1 + this.scorePlayer2;
      return (totalPoints + 1) % this.serviceInterval === 0;
    },
    swapService() {
      this.server = this.server === 1 ? 2 : 1;
      this.socket.emit('set_server', { player: this.server });
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
    },

    clearNames() {
      this.socket.emit('clear_names');
    },

    switchSides() {
      [this.player1Name, this.player2Name] = [this.player2Name, this.player1Name];

      this.socket.emit('switch_names', {
        player1: this.player1Name,
        player2: this.player2Name
      });
    },

    triggerConfetti(side) {
      const xPosition = side === "left" ? 0.3 : 0.7; // Left = 20%, Right = 80%
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { x: xPosition, y: 0.5 }, // Adjust x for left/right side
      });
    },

  openSettings() {
    this.showSettings = true;
  },

  closeSettings() {
    this.showSettings = false;
  },

    updateWinningScore() {
      this.socket.emit('update_winning_score', { winningScore: this.winningScore });
    },

    updateServiceInterval() {
      this.socket.emit('update_service_interval', { serviceInterval: this.serviceInterval });
    },

    playSound(type) {
      if (document.hidden) return; // Don't play if tab is inactive

      const sound = this.sounds[type];
      if (!sound) return;

      sound.currentTime = 0; // Restart the sound
      sound.play().catch((error) => {
        console.warn("Audio play blocked, waiting for user interaction", error);
        document.addEventListener("click", this.unlockAudio, { once: true });
        document.addEventListener("touchstart", this.unlockAudio, { once: true });
      });
    },

    unlockAudio() {
      Object.values(this.sounds).forEach(sound => {
        sound.play().catch(() => {});
      });
      document.removeEventListener("click", this.unlockAudio);
      document.removeEventListener("touchstart", this.unlockAudio);
    },
  },
  watch: {
    player1Name(newName, oldName) {
      if (newName !== oldName) {
        clearTimeout(this.nameUpdateTimeout);
        this.nameUpdateTimeout = setTimeout(() => {
          this.socket.emit('update_names', { player1: newName, player2: this.player2Name });
        }, 500);
      }
    },
    player2Name(newName, oldName) {
      if (newName !== oldName) {
        clearTimeout(this.nameUpdateTimeout);
        this.nameUpdateTimeout = setTimeout(() => {
          this.socket.emit('update_names', { player1: this.player1Name, player2: newName });
        }, 500);
      }
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
