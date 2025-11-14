# Eventia Core API

Sistema de gestión de eventos que permite administrar eventos, participantes y registros de asistencia mediante una API REST.

## Tabla de Contenidos

- [Arquitectura](#arquitectura)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Ejecución Local](#ejecución-local)
- [Ejecución de Pruebas](#ejecución-de-pruebas)
- [Pipeline CI/CD](#pipeline-cicd)
- [Endpoints de la API](#endpoints-de-la-api)
- [Justificación Tecnológica](#justificación-tecnológica)

## Arquitectura

El proyecto implementa una **arquitectura de capas** (Layered Architecture) que separa las responsabilidades en distintos niveles:

### Capas del Sistema
```
┌─────────────────────────────────────┐
│   Capa de Presentación (Views)     │  ← API REST
├─────────────────────────────────────┤
│   Capa de Lógica (Services)        │  ← Reglas de negocio
├─────────────────────────────────────┤
│   Capa de Acceso a Datos (Repos)   │  ← Gestión de BD y Caché
├─────────────────────────────────────┤
│   Capa de Datos (Models)           │  ← ORM Django
└─────────────────────────────────────┘
```

#### 1. Capa de Presentación (Views)
- Maneja las peticiones HTTP
- Valida datos de entrada mediante serializers
- Retorna respuestas JSON con códigos HTTP apropiados
- **Ubicación:** `events/views/`

#### 2. Capa de Lógica de Negocio (Services)
- Implementa las reglas del negocio:
  - Validación de cupos de eventos
  - Prevención de registros duplicados
  - Generación de estadísticas
- Desacoplada de HTTP y base de datos
- **Ubicación:** `events/services/`

#### 3. Capa de Acceso a Datos (Repositories)
- Abstrae operaciones de base de datos
- Implementa sistema de caché con Redis
- Gestiona invalidación de caché
- **Ubicación:** `events/repositories/`

#### 4. Capa de Datos (Models)
- Define estructura de datos
- Utiliza ORM de Django
- **Ubicación:** `events/models/`

## Requisitos

### Software Necesario
- Python 3.11+
- Docker y Docker Compose
- Git

### Dependencias Python
Ver `requirements.txt`:
- Django 5.0.1
- Django REST Framework 3.14.0
- MySQL Client 2.2.1
- Redis 5.0.1
- Django Redis 5.4.0
- pytest 7.4.4
- bandit 1.7.6

## Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd eventia
```

### 2. Crear entorno virtual
```bash
python -m venv .venv
```

**Windows:**
```bash
.venv\Scripts\activate
```

**Linux/Mac:**
```bash
source .venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crear archivo `.env` en la raíz:
```env
SECRET_KEY=django-insecure-wsb#k)(*rcipn$s$i+p*2$r9^rk-u+j7o_bmvp6u84(v6#%zqt
DEBUG=True
ALLOWED_HOSTS=*

DB_NAME=eventia_db
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3307

REDIS_URL=redis://127.0.0.1:6379/1
```

### 5. Levantar servicios con Docker
```bash
docker compose up -d
```

Esto iniciará:
- MySQL en puerto 3307
- Redis en puerto 6379

### 6. Ejecutar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear superusuario (opcional)
```bash
python manage.py createsuperuser
```

## Ejecución Local

### Iniciar servidor de desarrollo
```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/api/`

### Panel de administración
Acceder a: `http://localhost:8000/admin/`

## Ejecución de Pruebas

### Ejecutar todas las pruebas
```bash
pytest events/tests/ -v
```

### Pruebas por tipo

**Pruebas Unitarias:**
```bash
pytest events/tests/unit/ -v
```

**Pruebas de Integración:**
```bash
pytest events/tests/integration/ -v
```

**Pruebas E2E:**
```bash
pytest events/tests/e2e/ -v
```

### Cobertura de código
```bash
pytest --cov=events --cov-report=html
```

### Análisis de seguridad (Bandit)
```bash
bandit -r events/
```

## Pipeline CI/CD

El proyecto utiliza **GitHub Actions** para integración continua.

### Workflow: `.github/workflows/ci.yml`

#### Pasos del Pipeline:

1. **Checkout del código**
   - Descarga el repositorio

2. **Configuración del entorno**
   - Instala Python 3.11
   - Configura MySQL y Redis como servicios

3. **Instalación de dependencias**
```bash
   pip install -r requirements.txt
```

4. **Ejecución de pruebas unitarias**
   - Valida la lógica de negocio
   - Sin dependencias externas (mocks)

5. **Ejecución de pruebas de integración**
   - Valida repositorios con base de datos real
   - Verifica funcionamiento de caché

6. **Análisis estático de seguridad**
   - Ejecuta Bandit
   - Detecta vulnerabilidades comunes

7. **Ejecución de pruebas E2E**
   - Valida endpoints completos
   - Simula flujos de usuario reales

8. **Resultado**
   - ✅ Si todo pasa: imprime "OK"
   - ❌ Si algo falla: pipeline en estado Failed

### Activación del Pipeline
El pipeline se ejecuta automáticamente en:
- Push a ramas `main` o `develop`
- Pull requests a `main` o `develop`

## Endpoints de la API

### Eventos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/events/` | Listar todos los eventos |
| POST | `/api/events/` | Crear nuevo evento |
| GET | `/api/events/{id}/` | Obtener evento específico |
| PUT | `/api/events/{id}/` | Actualizar evento |
| DELETE | `/api/events/{id}/` | Eliminar evento |
| GET | `/api/events/{id}/statistics/` | Estadísticas del evento |

### Participantes

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/participants/` | Listar participantes |
| POST | `/api/participants/` | Crear participante |
| GET | `/api/participants/{id}/` | Obtener participante |
| PUT | `/api/participants/{id}/` | Actualizar participante |
| DELETE | `/api/participants/{id}/` | Eliminar participante |

### Asistencia

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/attendance/register/` | Registrar asistencia |
| DELETE | `/api/attendance/cancel/` | Cancelar asistencia |
| GET | `/api/attendance/event/{id}/` | Asistentes de un evento |
| GET | `/api/attendance/participant/{id}/` | Eventos de un participante |

## Justificación Tecnológica

### Django + Django REST Framework
- **Framework robusto y maduro** con amplia comunidad
- **ORM potente** que simplifica operaciones de base de datos
- **Django REST Framework** proporciona herramientas para APIs REST de calidad
- Excelente para proyectos que requieren escalabilidad

### MySQL
- **Base de datos relacional** ideal para datos estructurados
- Garantiza **integridad referencial** entre eventos, participantes y asistencias
- Ampliamente utilizada en producción
- Soporte transaccional robusto

### Redis
- **Cache en memoria** extremadamente rápido
- Reduce latencia en consultas frecuentes (estadísticas, listados)
- Mejora rendimiento significativamente
- Fácil integración con Django vía `django-redis`

### Arquitectura de Capas
- **Separación de responsabilidades** clara
- Facilita **testing** independiente de cada capa
- **Mantenibilidad** mejorada
- Permite **escalabilidad** horizontal

### Pytest
- Framework de testing **moderno y expresivo**
- Fixtures reutilizables
- Mejor manejo de errores que unittest
- Plugins como `pytest-django` y `pytest-cov`

### Bandit
- Análisis estático **especializado en seguridad**
- Detecta vulnerabilidades comunes en Python
- Integración sencilla en CI/CD
- Recomendado por OWASP

### GitHub Actions
- **CI/CD nativo** de GitHub
- Configuración mediante YAML simple
- Ejecución en contenedores aislados
- Gratuito para repositorios públicos

## Estructura del Proyecto
```
eventia/
├── eventia_core/          # Configuración del proyecto Django
├── events/                # Aplicación principal
│   ├── models/           # Modelos de datos
│   ├── repositories/     # Capa de acceso a datos
│   ├── services/         # Lógica de negocio
│   ├── serializers/      # Validación y serialización
│   ├── views/            # Endpoints de la API
│   ├── tests/            # Pruebas automatizadas
│   │   ├── unit/        # Pruebas unitarias
│   │   ├── integration/ # Pruebas de integración
│   │   └── e2e/         # Pruebas end-to-end
│   └── urls.py          # Rutas de la API
├── .github/
│   └── workflows/        # Pipeline CI/CD
├── docker-compose.yml    # Servicios Docker
├── requirements.txt      # Dependencias Python
├── pytest.ini           # Configuración de pytest
└── README.md            # Este archivo
```

## Autor

Proyecto desarrollado para el curso de Ingeniería de Software.

## Licencia

MIT License