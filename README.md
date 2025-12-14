# Odoo 18 - Docker Compose

## Inicio rápido

### Levantar los contenedores
```bash
docker-compose up -d
```

### Detener los contenedores
```bash
docker-compose down
```

### Ver logs
```bash
docker-compose logs -f web
```

## Acceso

- **URL**: http://localhost:8069
- **Usuario master por defecto**: admin
- **Contraseña master**: admin

## Estructura de carpetas

- `./config/` - Archivos de configuración de Odoo
- `./addons/` - Módulos personalizados de Odoo
- Volúmenes Docker:
  - `odoo-web-data` - Datos de Odoo
  - `odoo-db-data` - Base de datos PostgreSQL

## Configuración

Puedes modificar las credenciales de la base de datos en el archivo `.env`

## Comandos útiles

### Reiniciar Odoo
```bash
docker-compose restart web
```

### Acceder al contenedor de Odoo
```bash
docker exec -it odoo18 bash
```

### Acceder a PostgreSQL
```bash
docker exec -it odoo18_db psql -U odoo
```

### Ver todos los contenedores
```bash
docker-compose ps
```
