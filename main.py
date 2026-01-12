from fastapi import FastAPI, File, UploadFile, Form, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image, ImageDraw, ImageFont
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = "generated"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_meme(
    image: UploadFile = File(...),
    top_text: str = Form(""),
    bottom_text: str = Form("")
):
    img = Image.open(image.file)
    draw = ImageDraw.Draw(img)

    font = ImageFont.load_default()
    width, height = img.size

    draw.text((width/2 - 50, 10), top_text, font=font, fill="white")
    draw.text((width/2 - 50, height - 30), bottom_text, font=font, fill="white")

    output_path = f"{UPLOAD_DIR}/meme.png"
    img.save(output_path)

    return FileResponse(output_path, media_type="image/png")