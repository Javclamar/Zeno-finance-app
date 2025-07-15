<template>
  <div class='expense-container'>
    <div class='title'>Add an expense</div>
    <form @submit.prevent="handleSubmit">
      <div class='form-group'>
        <label for='name'>Name:</label>
        <input type='text' id='name' v-model='income.name' required />
        <label for='description'>Description:</label>
        <input type='text' id='description' v-model='income.description' />
        <label for='amount'>Amount:</label>
        <input type='float' id='amount' v-model='income.amount' min='1' required />
        <label for='date'>Date:</label>
        <input type='date' id='date' v-model='income.date' required />
        <label for='category'>Category:</label>
        <select id='category' v-model='income.category' required>
          <option value='FOOD'>Food</option>
          <option value='TRANSPORT'>Transport</option>
          <option value='ENTERTAINMENT'>Entertainment</option>
          <option value='UTILITIES'>Utilities</option>
          <option value='HEALTH'>Health</option>
          <option value='SALARY'>Salary</option>
          <option value='OTHER'>Other</option>
        </select>
        <button class='submit' type='submit'>Add Expense</button>
      </div>
    </form>
    <div class='back'>
      <router-link to='/dashboard' class='link'>Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script setup lang="ts">

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

interface Income {
  name: string;
  description: string;
  amount: number;
  date: string;
  category: string;
}

const income = ref<Income>({
  name: '',
  description: '',
  amount: 0,
  date: '',
  category: 'OTHER'
});

const handleSubmit = async () => {
  try {
    const response = await axios.post('/api/transactions/new', {
      ...income.value,
      date: income.value.date || new Date().toISOString().split('T')[0]
    }, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('token')}`
      },
      params: {
        type: 'expense'
      }
    });
    if (response.status === 200) {
      router.push('/dashboard');
    } else {
      console.error('Failed to add income:', response.data);
    }
  } catch (error) {
    console.error('Error adding income:', error);
  }
}
</script>

<style scoped>
.expense-container {
  margin: 0 auto;
  margin-top: 5rem;
  max-width: 80%;
  padding: 2rem;
  background-color: #212529;
  border-radius: 0.5rem;
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
  font-family: 'AtkinsonHyperlegibleMono';
  font-weight: bold;
  color: var(--texto);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  margin-bottom: 0.1rem;
  color: var(--texto);
  font-weight: 600;
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group input {
  padding: 0.3rem;
  border: 1px solid var(--fondo);
  background-color: var(--fondo-secundario);
  outline: 0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: var(--texto);
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group input:focus {
  border-color: rgba(167, 139, 250);
}

.form-group select {
  padding: 0.5rem;
  border: 1px solid var(--fondo);
  background-color: var(--fondo-secundario);
  outline: 0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: var(--texto);
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group select:focus {
  border-color: rgba(167, 139, 250);
}

.submit {
  display: inline-block;
  padding: 0.5rem 1rem;
  color: #fff;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: background-color 0.2s;
  margin: 1rem;
  font-size: 1rem;
  background-image: linear-gradient(144deg, #2c1620, #b94f41 50%, #642527);
  border: none;
  cursor: pointer;
  font-family: 'AtkinsonHyperlegibleMono';
}

.submit:hover {
  outline: 0;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}

.back {
  text-align: center;
  margin-top: 1rem;
  background-color: #0000;
  border: none;
}

.link {
  color: var(--texto);
  text-decoration: none;
  font-weight: bold;
  font-family: 'AtkinsonHyperlegibleMono';
}
</style>
