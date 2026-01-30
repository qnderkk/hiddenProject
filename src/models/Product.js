export class Product {
    constructor(id, name, price, image, rating, category = 'standard') {
        this.id = id;
        this.name = name;
        this.price = price;
        this.image = image;
        this.rating = rating;
        this.category = category;
    }

    getStarClass(index) {
        if (index <= Math.floor(this.rating)) return 'bx bxs-star';
        if (index === Math.ceil(this.rating) && this.rating % 1 !== 0) return 'bx bxs-star-half';
        return 'bx bx-star';
    }

    isNewArrival() {
        return this.category === 'new';
    }

    get formattedPrice() {
        return typeof this.price === 'number'
            ? this.price.toLocaleString() + '₽'
            : this.price;
    }
}