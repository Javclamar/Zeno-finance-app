import BudgetView from '@/views/BudgetView.vue'
import DashboardView from '@/views/DashboardView.vue'
import LoginView from '@/views/LoginView.vue'
import NewExpenseView from '@/views/NewExpenseView.vue'
import NewIncomeView from '@/views/NewIncomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TransactionsView from '@/views/TransactionsView.vue'

import { useAuthStore } from '@/stores/authStore'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestsOnly: true },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestsOnly: true },
    },
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: TransactionsView,
      meta: { requiresAuth: true },
    },
    {
      path: '/budgets',
      name: 'budgets',
      component: BudgetView,
      meta: { requiresAuth: true },
    },
    {
      path: '/transactions/new/income',
      name: 'new-income',
      component: NewIncomeView,
      meta: { requiresAuth: true },
    },
    {
      path: '/transactions/new/expense',
      name: 'new-expense',
      component: NewExpenseView,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (!authStore.isLoggedIn) {
    const token = new URLSearchParams(window.location.search).get('token')
    if (token) {
      localStorage.setItem('token', token)
      authStore.setLoggedIn(true)
      window.history.replaceState({}, '', to.path)
    }
  }

  if (to.meta.guestsOnly && authStore.isLoggedIn) {
    return next('/')
  }

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return next('/login')
  }

  next()
})

export default router
