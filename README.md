# 🕹️ pythonJuego2D

Un juego 2D modular desarrollado en Python con arquitectura ECS usando [esper](https://github.com/benmoran56/esper) y [pygame](https://www.pygame.org/). Validado localmente y en CI/CD con `pytest` y [act](https://github.com/nektos/act) para asegurar trazabilidad, reproducibilidad y defensa técnica.


## 🚀 Características

- Arquitectura basada en **Entity-Component-System (ECS)** con `esper`
- Renderizado en tiempo real con `pygame`
- Validación automatizada con `pytest`
- Compatible con **GitHub Actions** y validación local con `act`
- Preparado para entornos CI/CD sin entorno gráfico


## 📦 Requisitos

- Python 3.13+
- Docker (para usar `act`)
- `pip install -r requirements.txt`

```txt
esper==2.3
pygame==2.6.1
pytest