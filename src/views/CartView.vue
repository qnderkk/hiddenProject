<template>
  <div class="cart-container">
    <h1>Ваша корзина</h1>

    <div v-if="cart.items.length === 0" class="empty-cart">
      <p>В корзине пока ничего нет :(</p>
      <router-link to="/products" class="btn">Перейти в каталог</router-link>
    </div>

    <div v-else class="cart-content">
      <div class="cart-items">
        <div v-for="(item, index) in cart.items" :key="item.cartId" class="cart-item">
          <img :src="item.image" :alt="item.name" class="item-img">
          <div class="item-info">
            <h3>{{ item.name }}</h3>
            <p>{{ item.price }} ₽</p>
          </div>
          <i class='bx bx-trash' @click="cart.removeFromCart(item.cartId)"></i>
        </div>
      </div>

      <div class="cart-summary">
        <h3>Итого:</h3>
        <p class="total-price">{{ cart.totalPrice }} ₽</p>
        <button class="btn" @click="checkout">Оформить заказ</button>
        <button class="btn btn-clear" @click="cart.clearCart">Очистить корзину</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

const checkout = () => {
  alert('Заказ оформлен! (Тут будет логика отправки на бэкенд)')
}
</script>

<style scoped>
.cart-container { margin: 120px auto; max-width: 900px; padding: 20px; text-align: center; }
.cart-container h1 { margin-bottom: 30px; color: var(--main-color); }

.cart-content { display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }

.cart-item {
  display: flex; align-items: center; justify-content: space-between;
  padding: 15px; border-bottom: 1px solid #ddd; background: #fff;
  margin-bottom: 10px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
}

.item-img { width: 80px; height: 80px; object-fit: cover; border-radius: 5px; }

.item-info { flex: 1; text-align: left; margin-left: 20px; }

.bx-trash { font-size: 24px; color: #ff4d4d; cursor: pointer; transition: 0.3s; }
.bx-trash:hover { transform: scale(1.2); }

.cart-summary {
  background: #f9f9f9; padding: 20px; border-radius: 8px;
  height: fit-content; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.total-price { font-size: 24px; font-weight: bold; color: var(--main-color); margin: 15px 0; }

.btn {
  display: block; width: 100%; padding: 12px; background: var(--main-color);
  color: white; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 10px;
}

.btn-clear { background: #999; }

@media (max-width: 768px) {
  .cart-content { grid-template-columns: 1fr; }
}
</style>