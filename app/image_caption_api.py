import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile
from models.text import load_multi_modal_model, generate_image_caption
from PIL import Image
import io

models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    models["processor"], models["model"] = load_multi_modal_model()
    yield
    models.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/generate/caption")
async def serve_multi_modal_model_controller(image: UploadFile = File(...)):
    image_data = await image.read()
    image = Image.open(io.BytesIO(image_data))

    caption = generate_image_caption(
        models["processor"], models["model"], image
    )
    return caption


if __name__ == "__main__":
    uvicorn.run("image_caption_api:app", port=8000, reload=True)
