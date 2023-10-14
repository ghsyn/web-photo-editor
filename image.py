import os
import math
import numpy as np
from math import *
from tkinter import *  # GUI 라이브러리
from tkinter import messagebox
from tkinter.filedialog import *
from tkinter.simpledialog import *
from tkinter import simpledialog
import cv2  # OpenCV

def malloc(h, w, init=0) : 
    global window, canvas, paper
    global m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    retMemory = [ [ [init for _ in range(w)] for _ in range(h)] for _ in range(RGB)  ]
    return retMemory


def openImage() : # 이미지 불러오기
    global cvInPhoto, cvOutPhoto, window, canvas, paper
    global m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    filename = askopenfilename(parent=window, filetypes=(('컬러 파일', '*.jpg;*.png;*.bmp;*.tif'),
                                                         ('All Files', '*.*')))

    cvInPhoto = cv2.imread(filename)

    m_height, m_width = cvInPhoto.shape[:2]

    m_InputImage = malloc(m_height, m_width)

    for i in range(m_height):
        for k in range(m_width):    
            m_InputImage[B][i][k] = cvInPhoto.item(i, k, R) # 0, B
            m_InputImage[G][i][k] = cvInPhoto.item(i, k, G) # 1, G
            m_InputImage[R][i][k] = cvInPhoto.item(i, k, B) # 2, R

    equalImage()


def saveImage(): # 이미지 저장하기
    global window, canvas, paper
    global m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    if filename == None:
        return

    saveCvPhoto = np.zeros((m_Re_height, m_Re_width, 3), np.uint8)

    for i in range(m_Re_height):
        for k in range(m_Re_width):
            tup = tuple(([m_OutputImage[B][i][k], m_OutputImage[G][i][k], m_OutputImage[R][i][k]]))
            saveCvPhoto[i, k] = tup

    saveFp = asksaveasfile(parent=window, mode='wb', defaultextension='.',
                           filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))

    if saveFp == '' or saveFp == None:
        return

    cv2.imwrite(saveFp.name, saveCvPhoto)

    print('Save~')

def closeWindow(): # 에디터 종료하기
    # window.quit()
    window.destroy()

def displayImage() : # 이미지 보여주기
    global cvInPhoto, cvOutPhoto, window, canvas, paper,m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    if canvas != None :
        canvas.destroy()

    window.geometry(str(int(m_Re_width * 1.0)) + 'x' + str(int(m_Re_height * 1.0)))
    canvas = Canvas(window, height=m_Re_height, width=m_Re_width)
    paper = PhotoImage(height=m_Re_height, width=m_Re_width)
    canvas.create_image((m_Re_width / 2, m_Re_height / 2), image=paper, state='normal')


    rgbString = ''  
    for i in range(m_Re_height):
        tmpString = ''  
        for k in range(m_Re_width):
            r = m_OutputImage[R][i][k]
            g = m_OutputImage[G][i][k]
            b = m_OutputImage[B][i][k]
            tmpString += "#%02x%02x%02x " % (r, g, b)
        rgbString += "{" + tmpString + '} '

    paper.put(rgbString)
    canvas.pack()
    status.configure(text='이미지 정보 : ' + str(m_Re_width) + 'x' + str(m_Re_height)
                     + '    ' + filename)

def toOutImageCV():
    global cvInPhoto, cvOutPhoto, window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    m_Re_height, m_Re_width = cvOutPhoto.shape[:2]

    m_OutputImage = malloc(m_Re_height + 2, m_Re_width + 2)


    for i in range(1, m_Re_height):
        for k in range(1, m_Re_width):    
            if cvOutPhoto.ndim == 2 :
                m_OutputImage[B][i][k] = cvOutPhoto.item(i, k)
                m_OutputImage[G][i][k] = cvOutPhoto.item(i, k)
                m_OutputImage[R][i][k] = cvOutPhoto.item(i, k)
            else:
                m_OutputImage[B][i][k] = cvOutPhoto.item(i, k, R)   # 0, B
                m_OutputImage[G][i][k] = cvOutPhoto.item(i, k, G)   # 1, G
                m_OutputImage[R][i][k] = cvOutPhoto.item(i, k, B)   # 2, R


def  equalImage() :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    
    if filename == None:
        return


    m_Re_height = m_height; m_Re_width = m_width

    m_OutputImage = malloc(m_Re_height, m_Re_width)


    for rgb in range(RGB):
        for i in range(m_height) :
            for k in range(m_width) :
                m_OutputImage[rgb][i][k] = m_InputImage[rgb][i][k]

    displayImage()
    
    
def zoomInImage():
    global cvInPhoto, cvOutPhoto, window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    if filename == None:
        return
   
    cvOutPhoto = cv2.pyrUp(cvInPhoto)
    toOutImageCV()  

    displayImage()   
    
def zoomOutImage():
    global cvInPhoto, cvOutPhoto, window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    
    if filename == None:
        return
    
    cvOutPhoto=cv2.pyrDown(cvInPhoto)
    toOutImageCV()
    
    displayImage()

def rotateImage():  
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    
    if filename == None:
        return

  
    angle = askinteger('회전', '각도 입력(1~360):')
    rad = (3.14 / 180) * angle

    m_Re_height = int(abs(m_width * cos(rad)) + abs(m_height * sin(rad)))
    m_Re_width = int(abs(m_width * sin(rad)) + abs(m_height * cos(rad)))

   
    m_OutputImage = malloc(m_Re_height, m_Re_width)

 
    cen_x = cos(rad) * (m_height / 2) - sin(rad) * (m_width / 2)
    cen_y = sin(rad) * (m_height / 2) + cos(rad) * (m_width / 2)

    dif_x = (m_Re_height / 2) - cen_x
    dif_y = (m_Re_width / 2) - cen_y

    for i in range(m_height) :
        for k in range(m_width) :
            new_i = cos(rad) * i - sin(rad) * k + dif_x
            new_k = sin(rad) * i + cos(rad) * k + dif_y

            if (new_i >= 0 and new_i < m_Re_height) and (new_k >= 0 and new_k < m_Re_width) :
                m_OutputImage[R][int(new_i)][int(new_k)] = m_InputImage[R][i][k]
                m_OutputImage[G][int(new_i)][int(new_k)] = m_InputImage[G][i][k]
                m_OutputImage[B][int(new_i)][int(new_k)] = m_InputImage[B][i][k]

    displayImage()


def mirrorImage():
    global cvInPhoto, cvOutPhoto, window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    
    if filename == None:
        return
    
    cvOutPhoto=cv2.flip(cvInPhoto,1)
    toOutImageCV()
    
    displayImage()

def updownImage():
    global cvInPhoto, cvOutPhoto, window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    
    if filename == None:
        return
    
    cvOutPhoto=cv2.flip(cvInPhoto,0)
    toOutImageCV()
    
    displayImage()

def  lightImage() :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

   
    if filename == None :
        return

    
    m_Re_height = m_height; m_Re_width = m_width

    
    m_OutputImage = malloc(m_Re_height, m_Re_width)

    
    value = askinteger('밝게', '정수값 입력(1~255) :', minvalue=1, maxvalue=255)

    for rgb in range(RGB):
        for i in range(m_height) :
            for k in range(m_width) :
                pixel = m_InputImage[rgb][i][k] + value

                if pixel > 255 :
                    m_OutputImage[rgb][i][k] = 255
                else :
                    m_OutputImage[rgb][i][k] = pixel

    displayImage()

def  darkImage() :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename

    
    if filename == None :
        return

    
    m_Re_height = m_height; m_Re_width = m_width

    
    m_OutputImage = malloc(m_Re_height, m_Re_width)

   
    value = askinteger('어둡게', '정수값 입력(1~255) :', minvalue=1, maxvalue=255)

    for rgb in range(RGB):
        for i in range(m_height) :
            for k in range(m_width) :
                pixel = m_InputImage[rgb][i][k] - value

                if pixel < 0 :
                    m_OutputImage[rgb][i][k] = 0
                else :
                    m_OutputImage[rgb][i][k] = pixel

    displayImage()



sx, sy, ex, ey = [0] * 4

def  bwImage() :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey

    canvas.bind("<Button-1>",bwImage_click)
    canvas.bind("<ButtonRelease-1>", bwImage_drop)
    canvas.bind("<Button-3>", bwImage_rClick)
    canvas.bind("<B1-Motion>", moveMouse)

boxLine = None
def moveMouse(event) :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey, boxLine

    ex = event.x; ey = event.y

    if not boxLine :
        pass
    else :
        canvas.delete(boxLine)

    boxLine = canvas.create_rectangle(sx,sy,ex,ey, fill=None)

def bwImage_click(event) :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey

    sx = event.x
    sy = event.y

def bwImage_drop(event) :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey

    ex = event.x
    ey = event.y

    if sx > ex :
        sx, ex = ex, sx
    if sy > ey :
        sy, ey = ey, sy

    __bwImage()
    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<B1-Motion>" )
    canvas.unbind("<Button-3>")

def bwImage_rClick(event) :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey

    sx = 0;    sy = 0;    ex = m_width -1;    ey = m_height -1

    __bwImage()

    canvas.unbind("<Button-1>")
    canvas.unbind("<ButtonRelease-1>")
    canvas.unbind("<B1-Motion>" )
    canvas.unbind("<Button-3>")

def __bwImage() :
    global window, canvas, paper, m_InputImage, m_OutputImage, m_width, m_height, m_Re_width, m_Re_height, filename
    global sx, sy, ex, ey

    if filename == None :
        return

   
    m_Re_height = m_height; m_Re_width = m_width

    
    m_OutputImage = malloc(m_Re_height, m_Re_width)

   
    for i in range(m_height) :
        for k in range(m_width) :
            
            if (( sx <= k <= ex) and ( sy <= i <= ey)):
                value = (m_InputImage[R][i][k] + m_InputImage[G][i][k] + m_InputImage[B][i][k])/3
                if value > 128 :
                    m_OutputImage[R][i][k] = 255
                    m_OutputImage[G][i][k] = 255
                    m_OutputImage[B][i][k] = 255
                else :
                    m_OutputImage[R][i][k] = 0
                    m_OutputImage[G][i][k] = 0
                    m_OutputImage[B][i][k] = 0
            else :
                m_OutputImage[R][i][k] = m_InputImage[R][i][k]
                m_OutputImage[G][i][k] = m_InputImage[G][i][k]
                m_OutputImage[B][i][k] = m_InputImage[B][i][k]

    displayImage()

window, canvas, paper = None, None, None
m_InputImage, m_OutputImage = None, None    
m_width, m_height, m_Re_width, m_Re_height = [0] * 4
filename = None
R, G, B = 0, 1, 2   
RGB = 3

cvInPhoto, cvOutPhoto = None, None

if __name__ == '__main__' :

    window = Tk()

    mainMenu = Menu(window)
    window.config(menu=mainMenu)
    window.title('포토 에디터')
    window.geometry('500x500')
    status = Label(window, text='이미지 정보 :', bd=1, relief=SUNKEN, anchor=W)  # 상태창
    status.pack(side=BOTTOM, fill=X)

    # 메뉴 생성
    fileMenu = Menu(mainMenu)  # 메인 메뉴
    mainMenu.add_cascade(label='이미지', menu=fileMenu) 
    fileMenu.add_command(label='이미지 불러오기', command=openImage) 
    fileMenu.add_command(label='이미지 저장하기', command=saveImage)
    fileMenu.add_command(label='이미지 초기화', command=equalImage)
    fileMenu.add_command(label='에디터 종료하기', command=closeWindow)

    photoMenu = Menu(mainMenu)  # 사진 편집 메뉴
    mainMenu.add_cascade(label='편집', menu=photoMenu)
    photoMenu.add_command(label='확대', command=zoomInImage)
    photoMenu.add_command(label='축소', command=zoomOutImage)
    photoMenu.add_command(label='회전', command=rotateImage)
    photoMenu.add_command(label='좌우반전', command=mirrorImage)
    photoMenu.add_command(label='상하반전',command=updownImage)

    lightMenu = Menu(mainMenu) # 사진 밝기 조절 메뉴
    mainMenu.add_cascade(label='밝기 조절', menu=lightMenu)
    lightMenu.add_command(label='밝게', command=lightImage)
    lightMenu.add_command(label='어둡게', command=darkImage)


    window.mainloop()