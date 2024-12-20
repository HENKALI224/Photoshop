#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtWidgets import (
   QApplication, QWidget,
   QFileDialog,
   QLabel, QPushButton, QListWidget,
   QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt # нужна константа Qt.KeepAspectRatio для изменения размеров с сохранением пропорций
from PyQt5.QtGui import QPixmap # оптимизированная для показа на экране картинка


from PIL import Image
from PIL.ImageQt import ImageQt # для перевода графики из Pillow в Qt 
from PIL import ImageFilter
from PIL.ImageFilter import (
   BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE,
   EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN,
   GaussianBlur, UnsharpMask
)


app = QApplication([])#Создаем приложение
main_win = QWidget()# Cоздаем окно
main_win.setWindowTitle('Easy Editor')#Создание названия окна
main_win.resize(700, 500)


v1 = QVBoxLayout()
h2 = QHBoxLayout()
v3 = QVBoxLayout()#создаём вертикальный лейоут
h4 = QHBoxLayout()

list_pictures = QListWidget()#Список фото

lb_paint = QLabel('Картинка')

# кнопки
papka = QPushButton('Папка')
left = QPushButton('Лево')
right = QPushButton('Право')
miror = QPushButton('Зеркало')
fast = QPushButton('Резкость')
chb = QPushButton('Ч/Б')

h2.addWidget(left)
h2.addWidget(right)
h2.addWidget(miror)
h2.addWidget(fast)
h2.addWidget(chb)

v1.addWidget(papka)
v1.addWidget(list_pictures)

v3.addWidget(lb_paint)
v3.addLayout(h2)

h4.addLayout(v1)
h4.addLayout(v3)

main_win.setLayout(h4)



main_win.show()

workdir = ''

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFilenamesList():
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir),extensions)
    list_pictures.clear()
    for filename in filenames:
        list_pictures.addItem(filename)




main_win.show()
papka.clicked.connect(showFilenamesList)
class ImageProcesor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'modyfiet/'

    def loadImage(self,dir,filename):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        lb_paint.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_paint.width(),lb_paint.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        lb_paint.setPixmap(pixmapimage)
        lb_paint.show()

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def saveImage(self):
        #path = os.path.join(self.dir, self.save_dir)
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)#создаем папку в конце пути
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_miror(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)   

    def do_fast(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir,self.save_dir,self.filename)
        self.showImage(image_path)

def showChosenImage():
    if list_pictures.currentRow() >= 0:
        filename = list_pictures.currentItem().text()
        workimage.loadImage(workdir,filename)
        image_path = os.path.join(workimage.dir,workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcesor()
list_pictures.currentRowChanged.connect(showChosenImage)
chb.clicked.connect(workimage.do_bw)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
miror.clicked.connect(workimage.do_miror)
fast.clicked.connect(workimage.do_fast)


app.exec_()