<template>
  <div class="dashboard">
    <div class='title'>Welcome {{ user.name }}</div>
    <div class='balance'>
      <div class='balance-container'> Total Balance
        <div class='description'> Take a look at your total</div>
        <div class='money'> {{ money }}$</div>
      </div>
      <div class='balance-container'> Income
        <div class='description'> Your income this month</div>
        <div class='money'> {{ income }}$</div>
      </div>
      <div class='balance-container'> Spending
        <div class='description'> Your spendings this month</div>
        <div class='money'> {{ spending }}$</div>
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
        <div class="transaction" v-for="(tx, index) in transactions.slice(0, 4)" :key="index"
          :class="tx.amount >= 0 ? 'income' : 'expense'">
          <span>{{ categoryIcons[tx.category as keyof typeof categoryIcons] }}</span>
          <div class="transaction-title">
            {{ tx.name }}
            <div class="transaction-description">{{ tx.description }}</div>
            <div class="transaction-description">{{ tx.date.split('T')[0] }}</div>
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
const income = ref(null);
const spending = ref(null);
const transactions = ref<Array<{ name: string, description: string, amount: number, date: string, category: keyof typeof categoryIcons }>>([]);


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
    const response = await axios.get('/api/transactions/dashboard', {
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

const fetchUserMontlhyIncome = async () => {
  try {
    const response = await axios.get('/api/transactions/monthly-income', {
      params: { id: user.id },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    income.value = await response.data.monthlyIncome;
  } catch (error) {
    console.error('Error fetching user monthly income:', error);
  }
}

const fetchUserMontlhySpending = async () => {
  try {
    const response = await axios.get('/api/transactions/monthly-spending', {
      params: { id: user.id },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    spending.value = await response.data.monthlySpending;
  } catch (error) {
    console.error('Error fetching user monthly spending:', error);
  }
}

const fetchUserData = async () => {
  await fetchUserTransactions();
  await fetchUserMoney();
  await fetchUserMontlhyIncome();
  await fetchUserMontlhySpending();
};

onMounted(() => {
  fetchUserData();

  const params = new URLSearchParams(window.location.search);
  const token = params.get('token');

  if (token) {
    localStorage.setItem('token', token);
    window.history.replaceState({}, '', '/dashboard');
  }

});
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  font-family: 'AtkinsonHyperlegibleMono';
  width: 100%;
  padding: 1rem;
  margin: 0 1rem;
}

.title {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: #FFFF;
  text-align: center;
  font-weight: bold;
  letter-spacing: 1px;
}

.balance {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  justify-content: center;
}

.balance-container {
  flex: 1 1 250px;
  min-width: 220px;
  background-color: var(--fondo-secundario);
  padding: 0.5rem 1rem;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  color: #fff;
  font-weight: bold;
  margin-bottom: 0.5rem;
  transition: transform 0.2s;
}

.balance-container:hover {
  transform: translateY(-3px) scale(1.03);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
}

.balance-container .description {
  font-size: 0.9rem;
  color: var(--texto, #9DA7A9);
  margin-top: 0.3rem;
}

.balance-container .money {
  font-size: 1.2rem;
  font-weight: bold;
  margin-top: 0.5rem;
}

.transactions-container {
  display: flex;
  justify-content: space-evenly;
  align-items: flex-start;
  gap: 2rem;
  flex-wrap: wrap;
}

.flow {
  display: flex;
  flex-direction: column;
  flex: 1.2;
  font-size: 1.5rem;
  color: #fff;
  font-weight: 700;
  height: 30rem;
}

.graph {
  display: flex;
  margin-top: 1rem;
  background-color: var(--fondo-secundario, #1b2a2f);
  border-radius: 0.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  justify-content: center;
  height: 100%;
}

.graph canvas {
  width: 100%;
  height: 100%;
  border-radius: 0.5rem;
  padding: 1rem 0;
}

.transactions {
  flex: 0.8;
  font-size: 1.5rem;
  color: #fff;
  font-weight: 700;
  border-radius: 0.5rem;
  min-width: 250px;
}

.transaction {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--fondo-secundario, #1b2a2f);
  padding: 0.7rem;
  margin-top: 1rem;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.2s;
}

.transaction:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
}

.transaction-title {
  font-weight: bold;
  color: #FFF;
  font-size: 1rem;
  flex: 1;
  margin-left: 1rem;
  word-break: break-word;
}

.transaction-description {
  font-size: 0.8rem;
  color: var(--texto, #9DA7A9);
}

.transaction-amount {
  color: var(--texto-blanco, #fff);
  font-size: 1.2rem;
  text-align: right;
  margin: 1rem;
  flex: none;
  min-width: 80px;
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
  color: var(--texto-blanco, #fff);
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s, transform 0.2s;
  margin: 1rem 0;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
}

.income-button,
.expense-button {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: var(--texto-blanco, #fff);
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s, transform 0.2s;
  margin: 1rem;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
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
  transform: scale(1.07);
  transition: transform 0.2s ease-in-out;
}

.transactions-buttons {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  margin-top: 0.5rem;
  gap: 0.5rem;
}

@media (max-width: 600px) {
  .dashboard {
    margin-top: 1rem;
  }

  .balance {
    flex-direction: column;
    gap: 1rem;
  }

  .balance-container {
    height: 2rem;
  }

  .transactions-container {
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
  }

  .flow,
  .transactions {
    min-width: unset;
    font-size: 1.2rem;
  }

  .graph,
  .transactions {
    min-width: unset;
    padding: 0.5rem;
  }
}

@media (max-width: 600px) {
  .dashboard {
    margin-top: 0.5rem;
    padding: 0.2rem;
  }

  .title {
    font-size: 1.3rem;
    margin-bottom: 1rem;
  }

  .balance-container {
    min-width: 140px;
    padding: 0.7rem 1rem;
    font-size: 1rem;
    flex: 1;
  }

  .balance-container .money {
    font-size: 1.1rem;
  }

  .transactions-container {
    gap: 1rem;
  }

  .transaction {
    flex-direction: column;
    align-items: flex-start;
    padding: 0.5rem;
  }

  .transaction-title {
    margin-left: 0;
    margin-top: 0.5rem;
    font-size: 0.95rem;
  }

  .transaction-amount {
    margin: 0.5rem 0 0 0;
    font-size: 1rem;
  }

  .transactions-buttons {
    flex-direction: column;
    align-items: stretch;
    gap: 0.5rem;
  }

  .all-transactions,
  .income-button,
  .expense-button {
    margin: 0.5rem 0;
    font-size: 0.95rem;
    padding: 0.4rem 0.7rem;
  }
}
</style>
