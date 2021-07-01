# Gaming Review Aggregate - Ingeniería de Software - Grupo 6

## About Gaming Review Aggregate

El proyecto almacenado en el presente repositorio corresponde al proyecto semestral del curso **CC4401-Ingeniería de Software**, desarrollada en Python 3.9, **mediante el framework de Django 3.2**.El objetivo general del proyecto es la creación de una aplicación web funcional, con el fin de acercarnos al mundo del desarrollo de software, desarrollar habilidades de trabajo en equipo, y de aprender diversas metodologías y herramientas en el desarrollo de software.

La temática de la aplicación web es un portal dedicado a los videojuegos y principalmente enfocado en los jugadores. La idea es crear una página que le permita a las personas catalogar videojuegos según su experiencia con estos, pudiendo otorgarles un puntaje y opcionalemnte una reseña escrita que describa sus impresiones. Los videojuegos estarán almacenados en la base de datos de la aplicación web, siendo gestionados mediante modelos de Django. Por otro lado, los usuarios podrán crear perfiles en sus cuentas, tener un listado de sus videojuegos reseñados, poder visualizar las reseñas de amigos, y podrán ser capaces de añadir nuevos juegos a la base de datos comunitaria en caso de que estos no existan previamente, siguiendo el formato de wiki (como Wikipedia).

## Instrucciones Generales

Para poder utilizar esta aplicación web:

### Step 1
Instalar la versión del 3.2 framwork [**Django**](https://www.djangoproject.com/download/) en su computadora.

### Step 2
Clonar el repositorio de forma local
```postscript
git clone https://github.com/DCC-CC4401/Gamming-Review-Aggregate.git
```

### Step 3
Hacer migraciones en la carpeta ```gaming_review_aggregate```
```
cd /cloned-repository/Gamming-Review-Aggregate/gaming_review_aggregate
python manage.py makemigrations
python manage.py migrate
```

### Step 4
Correr la aplicación de forma local
```
python manage.py runserver
```

## Branches
- master
- estilos
- formulario

## Authors
- **Alexander Walmsley** - [AlexanderWalmsley](https://github.com/AlexanderWalmsley)
- **Esteban Courard Christie**
- **Felipe Leal Cerro** - [Lysorek](https://github.com/Lysorek)
- **Matias Ceda A.** - [tridimensionaal](https://github.com/tridimensionaal)
- **Nicolás García Ríos** - [Nicolas-Francisco](https://github.com/Nicolas-Francisco)
