function formatonumero2(numero) {
    let formattedNumber = new Intl.NumberFormat("es-CL").format(numero);
    return formattedNumber.replace(",", ".");
}

document.addEventListener('DOMContentLoaded', function() {
    // Cargar el carrito desde localStorage
    const cart = JSON.parse(localStorage.getItem('cart')) || {}; 

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
                const formattedPrice = formatonumero2(product.price);
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    ${product.name} - $${formattedPrice} x ${product.quantity}
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
    
        const formattedTotalPrice = formatonumero2(totalPrice);
        cartTotal.textContent = `Total: $${formattedTotalPrice}`;
        cartCount.textContent = totalItems; // Actualiza el contador en la barra de navegación
    
        // Actualiza el estado de los botones de agregar al carrito
        updateAddToCartButtons();
    }

    function saveCartToLocalStorage() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function updateAddToCartButtons() {
        document.querySelectorAll('.add-to-cart').forEach(button => {
            const productId = button.getAttribute('data-product-id');
            const productStock = parseInt(button.getAttribute('data-product-stock'));
            const productInCart = cart[productId];
            
            if (productStock <= 0) {
                button.disabled = true; // Desactiva el botón si no hay stock
                button.textContent = `Sin stock`;
            } else if (productInCart) {
                if (productInCart.quantity >= productStock) {
                    button.disabled = true; // Desactiva el botón si el carrito tiene el stock completo
                    button.textContent = `Límite alcanzado (${productStock})`;
                } else {
                    button.disabled = false; // Activa el botón si el stock no está completo
                    button.textContent = `Añadir al carrito (${productStock - productInCart.quantity})`;
                }
            } else {
                button.disabled = false; // Activa el botón si no hay el producto en el carrito
                button.textContent = `Añadir al carrito (${productStock})`;
            }
        });
    }

    function addToCart(productId, name, price, stock) {
        if (stock <= 0) {
            alert('Este producto está fuera de stock.');
            return;
        }

        if (cart[productId]) {
            if (cart[productId].quantity < stock) {  // Verifica si la cantidad en el carrito es menor que el stock
                cart[productId].quantity += 1;
            } else {
                alert(`No puedes agregar más de ${stock} unidades de este producto.`);
            }
        } else {
            cart[productId] = { id: productId, name: name, price: price, quantity: 1, stock: stock };
        }
        updateCartUI();
        saveCartToLocalStorage(); // Guarda el carrito en localStorage
    }

    function removeFromCart(productId) {
        if (cart[productId]) {
            if (cart[productId].quantity > 1) {
                cart[productId].quantity -= 1;
            } else {
                delete cart[productId];
            }
            updateCartUI();
            saveCartToLocalStorage(); // Guarda el carrito en localStorage
        }
    }

    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productName = this.getAttribute('data-product-name');
            const productPrice = parseFloat(this.getAttribute('data-product-price'));
            const productStock = parseInt(this.getAttribute('data-product-stock'));

            // Agregar al carrito sólo si hay stock disponible
            addToCart(productId, productName, productPrice, productStock);
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

    // Inicializa el estado de los botones al cargar la página
    updateAddToCartButtons();
    updateCartUI();
});












