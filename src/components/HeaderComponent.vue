<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <div class="left">
      <img src="@/assets/logo.svg" alt="Logo" class="logo" />
    </div>
    <div class="center">
      <nav>
        <ul class="nav1">
          <li><router-link to="/">Home</router-link></li>
          <li><router-link to="/about">About</router-link></li>
          <li><router-link to="/contact">Contact</router-link></li>
        </ul>
      </nav>
    </div>
    <div class="right">
      <nav v-if="!isLoggedIn">
        <ul class="nav2">
          <li class="login-link"><router-link to="/login" class="texto">Login</router-link></li>
          <li class="signup-link"><router-link to="/register" class="texto-negro">Sign Up</router-link></li>
        </ul>
      </nav>
      <nav v-else>
        <router-link to="/profile" style="color: var(--texto);">
          <font-awesome-icon icon="user" size="2x" style="fill: red;" />
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script setup>
import '@/assets/main.css';
import { useAuthStore } from '@/stores/auth';
import { onMounted } from 'vue';

const auth = useAuthStore();
const isLoggedIn = auth.isLoggedIn;

onMounted(() => {
  auth.loadTokenFromStorage();
});
</script>

<style scoped>
.header {
  width: 100%;
  background-color: var(--fondo);
  padding: 1rem;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 3rem;
}

.left,
.center,
.right {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.left {
  justify-content: flex-start;
}

.right {
  justify-content: flex-end;
}

.logo {
  height: auto;
  width: 40px;
  max-width: 100%;
}

.nav1,
.nav2 {
  list-style: none;
  display: flex;
  gap: 2rem;
  border-radius: 1rem;
  padding: 0.5rem;
}

.nav1 {
  background-color: var(--fondo-secundario);
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
  font-weight: bold;
}

.texto-negro {
  color: var(--fondo);
  text-decoration: none;
  font-weight: bold
}

.nav1 a {
  color: var(--texto);
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  float: left;
}

.nav1 a.active {
  background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
}
</style>