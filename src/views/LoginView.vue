<template>
  <div class="login-container">
    <div class="title">Login</div>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Email:</label>
        <input type="text" id="username" v-model="email" required />
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button class="login" type="submit">Sign In</button>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>
    <div class="message">Don't have an account yet? <router-link to="/register" class="link">Sign Up</router-link></div>

    <button class='google' @click="loginWithGoogle">
      <img src="@/assets/images/google.png" alt="Google Icon">
    </button>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const router = useRouter();
const auth = useAuthStore();
const { isLoggedIn } = storeToRefs(auth);

const handleLogin = async () => {
  errorMessage.value = '';
  successMessage.value = '';

  try {
    const response = await axios.post('/api/auth/login', {
      email: email.value,
      password: password.value
    });
    console.log('Login response:', response.data);

    if (response.data.token) {
      auth.login(response.data.token);
      successMessage.value = 'Successfully logged in! Redirecting...';
      if (isLoggedIn.value) {
        setTimeout(() => {
          router.push('/dashboard');
        }, 1000);
      }


    } else {
      errorMessage.value = 'Incorrect email or password.';
    }
  } catch (error) {
    if (axios.isAxiosError(error) && error.response && error.response.data && error.response.data.error) {
      console.error('Error during login:', error.response.data.error);
      errorMessage.value = error.response.data.error;
    } else {
      console.error('Error during login:', error);
      errorMessage.value = 'An unexpected error occurred during login.';
    }
  }
};

const loginWithGoogle = async () => {
  const clientId = "1075293173356-sq9qb0j70q44n1pc990qs807rajjf0fv.apps.googleusercontent.com";
  const redirectUri = 'http://localhost:3000/api/auth/google/callback';
  const scope = 'email profile';
  const responseType = 'code';
  const state = crypto.randomUUID();

  const authUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${clientId}&redirect_uri=${redirectUri}&response_type=${responseType}&scope=${scope}&state=${state}`;
  window.location.href = authUrl;
};
</script>

<style scoped>
.login-container {
  max-width: 80%;
  height: auto;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--fondo-secundario);
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.title {
  font-size: 2rem;
  margin-bottom: 1rem;
  font-family: 'AtkinsonHyperlegibleMono';
  font-weight: bold;
  text-align: center;
  color: var(--texto);
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: var(--texto);
  font-weight: 500;
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group input {
  padding: 0.5rem;
  border: 1px solid var(--fondo);
  background-color: var(--fondo-secundario);
  outline: 0;
  border-radius: 0.5rem;
  font-size: 1rem;
  color: var(--texto);
  font-family: 'AtkinsonHyperlegibleMono';
}

.form-group input:focus {
  border-color: rgba(167, 139, 250);
}

.login {
  display: block;
  width: 100%;
  background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
  box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
  padding: 0.75rem;
  text-align: center;
  color: #ffff;
  font-size: 1.2rem;
  font-family: 'AtkinsonHyperlegibleMono';
  border: none;
  border-radius: 0.375rem;
  font-weight: 600;
}

.message {
  margin-top: 1rem;
  font-family: 'AtkinsonHyperlegibleMono';
  text-align: center;
  color: var(--texto);
}

.link {
  color: var(--boton);
  margin-left: 0.5rem;
  font-family: 'AtkinsonHyperlegibleMono';
  text-decoration: none;
  font-weight: bold;
}

button:hover {
  outline: 0;
  transform: scale(1.05);
  transition: transform 0.2s ease-in-out;
}

.error {
  color: #e74c3c;
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
  font-family: 'AtkinsonHyperlegibleMono';

}

.success {
  color: green;
  text-align: center;
  margin-top: 1rem;
  font-weight: bold;
  font-family: 'AtkinsonHyperlegibleMono';
}

.google {
  background-color: var(--fondo);
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: 1rem;
}
</style>
