<template>
  <Header />
  <Hero />
  <Processes />
  <ValueProp />
  <Footer />
</template>

<script setup>
import Header from '@/components/landingPage/Header.vue';
import Hero from '@/components/landingPage/Hero.vue';
import Footer from '@/components/landingPage/Footer.vue';
import Processes from '@/components/landingPage/Processes.vue';
import ValueProp from '@/components/landingPage/ValueProp.vue';
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
