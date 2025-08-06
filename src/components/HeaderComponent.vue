<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <div class="left">
      <img src="/images/logo.svg" alt="Zave" class="logo" />
    </div>
    <div class="center">
      <nav role="navigation" aria-label="Main navigation">
        <ul class="nav1">
          <li><router-link to="/">Dashboard</router-link></li>
          <li><router-link to="/transactions">Transactions</router-link></li>
          <li><router-link to="/budgets">Budgets</router-link></li>
          <li><router-link to="/market">Stocks</router-link></li>
        </ul>
      </nav>
    </div>
    <div class="right">
      <nav role="navigation" aria-label="Main navigation" v-if="!isLoggedIn">
        <ul class="nav2">
          <li class="login-link"><router-link to="/login" class="texto">Login</router-link></li>
          <li class="signup-link"><router-link to="/register" class="texto-blanco">Sign Up</router-link></li>
        </ul>
      </nav>
      <nav role="navigation" aria-label="Main navigation" v-else>
        <router-link to="/profile" style="color: var(--texto);">
          <font-awesome-icon icon="user" size="2x" style="fill: red;" />
        </router-link>
        <button @click="handleLogout" class="logout-button">Logout</button>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import '@/assets/css/main.css';
import router from '@/router';
import { useAuthStore } from '@/stores/authStore';
import { storeToRefs } from 'pinia';

const auth = useAuthStore();
const { isLoggedIn } = storeToRefs(auth);

function handleLogout() {
  auth.logout();
  router.push('/login');
}
</script>

<style scoped>
.header {
  position: sticky;
  top: 0;
  width: 100%;
  background-color: #212529;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 3rem;
  z-index: 1000;
}

.left,
.center,
.right {
  flex: 1;
  display: flex;
  align-items: center;

}

.left {
  justify-content: flex-start;
  padding: 0.5rem;
}

.right {
  justify-content: flex-end;
  padding: 0.5rem;
}

.logo {
  width: 2.5rem;
  max-width: 100%;
}

.nav1,
.nav2 {
  list-style: none;
  display: flex;
  gap: 2rem;
  border-radius: 1rem;
}

.nav1 {
  justify-content: space-between;
}



.login-link {
  color: var(--texto);
  text-decoration: none;
  padding: 0.5rem 1rem;
}

.signup-link {
  align-items: center;
  background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
  border: 0;
  border-radius: 8px;
  box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
  box-sizing: border-box;
  color: #ffffff;
  display: flex;
  font-size: 18px;
  justify-content: center;
  line-height: 1em;
  max-width: 100%;
  min-width: 140px;
  padding: 3px;
  text-decoration: none;
  user-select: none;
  -webkit-user-select: none;
  touch-action: manipulation;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.3s;
  transform: scale(0.9);

}

.signup-link:active,
.signup-link:hover {
  outline: 0;
  transform: scale(1);
}

.signup-link span {
  background-color: rgb(5, 6, 45);
  padding: 16px 24px;
  border-radius: 6px;
  width: 100%;
  height: 100%;
  transition: 300ms;
}

.texto {
  color: var(--texto);
  text-decoration: none;
  font-family: 'AtkinsonHyperlegibleMono';
  font-weight: bold;
}

.texto-blanco {
  color: #ffff;
  font-family: 'AtkinsonHyperlegibleMono';
  text-decoration: none;
  font-weight: bold
}

.nav1 a {
  color: var(--texto);
  text-decoration: none;
  font-family: 'AtkinsonHyperlegibleMono';
  font-weight: bold;
  padding: 0.5rem 2rem;
  border-radius: 4px;
  float: left;
}

.nav1 a.active {
  background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
}

.logout-button {
  background-color: var(--fondo);
  text-decoration: underline;
  border: 0;
  border-radius: 8px;
  box-sizing: border-box;
  color: #ffffff;
  padding: 0.5rem 1rem;
  margin: 1rem;
}
</style>
