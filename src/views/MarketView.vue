<template>
  <div class='market-view'>
    <div class='stock-data'>
      <div class="search-container">
        <input v-model="searchInput" @input="onInput" @focus="showResults = true" type="text"
          placeholder="Search stocks..." />
        <font-awesome-icon icon="magnifying-glass" class='search-icon' />
        <ul v-if="showResults && searchResults.length" class="results-list">
          <li v-for="(ticker, index) in searchResults" :key="index"
            @click="selectedStock = ticker; showResults = false">
            {{ ticker }}
            <img v-if="ticker" :src="`https://financialmodelingprep.com/image-stock/${ticker}.png`"
              class="stock-image" />
          </li>
        </ul>
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
          <div class='prediction-title'>Prediction for next close</div>
          <div class='prediction-value' v-if="predictions[selectedStock]"> {{ predictions[selectedStock as
            string].toFixed(3)
            }}$
          </div>
        </div>
      </div>
    </div>
    <div class='news'>
      <div class='title-news'>Latest News</div>
      <ul v-if="news.length" class='news-list'>
        <li v-for="(item, index) in news" :key="index">
          <div class='image-container' v-if="item.images && item.images.length">
            <img v-if="item.images && item.images.length" :src="item.images[0].url" alt="News Image" />
          </div>
          <div class='news-content'>
            <h3>{{ item.headline }}</h3>
            <p>{{ item.summary }}</p>
            <p>
              <a :href="item.url" target="_blank" rel="noopener noreferrer">
                Read more
                <font-awesome-icon icon="arrow-right" />
              </a>
            </p>
          </div>
        </li>
      </ul>
      <p v-else>No news available for today.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import StockChart from '@/components/StockChart.vue';
import axios from 'axios';
import { onMounted, ref, watch } from 'vue';

type Predictions = Record<string, number>;

const token = localStorage.getItem('token');
const times = ['1 month', '3 months', '1 year'];
const selectedStock = ref('AAPL');
const selectedTime = ref(30);
const predictions = ref<Predictions>({});
const currentPrice = ref();

interface NewsItem {
  headline: string;
  summary: string;
  images?: ImageObjetct[];
  url?: string;
}

interface ImageObjetct {
  size: string;
  url: string;
}

const news = ref<NewsItem[]>([]);
const searchInput = ref('');
const showResults = ref(false)
const searchResults = ref([])
let timeout: number | undefined = undefined;

const onInput = () => {
  clearTimeout(timeout)
  if (!searchInput.value) {
    searchResults.value = []
    return
  }

  timeout = setTimeout(async () => {
    try {
      const response = await axios('/api/stocks/search', {
        params: { search: searchInput.value },
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      searchResults.value = response.data
    } catch (error) {
      console.error(error)
      searchResults.value = []
    }
  }, 300)
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

async function getNews(ticker: string = selectedStock.value) {
  try {
    const response = await axios.get('/api/stocks/stock-news', {
      params: {
        ticker: ticker
      },
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`
      }
    })
    news.value = response.data.news.data as NewsItem[];
  } catch (error) {
    console.error('Error fetching news for today', error)
  }
}

onMounted(() => {
  getPredictions()
  getCurrentPrice(selectedStock.value)
  getNews(selectedStock.value);
})

watch(selectedStock, () => {
  getCurrentPrice(selectedStock.value);
  getNews(selectedStock.value);
})

</script>

<style scoped="true">
.market-view {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin: 2vw 3vw;
  gap: 2vw;
}

.stock-data {
  font-family: 'AtkinsonHyperlegibleMono';
  color: #FFFF;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 0.7;
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
  font-size: 1.5vw;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1vw;
}

.chart-container {
  border-radius: 1rem;
  margin-bottom: 1vw;
  height: 50vh;
  width: 100%;
  padding: 1vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container canvas {
  width: 100%;
  height: 100%;
}

.time-selector {
  display: flex;
  gap: 0.5vw;
  justify-content: space-around;
  margin-bottom: 1vw;
  background-color: #212529;
  border-radius: 0.5vw;
  padding: 0.25vw 0.25vw;
  width: 100%;
}

.time-selector .time {
  cursor: pointer;
  padding: 0.25vw 5vw;
  font-weight: bold;
  color: #FFFF;
  transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
  user-select: none;
  width: 100%;
  border-radius: 0.25vw;
  text-align: center;
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
  border: 0.1vw solid rgba(255, 255, 255, 0.2);
  padding: 0.5vw 1vw;
  border-radius: 0.25vw;
  flex: 1
}

.prediction-title,
.current-price-title {
  font-size: 0.7vw;
  font-weight: 300;
  margin-bottom: 1vw;
  color: #FFFF;
}

.prediction-value,
.current-price-value {
  font-size: 1.3vw;
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

.search-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: left;
  margin-bottom: 1vw;
  position: relative;
  width: 100%;
}

.search-container input {
  flex: 1;
  padding: 0.5vw;
  border: none;
  border-radius: 0.25vw;
  background-color: #212529;
  color: var(--texto);
}

.search-container input::placeholder {
  color: #495057;
}

.search-container input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--fondo-secundario);
}

.results-list {
  position: absolute;
  background-color: #212529;
  top: 100%;
  padding: 0.5vw;
  width: 50%;
  list-style: none;
  color: var(--texto);
  border-radius: 0.25vw;
}

.results-list li {
  padding: 0.5vw;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-direction: row;
}



.stock-image {
  width: 1.5vw;
  height: 1.5vw;
  margin-left: 0.5vw;
  background-color: transparent;
}

.search-icon {
  position: absolute;
  right: 0.5vw;
  top: 0.5vw;
  color: var(--texto);
  cursor: pointer;
}

.news {
  flex: 0.3;
  font-family: 'AtkinsonHyperlegibleMono';
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.title-news {
  font-size: 1.2vw;
  font-weight: bold;
  margin-bottom: 1vw;
  text-align: center;
  color: #FFFF;
}

.news-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 1vw;
}

.news-list li {
  background-color: #212529;
  border-radius: 0.5vw;
  padding: 1vw;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: row;
  gap: 1vw;
}

.news-list li:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.image-container {
  flex: 0.3;
}

.news-content {
  flex: 0.7;
}

.news-list h3 {
  font-size: 0.7vw;
  color: var(--texto);
}

.news-list p {
  margin: 0.5vw 0;
  color: #adb5bd;
  font-size: 0.5vw;
}

.news-list img {
  max-width: 7vw;
  height: auto;
  margin-top: 0.5vw;
  border-radius: 0.5vw;
  object-fit: cover;
}

.news-list a {
  color: #8ecae6;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.5vw;
}
</style>
