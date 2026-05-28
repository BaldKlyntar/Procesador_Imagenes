# Procesador_Imagenes

El siguiente proyecto tiene como proposito procesar imagenes dependiendo de los parametros ingresados por el usuario. Las funcionalidades de el proyecto son las siguientes:

* Redimensionamiento de imagenes, el usuario puede cambias el alto y ancho de la imagen (px)
* Conversion de formatos (png, jpg, webp y gif)
* Aplicacion de filtros utilizando la herramienta PIL (escala de grises, sepia, invertido, contraste, brillo, etc)
* Generacion de miniatura, esta opcion genera una imagen extra como miniatura o 'thumbnail' con 5 escalas a elegir (px)

## Frontend

La UI es un archivo sencillo que utiliza html y css, este forma la estructura de un formulario donde el usuario puede ingresar la imagen a procesar:
* Drag and Drop
* Trigger event del explorador de archivos

Para la conexion con los endpoints hechos con fastAPI se utiliza app.js, donde reside la logica del frontend.
El archivo app.js se divide en 4 secciones:
* Selectores
  Para este proyecto se utilizo plain JavaScript por lo que fue necesario asignar una id a cada selector o elemento interactivo, la seccion selectores contiene a todos estos elementos
  utilizando getElementById.

* Thumbnail Event Listener
  Un event listener pequeño que se encarga de ocultar la seccion de generacion de miniaturas, si el usuario da click en el checkbox animado se cambiara el
  estado del selector mostrando un select box para elegir el tamaño de la miniatura

* Drag and Drop event Listener
  Aqui se define la logica para el contenedor de imagenes utilizando la propiedad event.dataTransfer.files

* Process button Event Listener
  Se definen las tres funciones importantes del proyecto:
  * handleProcessImage:
    Activada por el boton de procesar imagen, envia los parametros seleccionados por el usuario al backend como un objeto formData,
    realiza un fetch al endpoint process-image y al finalizar llama a las dos funciones restantes.
    
  * updateTaskStatus:
    Toma como argumento el estatus de la tarea que el worker esta realizando, dependiendo del estatus se asigna un porcentaje numerico a este para animar la barra de progreso,
    al finalizar, ya sea que se haya completado la tarea o haya fallado, se reinicia.
    
  * startTaskSSE:
    Es el encargado de suministrar el estado actual de la tarea a la funcion updateTaskStatus. Esta funcion abre una conexion persistente con el backend y
    se actualiza dependiendo de la respuesta que reciba del endpoint events, el cual recibe el identificador de la tarea "taskId" desde el frontend,
    argumento tomado del endpoint process-image.


## Backend

* main.py
  Aloja los endpoints utilizados para delegar tareas a los workers y recibir los parametros para el procesamiento de la imagen desde el frontend. Gracias a fastAPI utilizamos CORSMiddleware para permitir
  la conexion del frontend y evitar problemas de bloqueo.

* image_processor.py
  Se le puede considerar un util al ser utilizado por los workers, se encarga de aplicar los cambios a la imagen con ayuda de PIL.

* redis_client.py
  Crea la conexion a redis para administrar tareas pendientes y estados de procesamiento

* worker.py
  Se define un loop (While True) que de manera perpetua ejecuta el worker, definiendo un estado de espera indefinido hasta recibir una tarea. Al agregarse una tarea a la cola de redis, uno de los workers
  (el primero en llegar) realiza un lpop que retira el primer elemento de esta cola y empieza su trabajo. Al pasar a traves del flujo, los estados de la tarea se van actualizando hasta terminarla y
  finalizar con un completado, gracias a un bloque try except, sea el caso que se genere algun tipo de error, simplemente el estado se actualiza a error y se imprime el mensaje de error dentro de los logs
  de dicho worker.

* dockerfile
  Construye la imagen del contenedor, se crea el directorio /app y se realiza una copia de requirements.txt que contiene todas las dependencias instaladas al backend. Al inicializar el archivo corre un pip install y
  realiza la instalacion de dichas dependencias, finalmente ejecuta uvicorn en el puerto especificado.

* docker-compose.yml
  Aqui se definen los servicios del contenedor, entre ellos se encuentra redis y api (la cual aloja la configuracion de los tres workers)

