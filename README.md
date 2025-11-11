🕹️ pythonJuego2D
Juego 2D modular desarrollado en Python con arquitectura ECS usando  y . Validado localmente y en CI/CD con pytest y , asegurando trazabilidad, reproducibilidad y defensa técnica para entrevistas y portfolio.

🚀 Características
- 🧩 Arquitectura Entity-Component-System (ECS) con esper
- 🎮 Renderizado en tiempo real con pygame
- ✅ Validación automatizada con pytest
- 🔁 Integración continua con GitHub Actions
- 🐳 Validación local con act (simulación de CI/CD en Docker)
- 🧪 Modo CI automático: ejecución controlada sin entorno gráfico
- ⌨️ Controles con teclado (WASD / flechas) para movimiento del jugador
- 📄 Documentación modular para defensa técnica

📦 Requisitos
- Python 3.13+
- Docker (para usar act)
- Instalar dependencias:
    pip install -r requirements.txt
    esper==2.3
    pygame==2.6.1
    pytest

🧪 Validación en CI/CD
Este proyecto incluye un workflow de GitHub Actions que:
- Instala dependencias
- Ejecuta el juego en modo CI (CI=true)
- Corre pruebas con pytest
- Realiza commit automático si hay cambios
