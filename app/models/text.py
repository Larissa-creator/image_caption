from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch


def load_multi_modal_model() -> tuple:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    model.to(device)
    return processor, model


def generate_image_caption(
    processor: BlipProcessor,
    model: BlipForConditionalGeneration,
    image: Image.Image,
):
    # Resize image while maintaining aspect ratio
    max_dimension = 1024
    image.thumbnail((max_dimension, max_dimension), Image.LANCZOS)

    device = next(model.parameters()).device  # Get device (CPU or GPU)

    # Prepare inputs and move to the appropriate device
    inputs = processor(images=image, return_tensors="pt").to(device)

    # Generate caption
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption
