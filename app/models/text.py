from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image


def load_multi_modal_model() -> tuple[
    BlipProcessor, BlipForConditionalGeneration
]:
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base"
    )
    return processor, model


def generate_image_caption(
    processor: BlipProcessor,
    model: BlipForConditionalGeneration,
    image: Image.Image,
):
    image = image.resize((1024, 576))
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return {"caption": caption}
