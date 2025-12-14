/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";

class CR7Notification extends Component {
    setup() {
        this.env.services.bus_service.addChannel("cr7_siuuu");
        this.env.services.bus_service.addEventListener("notification", this._onNotification.bind(this));
    }

    _onNotification({ detail: notifications }) {
        for (const { payload, type } of notifications) {
            if (type === "cr7_celebration") {
                this.showCR7Popup(payload);
            }
        }
    }

    showCR7Popup(data) {
        // Crear overlay oscuro
        const overlay = document.createElement('div');
        overlay.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 9999;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            animation: fadeIn 0.3s;
        `;

        // Contenedor principal
        const container = document.createElement('div');
        container.style.cssText = `
            text-align: center;
            animation: zoomIn 0.5s;
        `;

        // Imagen de CR7
        const img = document.createElement('img');
        img.src = 'https://media.tenor.com/kIsxxeru_z0AAAAM/cristiano-ronaldo-siuu.gif';
        img.style.cssText = `
            max-width: 600px;
            max-height: 400px;
            border-radius: 20px;
            box-shadow: 0 0 50px rgba(255, 215, 0, 0.8);
            margin-bottom: 30px;
        `;

        // Texto
        const text = document.createElement('h1');
        text.innerHTML = data.message;
        text.style.cssText = `
            color: #FFD700;
            font-size: 48px;
            font-weight: bold;
            text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.8);
            margin: 20px;
            font-family: Arial, sans-serif;
            animation: pulse 1s infinite;
        `;

        // Orden
        const orderText = document.createElement('h2');
        orderText.innerHTML = `Pedido: ${data.order_name}`;
        orderText.style.cssText = `
            color: white;
            font-size: 32px;
            margin: 10px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.8);
        `;

        // Botón cerrar
        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '✖ Cerrar';
        closeBtn.style.cssText = `
            margin-top: 30px;
            padding: 15px 40px;
            font-size: 20px;
            background: #FFD700;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.3s;
        `;
        closeBtn.onmouseover = () => closeBtn.style.transform = 'scale(1.1)';
        closeBtn.onmouseout = () => closeBtn.style.transform = 'scale(1)';
        closeBtn.onclick = () => overlay.remove();

        // Agregar estilos CSS
        const style = document.createElement('style');
        style.innerHTML = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes zoomIn {
                from { transform: scale(0); }
                to { transform: scale(1); }
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.1); }
            }
        `;
        document.head.appendChild(style);

        // Montar todo
        container.appendChild(img);
        container.appendChild(text);
        container.appendChild(orderText);
        container.appendChild(closeBtn);
        overlay.appendChild(container);
        document.body.appendChild(overlay);

        // Auto-cerrar después de 8 segundos
        setTimeout(() => overlay.remove(), 8000);

        // Reproducir sonido (opcional)
        const audio = new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSmJ1O/TgjMGHWm98dyfSg0PU6vm7bJiGwk3ktTvzX0qBSh+zO3akTsKElyx6OyrWBQLSKXh8L1lHAUqi9Ps1YU1BxpmvO/cp0sMEFSr5uy0YBoJOJPU7s1+KgYof8zs25A6CxFcsei9VhMHSKXh8r5tIAUpidPu1YU1Bxpm');
        audio.play().catch(() => {});
    }
}

CR7Notification.template = "cr7.Notification";

export const cr7NotificationService = {
    start() {
        return new CR7Notification();
    },
};

registry.category("services").add("cr7NotificationService", cr7NotificationService);
