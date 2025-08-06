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

<script setup lang="ts">
import '@/assets/css/main.css';
import FooterComponent from '@/components/FooterComponent.vue';
import HeaderComponent from '@/components/HeaderComponent.vue';
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();
authStore.checkTokenValidity();
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
  flex: 1;
  width: 100%;
  background-color: var(--fondo);
  align-items: center;
  display: flex;
}
</style>
