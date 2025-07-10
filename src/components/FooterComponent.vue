<!-- src/components/Footer.vue -->
<template>
  <footer class="footer">
    <p>&copy; {{ currentYear }} Finance App</p>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear()
    }
  }
}
</script>

<style scoped>
.footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
  width: 100%;
}
</style>