  /* When the user clicks on the button,
  toggle between hiding and showing the dropdown content */
 // Esta función se llama cuando el usuario hace clic en el botón para mostrar u ocultar el menú desplegable
 function myFunction() {
    // Obtener el menú desplegable por su ID
    const dropdownMenu = document.getElementById("myDropdown");
    // Alternar la clase "show" para mostrar u ocultar el menú
    dropdownMenu.classList.toggle("show");
}

// Esta función se llama cuando el usuario escribe en el campo de búsqueda
function filterFunction() {
    // Obtener el texto ingresado por el usuario en el campo de búsqueda
    const inputField = document.getElementById("myInput");
    // Convertir el texto a mayúsculas para que la comparación sea insensible a mayúsculas/minúsculas
    const filterText = inputField.value.toUpperCase();
    // Obtener el menú desplegable por su ID
    const dropdownMenu = document.getElementById("myDropdown");
    // Obtener todos los enlaces dentro del menú desplegable
    const links = dropdownMenu.getElementsByTagName("a");

    // Iterar sobre cada enlace para aplicar el filtro
    for (let i = 0; i < links.length; i++) {
        // Obtener el texto del enlace actual
        const linkText = links[i].textContent || links[i].innerText;
        // Comprobar si el texto del enlace incluye el texto de búsqueda
        if (linkText.toUpperCase().indexOf(filterText) > -1) {
            // Si hay una coincidencia, mostrar el enlace
            links[i].style.display = ""; // Mostrar el enlace
        } else {
            // Si no hay coincidencia, ocultar el enlace
            links[i].style.display = "none"; // Ocultar el enlace
        }
    }
}

document.querySelectorAll('.precio').forEach(function(element) {
    // Obtén el texto y elimina el símbolo de dólar
    const precioTexto = element.textContent.replace('$', '').replace('.', '').replace(',', '.');
    const precio = parseFloat(precioTexto); // Convierte a float
    
    // Aplica formato con puntos como separador de miles
    if (!isNaN(precio)) { // Verifica que el valor sea un número
        element.textContent = '$' + precio.toLocaleString('es-ES');
    } else {
        element.textContent = '$0'; // Maneja caso de error o precio no válido
    }
});
