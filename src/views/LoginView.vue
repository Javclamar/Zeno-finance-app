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
            <button type="submit">Sign In</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>
        <div class="message">Don't have an account yet? <router-link to="/register" class="link">Sign Up</router-link>
        </div>
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
        const response = await axios.post('/api/auth/login', {
            email: email.value,
            password: password.value
        });
        console.log('Login response:', response.data);

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
        console.error('Error during login:', error.response.data.error);
        errorMessage.value = error.response.data.error;
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
    font-weight: bold;
    text-align: center;
    color: #ffff;
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
    border: 1px solid var(--fondo);
    background-color: var(--fondo-secundario);
    outline: 0;
    border-radius: 0.5rem;
    font-size: 1rem;
    color: var(--texto);
}

.form-group input:focus {
    border-color: rgba(167, 139, 250);
}

button {
    display: block;
    width: 100%;
    background-color: rgba(167, 139, 250, 1);
    padding: 0.75rem;
    text-align: center;
    color: var(--fondo);
    border: none;
    border-radius: 0.375rem;
    font-weight: 600;
}

.message {
    margin-top: 1rem;
    text-align: center;
    color: var(--texto);
}

.link {
    color: var(--boton);
    text-decoration: none;
    font-weight: bold;
}

button:hover {
    background-color: var(--boton-hover);
    transition: 1s;
}

.error {
    color: #e74c3c;
    text-align: center;
    margin-top: 1rem;
    font-weight: bold;

}

.success {
    color: var(--boton-hover);
    text-align: center;
}
</style>