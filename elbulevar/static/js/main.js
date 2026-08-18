document.addEventListener('DOMContentLoaded', () => {
    // Control del Menú Responsive
    const menuToggle = document.getElementById('menuToggle');
    const navMenu = document.getElementById('navMenu');

    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Validación interactiva del lado del cliente para el formulario de contacto
    const formContacto = document.getElementById('formContacto');
    if (formContacto) {
        formContacto.addEventListener('submit', (e) => {
            const nombre = document.getElementById('nombre').value.trim();
            const email = document.getElementById('email').value.trim();
            const asunto = document.getElementById('asunto').value.trim();
            const mensaje = document.getElementById('mensaje').value.trim();

            if (!nombre || !email || !asunto || !mensaje) {
                e.preventDefault();
                alert('Por favor, complete todos los campos antes de enviar el formulario.');
                return;
            }

            if (nombre.length < 3) {
                e.preventDefault();
                alert('El nombre ingresado debe tener al menos 3 caracteres.');
                return;
            }

            const regexEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!regexEmail.test(email)) {
                e.preventDefault();
                alert('Por favor ingrese una dirección de correo electrónico válida.');
                return;
            }
        });
    }
});