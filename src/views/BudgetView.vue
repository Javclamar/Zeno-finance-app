<template>
  <BudgetModal v-if="isModalOpen" @close="handleClose" @created="handleCreated" @updated="handleUpdated"
    :budget-to-update="budgetToEdit ?? undefined" />
  <div class='budget-view'>
    <div class='header'>
      <div class='title'>Budgets</div>
      <button class='add-budget' @click="isModalOpen = true">New Budget</button>
    </div>
    <div class='subtitle'>Active Budgets</div>
    <div class='budget-list'>
      <div v-for="budget in budgets" :key="budget.id" class="budget">
        <div class="budget-link">
          <div class="link-content">
            <div class="icon-dates">
              <div class="budget-category-icon">
                <span>{{ categoryIcons[budget.category as keyof typeof categoryIcons] }}</span>
              </div>
              <div class="dates">
                <div class="budget-startDate">{{ new Date(budget.startDate).toLocaleDateString() }} - {{ new
                  Date(budget.endDate).toLocaleDateString() }}</div>
              </div>
              <div class='amounts'>
                <div class='total-budget'> Total: {{ budget.amount }}$</div>
                <div class='total-budget'> Spent: {{ budget.spent }}$</div>
              </div>
              <div class="progress-bar">
                <div class="progress-bar-fill" :style="{ width: (budget.spent / budget.amount * 100) + '%' }"></div>
              </div>
              <div class='progress'> Spent {{ (budget.spent / budget.amount * 100).toFixed(2) + '%' }}</div>
            </div>
          </div>
          <div class=" buttons">
            <button class="edit-budget" @click="openModal(budget)">Edit</button>
            <button class="delete-budget" @click="deleteBudget(budget.id as unknown as number)">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { computed, onMounted, ref, watch } from 'vue';
import { useToast } from 'vue-toastification';
import BudgetModal from '../components/BudgetModal.vue';

const toast = useToast()
const token = localStorage.getItem('token');
const budgets = ref<Budget[]>([]);
const isModalOpen = ref(false);
const budgetToEdit = ref<Budget | null>(null)

const lowBudgets = computed(() =>
  budgets.value.filter(b => (b.spent / b.amount) >= 0.75)
)

if (!token) {
  throw new Error('No token found in localStorage');
}

interface MyJwtPayload {
  id: string;
  email: string;
  name: string;
}

interface Budget {
  id: number;
  category: string;
  amount: number;
  spent: number;
  startDate: string;
  endDate: string;
}

const categoryIcons = {
  FOOD: '🍔',
  TRANSPORT: '🚗',
  UTILITIES: '💡',
  ENTERTAINMENT: '🎮',
  HEALTH: '💊',
  SALARY: '💰',
  OTHER: '🔧',
};

const user = jwtDecode<MyJwtPayload>(token);

const fetchUserActiveBudgets = async () => {
  try {
    const response = await axios.get('api/budgets/active', {
      params: { id: user.id },
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    budgets.value = await response.data;
  } catch (error) {
    console.error('Error fetching user active budgets:', error);
  }
};

const deleteBudget = async (budgetId: number) => {
  try {
    await axios.delete('api/budgets/delete', {
      params: { id: budgetId },
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    budgets.value = budgets.value.filter(obj => obj.id !== budgetId);
  } catch (error) {
    console.error('Error deleting budget:', error);
  }
}

const handleCreated = (): void => {
  isModalOpen.value = false;
  fetchUserActiveBudgets();
}

const handleUpdated = (): void => {
  isModalOpen.value = false;
  fetchUserActiveBudgets();
}

const handleClose = (): void => {
  isModalOpen.value = false;
  budgetToEdit.value = null
}

function openModal(budget: Budget) {
  budgetToEdit.value = budget
  isModalOpen.value = true
}


onMounted(() => {
  fetchUserActiveBudgets();
});

watch(lowBudgets, (newVal) => {
  if (newVal.length > 0) {
    toast.warning(`⚠️ You have ${newVal.length} budget(s) below 25%!`)
  }
})
</script>

<style scoped>
.budget-view {
  font-family: 'AtkinsonHyperlegibleMono';
  margin: 3rem auto;
  width: 80%
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.title {
  font-size: 3vw;
  font-weight: bold;
  color: #FFFF
}

.subtitle {
  font-size: 2vw;
  margin-bottom: 1rem;
  color: #FFFF
}

.add-budget {
  display: inline-block;
  padding: 0.5rem;
  background-image: linear-gradient(144deg, #274e55, #267272 50%, #6becf5c5);
  color: #FFFF;
  border-radius: 0.5rem;
  text-decoration: none;
  margin: 1vw;
  font-size: 1vw;
  border: none;
  cursor: pointer;
  font-family: 'AtkinsonHyperlegibleMono';
}

.add-budget:hover {
  outline: 0;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}

.budget-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 50%;
}

.budget-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 1rem;
  margin-top: 1rem;
  border-radius: 10px;
  background-color: #212529
}

.link-content {
  display: flex;
  text-decoration: none;
  width: 90%;
}

.icon-dates {
  display: flex;
  gap: 2vw;
  align-items: center;
  width: 90%;
}

.budget-category-icon {
  flex: 0.3;
  width: 3rem;
  height: 3rem;
  border-radius: 20%;
  font-size: xx-large;
}

.dates {
  flex: 1.3;
  color: var(--texto);
  display: flex;
  gap: 1rem;
  font-size: 1.3vw;
}

.amounts {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  flex: 1;
  font-size: 1.3vw
}

.total-budget {
  color: #FFF;
  text-align: right;
  margin: 0.1rem;
  flex: 1
}

.buttons {
  display: flex;
  flex-direction: column;
  gap: 1vw;
  margin: 1vw;
  margin-left: 2vw;
  font-family: 'AtkinsonHyperlegibleMono'
}

.edit-budget {
  padding: 0.5vw;
  background-color: #ffb703;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer
}

.delete-budget {
  padding: 0.5vw;
  background-color: #e76f51;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer
}

.progress-bar {
  flex: 1;
  width: 100%;
  height: 0.5rem;
  background-color: #eee;
  border-radius: 0.2rem;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #e76f51;
  transition: width 0.3s ease;
}

.progress {
  flex: 0.2;
  text-decoration: none;
  color: #fff;
  font-size: 1.3vw
}
</style>
