<template>
  <div class="box">
    <div class="box-img">
      <img :src="product.image" :alt="product.name">
      <span v-if="product.isNewArrival()" class="badge-new">New</span>
    </div>
    <div class="title-price">
      <h3>{{ product.name }}</h3>
      <div class="stars">
        <i v-for="i in 5" :key="i" :class="product.getStarClass(i)"></i>
      </div>
    </div>
    <span>{{ product.formattedPrice }}</span>
    <i class='bx bx-cart' @click="emitAdd"></i>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'
// props.product теперь ожидается как экземпляр класса Product
const props = defineProps(['product'])
const emit = defineEmits(['add-to-cart'])

const emitAdd = () => {
  emit('add-to-cart', props.product)
}
</script>

<style scoped>
.badge-new {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--main-color);
  color: white;
  padding: 4px 10px;
  border-radius: 4px;
  font-size: 0.8rem;
}
.box { position: relative; }
</style>