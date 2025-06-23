<template>
    <div class="landing-view">
        <div class='title'>Bringin finance to everyday life</div>
        <div class='subtitle'>Your personal AI driven budget assistant</div>
        <div class='description'>Budgeting helps you save money, Zave grows it. Zave focuses on giving real-time advice
            for investing trough key performance indicators, not just saving money, but increasing it.</div>
        <div class='dashboard-amimation'></div>
        <div class='about'>Zave is the first serius project of our team, driven by ambition to provide an authentic aid
            to people that struggles managing expenses,
            bringin advice powered by various AI models, each one specialized in a specific field.</div>
        <div class='services'>
            <div class='service'>
                <div class='service-title'>Budgeting</div>
                <div class='service-description'>Zave helps you track your expenses and income, providing insights into
                    your financial habits.</div>
            </div>
            <div class='service'>
                <div class='service-title'>Investing</div>
                <div class='service-description'>Zave offers personalized investment advice based on your financial
                    goals and risk tolerance.</div>
            </div>
            <div class='start'>
                <div class='start-title'>Get Started</div>
                <div class='start-description'>Join Zave today and take control of your financial future.</div>
                <router-link to="/register" class='start-button'>Sign Up</router-link>
            </div>
        </div>
    </div>
</template>

<script setup>
import gsap from 'gsap';
import ScrollSmoother from 'gsap/ScrollSmoother';
import ScrollTrigger from 'gsap/ScrollTrigger';
import { onMounted } from 'vue';

gsap.registerPlugin(ScrollTrigger, ScrollSmoother);

onMounted(() => {
    // Aparece cada .service con desplazamiento + opacidad
    gsap.from('.service', {
        scrollTrigger: {
            trigger: '.service',
            start: 'top 80%',
            end: 'bottom 20%',
            scrub: true,
        },
        opacity: 0,
        y: 50,
        duration: 0.8,
        stagger: 0.3,
        ease: 'power2.out'
    })

    gsap.from('.title', {
        y: -40,
        opacity: 0,
        duration: 1,
        ease: 'power2.out'
    })

    gsap.from('.subtitle', {
        x: -40,
        opacity: 0,
        duration: 2,
        ease: 'power2.out',
        delay: 0.5
    })

    gsap.from('.description', {
        opacity: 0,
        x: 40,
        duration: 0.8,
        ease: 'power2.out'
    })


    gsap.from('.start', {
        scrollTrigger: {
            trigger: '.start',
            start: 'top 90%',
            end: 'bottom 70%',
            scrub: true,
        },
        opacity: 0,
        y: 50,
        duration: 0.8,
        ease: 'power2.out'
    })
})

</script>

<style scoped>
.landing-view {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    background-color: var(--fondo);
    color: var(--texto);
    margin: 4rem;
}

.title {
    font-size: 2rem;
    font-weight: 500;
    margin: 2rem;
    text-align: center;
    justify-content: center;
    font-family: 'AtkinsonHyperlegibleMono'
}

.subtitle {
    font-size: 6rem;
    margin: 2rem;
    text-align: center;
    font-weight: 600;
    line-height: 1;
    width: 100%;
    font-family: 'AtkinsonHyperlegibleMono'
}

.description {
    margin: 4rem;
    font-size: 1.5rem;
    text-align: center;
    max-width: 80%;
    line-height: 1.5;
    font-weight: 400;
    font-family: 'AtkinsonHyperlegibleMono';
}

.dashboard-amimation {
    width: 100%;
    height: 300px;
    background-image: url('@/assets/animation.gif');
    background-size: cover;
    background-position: center;
    margin-bottom: 2rem;
}

.about {
    font-size: 1.2rem;
    text-align: center;
    max-width: 800px;
    margin-bottom: 2rem;
    font-family: 'AtkinsonHyperlegibleMono'
}

.services {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4rem;
    margin: 3rem;
}

.service-description {
    font-size: 1.3rem;
    margin-top: 0.5rem;
    background-color: var(--fondo-secundario);
    padding: 1rem;
    border-radius: 8px;
    color: var(--texto);
    font-weight: 400;
    line-height: 1.5;
    font-family: 'AtkinsonHyperlegibleMono'
}

.service {
    padding: 1rem;
    border-radius: 8px;
    width: 80%;
    max-width: 600px;
    text-align: center;
    font-family: 'AtkinsonHyperlegibleMono';
}

.service-title {
    background-color: var(--fondo-secundario);
    margin-bottom: 1rem;
    padding: 0.5rem;
    border-radius: 8px;
    font-size: 1.5rem;
    font-weight: 500;
    font-family: 'AtkinsonHyperlegibleMono'
}

.start {
    padding: 1rem;
    width: 80%;
    max-width: 600px;
    text-align: center;
}

.start-title {
    background-color: var(--fondo-secundario);
    padding: 0.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'AtkinsonHyperlegibleMono'
}

.start-description {
    font-size: 1.3rem;
    background-color: var(--fondo-secundario);
    padding: 1rem;
    border-radius: 8px;
    margin-bottom: 3rem;
    font-weight: 400;
    line-height: 1.5;
    font-family: 'AtkinsonHyperlegibleMono'

}

.start-button {
    background-image: linear-gradient(144deg, #af40ff, #5b42f3 50%, #00ddeb);
    color: #ffff;
    box-shadow: rgba(151, 65, 252, 0.2) 0 15px 30px -5px;
    padding: 1rem 2rem;
    border-radius: 8px;
    text-decoration: none;
    font-size: 2rem;
    font-weight: 700;
    font-family: 'AtkinsonHyperlegibleMono'
}

.start-button:hover {
    transform: scale(2);
    transition: transform 0.2s ease-in-out;
}
</style>