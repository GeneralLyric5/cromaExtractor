from itertools import count
import cv2
from rembg import remove
from PIL import Image, ImageOps
import os
import moviepy.editor as mp




flag = False


capture = cv2.VideoCapture("test.mp4")
path ="C:/Users/emili/Desktop/CromaExtractor/photos/"
pathOriginal = "C:/Users/emili/Desktop/CromaExtractor/"
cont = 0

#Crear los frames en jpg
while (capture.isOpened()):
    ret, frame = capture.read()
    if(ret == True):
        cv2.imwrite(path + "IMG_%06d.jpg" % cont,frame)  
        cont += 1
    else:
        break

#Crear los frames sin fondo

max = cont
cont = 0
for cont in range(0,max):
    with open(path +"IMG_%06d.jpg" % cont,'rb') as i:
        with open(path +"IMG_%06d.png" % cont,'wb') as o:
                input = i.read()
                output = remove(input,providers=['CPUExecutionProvider'] )
                o.write(output)
#Crear los Frames con fondo verde
cont = 0
for cont in range(0,max):
    greenFrame = Image.open(path +"IMG_%06d.png" % cont)
    alfa = greenFrame.getchannel("A")
    #Verde
    verde = Image.new("RGB", greenFrame.size, (0, 255, 0))
    #axul
    #verde = Image.new("RGB", greenFrame.size, (0, 0, 255))
    alfa = ImageOps.invert(alfa)
    greenFrame.paste(verde, mask=alfa)
    greenFrame.save(path +"IMG_%06d.png" % cont)

cont = 0

frame = cv2.imread(path +"IMG_%06d.png" % cont)
height, width, layers = frame.shape
video = cv2.VideoWriter(path+"video.mp4", cv2.VideoWriter_fourcc(*"avc1"), 30, (width, height))

for cont in range(0,max):
    video.write(cv2.imread(path +"IMG_%06d.png" % cont))
    os.remove(path +"IMG_%06d.png" % (cont))
    os.remove(path +"IMG_%06d.jpg" % (cont))


video.release()
#Audio Transfer
original_video = mp.VideoFileClip("test.mp4")
final_video = mp.VideoFileClip(path + "video.mp4")
final_video = final_video.set_audio(original_video.audio)
final_video.write_videofile(path + "videoAudio.mp4", codec="libx264")


capture.release()
cv2.destroyAllWindows()
os.remove(path+"video.mp4")




            
          

           