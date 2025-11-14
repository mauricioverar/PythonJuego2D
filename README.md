# 🕹️ pythonJuego2D

**Juego 2D modular en Python** con arquitectura **Entity-Component-System (ECS)** usando `esper` y `pygame`. Validado localmente y en CI/CD con `pytest` y `act`, ideal para aprendizaje de diseño de software.


## 📚 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Ejecución del juego](#-ejecución-del-juego)
- [Controles](#-controles)
- [Validación CI/CD](#-validación-cicd)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Licencia](#-licencia)


## 🚀 Características

- 🧩 Arquitectura ECS con [esper](https://github.com/benmoran56/esper)
- 🎮 Renderizado en tiempo real con [pygame](https://www.pygame.org/)
- ✅ Validación automatizada con [pytest](https://docs.pytest.org/)
- 🔁 Integración continua con [GitHub Actions](https://docs.github.com/en/actions)
- 🐳 Validación local con [act](https://github.com/nektos/act)
- 🧪 Modo CI automático: ejecución controlada sin entorno gráfico (`CI=true`)
- ⌨️ Controles con teclado (WASD / flechas)
- 📄 Documentación modular para defensa técnica


## 📦 Requisitos

- Python 3.13+
- Docker (para usar `act`)
- Dependencias:

```bash
pip install -r requirements.txt
```


## ▶️ Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/mauricioverar/pythonJuego2D.git
   cd pythonJuego2D
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv env
   source env/bin/activate  # o .\env\Scripts\activate en Windows
   ```

3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```


## 🎮 Ejecución del juego

```bash
python src/main.py
```

Para modo CI/CD (sin entorno gráfico):

```bash
CI=true python src/main.py
```


## ⌨️ Controles

- `W` / `↑`: Mover arriba  
- `A` / `←`: Mover izquierda  
- `S` / `↓`: Mover abajo  
- `D` / `→`: Mover derecha  
- `Espacio` o `Enter`: Revelar celda


## 🧪 Validación CI/CD

El workflow de GitHub Actions:

- Instala dependencias
- Ejecuta el juego en modo CI (`CI=true`)
- Corre pruebas con `pytest`
- Realiza commit automático si hay cambios

Para simular localmente:

```bash
act push
```


## 🗂️ Estructura del proyecto

```
pythonJuego2D/
├── assets/             # Recursos gráficos y de sonido
├── src/                # Código fuente del juego
│   ├── main.py         # Punto de entrada
│   ├── components.py   # Componentes ECS
│   ├── systems.py      # Sistemas ECS
│   ├── input.py        # Manejo de entrada
│   ├── config.py       # Configuración global
│   ├── grid.py         # Lógica de tablero
│   └── test_main.py    # Pruebas automatizadas
├── requirements.txt    # Dependencias
├── README.md           # Documentación (este archivo)
└── .github/workflows/  # Workflows de CI/CD
```


## 📄 Licencia

MIT License. Libre para usar, modificar y compartir con atribución.
