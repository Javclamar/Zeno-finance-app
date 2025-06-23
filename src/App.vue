<!-- src/App.vue -->
<template>
  <div class="app-container">
    <HeaderComponent />

    <main class="main-content">
      <router-view />
    </main>

    <FooterComponent />
  </div>
</template>

<script setup>
import '@/assets/css/main.css'
import FooterComponent from '@/components/FooterComponent.vue'
import HeaderComponent from '@/components/HeaderComponent.vue'
import { jwtDecode } from 'jwt-decode'
import { onMounted, ref } from 'vue'

const estaAutenticado = ref(false)

onMounted(() => {
  const token = localStorage.getItem('token')
  if (token) {
    try {
      const decoded = jwtDecode(token)
      const exp = decoded.exp * 1000 // a ms
      if (Date.now() < exp) {
        estaAutenticado.value = true
      } else {
        localStorage.removeItem('token')
      }
    } catch {
      localStorage.removeItem('token')
    }
  }
})
</script>

<style>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
  align-items: center;
  background-color: var(--fondo);
}

.main-content {
  display: flex;
  flex: 1;
  padding: 1rem;
  width: 100%;
  margin-bottom: 2rem;
  background-color: var(--fondo);
  align-items: center;
  height: fit-content;
}
</style>