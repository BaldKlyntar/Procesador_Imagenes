//--------------------------------------------------- Selectores ----------------------------------------------------
const thumbnailCheckbox = document.getElementById("processor-thumbnail-checkbox");
const thumbnailOption = document.getElementById("processor-thumbnail-option");
const dropZone = document.getElementById("drop-zone");
const imageInput = document.getElementById("image-input");
const processButton = document.getElementById("process-button");
const formatSelect = document.getElementById("format-select");
const filterSelect = document.getElementById("filter-select");
const widthInput = document.getElementById("width-input");
const heightInput = document.getElementById("height-input");
const thumbnailSizeSelect = document.getElementById("thumbnail-size-select");
const progressBar = document.getElementById("progress-bar");



//--------------------------------------------------- Thumbnail Event Listener ----------------------------------------------------

thumbnailOption.style.display = "none"

const handleThumbnailToggle = () => {

    if (thumbnailCheckbox.checked){
        thumbnailOption.style.display = "block";
    } else{
        thumbnailOption.style.display = "none"
    }

}

thumbnailCheckbox.addEventListener(
    "change",
    handleThumbnailToggle
);
//--------------------------------------------------- Drag and drop Event Listener ----------------------------------------------------

dropZone.addEventListener("click", () => {
    imageInput.click()
});

dropZone.addEventListener("dragover", (event) => {
    event.preventDefault();
    dropZone.classList.add("drag-over")
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("drag-over");
});

dropZone.addEventListener("drop", (event) => {
    event.preventDefault();
    dropZone.classList.remove("drag-over");

    const file = event.dataTransfer.files[0];

    imageInput.files = event.dataTransfer.files;

    handleImageSelected(file);

});

imageInput.addEventListener("change", () => {
    const file = imageInput.files[0];

    if(!file) return;

    handleImageSelected(file);
})

const handleImageSelected = (file) => {
    if (!file || !file.type.startsWith("image/")) {
    alert("Selecciona un archivo de imagen válido");
    return;
    }

    console.log("Imagen seleccionada", file);

    dropZone.querySelector("h3").textContent = file.name;
    dropZone.querySelector("p").textContent = "Imagen lista para procesar"
    
}

//--------------------------------------------------- Process button Event Listener ----------------------------------------------------

const handleProcessImage = async () => {
    event.preventDefault()
    const file = imageInput.files[0];

    if(!file){
        alert("No se ha agregado ninguna imagen para procesar");
        return;
    }

    const payload = {
    format: formatSelect.value,
    filter: filterSelect.value,
    width: widthInput.value,
    height: heightInput.value,
    thumbnail: thumbnailCheckbox.checked,
    thumbnailSize: thumbnailCheckbox.checked
      ? thumbnailSizeSelect.value
      : null,
    };

    console.log("Imagen: ", file);
    console.log("Opciones: ", payload)

    const formData = new FormData();

    formData.append("image", file);
    formData.append("options", JSON.stringify(payload));

    const response = await fetch("http://127.0.0.1:8000/process-image", {
        method: "POST",
        body: formData
    })

    const data = await response.json();
    updateTaskStatus(data.status)
    startTaskSSE(data.task_id)
}

processButton.addEventListener("click", handleProcessImage);

const statusMap = {
  pending: "Pendiente",
  processing: "Procesando imagen",
  completed: "Completado",
  error: "Error"
};

const progressMap = {
  pending: "25%",
  processing: "50%",
  completed: "100%",
  error: "100%",
};

const updateTaskStatus = (status) => {
  const statusMap = {
    pending: "Pendiente...",
    processing: "Procesando imagen...",
    completed: "Completado",
    error: "Error al procesar",
  };


  progressBar.style.width =
    progressMap[status] || "0%";

  if(status === "completed" || status === "error"){
    setTimeout(() => {
        progressBar.style.width = "0%"
    }, 2500)
  }
};

const startTaskSSE = (taskId) => {
    const eventSource = new EventSource(
        `http://127.0.0.1:8000/tasks/${taskId}/events`
    );

    eventSource.addEventListener("status", (event) => {
        const data = JSON.parse(event.data);

        console.log(data.status)
        updateTaskStatus(data.status);

        if (data.status === "completed" || data.status === "error"){
            eventSource.close();
        }

    });

    eventSource.onerror = () => {
        updateTaskStatus("connection_error");
        eventSource.close()
    }
}