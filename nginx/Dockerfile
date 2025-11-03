FROM nginx:alpine

# 2. Eliminamos el archivo de configuración por defecto de Nginx
RUN rm /etc/nginx/conf.d/default.conf

# 3. Copiamos nuestro archivo de configuración personalizado (nginx.conf)
#    desde esta carpeta (nginx/) al lugar correcto dentro del contenedor.
COPY nginx.conf /etc/nginx/conf.d/