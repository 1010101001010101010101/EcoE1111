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
Si no funciona eso, correr estos comandos
1x1:
pip install django
pip install python-dotenv
pip install pymysql
pip install django-widget-tweaks

🗝️ Configurar variables de entorno

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

DJANGO_SECRET_KEY=django-insecure-123456
DJANGO_DEBUG=True
DB_ENGINE=mysql
DB_NAME=ecoenergy_db
DB_USER=root
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=3307

ingresamos a wampserver-->phpmyadmin---> ingresamos con root sin contraseña---> seleccionamos MariaDB
---> creamos la base de datos (ecoenergy_db)---> con el entorno env prendido realizamos lo siguiente---> APLICAR MIGRACIONES

Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

🌱 Cargar semillas (catálogo inicial)

Para crear los datos base del sistema, ejecuta el siguiente comando:

python manage.py seed_modules
python manage.py seed_roles_users
python manage.py seed_device_data

Estos comandos crean automáticamente:
-Usuarios con permisos y roles
-Productos con categorias, mediciones, alertruler,productalert etc con zonas asignadas
Ojo tenemos que ingresar con un administrador para poder modificar un problema con organizacion ya que
cuando cree la semilla no le asigno automaticamente una zona a una organizacion entonces
tenemos que buscar las zonas sin organizacion y asignarselas.
podemos irnos a organizations--->ingresamos a cualquiera de las 3 y si veemos que no tiene una zona asignada, 
se la podemos asignar a travez de un inline, Zona Centro, Zona Sur o Zona Norte. solo 1 por organizations.


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

🧠 Panel de administración
Acceder al admin
python manage.py runserver


URL: http://127.0.0.1:8000/admin/

Usuario de prueba:

primero ingresamos con un admin, el cuenta con todos los permisos
user: admin_mi_empresa
pass: admin123

desde aqui podemos ir a user profile y veemos en que
organizacion esta nuestro user cliente_mi_empresa podemos ver que el esta en Mi empresa, luego nos vamos a device y le asignamos zonas y organizacion a los dispositivos que esten sin este.

dejaremos solo 2 dispositivos en la zona Norte y 2 en la Zona Sur
los que dejemos en la zona norte se los asignamos a mi empresa
y los que dejemos en Zona Sur se los asignamos a la organizacion tu empresa.

Cliente Prueba

despues ingresamos con:
user: cliente_mi_empresa
password: cliente123



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
