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
  margin: 2rem auto;
  width: 90%;
  max-width: 1200px;
  padding: 0 1rem;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.title {
  font-size: 2rem;
  font-weight: bold;
  color: #FFFF;
}

.subtitle {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #FFFF;
}

.add-budget {
  padding: 0.75rem 1.5rem;
  background-image: linear-gradient(144deg, #274e55, #267272 50%, #6becf5c5);
  color: #FFFF;
  border-radius: 0.5rem;
  text-decoration: none;
  margin: 0.5rem;
  font-size: 1rem;
  border: none;
  cursor: pointer;
  font-family: 'AtkinsonHyperlegibleMono';
  transition: transform 0.2s ease-in-out;
}

.budget-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 10px;
  background-color: #212529;
  flex-wrap: wrap;
  gap: 1rem;
}

.link-content {
  display: flex;
  flex: 1;
  min-width: 280px;
}

.icon-dates {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
  width: 100%;
}

.budget-category-icon {
  width: 3rem;
  height: 3rem;
  border-radius: 20%;
  font-size: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.dates {
  color: var(--texto);
  font-size: 1rem;
  flex: 1;
  min-width: 200px;
}

.amounts {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 1rem;
  min-width: 150px;
}

.total-budget {
  color: #FFF;
  margin: 0.1rem;
}

.buttons {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.edit-budget,
.delete-budget {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  font-size: 0.9rem;
  transition: transform 0.2s ease;
}

.edit-budget {
  background-color: #ffb703;
}

.delete-budget {
  background-color: #e76f51;
}

.progress-bar {
  width: 100%;
  height: 0.5rem;
  background-color: #eee;
  border-radius: 0.2rem;
  overflow: hidden;
  margin: 0.5rem 0;
}

.progress {
  color: #fff;
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

/* Hover effects */
.add-budget:hover,
.edit-budget:hover,
.delete-budget:hover {
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .budget-view {
    width: 100%;
    padding: 0 0.5rem;
  }

  .title {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1.1rem;
  }

  .dates,
  .amounts {
    font-size: 0.9rem;
  }

  .buttons {
    flex-direction: column;
    width: 100%;
  }

  .edit-budget,
  .delete-budget {
    width: 100%;
    margin: 0.25rem 0;
  }
}
</style>
