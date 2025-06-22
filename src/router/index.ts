import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import { createRouter, createWebHistory } from 'vue-router';


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: (to) => {
        const isAuthenticated = !!localStorage.getItem('token');
        return isAuthenticated ? '/dashboard' : '/login';
      }
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { guestsOnly: true }
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { guestsOnly: true }
    }
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // o usar Vuex/Pinia

  if (to.meta.guestsOnly && isAuthenticated) {
    return next('/dashboard');
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next('/login');
  }

  next();
});


export default router
