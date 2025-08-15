from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse, HTMLResponse
from PIL import Image, ImageDraw, ImageFont
import io

app = FastAPI(title="Planetarium API")

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

# 🎨 Funções utilitárias
def create_canvas():
    img = Image.new("RGB", (CANVAS_WIDTH, CANVAS_HEIGHT), "black")
    draw = ImageDraw.Draw(img)
    return img, draw

def draw_stars(draw):
    import random
    for _ in range(int((CANVAS_HEIGHT + CANVAS_WIDTH) / 8)):
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(1, 2)
        draw.ellipse((x, y, x + size, y + size), fill="white")

def draw_text(draw, text):
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    draw.text((10, 10), text, fill="white", font=font)

# 🪐 Funções de planetas
def draw_mercury():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((190, 190, 210, 210), fill="darkgoldenrod")
    draw_text(draw, "Mercury")
    return img

def draw_venus():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((175, 175, 225, 225), fill="goldenrod")
    draw_text(draw, "Venus")
    return img

def draw_earth():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((175, 175, 225, 225), fill="royalblue")
    draw.rectangle((200, 180, 220, 200), fill="forestgreen")
    draw_text(draw, "Earth")
    return img

def draw_mars():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((190, 190, 210, 210), fill="red")
    draw_text(draw, "Mars")
    return img

def draw_jupiter():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((50, 50, 350, 350), fill="burlywood")
    draw.line((50, 200, 350, 200), fill="crimson", width=3)
    draw_text(draw, "Jupiter")
    return img

def draw_saturn():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((50, 50, 350, 350), fill="tan")
    for i in range(7):
        draw.line((0, 200 + i*2, 400, 200 - i*2), fill="white")
    draw_text(draw, "Saturn")
    return img

def draw_uranus():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((85, 85, 315, 315), fill="cyan")
    draw_text(draw, "Uranus")
    return img

def draw_neptune():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((85, 85, 315, 315), fill="dodgerblue")
    draw_text(draw, "Neptune")
    return img

def draw_sun():
    img, draw = create_canvas()
    draw_stars(draw)
    draw.ellipse((-300, -300, 700, 700), fill="yellow")
    draw_text(draw, "Sun")
    return img

def draw_pluto():
    img, draw = create_canvas()
    draw_stars(draw)
    messages = ["Pluto", "is", "NOT", "a", "Planet!", "(ノಠ益ಠ)ノ彡┻━┻"]
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    for i, msg in enumerate(messages):
        draw.text((10, 10 + i * 30), msg, fill="white", font=font)
    return img

# Dicionário de planetas
planet_dict = {
    "mercury": draw_mercury,
    "venus": draw_venus,
    "earth": draw_earth,
    "mars": draw_mars,
    "jupiter": draw_jupiter,
    "saturn": draw_saturn,
    "uranus": draw_uranus,
    "neptune": draw_neptune,
    "pluto": draw_pluto,
    "sun": draw_sun
}

# API Endpoints
@app.get("/", response_class=HTMLResponse)
def index():
    planets_html = "".join(
        [f"<li><a href='/planet/{p}' target='_blank'>{p.title()}</a></li>" for p in planet_dict]
    )
    return f"""
    <html>
        <head><title>Planetarium</title></head>
        <body style="background:black;color:white;font-family:sans-serif">
            <h1>The Planetarium 🌌</h1>
            <p>Click a planet to view:</p>
            <ul>{planets_html}</ul>
        </body>
    </html>
    """

@app.get("/planets")
def list_planets():
    return {"planets": list(planet_dict.keys())}

@app.get("/planet/{name}")
def get_planet(name: str):
    name = name.lower()
    if name not in planet_dict:
        raise HTTPException(status_code=404, detail="Planet not found")
    img = planet_dict[name]()
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
