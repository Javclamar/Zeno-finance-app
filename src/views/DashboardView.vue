<template>
  <div class="dashboard">
    <div class="dashboard-content">
      <div class='title'>Welcome {{ user.name }}</div>
      <div class='balance'>
        <div class='balance-container'> Total Balance
          <div class='description'> Take a look at your total</div>
          <div class='money'> {{ money }}$</div>
        </div>
        <div class='balance-container'> Income
          <div class='description'> Your income this month</div>
          <div class='money'> {{ money }}$</div>
        </div>
        <div class='balance-container'> Spending
          <div class='description'> Your spendings this month</div>
          <div class='money'> {{ money }}$</div>
        </div>
      </div>

      <div class='transactions-container'>
        <div class='flow'>
          Balance flow this month
          <div class='graph'>
            <BalanceChart />
          </div>
        </div>

        <div class="transactions">Last transactions
          <div class="transaction" v-for="(tx, index) in transactions.slice(0, 5)" :key="index"
            :class="tx.amount >= 0 ? 'income' : 'expense'">
            <span>{{ categoryIcons[tx.category as keyof typeof categoryIcons] }}</span>
            <div class="transaction-title">
              {{ tx.name }}
              <div class="transaction-description">{{ tx.description }}</div>
            </div>
            <div class="transaction-amount">
              <font-awesome-icon :icon="tx.amount >= 0 ? 'arrow-up' : 'arrow-down'"
                :style="{ color: tx.amount >= 0 ? 'lightgreen' : 'tomato' }" />
              {{ tx.amount }}$
            </div>
          </div>
          <div class="transactions-buttons">
            <router-link to="/transactions" class="all-transactions">View all transactions</router-link>
            <router-link to="/transactions/new/income" class="income-button">Add income</router-link>
            <router-link to="/transactions/new/expense" class="expense-button">Add expense</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { onMounted, ref } from 'vue';
import BalanceChart from '../components/BalanceChart.vue';

const token = localStorage.getItem('token');
if (!token) {
  throw new Error('No token found in localStorage');
}

interface MyJwtPayload {
  id: string;
  email: string;
  name: string;
}

const user = jwtDecode<MyJwtPayload>(token);
const money = ref(null);
const transactions = ref<Array<{ name: string, description: string, amount: number, category: keyof typeof categoryIcons }>>([]);

const categoryIcons = {
  FOOD: '🍔',
  TRANSPORT: '🚗',
  UTILITIES: '💡',
  ENTERTAINMENT: '🎮',
  HEALTH: '💊',
  SALARY: '💰',
  OTHER: '🔧',
};

const fetchUserTransactions = async () => {
  try {
    const response = await axios.get('/api/user/transactions', {
      params: { id: user.id },
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    );
    transactions.value = await response.data;
  } catch (error) {
    console.error('Error fetching user transactions:', error);
  }
};

const fetchUserMoney = async () => {
  try {
    const response = await axios.get('/api/user/money', {
      params: { id: user.id },
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    );
    money.value = await response.data;
  } catch (error) {
    console.error('Error fetching user money:', error);
  }
};

const fetchUserData = async () => {
  await fetchUserTransactions();
  await fetchUserMoney();
};

onMounted(() => {
  fetchUserData();

  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');

  if (token) {
    localStorage.setItem('token', token);
    window.history.replaceState({}, '', '/dashboard');
    console.log('Token guardado:', token);
  }

});
</script>

<style scoped>
.dashboard {
  display: flex;
  min-height: 100vh;
  font-family: 'AtkinsonHyperlegibleMono';
  min-width: 100%;
  margin-top: 3rem;
}

.dashboard-content {
  margin-left: 70px;
  padding: 2rem;
  flex: 1;
}

.title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #fff
}

.texto-blanco {
  color: var(--texto-blanco);
}

.balance {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.balance-container {
  flex: 1;
  min-width: 20rem;
  background-color: var(--fondo-secundario);
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  color: #fff;
  font-weight: 600;
}

.balance-container .description {
  font-size: 0.7rem;
  color: var(--texto);
  margin-top: 0.3rem;
}

.balance-container .money {
  font-size: 1.5rem;
  font-weight: bold;
}

.transactions-container {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-start;
  gap: 2rem;
}

.flow {
  flex: 1.2;
  font-size: 1.5rem;
  color: #fff;
  font-weight: 700;
}

.graph {
  margin-top: 1rem;
  background-color: var(--fondo-secundario);
  border-radius: 0.5rem;
  padding: 0.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

.transactions {
  flex: 0.8;
  font-size: 1.5rem;
  color: #fff;
  font-weight: 700;
  border-radius: 0.5rem;
}

.transaction {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  background-color: var(--fondo-secundario);
  padding: 0.5rem;
  margin-top: 1rem;
  border-radius: 10px;
}

.transaction-title {
  font-weight: bold;
  color: #FFF;
  font-size: 1.2rem;
  flex: auto;
  margin-left: 1rem;
}

.transaction-description {
  font-size: 0.85rem;
  color: var(--texto);
}

.transaction-amount {
  color: var(--texto-blanco);
  font-size: 1.2rem;
  text-align: right;
  margin: 1rem;
  flex: auto;
}

.income {
  border-left: 0.5rem solid lightgreen;
}

.expense {
  border-left: 0.5rem solid tomato;
}

.all-transactions {
  display: inline-block;
  padding: 0.5rem;
  background-image: linear-gradient(144deg, #274e55, #267272 50%, #6becf5c5);
  box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
  color: var(--texto-blanco);
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s;
  margin: 1rem;
  font-size: 1rem;
}

.income-button,
.expense-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: var(--texto-blanco);
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s;
  margin: 1rem;
  font-size: 1rem;
}

.income-button {
  background-image: linear-gradient(144deg, #133034, #1b4332 50%, #2d6a4f);
  box-shadow: rgb(27, 43, 28) 0 15px 30px -5px;
}

.expense-button {
  background-image: linear-gradient(144deg, #2c1620, #642527 50%, #b94f41);
  box-shadow: rgba(73, 26, 26, 0.747) 0 15px 30px -5px;
}

.income-button:hover,
.expense-button:hover,
.all-transactions:hover {
  outline: 0;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}

.transactions-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 0.5rem;
}
</style>
