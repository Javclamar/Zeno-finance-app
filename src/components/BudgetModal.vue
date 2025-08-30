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
          <input type='date' id='startDate' v-model='budget.startDate' required pattern="\d{4}-\d{2}-\d{2}"
            inputmode="numeric" :min="new Date().toISOString().split('T')[0]" />
          <label for='endDate'>End Date:</label>
          <input type='date' id='endDate' v-model='budget.endDate' required pattern="\d{4}-\d{2}-\d{2}"
            inputmode="numeric" :min="budget.startDate || new Date().toISOString().split('T')[0]" />
          <button class='submit' type='submit'>{{ props.budgetToUpdate ? 'Update' : 'Create' }}</button>
          <button class='close' @click=handleClose()>Close</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import router from '@/router';
import axios from 'axios';
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
  background: rgba(0, 0, 0, 0.75);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;

}

.modal-content {
  background: #212529;
  padding: 2rem;
  border-radius: 12px;
  width: 100%;
  max-width: 40rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  animation: modalFadeIn 0.3s ease-out;
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-title {
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
  color: #FFFF;
  text-align: center;
}

.form-group label {
  color: var(--texto);
  font-weight: 600;
  font-size: 0.9rem;
}

.form-group input,
.form-group select {
  padding: 0.75rem;
  border: 1px solid var(--fondo);
  background-color: var(--fondo-secundario);
  outline: none;
  border-radius: 8px;
  font-size: 1rem;
  color: var(--texto);
  font-family: 'AtkinsonHyperlegibleMono';
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.form-group .form-group input:focus,
.form-group select:focus {
  border-color: rgba(167, 139, 250, 0.8);
  box-shadow: 0 0 0 2px rgba(167, 139, 250, 0.2);
}

.form-group input:hover,
.form-group select:hover {
  border-color: rgba(167, 139, 250, 0.5);
}

.submit {
  padding: 0.75rem 1.5rem;
  color: #fff;
  border-radius: 8px;
  text-decoration: none;
  margin: 1rem 0;
  font-size: 1rem;
  background-image: linear-gradient(144deg, #274e55, #267272 50%, #6becf5c5);
  border: none;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  font-family: 'AtkinsonHyperlegibleMono';
}

.submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(107, 236, 245, 0.2);
}

.submit:active {
  transform: translateY(0);
}

.close {
  width: 100%;
  padding: 0.75rem;
  border: none;
  color: #b94f41;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  background: transparent;
  transition: all 0.2s ease;
  font-family: 'AtkinsonHyperlegibleMono';
}

.close:hover {
  color: #e76f51;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive Styles */
@media (max-width: 768px) {
  .modal-content {
    padding: 1.5rem;
  }

  .form-title {
    font-size: 1.5rem;
    margin-bottom: 1rem;
  }
}

@media (max-width: 480px) {
  .modal {
    padding: 0.5rem;
  }

  .modal-content {
    padding: 1rem;
  }

  .form-title {
    font-size: 1.25rem;
  }

  .form-group input,
  .form-group select {
    padding: 0.6rem;
    font-size: 0.95rem;
  }

  .submit,
  .close {
    padding: 0.6rem;
    font-size: 0.95rem;
  }
}
</style>
