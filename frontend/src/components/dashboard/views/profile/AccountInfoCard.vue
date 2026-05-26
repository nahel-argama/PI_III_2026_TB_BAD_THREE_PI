<template>
  <article
    class="rounded-[28px] border border-slate-200/85 bg-white p-5 shadow-[0_20px_60px_rgba(15,23,42,0.08)] transition duration-300 hover:shadow-[0_28px_75px_rgba(15,23,42,0.13)] sm:p-7"
  >
    <h3 class="text-xl font-black tracking-tight text-slate-900">{{ title }}</h3>

    <div class="mt-6 space-y-6">
      <InfoSection
        v-for="section in sections"
        :key="section.title"
        :title="section.title"
        :fields="section.fields"
      />
    </div>
  </article>
</template>

<script setup>
import InfoSection from './InfoSection.vue';

defineProps({
  title: {
    type: String,
    required: true,
  },
  sections: {
    type: Array,
    default: () => [],
  },
});
</script>
