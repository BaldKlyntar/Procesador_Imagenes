from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import os

PROCESSED_DIR = "processed"

def apply_filter(image, filter_name):
    filter = filter_name

    match filter:
        case "grayscale":
            return ImageOps.grayscale(image).convert("RGB")
        case "sepia":
            grayscale = ImageOps.grayscale(image)
            return ImageOps.colorize(
                grayscale,
            "#704214",
            "#C0A080"
            ).convert("RGB")
        case "invert":
            return ImageOps.invert(image.convert("RGB"))
        case "blur":
            return image.filter(ImageFilter.BLUR)
        case "brightness":
            enhancer = ImageEnhance.Brightness(image)
            return enhancer.enhance(1.5)
        case "contrast":
            enhancer = ImageEnhance.Contrast(image)
            return enhancer.enhance(1.5)
        
    return image

def process_image(task):
    task_id = task["task_id"]
    image_path = task["image_path"]
    options = task["options"]

    image = Image.open(image_path)

    width = options.get("width")
    height = options.get("height")

    if width and height:
        image = image.resize((int(width), int(height)))
    
    filter_name = options.get("filter")

    if filter_name:
        image = apply_filter(image, filter_name)

    output_format = options.get("format", "png")
    output_filename = f"{task_id}.{output_format}"
    output_path = os.path.join(PROCESSED_DIR, output_filename)

    if output_format in ["jpg", "jpeg"]:
        image = image.convert("RGB")
        save_format = "JPEG"
    else:
        save_format = output_format.upper()
    
    image.save(output_path, save_format)

    if options.get("thumbnail"):
        thumbnail_size = int(options.get("thumbnailSize", 128))

        thumbnail = image.copy()
        thumbnail.thumbnail((thumbnail_size, thumbnail_size))
        thumbnail_filename = f"{task_id}_thumbnail.{output_format}"
        thumbnail_path = os.path.join(PROCESSED_DIR, thumbnail_filename)

        thumbnail.save(thumbnail_path, save_format)

    return output_path