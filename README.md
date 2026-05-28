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
  Se definen las tres funciones importantes del proyecto: handleProcessImage, activada por el boton de procesar imagen, envia los parametros seleccionados por el usuario al backend
  como un objeto formData, realiza un fetch al endpoint process-image y al finalizar llama a las dos funciones restantes.
  La funcion updateTaskStatus toma como argumento el estatus de la tarea que el worker esta realizando, dependiendo del estatus se asigna un porcentaje numerico
  a este para animar la barra de progreso, al finalizar, ya sea que se haya completado la tarea o haya fallado, se reinicia.
  Finalmente startTaskSSE es el encargado de suministrar el estado actual de la tarea a la funcion updateTaskStatus. Esta funcion abre una conexion persistente con el backend
  y se actualiza dependiendo de la respuesta que reciba del endpoint events, el cual recibe el identificador de la tarea "taskId" desde el frontend, argumento tomado del endpoint
  process-image.


## Backend

