# Sistema de Cargos

Sistema de gestión de cargos judiciales desarrollado para el Consejo Superior de la Judicatura.

## Características

- Gestión de despachos judiciales
- Control de funcionarios
- Registro de novedades
- Exportación de datos a Excel
- Sistema de autenticación y permisos

## Requisitos

- Python 3.x
- Django 5.x
- PostgreSQL
- Otras dependencias en requirements.txt

## Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/nombre-repositorio.git
cd nombre-repositorio
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos en settings.py

5. Realizar migraciones
```bash
python manage.py migrate
```

6. Crear superusuario
```bash
python manage.py createsuperuser
```

7. Ejecutar el servidor
```bash
python manage.py runserver
```
```

2. Crea un archivo `requirements.txt`:
```bash
pip freeze > requirements.txt
```

¿Necesitas ayuda con alguno de estos pasos?
