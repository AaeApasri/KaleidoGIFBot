from PIL import Image, ImageDraw,ImageFilter
import PIL.ImageOps as im
import numpy as np
import moviepy.editor as mpy
import moviepy.video.fx.all as vfx
import os


def onepic():
    global output
	#creat mask base the same size with source image 
    mask = Image.new('RGBA', base.size, (255,255,255,0))
    x, y = base.size
    #print("base size: %sx%s"%(x,y))

# one variable to vary the size of triangle
    var = y/17

# Define triangle mask position (triangle with 20 degree)
    (originx,originy) = (int(0.4*x),int(y))
    trih = int(12*var)  #fix formular for triangle height
    triw = int(4.2*var) #fix formular for triangle width
    polygonpos = [(originx,originy),
    (originx+triw,originy), 
    (originx+triw/2,originy-trih)]
    #print(trih,triw)


# Create mask
    draw = ImageDraw.Draw(mask,'RGBA')
    draw.polygon(polygonpos,(0,0,0,255))
    del draw
    mask.save("mask.png")

# Get the Alpha band from the template
    tmplt = Image.open('mask.png')
    A = tmplt.split()[3]


#make one piece of triangle on transparent bg
    [R,G,B]=base.split()
    tri = Image.merge('RGBA', (R, G, B, A))

#crop it to the exact size of triangle!! to create primary pattern
#box (left, top , right, buttom)
    box =(originx,(originy-trih),(originx+triw),originy)
    pattern_plain=tri.crop(box)
    pattern_plain.save('pattern_plain.png')
    #print('....pattern created....')


# add style to pattern
    pattern = pattern_plain
    #pattern= pattern_plain.filter(ImageFilter.BLUR)
    pattern.save('pattern_tri.png')
    #print('....stylized pattern....')


#make square canvas for the output (wide = double size of height of primary pattern)
    canvas =Image.new('RGBA',(2*trih,2*trih), (255,255,255,0))
    canvas.save('tmpcanvas.png')
    pcanvas=Image.new('RGBA',(2*trih,2*trih), (255,255,255,0))


#put pattern on the canvas
#make sure to put the tip of the triangle at the center of the canvas
#because when we rotate the center of the object is the pivot point
#note: paste command require the coordinate of top left corner
#so point to paste the pattern is . . .
    ccenterx = int(trih-triw/2) 
    canvas.paste(pattern_plain,(ccenterx,trih))


# start rotate the pattern around every 40 degree

    for i in range (0,360,40):
        tmpcanvas = canvas
        tmppat = canvas.rotate(i)
        canvas= Image.alpha_composite(tmpcanvas,tmppat)

# now we get half of the things
    half = canvas
    #print('half already')
#mirror the half and put in the space to create simple kaleidoscpoe effect
    mirror = im.mirror(half)
    half2= mirror.rotate(20)
    #print('mirrored')

#merge 2 half
    output=Image.alpha_composite(half,half2)



def makegif(outfilename):
    global clipsize
    clip = mpy.ImageSequenceClip(outfilename, fps=6)
    #make GIF
    #clip.write_gif("%s.gif"%filename) 
    clip.write_gif("final.gif")

    #check GIF size

    clipsize = int(os.stat('final.gif').st_size)
    print(clipsize)

    while clipsize>3000000:
        print("GIF is too big..resizing")
        clips = clip.resize(0.8)
        clips.write_gif("final.gif")
        clip = clips
        clipsize = int(os.stat('final.gif').st_size)
 
   
def makekaleido():
    global imgfile, filename,source,x,y,mask, base, output
    
    #put image path
    imgfile = "img.jpg"
    filename = imgfile[:-4]
    print(filename)

    #load Image
    source = Image.open(imgfile)
    x, y = source.size
    
    #resize

    maxsize = 2000
    if x > maxsize:
        newy = int(maxsize*y/x)
        source =source.resize((maxsize,newy), Image.ANTIALIAS)
        print('resized')
    
    #creat mask base the same size with source image 
    mask = Image.new('RGBA', source.size, (255,255,255,0))
    print("mask size:%sx%s"%source.size)

    #rotate source n times for a degree
    n= 20
    outfilename=[]
    for a in range(n+n-2):
        outfilename.insert(a,'0')
    a= 10
    base = source
    for i in range(n):
        base = source.rotate(31+i*a)
        onepic()
        #resize
        ox,oy=output.size
        maxpatsize = 350
        if ox > maxpatsize:
            oy = int(maxpatsize*oy/ox)
            output = output.resize((maxpatsize,oy), Image.ANTIALIAS)
        
        output.save('%s%s.jpg'%(filename,i))
        
        outfilename[i] = filename+str(i)+'.jpg'
        # make list of file names (in loop) for GIF 
        if i!=0:
            outfilename[2*n-2-i] = filename+str(i)+'.jpg'

    print(outfilename)
    makegif(outfilename)
    # check whether the gif is bigger than 5MB if bigger...resize it
    #...
    #...
    #return clipsize


#######MAIN#########
if __name__ == '__main__':
    makekaleido()

	