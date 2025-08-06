<template>
  <div class='modal'>
    <div class='modal-content'>
      <div class='form-title'>{{ props.budgetToUpdate ? 'Update Budget' : 'Create new Budget' }}</div>
      <form @submit.prevent="handleSubmit">
        <div class='form-group'>
          <label for='category'>Budget Category:</label>
          <select id='category' v-model='budget.category' required>
            <option value='FOOD'>Food</option>
            <option value='TRANSPORT'>Transport</option>
            <option value='ENTERTAINMENT'>Entertainment</option>
            <option value='UTILITIES'>Utilities</option>
            <option value='HEALTH'>Health</option>
            <option value='OTHER'>Other</option>
          </select>
          <label for='amount'> Budget Amount:</label>
          <input type='float' id='amount' v-model='budget.amount' min='1' required />
          <label for='startDate'>Start Date:</label>
          <input type='date' id='startDate' v-model='budget.startDate' required />
          <label for='endDate'>End Date:</label>
          <input type='date' id='endDate' v-model='budget.endDate' required />
          <button class='submit' type='submit'>{{ props.budgetToUpdate ? 'Update' : 'Create' }}</button>
          <button class='close' @click=handleClose()>Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import axios, { AxiosError } from 'axios';
import { ref, watch } from 'vue';
import { useToast } from 'vue-toastification';

const toast = useToast()
const emit = defineEmits(['close', 'created', 'updated']);
const token = localStorage.getItem('token');
const props = defineProps({
  budgetToUpdate: { type: Object, default: null }
})

if (!token) {
  throw new Error('No token found in localStorage');
}

const budget = ref({
  budgetId: "",
  category: 'OTHER',
  amount: 0,
  startDate: '',
  endDate: ''
});

watch(() => props.budgetToUpdate, (newVal) => {
  if (newVal) {
    budget.value = {
      budgetId: newVal.id,
      category: newVal.category,
      amount: newVal.amount,
      startDate: new Date(newVal.startDate).toISOString().split('T')[0],
      endDate: new Date(newVal.endDate).toISOString().split('T')[0]
    }
  }
}, { immediate: true })

async function handleSubmit() {
  if (props.budgetToUpdate) {
    await handleUpdate();
    emit('updated')
  } else {
    await handleCreate()
    emit('created')
  }
}

const handleUpdate = async (): Promise<void> => {
  try {
    const response = await axios.put('/api/budgets/update', {
      ...budget.value,
    },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
    if (response.status === 200) {
      router.push('/budgets');
    } else {
      console.error('Failed update budget:', response.data);
    }
  } catch (error) {
    console.error('Error updating budget:', error);
  }
}

const handleCreate = async (): Promise<void> => {
  try {
    const response = await axios.post('/api/budgets/new', {
      ...budget.value,
    },
      {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        }
      })
    if (response.status === 200) {
      router.push('/budgets');
    } else {
      console.error('Failed create budget:', response.data);
    }
  } catch (error: unknown) {
    if (axios.isAxiosError(error)) {
      console.log(error.response?.data)
      const backendMessage = error.response?.data?.error || 'Unknown error'
      toast.error(`❌ ${backendMessage}`)
    } else {
      console.error(error)
      toast.error('❌ Unknown error')
    }
  }
}

function handleClose() {
  budget.value = {
    budgetId: "",
    category: 'OTHER',
    amount: 0,
    startDate: '',
    endDate: ''
  }
  emit("close")
}
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: #212529;
  padding: 1.5rem;
  border-radius: 8px;
  width: 40rem;
  flex-direction: column;
  align-items: center;
}

.form-group {
  display: flex;
  flex-direction: column;

}

.form-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 2rem;
  color: #FFFF;
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group label {
  margin-bottom: 0.3rem;
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
  margin-bottom: 2rem;
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
  margin-bottom: 2rem;
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
  margin: 1rem;
  font-size: 1rem;
  background-image: linear-gradient(144deg, #274e55, #267272 50%, #6becf5c5);
  border: none;
  font-weight: bold;
  cursor: pointer;
}

.submit:hover {
  outline: 0;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}

.close {
  text-align: center;
  margin: auto;
  background-color: #0000;
  padding: 1rem;
  border: none;
  color: #b94f41;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
}
</style>
