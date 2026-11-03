import sys,os,glob,numpy as np
from PIL import Image,ImageDraw,ImageFont
L='/Users/robertreff/Desktop/Website-Projekte/Wirtschaft am Schlössli Bottighofen/_quelle/extern/logo/schloessli-logo-transparent.png'
a=np.array(Image.open(L).convert('RGBA'))[:,:,3]>110
row=a[780+222:780+290, 300+550:300+1100]
cols=row.any(0);segs=[];i=0
while i<len(cols):
    if cols[i]:
        j=i
        while j<len(cols) and cols[j]: j+=1
        segs.append((i,j));i=j
    else:i+=1
print(len(segs),'segs')
def crop(m):
    ys,xs=np.where(m);return m[ys.min():ys.max()+1,xs.min():xs.max()+1]
logo=[crop(row[:,s:e]) for s,e in segs]
txt='WIRTSCHAFT'
# stroke width of I (letter 2)
print('I width px',logo[1].shape, 'cap h', logo[0].shape[0])
def rend(font,ch):
    img=Image.new('L',(500,500),0);d=ImageDraw.Draw(img);d.text((100,50),ch,font=font,fill=255);return crop(np.array(img)>128)
res=[]
for f in sys.argv[1:]:
  axes=None
  try:
    font=ImageFont.truetype(f,300); axes=font.get_variation_axes()
  except Exception: pass
  ws=[None] if not axes else [300,350,400,450,500]
  for w in ws:
    font=ImageFont.truetype(f,300)
    if w:
      vals=[]
      for ax in axes:
        n=ax['name'] if isinstance(ax['name'],str) else ax['name'].decode()
        vals.append(w if n.lower().startswith('weight') else ax['default'])
      font.set_variation_by_axes(vals)
    sc=[];ar=[];sw=[]
    for ch,g in zip(txt,logo):
      r=rend(font,ch);H,W=g.shape
      rr=np.array(Image.fromarray(r.astype(np.uint8)*255).resize((W,H),Image.LANCZOS))>128
      sc.append((g&rr).sum()/max(1,(g|rr).sum()));ar.append(abs(r.shape[1]/r.shape[0]-W/H)/(W/H))
    res.append((np.mean(sc)-0.5*np.mean(ar),np.mean(sc),np.mean(ar),os.path.basename(f),w))
for r in sorted(res,reverse=True)[:14]: print('%.3f iou=%.3f asp=%.3f %s %s'%r)
