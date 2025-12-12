# Autenticación con Argon2id y SQLite

## 📋 Descripción del Proyecto

Este proyecto es una ejemplificación de un sistema seguro de **autenticación de usuarios** implementado con FastAPI, utilizando el algoritmo **Argon2id** para el hash de contraseñas y **SQLite** para el almacenamiento de datos.

### ¿Por qué se hizo este proyecto?

La autenticación segura es uno de los pilares fundamentales de cualquier aplicación web moderna. Este proyecto fue creado para demostrar las mejores prácticas en:

- **Hash seguro de contraseñas** usando Argon2id (ganador de la competencia Password Hashing Competition en 2015)
- **Uso de "pepper"** como capa adicional de seguridad más allá del salt
- **Validación de entrada** con Pydantic
- **Gestión de base de datos** con SQLite
- **API REST** moderna con FastAPI

### Idea de la Ejemplificación

Esta ejemplificación busca mostrar un flujo completo de autenticación que incluye:

1. **Registro de usuarios** con validación de contraseña
2. **Login** con verificación segura
3. **Almacenamiento seguro** de credenciales
4. **Configuración sensible** con variables de entorno

### ¿Para qué sirve?

Esta aplicación puede usarse como:

- **Base de aprendizaje** sobre seguridad en autenticación
- **Punto de partida** para proyectos que requieran sistema de autenticación
- **Referencia** de mejores prácticas en FastAPI
- **Ejemplo** de integración de Argon2id en Python

---

## 🔐 Seguridad: Argon2id y Pepper

### ¿Qué es Argon2id?

Argon2id es un algoritmo de hash de contraseñas ganador de la Password Hashing Competition. Es resistente a ataques de fuerza bruta y ataques GPU/ASIC gracias a su:

- **Alto costo de memoria** (64 MB por defecto)
- **Consumo de CPU optimizado** (3 iteraciones)
- **Paralelización** (4 threads)

### ¿Qué es un Pepper?

Un pepper es una cadena secreta similar al salt, pero con diferencia clave:

- **Salt**: Se almacena junto al hash (genera diferentes hashes para la misma contraseña)
- **Pepper**: Se mantiene secreto en variables de entorno (agrega una capa adicional de seguridad)

En este proyecto: `contraseña_final = contraseña_usuario + APP_PEPPER`

---

## 📦 Requisitos

### Versión de Python

- **Python 3.9 o superior** (recomendado 3.11+)

### Dependencias

```
fastapi>=0.109.0
argon2-cffi>=23.1.0
pydantic>=2.0.0
python-dotenv>=1.0.0
uvicorn[standard]>=0.27.0
```

---

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
cd autenticacion_almacenamiento_py
```

### 2. Crear un entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install fastapi "fastapi[standard]" argon2-cffi pydantic python-dotenv uvicorn
```

O usando un archivo requirements.txt:

```bash
pip install -r requirements.txt
```

### 4. Generar y configurar el APP_PEPPER

**Opción A: Usar el script automático (RECOMENDADO)**

```bash
python generate_pepper.py
```

Este script:
- Genera una clave aleatoria segura de 32 caracteres
- Crea o actualiza el archivo `.env` con `APP_PEPPER`
- Muestra confirmación de éxito

**Opción B: Generar manualmente con Python**

```bash
python -c "import secrets; print('APP_PEPPER=' + secrets.token_urlsafe(32))"
```

Luego crear un archivo `.env` en la raíz del proyecto:

```env
APP_PEPPER=tu_clave_generada_aqui
```

**Opción C: Usar openssl (desde terminal)**

```bash
# Linux/macOS
openssl rand -base64 32

# Windows (PowerShell)
[System.Convert]::ToBase64String([System.Security.Cryptography.RNGCryptoServiceProvider]::new().GetBytes(32))
```

### 5. Ejecutar la aplicación

```bash
uvicorn main:app --reload
```

La API estará disponible en: `http://127.0.0.1:8000`

### 6. Acceder a la documentación interactiva

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 📚 Endpoints

### POST /register

Registra un nuevo usuario.

**Request:**
```json
{
  "username": "juan",
  "password": "miContraseña123"
}
```

**Response (201):**
```json
{
  "message": "Usuario registrado correctamente."
}
```

**Errores:**
- `400`: La contraseña debe tener más de 7 caracteres
- `400`: El usuario ya existe

### POST /login

Inicia sesión con un usuario existente.

**Request:**
```json
{
  "username": "juan",
  "password": "miContraseña123"
}
```

**Response (200):**
```json
{
  "message": "Inicio de sesión exitoso."
}
```

**Errores:**
- `404`: Usuario no encontrado
- `401`: Credenciales inválidas

---

## 📂 Estructura del Proyecto

```
autenticacion_almacenamiento_py/
├── main.py                    # Aplicación principal
├── generate_pepper.py         # Script para generar APP_PEPPER
├── .env                       # Variables de entorno (crear con generate_pepper.py)
├── .env.example               # Ejemplo de variables de entorno
├── .gitignore                 # Archivos a ignorar en Git
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

---

## 🔧 Configuración

### Variables de Entorno (.env)

```env
APP_PEPPER=tu_clave_super_secreta_aqui
```

⚠️ **IMPORTANTE**: Nunca commits el archivo `.env` a Git. Use `.gitignore`:

```
.env
users.db
__pycache__/
*.pyc
venv/
```

---

## 📝 Ejemplos de Uso

### Usando cURL

```bash
# Registrar un usuario
curl -X POST "http://127.0.0.1:8000/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"ContraseñaSegura123"}'

# Iniciar sesión
curl -X POST "http://127.0.0.1:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"ContraseñaSegura123"}'
```

### Usando Python

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Registrar
response = requests.post(
    f"{BASE_URL}/register",
    json={"username": "bob", "password": "OtraContraseña456"}
)
print(response.json())

# Login
response = requests.post(
    f"{BASE_URL}/login",
    json={"username": "bob", "password": "OtraContraseña456"}
)
print(response.json())
```

---

## 🔑 Detalles de Implementación

### Hash de Contraseñas

```python
def hash_password(plain_password: str) -> str:
    value = plain_password + PEPPER  # Se añade el pepper
    return ph.hash(value)  # Argon2id genera hash + salt
```

### Verificación de Contraseñas

```python
def verify_password(plain_password: str, stored_hash: str) -> bool:
    value = plain_password + PEPPER
    try:
        ph.verify(stored_hash, value)  # Compara con el hash almacenado
        return True
    except VerifyMismatchError:
        return False
```

### Parámetros de Argon2id

| Parámetro   | Valor     | Descripción                                          |
| ----------- | --------- | ---------------------------------------------------- |
| time_cost   | 3         | Iteraciones (equilibrio entre seguridad y velocidad) |
| memory_cost | 64,000 KB | ~64 MB de memoria                                    |
| parallelism | 4         | Número de threads para paralelización                |
| hash_len    | 32        | Longitud del hash (bytes)                            |
| salt_len    | 16        | Longitud del salt (bytes)                            |

---

## 🧪 Pruebas

Para probar manualmente en Swagger UI:

1. Ir a `http://127.0.0.1:8000/docs`
2. Expandir `/register`
3. Hacer clic en "Try it out"
4. Introducir datos y ejecutar
5. Repetir con `/login`

---

## ⚙️ Personalización

### Cambiar requisitos de contraseña

En `main.py`, línea ~140:
```python
if len(user.password) <= 7:  # Cambiar número de caracteres
```

### Ajustar parámetros de Argon2id

En `main.py`, línea ~24:
```python
ph = PasswordHasher(
    time_cost=3,        # Aumentar = más seguro pero lento
    memory_cost=64_000, # Aumentar = más seguro pero más memoria
    parallelism=4,      # Aumentar = más rápido (más threads)
    hash_len=32,
    salt_len=16,
)
```

---

## 📋 Base de Datos

### Esquema de usuarios

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
```

La base de datos SQLite se crea automáticamente en `users.db` al iniciar la aplicación.


