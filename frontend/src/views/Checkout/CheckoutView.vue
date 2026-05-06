<template>
  <div class="checkout-container min-h-screen bg-white">
    <CheckoutHeader />

    <!-- Main Content Grid -->
    <div class="bg-white py-12">
      <div class="container mx-auto px-6">
        <div class="grid grid-cols-1 gap-6 lg:grid-cols-3 lg:gap-8">
          <!-- LEFT COLUMN (65-70% width) -->
          <div class="space-y-6 lg:col-span-2">
            <CheckoutOrderSummary :items="checkout.items.value" />
            <CheckoutProducersInfo :producer="checkout.producer.value" />
            <CheckoutDelivery />
          </div>

          <!-- RIGHT COLUMN (30-35% width, sticky) -->
          <div class="lg:sticky lg:top-24 lg:h-fit">
            <div class="space-y-6">
              <CheckoutValuesSummary
                :subtotal="checkout.subtotal.value"
                :platform-fee="checkout.platformFee.value"
                :total="checkout.total.value"
              />
              <CheckoutPayment
                :selected-payment-id="checkout.selectedPaymentId.value"
                :pix="true"
                :boleto="true"
                :credit-card="true"
                :on-select-payment-method="checkout.selectPaymentMethod"
              />
              <CheckoutFooter />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCheckout } from '@/composables/useCheckout';
import CheckoutHeader from '@/components/checkout/CheckoutHeader.vue';
import CheckoutOrderSummary from '@/components/checkout/CheckoutOrderSummary.vue';
import CheckoutProducersInfo from '@/components/checkout/CheckoutProducersInfo.vue';
import CheckoutPayment from '@/components/checkout/CheckoutPayment.vue';
import CheckoutDelivery from '@/components/checkout/CheckoutDelivery.vue';
import CheckoutValuesSummary from '@/components/checkout/CheckoutValuesSummary.vue';
import CheckoutFooter from '@/components/checkout/CheckoutFooter.vue';

// Initialize checkout state
const checkout = useCheckout();
</script>

<style scoped></style>
