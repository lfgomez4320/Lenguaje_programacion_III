# VideoStream API 🎥

> Sistema moderno de gestión de contenido multimedia desarrollado con Flask

## 🚀 Características

- **API RESTful completa** con operaciones CRUD
- **Arquitectura modular** y escalable
- **Base de datos SQLite** con ORM SQLAlchemy
- **Logging integrado** para monitoreo
- **Paginación y filtros** avanzados
- **Métricas de engagement** automáticas
- **Soft delete** para preservar datos
- **CORS habilitado** para frontend

## 📁 Estructura del Proyecto

```
videostream-api/
├── app.py                    # Aplicación principal con factory pattern
├── config.py                 # Configuraciones por ambiente
├── database.py               # Configuración de base de datos
├── models/
│   └── multimedia.py         # Modelo de contenido multimedia
├── api/
│   └── endpoints.py          # Endpoints de la API REST
├── requirements.txt          # Dependencias
└── README.md                # Documentación
```

## 🛠️ Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone <tu-repo>
   cd videostream-api
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate   # Windows
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

La API estará disponible en `http://localhost:5000`

## 📚 Documentación de la API

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/videos` | Listar videos con paginación |
| `POST` | `/api/v1/videos` | Crear nuevo video |
| `GET` | `/api/v1/videos/{id}` | Obtener video específico |
| `PUT` | `/api/v1/videos/{id}` | Crear/actualizar video |
| `PATCH` | `/api/v1/videos/{id}` | Actualización parcial |
| `DELETE` | `/api/v1/videos/{id}` | Eliminar video (soft delete) |

### Ejemplos de Uso

#### Crear un video
```bash
curl -X POST http://localhost:5000/api/v1/videos \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Tutorial de Python Avanzado",
    "description": "Aprende conceptos avanzados de Python",
    "duration_seconds": 1800,
    "resolution": "1920x1080"
  }'
```

#### Obtener videos con filtros
```bash
# Buscar videos
curl "http://localhost:5000/api/v1/videos?search=python&page=1&per_page=5"

# Videos trending
curl "http://localhost:5000/api/v1/videos?trending=true"
```

#### Actualizar métricas
```bash
curl -X PATCH http://localhost:5000/api/v1/videos/1 \
  -H "Content-Type: application/json" \
  -d '{"like_count": 150, "view_count": 2500}'
```

## 🎯 Características Avanzadas

### Métricas de Engagement
- **Ratio de engagement**: Cálculo automático de likes vs interacciones totales
- **Trending**: Ordenamiento por popularidad
- **Contador de vistas**: Incremento automático al consultar

### Filtros y Búsqueda
- Búsqueda por título
- Paginación configurable
- Ordenamiento por fecha o popularidad

### Logging y Monitoreo
- Logs estructurados con timestamps
- Tracking de operaciones importantes
- Manejo de errores centralizado

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# .env
SECRET_KEY=tu-clave-secreta
DATABASE_URL=sqlite:///videostream.db
FLASK_ENV=development
```

### Configuraciones por Ambiente
- **Development**: Debug habilitado, logging verbose
- **Production**: Optimizado para rendimiento
- **Testing**: Base de datos en memoria

## 🧪 Testing

```bash
# Ejecutar tests (cuando se implementen)
python -m pytest tests/
```

## 📈 Roadmap

- [ ] Autenticación JWT
- [ ] Sistema de categorías
- [ ] Upload de archivos
- [ ] Cache con Redis
- [ ] Documentación Swagger
- [ ] Tests unitarios
- [ ] Docker containerization

## 👨‍💻 Desarrollado por

**Luis Felipe Gomez** - Estudiante de Programación  
Universidad: Universidad Cooperativa Remington  
Curso: Laboratorio de Programación 3

---

*VideoStream API - Transformando la gestión de contenido multimedia* 🎬
