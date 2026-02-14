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
import { useRouter } from 'vue-router'

const cart = useCartStore()
const router = useRouter()

const checkout = async () => {
  if (cart.items.length === 0) return

  // 1. Спрашиваем адрес (временно через prompt)
  const address = prompt("Введите адрес доставки:", "ул. Пушкина, д. Колотушкина")
  if (!address) return

  // 2. Группируем товары по ID для бэкенда (считаем количество)
  const groupedItems = cart.items.reduce((acc, item) => {
    const found = acc.find(i => i.product_id === item.id)
    if (found) {
      found.quantity += 1
    } else {
      acc.push({ product_id: item.id, quantity: 1 })
    }
    return acc
  }, [])

  // 3. Формируем объект заказа по твоей схеме OrderCreate
  const orderPayload = {
    delivery_address: address,
    items: groupedItems
  }

  try {
    const response = await fetch('http://127.0.0.1:8000/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'Authorization': `Bearer ${localStorage.getItem('token')}` // если будет токен
      },
      body: JSON.stringify(orderPayload)
    })

    if (response.ok) {
      const result = await response.json()
      alert(`Заказ №${result.id} успешно оформлен!`)
      cart.clearCart() // Очищаем корзину после успеха
      router.push('/products') // Уводим пользователя на каталог
    } else {
      const error = await response.json()
      alert("Ошибка при оформлении: " + (error.detail || "Неизвестная ошибка"))
    }
  } catch (err) {
    console.error(err)
    //alert("Сервер бэкенда недоступен")
  }
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