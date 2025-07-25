<template>
  <Line :key="chartKey" :data="chartData" :options="chartOptions" />
</template>

<script setup lang="ts">
import axios from 'axios';
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LinearScale,
  LineElement,
  PointElement,
  Title,
  Tooltip
} from 'chart.js';
import { onMounted, ref, watch } from 'vue';
import { Line } from 'vue-chartjs';

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
);

interface Stock {
  Date: string,
  Close: number
}

const token = localStorage.getItem('token')
const chartKey = ref(0);

const props = defineProps({
  ticker: String,
  days: Number
})

const chartData = ref({
  labels: [] as string[],
  datasets: [
    {
      label: 'Close',
      data: [] as number[],
      fill: true,
      borderColor: '#9DA7A9',
      tension: 0.3
    }
  ]
})

const chartOptions = ref({
  responsive: true,
  plugins: {
    legend: {
      display: true
    }
  },
  scales: {
    x: {
      grid: {
        color: '#133034',
      },
      ticks: {
        color: '#9DA7A9',
        font: { family: 'AtkinsonHyperlegibleMono' }
      }
    },
    y: {
      min: 0,
      max: 600,
      beginAtZero: true,
      title: {
        display: true,
        text: 'Balance ($)',
        color: '#9DA7A9',
        font: { family: 'AtkinsonHyperlegibleMono' }
      },
      grid: {
        color: '#0002'
      },
      ticks: {
        color: '#9DA7A9',
        font: { family: 'AtkinsonHyperlegibleMono' }
      }
    }
  }
});

async function getStockData(ticker: string, days: number) {
  try {
    const response = await axios.get('/api/stocks/stock-data', {
      params: {
        ticker,
        days
      },
      headers: {
        'Content-Type': 'application/ json',
        Authorization: `Bearer ${token}`
      }
    });

    const stockData = (response.data as Stock[]).map(stock => ({
      Date: new Date(stock.Date).toISOString().split('T')[0],
      Close: parseFloat((stock as Stock).Close as unknown as string)
    }))

    stockData.sort((a, b) => new Date(a.Date).getTime() - new Date(b.Date).getTime())

    const labels = stockData.map(s => s.Date);
    const data = stockData.map(s => s.Close);

    const maxStock = Math.max(...data);
    const minStock = Math.min(...data);
    const range = maxStock - minStock
    const padding = range * 0.1;

    chartData.value.labels = labels;
    chartData.value.datasets[0].data = data;
    chartOptions.value.scales.y.max = maxStock + padding;
    chartOptions.value.scales.y.min = minStock - padding;
    chartKey.value++;
  } catch (error) {
    console.error(`Error loading the chart: ${error}`)
  }
}

onMounted(() => {
  getStockData(props.ticker as string, props.days as number);
});

watch(() => [props.ticker, props.days], () => {
  getStockData(props.ticker as string, props.days as number);
});

</script>
