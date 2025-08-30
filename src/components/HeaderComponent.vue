<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <div class="left">
      <img src="/favicon.ico" alt="Zave" class="logo" />
    </div>
    <div class="center">
      <button class="burger" @click="toggleMenu" aria-label="Toggle navigation">
        <span></span>
        <span></span>
        <span></span>
      </button>
      <nav role="navigation" aria-label="Main navigation">
        <ul class="nav1" :class="{ open: menuOpen }">
          <li><router-link to="/" @click="toggleMenu">Dashboard</router-link></li>
          <li><router-link to="/transactions" @click="toggleMenu">Transactions</router-link></li>
          <li><router-link to="/budgets" @click="toggleMenu">Budgets</router-link></li>
          <li><router-link to="/market" @click="toggleMenu">Stocks</router-link></li>
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
import { ref } from 'vue';

const auth = useAuthStore();
const { isLoggedIn } = storeToRefs(auth);
const menuOpen = ref(false);

function handleLogout() {
  auth.logout();
  router.push('/login');
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #212529;
  color: var(--texto, #9DA7A9);
  padding: 0.5rem 2rem;
  box-shadow: 0 2px 8px #0002;
  width: 100%;
  font-family: 'AtkinsonHyperlegibleMono';
}

.logo {
  width: 40px;
  height: 40px;
}

.center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.burger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
}

.burger span {
  display: block;
  width: 25px;
  height: 3px;
  background: var(--texto, #9DA7A9);
  border-radius: 2px;
  transition: 0.3s;
}

.nav1 {
  display: flex;
  gap: 4rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav1 li a {
  color: var(--texto, #9DA7A9);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav1 li a:hover {
  color: var(--accent, #fff);
}

.right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.logout-button {
  background: var(--accent, #9DA7A9);
  color: #133034;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-left: 1rem;
}

.logout-button:hover {
  background: #fff;
  color: #133034;
}

.nav2 {
  display: flex;
  gap: 1rem;
  list-style: none;
  margin: 0;
  padding: 0;
  align-items: center;
}

.texto {
  color: var(--texto, #9DA7A9);
  text-decoration: none;
  font-weight: normal;
}

.signup-link {
  background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.signup-link .texto-blanco {
  color: #FFFF;
  text-decoration: none;
  font-weight: normal;
}

.signup-link:hover {
  scale: 1.05;
  transition: scale 0.2s ease-in-out;
}

.signup-link .texto-blanco {
  color: #FFFF;
  text-decoration: none;
  font-weight: normal;
}


@media (max-width: 900px) {
  .header {
    flex-direction: row;
  }

  .nav1 {
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    background: #212529;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem 2rem;
    display: none;
    z-index: 10;
    transition: all 0.3s ease-in-out;
  }

  .nav1.open {
    display: flex;
  }

  .burger {
    display: flex;
    margin: 1rem 0;
  }

  .center {
    align-items: center;
    margin-left: 3.5rem;
  }
}
</style>
