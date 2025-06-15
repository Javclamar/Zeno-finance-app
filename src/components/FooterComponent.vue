<!-- src/components/Footer.vue -->
<template>
    <footer class="footer">
      <p>&copy; {{ currentYear }} Mi Sitio Web. Todos los derechos reservados.</p>
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
  }
  </style>