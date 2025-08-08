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

<style scoped>
.market-view {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  margin: 2rem;
  gap: 2rem;
}

.stock-data {
  font-family: 'AtkinsonHyperlegibleMono';
  color: #FFFF;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 0.7;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 1rem;
}

.chart-container {
  border-radius: 1rem;
  margin-bottom: 1rem;
  height: 400px;
  width: 100%;
  padding: 1rem;
}

.time-selector {
  display: flex;
  gap: 0.5rem;
  justify-content: space-between;
  margin-bottom: 1rem;
  background-color: #212529;
  border-radius: 0.5rem;
  padding: 0.5rem;
  width: 100%;
}

.time-selector .time {
  flex: 1;
  cursor: pointer;
  padding: 0.5rem 2rem;
  font-weight: bold;
  color: #FFFF;
  transition: background-color 0.25s ease;
  user-select: none;
  border-radius: 0.25rem;
  text-align: center;
}

.time-selector .time.selected {
  background-color: var(--fondo-secundario);
  color: var(--texto);
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.time-selector .time:hover {
  background-color: var(--fondo-secundario);
  opacity: 0.8;
}

.close-values {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  margin: 1rem 0;
  width: 100%;
}

.prediction,
.current-price {
  text-align: left;
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 1rem;
  border-radius: 0.25rem;
  flex: 1;
}

.prediction-title,
.current-price-title {
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
  color: #FFFF;
}

.prediction-value,
.current-price-value {
  font-size: 1.2rem;
  font-weight: bold;
  color: var(--texto);
}

.news {
  flex: 0.3;
  min-width: 300px;
}

.title-news {
  font-size: 1.2rem;
  margin-bottom: 1rem;
}

.news-list {
  list-style: none;
  padding: 0;
}

.news-list li {
  display: flex;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: var(--fondo-secundario);
  border-radius: 0.5rem;
  transition: transform 0.2s ease;
  background-color: #212529;
}

.news-list li:hover {
  transform: translateY(-2px);
}

.news-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.news-list h3 {
  color: #fff;
  margin: 0;
}

.news-list p {
  color: var(--texto);
  margin: 0;
}

.news-list a {
  color: var(--texto);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: color 0.2s ease;
}

.news-list a:hover {
  color: #fff;
}

.image-container {
  flex: 0 0 100px;
  height: 100px;
  overflow: hidden;
  border-radius: 0.25rem;
}

.news-list img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.search-container {
  position: relative;
  width: 100%;
  max-width: 600px;
  margin-bottom: 1rem;
}

.search-container input {
  width: 100%;
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 1px solid var(--fondo);
  border-radius: 0.5rem;
  background-color: #212529;
  color: var(--texto);
  font-family: 'AtkinsonHyperlegibleMono';
  font-size: 1rem;
  transition: all 0.2s ease;
}

.search-container input:focus {
  outline: none;
  border-color: var(--texto);
  box-shadow: 0 0 0 2px rgba(171, 231, 229, 0.2);
}

.search-icon {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--texto);
  pointer-events: none;
}

.results-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background-color: #212529;
  border-radius: 0.5rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  list-style: none;
  max-height: 200px;
  overflow-y: auto;
  z-index: 10;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.results-list li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem;
  cursor: pointer;
  transition: background-color 0.2s ease;
  border-radius: 0.25rem;
}

.results-list li:hover {
  background-color: rgba(171, 231, 229, 0.1);
}

.stock-image {
  width: 24px;
  height: 24px;
  object-fit: contain;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .market-view {
    margin: 1rem;
    gap: 1rem;
  }

  .chart-container {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .market-view {
    flex-direction: column;
  }

  .stock-data,
  .news {
    flex: 1;
    width: 100%;
  }

  .time-selector .time {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .close-values {
    flex-direction: column;
    gap: 1rem;
  }

  .news-list li {
    flex-direction: column;
  }

  .image-container {
    width: 100%;
  }

  .news-list img {
    max-width: 100%;
    height: 200px;
    object-fit: cover;
  }

  .search-container {
    max-width: 100%;
  }

  .search-container input {
    font-size: 0.9rem;
    padding: 0.6rem 2.25rem 0.6rem 0.75rem;
  }

  .results-list {
    max-height: 180px;
  }

  .results-list li {
    padding: 0.6rem;
    font-size: 0.9rem;
  }
}

@media (max-width: 480px) {
  .market-view {
    margin: 0.5rem;
  }

  .title {
    font-size: 1.2rem;
  }

  .time-selector {
    flex-direction: column;
    gap: 0.5rem;
  }

  .time-selector .time {
    width: 100%;
    padding: 0.75rem;
  }

  .prediction-title,
  .current-price-title {
    font-size: 0.8rem;
  }

  .prediction-value,
  .current-price-value {
    font-size: 1rem;
  }

  .news-list h3 {
    font-size: 0.9rem;
  }

  .news-list p {
    font-size: 0.8rem;
  }

  .search-container input {
    font-size: 0.85rem;
    padding: 0.5rem 2rem 0.5rem 0.75rem;
  }

  .results-list {
    max-height: 160px;
  }

  .results-list li {
    padding: 0.5rem;
    font-size: 0.85rem;
  }

  .stock-image {
    width: 20px;
    height: 20px;
  }
}
</style>
