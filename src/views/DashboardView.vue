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
            <div class='title'>Welcome {{ user.name }}</div>
            <div class='balance'>
                <div class='balance-container'> Total Balance
                    <div class='description'> Take a look at your total</div>
                    <div class='money'> {{ money }}$</div>
                </div>
                <div class='balance-container'> Income
                    <div class='description'> Your income this month</div>
                    <div class='money'> {{ money }}$</div>
                </div>
                <div class='balance-container'> Spending
                    <div class='description'> Your spendings this month</div>
                    <div class='money'> {{ money }}$</div>
                </div>
            </div>

            <div class='flow'>
                Balance flow this month
                <div class='graph'>
                    <BalanceChart />
                </div>
            </div>

            <div class='transactions'> Last 3 transactions
                 <div class='transaction'> </div>
            </div>



        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { jwtDecode } from 'jwt-decode';
import { onMounted, ref } from 'vue';
import BalanceChart from '../components/BalanceChart.vue';

const token = localStorage.getItem('token');
const user = jwtDecode(token);
const money = ref(null);
const transactions = ref(null);

const fetchUserTransactions = async () => {
    try {
        const response = await axios.get('/api/user/transactions', {
            params: { id: user.id },
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
        );
        transactions.value = await response.data;
    } catch (error) {
        console.error('Error fetching user transactions:', error);
    }
};

const fetchUserMoney = async () => {
    try {
        const response = await axios.get('/api/user/money', {
            params: { id: user.id },
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
        );
        money.value = await response.data;
    } catch (error) {
        console.error('Error fetching user money:', error);
    }
};

const fetchUserData = async () => {
    await fetchUserTransactions();
    await fetchUserMoney();
};

onMounted(() => {
    fetchUserData();
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
    display: flex;
    grid-column: span 3 / span 3;
    font-size: 2.5rem;
    font-weight: 700;
    font-family: 'AtkinsonHyperlegibleMono';
    color: var(--texto);
    text-align: center;
    align-items: center;
    justify-content: center;
}

.texto-blanco {
    color: var(--texto-blanco);
}

.balance {
    grid-column: span 2 / span 2;
    grid-row: span 4 / span 4;
    grid-column-start: 1;
    grid-row-start: 2;
    border-radius: 2rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;

}

.balance-container {
    color: var(--texto);
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: 1.7rem;
    background-color: var(--fondo-secundario);
    border-radius: 2rem;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    margin: 0.5rem 0;
    width: 100%;
}

.description {
    color: var(--texto);
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: xx-small;
}

.money {
    color: var(--texto);
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: 2rem;
    margin: 0.5rem 0;
}

.flow {
    grid-column: span 4 / span 4;
    grid-row: span 3 / span 3;
    grid-column-start: 3;
    grid-row-start: 3;
    background-color: var(--fondo-secundario);
    border-radius: 2rem;
    color: var(--texto);
    font-family: 'AtkinsonHyperlegibleMono';
    font-size: 1.7rem;
    display: flex;
    flex-direction: column;
    padding: 2rem;
    margin: 0.5rem 0;
    width: 100%;
}

.graph {
    margin: 1rem
}

.transactions {
    grid-column: span 3 / span 3;
    grid-row: span 5 / span 5;
    grid-column-start: 7;
    grid-row-start: 1;
    background-color: var(--fondo-secundario)
    
}
</style>