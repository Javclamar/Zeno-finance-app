<template>
  <div class='market-view'>
    <div class='stock-selector'>
      <div v-for="stock in stocks" :key="stock" @click="toggleStock(stock)" class="stock">
        <img :src="`/images/${stock}.svg`" class="stock-image" />
      </div>
    </div>
    <div class='title'>Stocks for {{ selectedStock }}</div>
    <div class='chart-container'>
      <StockChart :ticker="selectedStock" :days="selectedTime" />
    </div>
    <div class='time-selector'>
      <div v-for="time in times" :key="time" @click="toggleTime(time)" class="time">{{ time }}</div>
    </div>
    <div class='prediction'>
      <div class='prediction-title'>Prediction for {{ selectedStock }} tomorrows close</div>
      <div class='prediction' v-if="predictions[selectedStock]"> {{ predictions[selectedStock as string].toFixed(3) }}$
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StockChart from '@/components/StockChart.vue';
import axios from 'axios';
import { onMounted, ref } from 'vue';

type Predictions = Record<string, number>;

const token = localStorage.getItem('token')
const stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ']
const times = ['1 month', '3 months', '1 year']
const selectedStock = ref('AAPL');
const selectedTime = ref(30)
const predictions = ref<Predictions>({});

function toggleStock(stock: string) {
  selectedStock.value = stock
}

function toggleTime(time: string) {
  if (time == '1 month') {
    selectedTime.value = 30
  } else if (time == '3 months') {
    selectedTime.value = 90
  } else {
    selectedTime.value = 360
  }
}

async function getPredictions() {
  try {
    const response = await axios.get('/api/stocks/predictions', {
      headers: {
        'Content-Type': 'application/ json',
        Authorization: `Bearer ${token}`
      }
    })
    predictions.value = response.data as Predictions

  } catch (error) {
    console.error('Error fetching predictions for today', error)
  }
}

onMounted(() => {
  getPredictions()
})

</script>

<style scoped="true">
.market-view {
  min-width: 40%;
  margin: 0 auto;
  font-family: 'AtkinsonHyperlegibleMono';
  color: #FFFF;
  padding: 2vw;
  border-radius: 2rem;
  margin-top: 3vw;
}

.stock-selector {
  display: flex;
  gap: 1vw;
  margin-bottom: 20px;
  justify-content: center;
}

.stock-selector .stock {
  cursor: pointer;
  border: 2px solid transparent;
  border-radius: 6px;
  padding: 6px;
  transition: border-color 0.3s ease, transform 0.2s ease;
}

.stock-selector .stock:hover {
  border-color: #007bff;
  transform: scale(1.1);
}

.stock-selector .stock.selected {
  border-color: #0056b3;
  box-shadow: 0 0 8px #0056b3aa;
}

.stock-image {
  width: 3vw;
  height: 2vw;
  user-select: none;
  pointer-events: none;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2vw;
}

.chart-container {
  background-color: var(--fondo-secundario);
  border-radius: 1rem;
  padding: 1vw;
  margin-bottom: 2vw;
  min-height: 30%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.time-selector {
  display: flex;
  gap: 0.5vw;
  justify-content: center;
  margin-bottom: 1vw;
  background-color: #212529;
  border-radius: 0.5vw;
  padding: 0.25vw 0.25vw;
}

.time-selector .time {
  cursor: pointer;
  padding: 0.5vw 6vw;
  font-weight: 600;
  color: #FFFF;
  transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
  user-select: none;
  width: auto;
  border-radius: 0.25vw;
}

.time-selector .time:hover {
  background-color: var(--fondo-secundario);
}

.prediction {
  margin: 0 auto;
  text-align: center;
  font-size: 1.3rem;
  color: #222;
}

.prediction-title {
  font-weight: 600;
  margin-bottom: 1vw;
  color: #FFFF;
}

.prediction .prediction {
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--texto);
}
</style>
