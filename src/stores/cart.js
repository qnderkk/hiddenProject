import { defineStore } from 'pinia'

export const useCartStore = defineStore('cart', {
  state: () => ({
    // Загружаем из localStorage, если там что-то есть, иначе пустой массив
    items: JSON.parse(localStorage.getItem('cart')) || []
  }),
  getters: {
    // Считаем общее кол-во товаров
    totalCount: (state) => state.items.length,
    // Считаем общую сумму (предположим, у товара есть поле price)
    totalPrice: (state) => state.items.reduce((sum, item) => sum + item.price, 0)
  },
  actions: {
    addToCart(product) {
      this.items.push({ ...product, cartId: Date.now() }) // Добавляем уникальный ключ
      this.save()
    },
    removeFromCart(cartId) {
      this.items = this.items.filter(item => item.cartId !== cartId)
      this.save()
    },
    clearCart() {
      this.items = []
      this.save()
    },
    save() {
      localStorage.setItem('cart', JSON.stringify(this.items))
    }
  }
})