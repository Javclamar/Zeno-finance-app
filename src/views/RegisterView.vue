<template>
    <div class="register-container">
        <h1>Register</h1>
        <form @submit.prevent="handleregister">
            <div class="form-group">
                <label for="username">Email:</label>
                <input type="text" id="username" v-model="email" required />
                <label for="password">Contraseña:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Register</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>
        <p>Ya tienes una cuenta? <router-link to="/">Inicia sesión aquí</router-link></p>
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
const handleregister = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const response = await axios.post('/api/register', {
            email: email.value,
            password: password.value
        });

        if (response.data.token) {
            localStorage.setItem('token', response.data.token);
            successMessage.value = 'Successfully registered in! Redirecting...';
            setTimeout(() => {
                router.push('/');
            }, 2000);
        } else {
            errorMessage.value = 'Incorrect email or password.';
        }
    } catch (error) {
        console.error('Error during register:', error);
        errorMessage.value = 'There was an error during registration. Please try again later.';
    }
};
</script>