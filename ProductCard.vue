<template>
  <div class="box">
    <div class="box-img">
      <img :src="getImageUrl(product.image)" :alt="product.title" @error="handleImageError">
    </div>
    <div class="title-price">
      <h3>{{ product.title || 'Gray Chair' }}</h3>
      <div class="stars">
        <i class='bx bxs-star'></i>
        <i class='bx bxs-star'></i>
        <i class='bx bxs-star'></i>
        <i class='bx bxs-star'></i>
        <i class='bx bxs-star-half'></i>
      </div>
    </div>
    <span>${{ product.price || 46 }}</span>
    <i class='bx bx-cart' @click="addToCart" ref="cartIcon"></i>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'

const props = defineProps({
  product: {
    type: Object,
    required: true,
    default: () => ({
      id: Date.now(),
      title: 'Gray Chair',
      price: 46,
      image: 'img/new1.jpg'
    })
  }
})

const cartStore = useCartStore()
const cartIcon = ref(null)

const getImageUrl = (path) => {
  if (!path) return '/img/new1.jpg'
  if (path.startsWith('http') || path.startsWith('/')) {
    return path
  }
  return `/${path}`
}

const handleImageError = (event) => {
  console.error('Image failed to load:', props.product.image)
  event.target.src = '/img/new1.jpg'
}
const addToCart = () => {
  cartStore.addItem({
    id: props.product.id || Date.now(),
    title: props.product.title || 'Gray Chair',
    price: Number(props.product.price) || 46,
    image: getImageUrl(props.product.image),
    quantity: 1
  })

  cartStore.toggleCartModal()

  if (cartIcon.value) {
    cartIcon.value.style.transform = 'scale(1.3)'
    setTimeout(() => {
      cartIcon.value.style.transform = 'scale(1)'
    }, 300)
  }
}
</script>

<style scoped>
.bx-cart {
  cursor: pointer;
  transition: transform 0.3s ease;
}
</style>