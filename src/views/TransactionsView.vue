<template>
  <div class='all-transactions'>
    <div class='title'>Transactions</div>
    <div class='search-bar'>
      <input type='text' placeholder='Search transactions...' v-model="searchInput" />
      <button class='search-button' @click="searchTransactions">
        <font-awesome-icon icon="magnifying-glass" style=" font-size: large " />
      </button>
    </div>
    <div class='pagination-buttons'>
      <div class='page'><button class='page-button' @click="currentPage--"
          :disabled="currentPage <= 1">Previous</button>
        <span>Page {{ currentPage }}</span>
        <button class='page-button' @click="currentPage++" :disabled="!hasMore">Next</button>
      </div>
      <div class='page-size'>
        <button class='page-button' @click="pageSize--" :disabled="pageSize <= 1"><font-awesome-icon icon="arrow-down"
            style=" font-size: large " /></button>
        <span>{{ pageSize }}</span>
        <button class='page-button' @click="pageSize++" :disabled="pageSize >= 20"><font-awesome-icon icon="arrow-up"
            style=" font-size: large " /></button>
      </div>
    </div>
    <div class='transactions-list'>
      <div class='transaction' v-for="(tx, index) in transactions" :key="index"
        :class="tx.amount >= 0 ? 'income' : 'expense'">
        <div class='icon'>{{ categoryIcons[tx.category as keyof typeof categoryIcons] }}</div>
        <div class="transaction-title">
          {{ tx.name }}
          <div class="transaction-description">{{ tx.description }}</div>
          <div class="transaction-date"> {{ tx.date.split('T')[0] }}</div>
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
import { onMounted, ref, watch } from 'vue';


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
const transactions = ref<Array<{ name: string, description: string, amount: number, category: keyof typeof categoryIcons, date: string }>>([]);
const currentPage = ref(1);
const pageSize = ref(10);
const hasMore = ref(true);
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
    const response = await axios.get('/api/transactions/user', {
      params: {
        id: user.id,
        page: currentPage.value,
        pageSize: pageSize.value
      },
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
    );
    transactions.value = response.data;
    hasMore.value = response.data.length === pageSize.value;
  } catch (error) {
    console.error('Error fetching user transactions:', error);
  }
};

const searchTransactions = async () => {
  try {
    const response = await axios.get('/api/transactions/search', {
      params: { id: user.id, search: searchInput.value },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    transactions.value = response.data;
  } catch (error) {
    console.error('Error searching transactions:', error);
  }
};

onMounted(() => {
  fetchUserTransactions();
});
watch(currentPage, () => {
  fetchUserTransactions()
})
watch(pageSize, () => {
  currentPage.value = 1
  fetchUserTransactions()
})
</script>

<style scoped>
.all-transactions {
  max-width: 70%;
  min-width: 40%;
  flex: 1;
  flex-direction: column;
  padding: 2rem;
  margin: 3rem auto;
  margin-bottom: 1rem;
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
  min-width: 40%;
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

.pagination-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 1rem 0;
  flex-wrap: wrap;
  gap: 1rem;
}

.page,
.page-size {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.page-button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  min-width: 44px;
  height: 40px;
  background-color: #495057;
  color: #FFF;
  cursor: pointer;
}

.page-button:disabled {
  background-color: #212529;
  cursor: not-allowed;
}

@media (max-width: 600px) {
  .pagination-buttons {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .page,
  .page-size {
    width: 100%;
    justify-content: center;
  }

  .all-transactions {
    max-width: 95%;
    padding: 1rem;
    margin: 1rem auto;
  }
}

/* Add hover effects */
.page-button:hover:not(:disabled) {
  background-color: #343a40;
  transform: translateY(-1px);
  transition: all 0.2s ease;
}
</style>
