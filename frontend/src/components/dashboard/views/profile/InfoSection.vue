<template>
  <section>
    <h4 class="text-sm font-bold tracking-[0.16em] text-slate-500 uppercase">{{ title }}</h4>
    <dl class="mt-3 grid grid-cols-1 gap-x-10 gap-y-4 md:grid-cols-2">
      <InfoField
        v-for="field in fields"
        :key="`${title}-${field.label}`"
        :label="field.label"
        :value="field.value"
        :full="field.full"
      />
    </dl>
  </section>
</template>

<script setup>
import InfoField from './InfoField.vue';

defineProps({
  title: {
    type: String,
    required: true,
  },
  fields: {
    type: Array,
    default: () => [],
  },
});
</script>
