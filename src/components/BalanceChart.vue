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
import { jwtDecode } from 'jwt-decode';
import { onMounted, ref } from 'vue';
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

interface MyJwtPayload {
  id: string;
  email: string;
  name: string;
}

const token = localStorage.getItem('token');
const user = token ? jwtDecode<MyJwtPayload>(token) : null;
const chartKey = ref(0);

interface Transaction {
  id: number;
  name: string;
  description: string;
  amount: number;
  date: string;
  userId: number;
}

const chartData = ref({
  labels: [] as string[],
  datasets: [
    {
      label: 'Balance',
      data: [] as number[],
      fill: true,
      borderColor: '#9DA7A9',
      tension: 0.3
    }
  ]
});

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

onMounted(async () => {
  if (!user) {
    console.error('User is not authenticated.');
    return;
  }
  const response = await axios.get('/api/transactions/monthly', {
    params: { id: user.id },
    headers: {
      Authorization: `Bearer ${token}`
    }
  }

  );
  const transactions = (response.data as Transaction[]).map(tx => ({
    ...tx,
    amount: parseFloat((tx as Transaction).amount as unknown as string),
    date: new Date(tx.date).toISOString().split('T')[0]
  })) as Transaction[];

  transactions.sort((a, b) => new Date(a.date).getDate() - new Date(b.date).getDate());

  let balance = 0;
  const labels: string[] = [];
  const data: number[] = [];

  transactions.forEach(tx => {
    balance += tx.amount;
    labels.push(tx.date.split('-')[2]);
    data.push(balance);
  });

  const maxBalance = Math.max(...data);
  const minBalance = Math.min(...data);
  const padding = 200;

  chartData.value.labels = labels;
  chartData.value.datasets[0].data = data;
  chartOptions.value.scales.y.max = maxBalance + padding;
  chartOptions.value.scales.y.min = minBalance - padding;
  chartKey.value++;
});

</script>
