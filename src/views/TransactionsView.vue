<template>
  <div class='all-transactions'>
    <div class='title'>Transactions</div>
    <div class='search-bar'>
      <input type='text' placeholder='Search transactions...' v-model="searchInput" />
      <button class='search-button' @click="searchTransactions">
        <font-awesome-icon icon="magnifying-glass" style=" font-size: large " />
      </button>
    </div>
    <div class='transactions-list'>
      <div class='transaction' v-for="(tx, index) in transactions" :key="index"
        :class="tx.amount >= 0 ? 'income' : 'expense'">
        <div class='icon'>{{ categoryIcons[tx.category as keyof typeof categoryIcons] }}</div>
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
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { onMounted, ref } from 'vue';


const searchInput = ref('');
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
const transactions = ref<Array<{ name: string, description: string, amount: number, category: keyof typeof categoryIcons }>>([]);

const categoryIcons = {
  FOOD: '🍔',
  TRANSPORT: '🚗',
  UTILITIES: '💡',
  ENTERTAINMENT: '🎮',
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

const searchTransactions = async () => {
  try {
    const response = await axios.get('/api/user/transactions/search', {
      params: { id: user.id, search: searchInput.value },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    transactions.value = await response.data;
  } catch (error) {
    console.error('Error searching transactions:', error);
  }
};

onMounted(() => {
  fetchUserTransactions();
});
</script>

<style scoped>
.all-transactions {
  max-width: 80%;
  min-width: 50%;
  flex: 1;
  flex-direction: column;
  padding: 2rem;
  margin: 3rem auto;
  font-family: 'AtkinsonHyperlegibleMono';
}

.title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 1rem;
  color: #FFFF;
}

.search-bar {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 1rem;
}

.search-bar input {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 5px;
  background-color: #212529;
  color: var(--texto);
}

.search-bar input::placeholder {
  color: #495057;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--fondo-secundario);
}

.search-bar button {
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  background-color: var(--fondo);
  color: var(--texto);
  cursor: pointer;
}

.transactions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 50%;
}

.transaction {
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  padding: 0.5rem;
  margin-top: 1rem;
  border-radius: 10px;
}

.transaction-title {
  font-weight: bold;
  color: var(--texto);
  flex: auto;
  margin-left: 1rem;
}

.transaction-description {
  font-size: 0.85rem;
  color: #FFFF;
}

.transaction-amount {
  color: #FFF;
  font-size: 700;
  text-align: right;
  margin: 1rem;
  flex: auto;
}

.icon {
  width: 3rem;
  height: 3rem;
  font-size: xx-large;
  background-color: var(--fondo-secundario);
  border-radius: 20%;
}
</style>
