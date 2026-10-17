"""Render original BatchLens submission posters from verified app screenshots.
Optional authoring dependency: reportlab. Runtime application does not require it.
Run from the repository root. Raster previews use pdftoppm separately.
"""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/submission'
FONT=Path('/System/Library/Fonts/Supplemental')
if (FONT/'Arial.ttf').exists():
    pdfmetrics.registerFont(TTFont('Body',str(FONT/'Arial.ttf')))
    pdfmetrics.registerFont(TTFont('Bold',str(FONT/'Arial Bold.ttf')))
else:
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    # Portable built-ins when the authoring machine has no Arial.
    from reportlab.pdfbase.pdfmetrics import Font,registerFont
    registerFont(Font('Body','Helvetica','WinAnsiEncoding'))
    registerFont(Font('Bold','Helvetica-Bold','WinAnsiEncoding'))
BG='#081F1C';CARD='#102D28';MINT='#A9E6C8';WHITE='#F0F7ED';MUTED='#B5CAC0';AMBER='#F5BA59'
LIVE='https://batchlens-hk3hxwi5na-as.a.run.app/'
REPO='https://github.com/mk-tdev/BatchLens'
def text(c,x,y,s,size=20,color=WHITE,bold=False):
    c.setFillColor(HexColor(color));c.setFont('Bold' if bold else 'Body',size);c.drawString(x,y,s)
def para(c,x,y,s,width,size=20,color=MUTED,leading=None,bold=False):
    leading=leading or size*1.35;words=s.split();line=''
    for word in words:
        candidate=(line+' '+word).strip()
        if pdfmetrics.stringWidth(candidate,'Bold' if bold else 'Body',size)>width and line:
            text(c,x,y,line,size,color,bold);y-=leading;line=word
        else:line=candidate
    if line:text(c,x,y,line,size,color,bold);y-=leading
    return y

def card(c,x,y,w,h):
    c.setFillColor(HexColor(CARD));c.setStrokeColor(HexColor('#285247'));c.roundRect(x,y,w,h,18,fill=1,stroke=1)
def photo(c,file,x,y,w,h):
    c.drawImage(ImageReader(str(OUT/file)),x,y,w,h,preserveAspectRatio=True,anchor='c',mask='auto')
def qr(c,url,x,y,size):
    c.setFillColor(HexColor(WHITE));c.roundRect(x-8,y-8,size+16,size+16,8,fill=1,stroke=0)
    q=QrCodeWidget(url);b=q.getBounds();d=Drawing(size,size,transform=[size/(b[2]-b[0]),0,0,size/(b[3]-b[1]),0,0]);d.add(q);renderPDF.draw(d,c,x,y)
def base(name,w,h,title):
    c=canvas.Canvas(str(OUT/name),pagesize=(w,h));c.setTitle(title);c.setAuthor('PixelTrendAnalytics');c.setSubject('AI Builder Cup 2026 - BatchLens manufacturing quality investigation');c.setFillColor(HexColor(BG));c.rect(0,0,w,h,fill=1,stroke=0);return c

def overview():
    c=base('BatchLens-Project-Poster.pdf',1600,1000,'BatchLens - Project overview')
    text(c,64,940,'PIXELTRENDANALYTICS / AI BUILDER CUP 2026',19,MINT,True)
    text(c,64,874,'BatchLens',66,WHITE,True)
    text(c,64,827,'A factory story. A real AI investigator.',29,MINT,True)
    y=para(c,64,761,'One leaking cap. Four shipments. Pip follows the evidence, compares possible causes and proposes the next useful inspection.',630,27,WHITE,37)
    para(c,64,y-18,'Gemini reads original records and calls validated tools. Operators approve missions, record results and review the handover.',600,22,MUTED,31)
    card(c,760,430,776,410);photo(c,'live-walkable-factory.png',778,448,740,374)
    text(c,778,410,'ACTUAL PROTOTYPE / EXPLORE THE NORTHSTAR FACTORY',16,MINT,True)
    crews=[('Mira.png','Mira / Evidence','Read sources. Review the facts.'),('Sol.png','Sol / Assembly','Follow the lot. Compare scope.'),('Pip.png','Pip / Investigator','Propose a check. Reassess results.')]
    for i,(f,title,body) in enumerate(crews):
        x=64+i*500;card(c,x,222,472,148);photo(c,f,x+18,245,85,103);text(c,x+120,316,title,23,MINT,True);para(c,x+120,280,body,325,20,MUTED,27)
    text(c,64,175,'GEMINI ON VERTEX AI  /  CLOUD RUN  /  FIRESTORE',20,AMBER,True)
    text(c,64,137,'Synthetic case and operator results. Live AI. Human-reviewed decisions.',19,MUTED)
    text(c,64,91,'Manufacturing: Intelligent Operations & Industrial Efficiency',18,WHITE)
    text(c,64,54,'Source and research: github.com/mk-tdev/BatchLens',19,MINT)
    c.linkURL(REPO,(60,42,600,78),relative=0)
    qr(c,LIVE,1402,57,100);text(c,1195,98,'TRY THE FACTORY',19,MINT,True);text(c,1195,69,'Scan the live demo',17,MUTED)
    c.showPage();c.save()

def loop():
    c=base('BatchLens-Agentic-Workflow-Poster.pdf',1080,1440,'BatchLens - Agentic investigation loop')
    text(c,56,1380,'BATCHLENS / PIXELTRENDANALYTICS',20,MINT,True)
    text(c,56,1306,'Pip investigates.',56,WHITE,True)
    text(c,56,1240,'Operators decide.',56,MINT,True)
    para(c,56,1192,'Real Gemini tool calling connects evidence to an inspection mission, then learns from an operator-entered result.',950,25,MUTED,34)
    rows=[('01','READ & TRACE','GEMINI + VALIDATED TOOLS','Read source images and ledgers. Recover the missing slip. Cite original records.'),('02','COMPARE CAUSES','GEMINI FINDINGS','Compare component, assembly and handling explanations. Preserve missing evidence.'),('03','PROPOSE A MISSION','AI DRAFT / HUMAN APPROVAL','Select a fictional approved procedure. The operator approves the demo mission.'),('04','RECORD & REASSESS','OPERATOR RESULT -> GEMINI','Record a labelled synthetic result. Gemini revises its hypotheses with R-source citations.')]
    y=1000
    for n,title,role,body in rows:
        card(c,56,y,968,132);text(c,80,y+80,n,34,AMBER,True);text(c,156,y+91,title,26,WHITE,True);text(c,156,y+62,role,15,MINT,True);para(c,156,y+34,body,820,19,MUTED,25);y-=154
    card(c,56,201,968,296)
    photo(c,'pip-mission-result.png',76,221,292,256)
    text(c,400,449,'THE VERIFIED DEMO',21,AMBER,True)
    para(c,400,409,'R1: 2 of 5 fictional assemblies leak. Gemini changes a hypothesis from unresolved to supported.',565,24,WHITE,33,True)
    para(c,400,285,'A small synthetic sample does not prove a lot-wide defect. Findings remain for human review.',565,20,MUTED,28)
    text(c,56,155,'OPERATIONS RADIO',18,AMBER,True)
    para(c,56,122,'Ask case-specific questions with citations. General queries are refused. Chat cannot change approvals.',780,20,MUTED,27)
    text(c,56,49,'Next: review scope, approve action drafts, save and export the handover.',18,WHITE)
    c.linkURL(REPO,(54,32,850,75),relative=0);qr(c,REPO,922,55,78)
    c.showPage();c.save()

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True);overview();loop()
    print('Created two original, editable-vector PDF posters using actual app screenshots.')
