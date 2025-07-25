<template>
  <div class='market-view'>
    <div class='stock-selector'>
      <div v-for="stock in stocks" :key="stock" @click="toggleStock(stock)"
        :class="['stock', { selected: stock === selectedStock }]">
        <img :src="`/images/${stock}.svg`" class="stock-image" />
      </div>
    </div>
    <div class='title'>Stocks for {{ selectedStock }}</div>
    <div class='chart-container'>
      <StockChart :ticker="selectedStock" :days="selectedTime" />
    </div>
    <div class='time-selector'>
      <div v-for="time in times" :key="time" @click="toggleTime(time)"
        :class="['time', { selected: time === convertTime(selectedTime) }]">{{ time }}</div>
    </div>
    <div class='close-values'>
      <div class='current-price'>
        <div class='current-price-title'>Current Price</div>
        <div class='current-price-value'>{{ currentPrice }}$</div>
      </div>
      <div class='prediction'>
        <div class='prediction-title'>Prediction for tomorrows close</div>
        <div class='prediction-value' v-if="predictions[selectedStock]"> {{ predictions[selectedStock as
          string].toFixed(3)
        }}$
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import StockChart from '@/components/StockChart.vue';
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';

type Predictions = Record<string, number>;

const token = localStorage.getItem('token')
const stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'META', 'TSLA', 'NFLX', 'NVDA', 'JPM', 'BAC', 'SPY', 'QQQ']
const times = ['1 month', '3 months', '1 year']
const selectedStock = ref('AAPL');
const selectedTime = ref(30)
const predictions = ref<Predictions>({});
const currentPrice = ref()

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

function convertTime(time: number) {
  if (time == 30) {
    return '1 month'
  } else if (time == 90) {
    return '3 months'
  } else {
    return '1 year'
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

async function getCurrentPrice(ticker: string) {
  try {
    const response = await axios.get('/api/stocks/current-price', {
      params: {
        ticker: ticker
      },
      headers: {
        'Content-Type': 'application/ json',
        Authorization: `Bearer ${token}`
      }
    })
    currentPrice.value = response.data.currentPrice.price
  } catch (error) {
    console.error('Error fetching current price for today', error)
  }
}

onMounted(() => {
  getPredictions()
  getCurrentPrice(selectedStock.value)
})

watch(selectedStock, () => {
  getCurrentPrice(selectedStock.value);
})

</script>

<style scoped="true">
.market-view {
  margin: 0 auto;
  font-family: 'AtkinsonHyperlegibleMono';
  color: #FFFF;
  padding: 2vw;
  border-radius: 2rem;
  margin-top: 3vw;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stock-selector {
  display: flex;
  gap: 2vw;
  margin-bottom: 1vw;
  justify-content: center;
}

.stock-selector .stock {
  cursor: pointer;
  border: 0.1vw solid transparent;
  border-radius: 0.25vw;
  padding: 0.25vw;
  transition: border-color 0.3s ease, transform 0.2s ease;
}

.stock-selector .stock:hover {
  border-color: var(--texto);
  transform: scale(1.1);
}

.stock-selector .stock.selected {
  border-color: var(--texto);
  box-shadow: 0 0 8px #0056b3aa;
}

.stock-image {
  width: 1.5vw;
  height: 1.5vw;
  user-select: none;
  pointer-events: none;
}

.title {
  font-size: 1.6rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1vw;
}

.chart-container {
  border-radius: 1rem;
  margin-bottom: 1vw;
  height: 50vh;
  width: 100vh;
  padding: 1vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.time-selector {
  display: flex;
  gap: 0.5vw;
  justify-content: space-between;
  margin-bottom: 1vw;
  background-color: #212529;
  border-radius: 0.5vw;
  padding: 0.25vw 0.25vw;
  width: 100vh;
}

.time-selector .time {
  cursor: pointer;
  padding: 0.25vw 5vw;
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

.time-selector .time.selected {
  background-color: var(--fondo-secundario);
}

.prediction,
.current-price {
  text-align: left;
  font-size: 1.3rem;
  border: 0.1vw solid rgba(255, 255, 255, 0.2);
  padding: 0.5vw 1vw;
  border-radius: 0.25vw;
  flex: 1
}

.prediction-title,
.current-price-title {
  font-size: medium;
  font-weight: 300;
  margin-bottom: 1vw;
  color: #FFFF;
}

.prediction-value,
.current-price-value {
  font-size: 1.6rem;
  font-weight: bold;
  color: var(--texto);
}

.close-values {
  display: flex;
  justify-content: space-between;
  gap: 1vw;
  margin: 1vw 0;
  width: 100vh;
}
</style>
