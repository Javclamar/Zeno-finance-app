<template>
    <div class="login-container">
        <div class="title">Login</div>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">Email:</label>
                <input type="text" id="username" v-model="email" required />
                <label for="password">Contraseña:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Iniciar Sesión</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>
        <p>Don't have an account yet? <router-link to="/register">Register Here</router-link></p>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const router = useRouter();
const handleLogin = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const response = await axios.post('/api/login', {
            email: email.value,
            password: password.value
        });

        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            successMessage.value = 'Successfully logged in! Redirecting...';
            setTimeout(() => {
                router.push('/');
            }, 2000);
        } else {
            errorMessage.value = 'Incorrect email or password.';
        }
    } catch (error) {
        console.error('Error during login:', error);
        errorMessage.value = 'There was an error during login. Please try again later.';
    }
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
}

.title {
    font-size: 2rem;
    margin-bottom: 1rem;
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
}

.form-group input {
    padding: 0.5rem;
    border: 1px solid var(--borde);
    border-radius: 5px;
    font-size: 1rem;
}

.form-group input:focus {
    border-color: var(--borde-foco);
    outline: none;
}

button {
    padding: 0.5rem;
    background-color: var(--boton);
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
}

button:hover {
    background-color: var(--boton-hover);
    transition: 1s;
}
</style>