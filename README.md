# 🚀 Growfi API - Prueba Técnica

Esta es una API desarrollada con **Django REST Framework** que gestiona **usuarios y transacciones** con validación mediante **AWS Lambda**.

## 📌 Características

✅ **Autenticación con Tokens** - Cada usuario obtiene un token único.  
✅ **Validación de Transacciones con AWS Lambda** - Se verifica cada transacción antes de guardarla.  
✅ **API Segura con Django REST Framework** - Requiere autenticación para acceder.  
✅ **Base de Datos Relacional** - Soporte para **PostgreSQL** o **SQLite**.  

---

### **Stack :computer:**

El proyecto esta construido sobre el siguiente stack tecnológico:

- **Python**: >=3.9
- **PostgreSQL**: >=12
- **Git**
- **virtualenv**

---

## 🚀 **Instalación y Configuración**

### 📌 **1 Clonar el Proyecto**
```bash
git clone https://github.com/Edga-r17/growfi_api.git
cd growfi-api
```
### 📌 **2 Crear un Entorno Virtual**

Usaremos `virtualenv` para crear un entorno virtual aislado para las dependencias del proyecto:
Crear el ambiente virtual usando [pyenv](https://github.com/pyenv/pyenv#installation)
Activar el ambiente virtual
```bash
pyenv activate <nombre_del_ambiente_creado>
```

### 📌 **3 Instalar Dependencias**
Instala las dependencias requeridas desde el archivo `requirements.txt`:
```bash
pip install -r requirements.txt

```

### 📌 **4. Configurar la base de datos PostgreSQL**
1. Crea una base de datos en PostgreSQL para este proyecto:
   ```sql
   CREATE DATABASE growfi;
   ```

### 📌 **5 Configurar Variables de Entorno**
```env
export DB_USER='postgres'
export DB_PASSWORD='postgres'
export DB_PORT=5432
export DB_HOST='localhost'
export DB_NAME='growfi'
export DJANGO_SETTINGS_MODULE='growfi_api.settings'
export GROWFI_SECRET_KEY='django-insecure-j7d)ulpinavurqp20+hk-)g2ou8sf60t-gevgpi!7lqin*0%bv'
```
Activa las variables de entorno al iniciar el proyecto:
```bash
source .env
```

### 📌 **6. Aplicar migraciones**
Ejecuta las migraciones para crear las tablas necesarias en la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 📌 **7. Iniciar el Servidor**
```bash
python manage.py runserver
```
La API estará disponible en:
http://127.0.0.1:8000/api/

## 🚀 8. Documentación de la API en Postman

Para facilitar las pruebas de la API, hemos creado una **colección en Postman** con todos los endpoints.

🔗 **Accede a la documentación completa aquí:**  
[![Ver en Postman](https://img.shields.io/badge/Ver%20Documentación%20en-Postman-orange?style=for-the-badge&logo=postman)](https://documenter.getpostman.com/view/27478850/2sAYk7Sizc)

📌 **Pasos para usar la colección en Postman:**
1. **Haz clic en el enlace** y abre la documentación.
2. **Haz clic en "Run in Postman"** para importar la colección a Postman.
3. **Configura la variable de entorno `base_url`** con la URL de tu API local o en producción.
4. **Prueba cada endpoint directamente en Postman.**

---

## 🚀 Endpoints Disponibles en la API

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| **POST** | `/api/users/` | Registra un nuevo usuario |
| **GET**  | `/api/user/<int:pk>/info/` | Obtiene el perfil del usuario autenticado |
| **PATCH** | `/api/user/<int:pk>/info/` | Actualiza el perfil del usuario |
| **POST** | `/api/transacciones/` | Crea una nueva transacción |
| **GET**  | `/api/resumen/<user_id>/` | Obtiene un resumen de gastos del usuario |

Para más detalles, consulta la documentación de Postman. 📖🚀