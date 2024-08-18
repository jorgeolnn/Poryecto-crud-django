// carrito.js

document.addEventListener('DOMContentLoaded', function() {
    const cart = {}; // Objeto para almacenar los productos en el carrito

    function updateCartUI() {
        const cartItemsContainer = document.getElementById('cart-items');
        const cartTotal = document.getElementById('cart-total');
        const cartContainer = document.getElementById('cart-container');
        const cartCount = document.getElementById('cart-count');
        
        cartItemsContainer.innerHTML = '';
        let totalItems = 0;
        let totalPrice = 0;

        for (const productId in cart) {
            if (cart.hasOwnProperty(productId)) {
                const product = cart[productId];
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    ${product.name} - $${product.price} x ${product.quantity}
                    <button class="btn btn-danger btn-sm remove-from-cart" data-product-id="${productId}">Eliminar</button>
                `;
                cartItemsContainer.appendChild(listItem);
                totalItems += product.quantity;
                totalPrice += product.price * product.quantity;
            }
        }

        if (totalItems === 0) {
            cartItemsContainer.innerHTML = '<li>El carrito está vacío.</li>';
            cartContainer.style.display = 'none'; // Oculta el contenedor si el carrito está vacío
        } else {
            cartContainer.style.display = 'block'; // Muestra el contenedor si hay productos en el carrito
        }

        cartTotal.textContent = `Total: $${totalPrice.toFixed(2)}`;
        cartCount.textContent = totalItems; // Actualiza el contador en la barra de navegación
    }

    function addToCart(productId, name, price) {
        if (cart[productId]) {
            cart[productId].quantity += 1;
        } else {
            cart[productId] = { id: productId, name: name, price: price, quantity: 1 };
        }
        updateCartUI();
    }

    function removeFromCart(productId) {
        if (cart[productId]) {
            if (cart[productId].quantity > 1) {
                cart[productId].quantity -= 1;
            } else {
                delete cart[productId];
            }
            updateCartUI();
        }
    }

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const productPrice = parseFloat(this.getAttribute('data-product-price'));
            addToCart(productId, productName, productPrice);
        });
    });

    document.getElementById('cart-items').addEventListener('click', function(event) {
        if (event.target.classList.contains('remove-from-cart')) {
            const productId = event.target.getAttribute('data-product-id');
            removeFromCart(productId);
        }
    });

    document.getElementById('checkout').addEventListener('click', function() {
        window.location.href = '/checkout/';  // Asegúrate de que esta URL apunte a tu vista de checkout
    });
});
