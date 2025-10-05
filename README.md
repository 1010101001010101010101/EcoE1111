## ⚙️ Instalación del proyecto

### 1️⃣ Clonar el repositorio
```bash
git clone https://github.com/1010101001010101010101/EcoE1111.git
cd EcoE1111
2️⃣ Crear y activar el entorno virtual
python -m venv env
env\Scripts\activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

🗝️ Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

DB_NAME=ecoenergy_db
DB_USER=root
DB_PASSWORD=tu_contraseña_mysql
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=django-insecure-123456
DEBUG=True

🧩 Base de datos
Crear base de datos MySQL
mysql -u root -p
CREATE DATABASE ecoenergy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;

Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

🌱 Cargar semillas (catálogo inicial)

Para crear los datos base del sistema, ejecuta el siguiente comando:

python manage.py seed_catalog_es


Este comando crea automáticamente:

2 Category

3 Product

2 AlertRule

Relaciones Product ↔ AlertRule con distintos umbrales

1 Organization, 2 Zone y 3 Device

🧠 Panel de administración
Acceder al admin
python manage.py runserver


URL: http://127.0.0.1:8000/admin/

Usuario de prueba:

user: admin
pass: admin123

🧩 Estructura principal

organizations → Organizaciones y zonas

dispositivos → Dispositivos, categorías, productos, mediciones

accounts → Usuarios, roles y autenticación

🧾 Git y ramas

Cada unidad se trabaja en una rama distinta:

git checkout -b U2-C1_BD
git checkout -b U2-C2_AdminBasico
git checkout -b U2-C3_AdminPro
git checkout -b U2-C4_RolesUsuarios


Subir cambios:

git add .
git commit -m "Avance U2-C4: roles y organizaciones"
git push origin U2-C4_RolesUsuarios

🧩 Tecnologías utilizadas

Python 3.13

Django 5.2

MySQL 8.4

PyMySQL

Bootstrap 5 (templates admin)