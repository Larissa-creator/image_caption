import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate/caption")
async def serve_multi_modal_model_controller(image: UploadFile = File(...)):
    try:
        image_data = await image.read()
        image = Image.open(io.BytesIO(image_data))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    try:
        caption = generate_image_caption(
            models["processor"], models["model"], image
        )
        return {"caption": caption}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to generate caption.")

if __name__ == "__main__":
    uvicorn.run("image_caption_api:app", host="0.0.0.0", port=8000, reload=True)
