# KEV Dashboard (Dash + Railway)

Este dashboard web interactivo muestra las vulnerabilidades activamente explotadas del catálogo KEV (CISA) en los últimos 7 días. Desarrollado con **Plotly Dash** y preparado para despliegue en **Railway**.

## 🚀 Despliegue rápido en Railway

1. Crea un nuevo repositorio en GitHub y sube estos archivos.
2. Ve a [https://railway.app](https://railway.app) e inicia sesión con GitHub.
3. Haz clic en "New Project" > "Deploy from GitHub Repo".
4. Selecciona tu repositorio con este proyecto.
5. Railway detectará automáticamente el `Procfile` y desplegará la app.

## 📁 Estructura

- `kev_dashboard_generator.py` – script principal de Dash.
- `requirements.txt` – dependencias necesarias.
- `Procfile` – define el comando de ejecución para entornos PaaS.

## 📊 Funcionalidades

- Filtros dinámicos por proveedor y producto.
- Tabla interactiva de vulnerabilidades.
- Gráficos por proveedor y por fecha de inclusión.
