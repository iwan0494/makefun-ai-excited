from PIL import Image, ImageDraw, ImageFilter
import math, random
random.seed(14)
S=1024
im=Image.new('RGB',(S,S)); p=im.load()
# dusk gradient
stops=[(0,(7,12,42)),(.43,(22,26,78)),(.72,(138,49,100)),(1,(255,151,102))]
for y in range(S):
 t=y/(S-1)
 for i in range(len(stops)-1):
  if stops[i][0]<=t<=stops[i+1][0]:
   a,c=stops[i]; b,d=stops[i+1]; u=(t-a)/(b-a)
   col=tuple(round(c[k]*(1-u)+d[k]*u) for k in range(3)); break
 for x in range(S): p[x,y]=col
# glow discs / horizon haze
glow=Image.new('RGBA',(S,S)); gd=ImageDraw.Draw(glow)
gd.ellipse((360,355,920,780),fill=(255,93,133,80)); glow=glow.filter(ImageFilter.GaussianBlur(90)); im=Image.alpha_composite(im.convert('RGBA'),glow)
# motion ribbons behind fish
r=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(r)
for j in range(11):
 y=590+j*17
 d.arc((-200,y-210,855,y+300),190,330,fill=(71,232,255,95-j*5),width=3+(j%3))
 d.line([(0,y+90),(230,y+45),(420,y-8)],fill=(255,123,205,70),width=2)
r=r.filter(ImageFilter.GaussianBlur(2)); im=Image.alpha_composite(im,r)
# city skyline silhouettes, warm windows
city=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(city)
d.rectangle((0,760,1024,1024),fill=(8,13,37,255))
# buildings set on horizon, mix heights
x=-10
while x<1040:
 w=random.randint(36,82); h=random.randint(85,245); top=760-h
 d.rectangle((x,top,x+w,790),fill=random.choice([(12,21,55,255),(13,25,56,255),(19,25,61,255)]))
 # rooftop antenna
 if random.random()<.38: d.line((x+w*.55,top,x+w*.55,top- random.randint(20,60)),fill=(57,196,226,180),width=2)
 for wx in range(x+8,x+w-4,12):
  for wy in range(top+12,770,18):
   if random.random()<.42: d.rectangle((wx,wy,wx+4,wy+7),fill=random.choice([(255,177,91,170),(66,210,255,170),(255,83,169,160)]))
 x+=w+random.randint(3,13)
# foreground city edge
d.polygon([(0,850),(145,820),(270,855),(420,815),(560,850),(710,810),(860,843),(1024,800),(1024,1024),(0,1024)],fill=(5,10,29,255))
# perspective water / neon reflections
for j in range(70):
 x=random.randint(0,1024); y=random.randint(850,1020); w=random.randint(8,70)
 color=random.choice([(255,118,118,90),(48,203,255,95),(241,83,177,90)])
 d.line((x,y,x+w,y+random.randint(0,7)),fill=color,width=random.choice([1,2,3]))
im=Image.alpha_composite(im,city)
# koi: diagonal upward from lower-left to upper-right. Render layers on transparent canvas.
fish=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(fish)
# tail and fins, luminous cyan outer shape
# tail lobes
# fish body axis from (330,700) to (720,390)
d.polygon([(370,686),(253,793),(283,690),(204,616),(351,642)],fill=(22,218,238,255),outline=(203,255,242,255))
d.polygon([(420,655),(360,790),(470,719),(513,746),(500,635)],fill=(28,190,222,255),outline=(168,251,245,255))
# body path-like ellipse rotated
body=Image.new('RGBA',(600,330)); bd=ImageDraw.Draw(body)
bd.ellipse((20,35,575,290),fill=(229,244,225,255),outline=(64,255,234,255),width=8)
# orange patches
bd.ellipse((65,43,220,150),fill=(255,108,70,255)); bd.ellipse((300,34,458,133),fill=(255,126,65,255)); bd.ellipse((405,150,556,263),fill=(255,94,64,255)); bd.ellipse((179,177,323,280),fill=(255,112,75,255))
# scale arcs, subtle cool iridescence
sd=ImageDraw.Draw(body)
for yy in range(70,270,28):
 for xx in range(55+(yy//28%2)*17,555,34):
  sd.arc((xx-18,yy-15,xx+18,yy+18),5,175,fill=(82,193,193,150),width=2)
# head mark + eye
bd.ellipse((481,92,500,111),fill=(9,20,44,255)); bd.ellipse((485,94,491,100),fill=(255,255,255,255))
# gill
bd.arc((430,85,482,200),80,280,fill=(37,133,153,210),width=5)
# fins
bd.polygon([(304,179),(230,275),(346,234)],fill=(92,222,224,210),outline=(222,255,240,230))
body=body.rotate(34,resample=Image.Resampling.BICUBIC,expand=True)
fish.alpha_composite(body,(415,202))
# whiskers and fin rays
d=ImageDraw.Draw(fish)
d.arc((816,299,929,410),195,285,fill=(207,255,243,220),width=4)
d.arc((810,326,920,431),200,285,fill=(207,255,243,180),width=3)
# fins rays tail
for i in range(5): d.line((288+i*10,677,240+i*12,755),fill=(205,255,244,150),width=2)
# luminous rim outside blur
rim=fish.getchannel('A').filter(ImageFilter.GaussianBlur(22)); aura=Image.new('RGBA',(S,S),(24,240,255,0)); aura.putalpha(rim.point(lambda v:int(v*.60))); im=Image.alpha_composite(im,aura); im=Image.alpha_composite(im,fish)
# Crisp highlights and city-colour streaks make the koi's scales catch the skyline.
hi=Image.new('RGBA',(S,S)); d=ImageDraw.Draw(hi)
d.arc((494,273,941,726),201,339,fill=(255,255,222,210),width=5)
for k in range(18):
 x=524+k*17; y=int(594-(x-524)*.63)
 d.line((x,y,x+random.randint(7,16),y-random.randint(8,19)),fill=random.choice([(255,235,168,180),(50,234,255,210),(255,107,156,160)]),width=2)
# sparkle accents, not fireworks
for x,y,rad in [(780,315,15),(444,500,10),(912,487,8),(602,277,7)]:
 d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(255,255,231,230)); d.ellipse((x-rad*2,y-rad*2,x+rad*2,y+rad*2),outline=(100,251,255,130),width=2)
im=Image.alpha_composite(im,hi)
# atmospheric grain-free sharpen, convert palette optimized PNG
im=im.convert('RGB').resize((1024,1024),Image.Resampling.LANCZOS)
im.save('entry.png',format='PNG',optimize=True)
