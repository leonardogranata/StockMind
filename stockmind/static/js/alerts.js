document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('django-messages');

    if (!container) {
        console.log("Nenhum container de mensagens encontrado.");
        return;
    }

    try {
        const messages = JSON.parse(container.textContent);
        console.log("Mensagens recebidas:", messages);

        messages.forEach(msg => {
            Swal.fire({
                icon: msg.tags.includes('error') ? 'error' : 'success',
                title: msg.message,
                showConfirmButton: false,
                timer: 3000,
                background: '#23272A',   
                color: '#f5f5f5',        
                customClass: {
                    popup: 'swal2-custom-popup'
                }
            });
        });
    } catch (e) {
        console.error("Erro ao ler mensagens do Django:", e);
    }
});
