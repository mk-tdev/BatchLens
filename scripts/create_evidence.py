"""Render original synthetic evidence from authored data, not from generated product imagery."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import csv
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'backend/scenarios/bottles_v1/assets'; OUT.mkdir(parents=True,exist_ok=True)
fontpaths=['/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']
fontpath=next((p for p in fontpaths if Path(p).exists()),None)
def font(n): return ImageFont.truetype(fontpath,n) if fontpath else ImageFont.load_default(size=n)
def page(title,sub,rows,file,obscure=False):
    im=Image.new('RGB',(1000,1200),'#fbfcf6'); d=ImageDraw.Draw(im)
    d.rectangle((0,0,1000,19),fill='#284e3b')
    d.text((75,75),'N / NORTHSTAR BOTTLES',font=font(25),fill='#37543f')
    d.text((75,170),title,font=font(43),fill='#284632')
    d.text((75,240),sub,font=font(20),fill='#87927c')
    d.line((75,300,925,300),fill='#cdd7c3',width=2)
    y=350
    for label,value in rows:
        d.text((75,y),label.upper(),font=font(18),fill='#8a977e')
        if obscure and label=='Finished batch':
            # Draw an opaque redaction over an empty area. No answer exists beneath it.
            for k in range(7): d.line((75,y+42+k*3,520,y+47+k*3),fill='#b2b5a6',width=7)
        else:d.text((75,y+38),value,font=font(30),fill='#3e5b43')
        y+=130
    d.line((75,1050,925,1050),fill='#d7dfcf',width=2)
    d.text((75,1090),'ORIGINAL SYNTHETIC CASE / FOR DEMONSTRATION ONLY',font=font(16),fill='#8c9880')
    im.save(OUT/file)
page('Product identification','Reusable bottle collection · 650 ml', [('Product','NORTHSTAR / REUSABLE BOTTLE'),('Batch','B101'),('Manufactured','12 October 2026'),('Material','Stainless steel body / polymer cap')],'label.png')
page('Supplier inspection report','Quality control · 14 October 2026', [('Component lot','CAP-17'),('Inspection result','OUT OF TOLERANCE'),('Observed exception','Cap seal dimension outside specification'),('Disposition','Quality review required')],'supplier-report.png')
for clear in [False,True]:
    page('Packing slip','Distribution record · 14 October 2026',[('Shipment','S4'),('Finished batch','B104' if clear else ''),('Quantity','500 units'),('Destination','Penang / East')], 'packing-slip-clear.png' if clear else 'packing-slip-obscured.png',obscure=not clear)
(OUT/'complaint.txt').write_text('NORTHSTAR BOTTLES\nCustomer support record / E1\n15 October 2026\n\nSubject: Water escaping around the cap\n\n“I bought a reusable bottle last week. When I turn it on its side, water escapes around the cap even after I tighten it. I have attached a photo of the product label.”\n\nReported symptom: cap seal leakage.\nAttached label: E2.\n\nThe complaint identifies a symptom. It does not establish the physical cause or the condition of other products.\n\nOriginal synthetic case. No real customer data.\n')
(OUT/'production.csv').write_text('finished_batch,component_lot\nB101,CAP-17\nB102,CAP-17\nB103,CAP-18\nB104,CAP-17\n')
(OUT/'shipments.csv').write_text('shipment_id,finished_batch,units,destination\nS1,B101,600,Singapore Central\nS2,B102,400,Johor Bahru North\nS3,B103,500,Kuala Lumpur West\nS4,,500,Penang East\n')
print('Created seven original case artifacts.')
