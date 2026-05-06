<template>
  <section class="bg-white py-12">
    <div class="container mx-auto px-6">
      <div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
        <!-- Resumo do Pedido -->
        <div class="lg:col-span-2">
          <div class="rounded-2xl border border-slate-400 p-8">
            <h2 class="mb-6 text-2xl font-black text-slate-900">Resumo do Pedido</h2>

            <!-- Itens do Pedido -->
            <div class="space-y-6">
              <div
                v-for="item in orderItems"
                :key="item.id"
                class="flex gap-4 border-b border-slate-100 pb-6 last:border-0"
              >
                <img :src="item.image" :alt="item.name" class="h-20 w-20 rounded-lg object-cover" />
                <div class="flex-1">
                  <h3 class="font-black text-slate-900">{{ item.name }}</h3>
                  <div class="text-sm text-slate-600">Produtor: {{ item.producer }}</div>
                  <div class="mt-2 flex items-center gap-4 text-xs text-slate-600">
                    <span class="h-4 w-4 rounded bg-slate-200"></span>
                    <span>{{ item.quantity }} kg</span>
                    <span class="h-4 w-4 rounded bg-slate-200"></span>
                    <span>R$ {{ item.pricePerKg.toFixed(2) }}</span>
                    <span class="h-4 w-4 rounded bg-slate-200"></span>
                    <span>{{ item.distance }} km</span>
                    <span v-if="item.inStock" class="inline-flex items-center gap-1 text-green-600">
                      <div class="h-4 w-4 rounded bg-green-200"></div>
                      Pronta Entrega
                    </span>
                  </div>
                </div>
                <div class="text-right">
                  <p class="font-black text-slate-900">R$ {{ item.total.toFixed(2) }}</p>
                </div>
              </div>
            </div>

            <!-- Informações dos Produtores -->
            <div class="mt-8 border-t border-slate-100 pt-6">
              <h3 class="mb-4 font-black text-slate-900">Informações dos Produtores</h3>
              <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <div
                  v-for="producer in producers"
                  :key="producer.id"
                  class="rounded-xl border border-slate-400 p-4"
                >
                  <p class="font-black text-slate-900">{{ producer.name }}</p>
                  <div class="mt-2 flex items-center gap-2 text-sm text-slate-600">
                    <div class="h-4 w-4 rounded bg-slate-200"></div>
                    {{ producer.location }}
                  </div>
                  <div
                    v-if="producer.trusted"
                    class="mt-2 inline-flex items-center gap-1 rounded-full bg-green-100 px-3 py-1 text-xs font-semibold text-green-700"
                  >
                    <div class="h-3 w-3 rounded bg-green-300"></div>
                    Alta Confiabilidade
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Resumo de Valores -->
        <div>
          <div class="sticky top-24 rounded-2xl border border-slate-400 p-8">
            <h2 class="mb-6 text-2xl font-black text-slate-900">Resumo de Valores</h2>

            <div class="space-y-4">
              <div class="flex justify-between text-slate-600">
                <span>Subtotal em Produtos</span>
                <span class="font-semibold">R$ {{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-slate-600">
                <span class="flex items-center gap-2">
                  Taxa da Plataforma
                  <div class="h-4 w-4 rounded bg-slate-200"></div>
                </span>
                <span class="font-semibold">R$ {{ platformFee.toFixed(2) }}</span>
              </div>
              <div class="border-t border-slate-100 pt-4">
                <div class="flex justify-between">
                  <span class="text-lg font-black text-slate-900">Total</span>
                  <span class="text-2xl font-black text-green-600">R$ {{ total.toFixed(2) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue';

const orderItems = [
  {
    id: 1,
    name: 'Tomate Carmem',
    producer: 'Sítio Novo',
    image: `https://picsum.photos/80/80?random=${Math.random()}`,
    quantity: 150,
    pricePerKg: 3.5,
    distance: 45,
    inStock: true,
    get total() {
      return this.quantity * this.pricePerKg;
    },
  },
  {
    id: 2,
    name: 'Alface Crespa',
    producer: 'Sítio Verde Vale',
    image: `https://picsum.photos/80/80?random=${Math.random()}`,
    quantity: 50,
    pricePerKg: 2.0,
    distance: 20,
    inStock: true,
    get total() {
      return this.quantity * this.pricePerKg;
    },
  },
];

const producers = [
  {
    id: 2,
    name: 'Sítio Verde Vale',
    location: 'Ibiúna - SP (20 km)',
    trusted: true,
  },
];

const subtotal = computed(() =>
  orderItems.reduce((sum, item) => sum + item.quantity * item.pricePerKg, 0),
);
const platformFee = computed(() => subtotal.value * 0.05);
const total = computed(() => subtotal.value + platformFee.value);
</script>

<style scoped></style>
