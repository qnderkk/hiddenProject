import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    // Синхронизация с localStorage
    items: JSON.parse(localStorage.getItem('cart')) || []
  }),
  getters: {
    // Считает количество товаров для кружка над корзиной
    totalCount: (state) => state.items.length,
    // Считает итоговую сумму всех товаров
    totalPrice: (state) => state.items.reduce((sum, item) => sum + Number(item.price), 0)
  },
  actions: {
    addToCart(product) {
      // Добавляем cartId, чтобы можно было удалить конкретный экземпляр товара
      this.items.push({ ...product, cartId: Date.now() + Math.random() })
      this.save()
    },
    removeFromCart(cartId) {
      this.items = this.items.filter(item => item.cartId !== cartId)
      this.save()
    },
    save() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    },
    // Внутри actions: { ... }
    clearCart() {
      this.items = []; // Очищаем массив в памяти
      this.save();     // Сохраняем пустой массив в localStorage
    }
  }
})