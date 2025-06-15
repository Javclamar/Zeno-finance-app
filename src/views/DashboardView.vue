<template>
    <div class="dashboard">
        <HeaderComponent />
        <main class="dashboard-content">
            <p>Welcome to your dashboard!</p>
            <p>Here you can manage your settings and view your data.</p>
        </main>
        <FooterComponent />
    </div>
</template>

<script setup>
import FooterComponent from '@/components/FooterComponent.vue';
import HeaderComponent from '@/components/HeaderComponent.vue';
import { onMounted, ref } from 'vue';

const usuarios = ref([]);

const fetchUserName = async () => {
    try {
        const response = await axios.get('/user/name');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        usuarios.value = await response.json();
    } catch (error) {
        console.error('Error fetching usuarios:', error);
    }
};

const fetchUserTransactions = async () => {
    try {
        const response = await axios.get('/user/transactions');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const transactions = await response.json();
        console.log(transactions);
    } catch (error) {
        console.error('Error fetching user transactions:', error);
    }
};

const fetchUserMoney = async () => {
    try {
        const response = await axios.get('/user/money');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const money = await response.json();
        console.log(money);
    } catch (error) {
        console.error('Error fetching user money:', error);
    }
};

const fetchUserData = async () => {
    await fetchUserName();
    await fetchUserTransactions();
    await fetchUserMoney();
};

onMounted(() => {
    fetchUserData
});
</script>