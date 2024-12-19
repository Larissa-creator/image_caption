from fastapi import FastAPI, File, UploadFile
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import io

app = FastAPI()

# Load the model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.post("/generate_caption")
async def generate_caption(file: UploadFile = File(...)):
    # Load image
    image = Image.open(io.BytesIO(await file.read()))
    
    # Generate caption
    inputs = processor(image, return_tensors="pt")
    outputs = model.generate(**inputs)
    caption = processor.decode(outputs[0], skip_special_tokens=True)

    return {"caption": caption}
