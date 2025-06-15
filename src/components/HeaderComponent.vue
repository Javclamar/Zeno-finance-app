<!-- src/components/Header.vue -->
<template>
  <header class="header">
    <img src="@/assets/logo.svg" alt="Logo" class="logo" />
    <nav>
      <ul class="nav">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/about">About</router-link></li>
        <li><router-link to="/contact">Contact</router-link></li>
      </ul>
    </nav>
  </header>
</template>

<script>
import '@/assets/main.css';
export default {
  name: 'Header',
  props: {
    title: {
      type: String,
      default: 'My App'
    }
  }
}
</script>

<style scoped>
.header {
  background-color: var(--fondo-secundario);
  color: var(--texto);
  padding: 1rem;
  min-width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.nav {
  list-style: none;
  display: flex;
  gap: 4rem;
  justify-content: center;
  padding: 0;
}

.nav a {
  color: var(--texto);
  text-decoration: none;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-radius: 4px;
}

.nav a:hover {
  background-color: var(--fondo);
  transition: 1s
}

.logo {
  height: 50px;
  width: auto;
}
</style>