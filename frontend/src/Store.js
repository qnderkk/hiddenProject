import { ref, computed } from 'vue'

const cartItems = ref([])
const isCartOpen = ref(false)

export const useCart = () => {
    const totalPrice = computed(() =>
        cartItems.value.reduce((sum, item) => sum + item.price, 0)
    )

    const addToCart = (product) => {
        cartItems.value.push(product)
        isCartOpen.value = true
    }

    const removeFromCart = (index) => {
        cartItems.value.splice(index, 1)
    }

    return {
        cartItems,
        isCartOpen,
        totalPrice,
        addToCart,
        removeFromCart
    }
}