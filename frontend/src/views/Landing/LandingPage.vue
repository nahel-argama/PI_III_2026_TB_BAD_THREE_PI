<template>
  <Header />
  <Hero />
  <ProblemSection />
  <SolutionSection />
  <FeaturesSection />
  <TargetAudienceSection />
  <Footer />
</template>

<script setup>
import Header from '@/components/landingPage/Header.vue';
import Hero from '@/components/landingPage/Hero.vue';
import ProblemSection from '@/components/landingPage/ProblemSection.vue';
import SolutionSection from '@/components/landingPage/SolutionSection.vue';
import FeaturesSection from '@/components/landingPage/FeaturesSection.vue';
import TargetAudienceSection from '@/components/landingPage/TargetAudienceSection.vue';
import Footer from '@/components/landingPage/Footer.vue';
</script>

<style>
html {
  scroll-behavior: smooth;
}
</style>
