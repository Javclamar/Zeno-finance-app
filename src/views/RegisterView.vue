<template>
    <div class="register-container">
        <div class="title">Sing Up</div>
        <form @submit.prevent="handleregister">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" id="name" v-model="name" required />

                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required />

                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />

                <label for="password">Repeat Password:</label>
                <input type="password" id="repeatPassword" v-model="repeatPassword" required />
            </div>
            <button type="submit">Register</button>
            <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
            <p v-if="successMessage" class="success">{{ successMessage }}</p>
        </form>
        <div class="message">Already have an account? <router-link to="/" class="link">Login here</router-link></div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const name = ref('');
const repeatPassword = ref('');
const email = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const router = useRouter();

const handleregister = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    if (password.value !== repeatPassword.value) {
        errorMessage.value = 'Passwords do not match.';
        return;
    }

    try {
        await axios.post('/api/auth/register', {
            name: name.value,
            email: email.value,
            password: password.value,
            repeatPassword: repeatPassword.value
        });
        successMessage.value = 'Registration successful! You can now log in.';
        setTimeout(() => {
            router.push('/login');
        }, 2000);
    } catch (error) {
        console.error('Error during register:', error);
        errorMessage.value = error.response?.data?.error || 'An error occurred during registration.';
    }
};
</script>

<style scoped>
.register-container {
    max-width: 80%;
    height: auto;
    margin: 0 auto;
    padding: 20px;
    background-color: var(--fondo-secundario);
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
    font-size: 2rem;
    margin-bottom: 1rem;
    font-weight: 700;
    font-family: 'AtkinsonHyperlegibleMono';
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
    font-weight: 600;
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: 1rem;
    color: var(--texto);
}

.form-group input {
    padding: 0.5rem;
    border: 1px solid var(--fondo);
    background-color: var(--fondo-secundario);
    outline: 0;
    border-radius: 0.5rem;
    font-size: 1rem;
    font-family: 'AtkinsonHyperlegibleMono';
    margin-bottom: 0.5rem;
    color: var(--texto);
}

.form-group input:focus {
    border-color: rgba(167, 139, 250);
}

button {
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
    text-align: center;
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: 1rem;
    font-weight: 400;
    color: var(--texto);
}

.link {
    margin-top: 1rem;
    display: inline-block;
    font-size: 1rem;
    font-family: 'AtkinsonHyperlegibleMono';
    color: var(--boton);
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
</style>