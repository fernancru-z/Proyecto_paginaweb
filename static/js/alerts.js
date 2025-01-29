document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    fetch('/login', {
        method: 'POST',
        body: new URLSearchParams(new FormData(this))
    }).then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/';
        } else {
            alert(data.message);
        }
    });
});

// ocupando sweet alert
function mostrarAlerta(mensajes) {
    mensajes.forEach(([categoria, mensaje]) => {
        if (categoria === 'success') {
            Swal.fire({
                icon: 'success',
                title: '¡Éxito!',
                text: mensaje,
                confirmButtonText: 'OK'
            }).then(() => {
                // Redirigir a la página de login después de mostrar la alerta
                window.location.href = "/login";
            });
        } else if (categoria === 'error') {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: mensaje,
                confirmButtonText: 'OK'
            });
        }
    });
}