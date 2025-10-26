
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

def render_contract(data: dict, path: str) -> str:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(p), pagesize=A4)
    c.setFont("Helvetica", 12)
    c.drawString(50, 800, "ДОГОВОР КУПЛИ-ПРОДАЖИ АВТОМОБИЛЯ")
    y = 770
    for k, v in data.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 20
    c.showPage()
    c.save()
    return str(p)
