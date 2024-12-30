#from fastapi import FastAPI, File, UploadFile
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Response, status
from models.text import load_text_model, generate_text
# from PIL import Image
# from transformers import BlipProcessor, BlipForConditionalGeneration
# import io

models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    models["text2text"] = load_text_model()
    yield
    # add cleanup code here
    models.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/generate/text")
def serve_language_model_controller(prompt=Query(...)): 
    pipe = load_text_model()
    output = generate_text(pipe, prompt)
    return output

if __name__ == "__main__":
  uvicorn.run("image_caption_api:app", port=8000, reload=True)



# Load the model and processor
# processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
# model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# @app.post("/generate_caption")
# async def generate_caption(file: UploadFile = File(...)):
#     # Load image
#     image = Image.open(io.BytesIO(await file.read()))
    
#     # Generate caption
#     inputs = processor(image, return_tensors="pt")
#     outputs = model.generate(**inputs)
#     caption = processor.decode(outputs[0], skip_special_tokens=True)

#     return {"caption": caption}
