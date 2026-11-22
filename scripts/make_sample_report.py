"""Generate a fake sustainability report PDF (fictional company) for demos and smoke tests.

Usage: python scripts/make_sample_report.py data/reports/northwind_sample_2024.pdf
"""
import sys
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

out = sys.argv[1]
pages = [
    ["Message from our CEO",
     "At Northwind Fictional Goods, sustainability is at the heart of everything we do. We are committed to a sustainable future for generations to come and we will play our part in tackling climate change.",
     "Revenue grew 6% to $2.1 billion in 2024, driven by strong demand in our home goods segment."],
    ["Climate",
     "We will reduce absolute Scope 1 and 2 greenhouse gas emissions by 46% by 2030 from a 2021 baseline, a target validated by the Science Based Targets initiative.",
     "We aim to significantly reduce our Scope 3 emissions over time by working with suppliers.",
     "• We will source 100% renewable electricity for all owned sites by 2027",
     "• We continue to explore opportunities to electrify our delivery fleet",
     "In 2023 we reduced emissions by 9% through LED retrofits at 14 warehouses."],
    ["Waste and packaging",
     "Our goal is to cut virgin plastic in packaging by 30% by 2026 compared to 2020 levels.",
     "We strive to minimise waste to landfill wherever possible and improve recycling across our business.",
     "We seek to make our packaging more sustainable in the coming years."],
    ["Water",
     "We will reduce water withdrawal per unit produced by 20% by 2028 against a 2022 baseline at our 6 manufacturing facilities.",
     "We hope to further reduce our water use going forward."],
]

c = canvas.Canvas(out, pagesize=letter)
W, H = letter
for i, paras in enumerate(pages, start=1):
    c.setFont("Helvetica", 8)
    c.drawString(50, H - 30, "Northwind Fictional Goods | Sustainability Report 2024")
    c.drawString(W / 2, 30, str(i))
    y = H - 70
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, paras[0]); y -= 28
    c.setFont("Helvetica", 10)
    for p in paras[1:]:
        for line in simpleSplit(p, "Helvetica", 10, W - 100):
            c.drawString(50, y, line); y -= 14
        y -= 10
    c.showPage()
c.save()
print("wrote", out)
