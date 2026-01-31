import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/Home.vue'
import ProductsPage from '../components/Products.vue'
import AccountPage from '../components/PersonalAccount.vue'
import CartPage from '../views/CartView.vue' // Добавь этот импорт

const routes = [
    { path: '/', name: 'Home', component: HomePage },
    { path: '/products', name: 'Products', component: ProductsPage },
    { path: '/account', name: 'Account', component: AccountPage },
    { path: '/cart', name: 'Cart', component: CartPage } // Добавь этот маршрут
]

const router = createRouter({
    history: createWebHistory(),
    routes,
    scrollBehavior(to) {
        if (to.hash) return { el: to.hash, behavior: 'smooth' }
        return { top: 0 }
    }
})

export default router