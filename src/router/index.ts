import DashboardView from '@/views/DashboardView.vue'
import LandingView from '@/views/LandingView.vue'
import LoginView from '@/views/LoginView.vue'
import NewExpenseView from '@/views/NewExpenseView.vue'
import NewIncomeView from '@/views/NewIncomeView.vue'
import RegisterView from '@/views/RegisterView.vue'
import SettingsView from '@/views/SettingsView.vue'
import TransactionsView from '@/views/TransactionsView.vue'

import { useAuthStore } from '@/stores/authStore'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: LandingView,
    },
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
      path: '/dashboard',
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
      path: '/settings',
      name: 'settings',
      component: SettingsView,
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
      name: 'new-income',
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
    return next('/dashboard')
  }

  if (to.meta.requiresAuth && !authStore.isLoggedIn) {
    return next('/login')
  }

  next()
})

export default router
