<template>
    <div class="dashboard">
        <div class='dashboard-sidebar'>
            <div class='icon'><router-link to="/dashboard" class='texto-blanco'>
                    <font-awesome-icon icon="house" />
                </router-link></div>
            <div class='icon'><router-link to="/profile" class='texto-blanco'>
                    <font-awesome-icon icon="user" />
                </router-link></div>
            <div class='icon'><router-link to="/transactions" class='texto-blanco'>
                    <font-awesome-icon icon="wallet" />
                </router-link></div>
            <div class='icon'><router-link to="/settings" class='texto-blanco'>
                    <font-awesome-icon icon="gear" />
                </router-link></div>
        </div>
        <div class="dashboard-content">
            <div class='title'>Welcome {usuario}</div>
        </div>
        <div class='transactions'>

        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';


const usuario = ref('');

const fetchUserName = async () => {
    try {
        const response = await axios.get('/user/name');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        usuario.value = await response.json();
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

<style scoped>
.dashboard {
    display: grid;
    grid-template-columns: repeat(11, 1fr);
    grid-template-rows: repeat(5, 1fr);
    gap: 2rem;
    width: 100%;
    margin: 5rem 2rem;
    height: fit-content;

}

.dashboard-sidebar {
    grid-row: span 5 / span 5;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background-color: var(--fondo-secundario);
    padding: 1rem;
    border-radius: 10px;
    width: 4rem;
    gap: 6rem;
}

@media (max-width: 768px) {
    .dashboard-sidebar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4rem;
        /* barra horizontal más pequeña */
        flex-direction: row;
        gap: 1rem;
        padding: 0.5rem 1rem;
        border-radius: 0;
        justify-content: space-around;
        background-color: var(--fondo-secundario);
    }
}



.icon {
    width: 6rem;
    height: 6rem;
    display: flex;
    justify-content: center;
    align-items: center;
    color: var(--texto);
}

.icon:hover {
    background-color: var(--fondo-secundario);
    color: var(--texto-blanco);
}

.dashboard-content {
    grid-column: span 10 / span 10;
    grid-row: span 5 / span 5;
    display: grid;
    grid-template-columns: repeat(9, 1fr);
    grid-template-rows: repeat(5, 1fr);
    gap: 2rem;
}

.title {
    grid-column: span 2 / span 2;
    font-size: 2rem;
    font-weight: bold;
    font-family: 'AtkinsonHyperlegibleMono';
    color: var(--texto);
    text-align: center;
    align-items: center;
    margin: 1rem;
}

.texto-blanco {
    color: var(--texto-blanco);
}
</style>