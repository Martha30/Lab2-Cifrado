#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#Ejercicio 1
#26/07/2021

import struct

def word(w):
  # 2 byte
  return struct.pack('=h', w)
def char(c):
  return struct.pack('=c',c.encode('ascii'))
def dword(d):
  # 4 bytes
  return struct.pack('=l', d)
def color(r, g, b):
  return bytes([b, g, r])  

#MIS VARIABLES GLOBALES
BLACK = color(3, 3, 3)
WHITE = color(255, 255, 255)

class Renderer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.current_color = WHITE
    self.clear()

#(05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
  def glInit():
    pass

#05 puntos) Deben crear una función glCreateWindow(width, height) que inicialice su framebuffer con un tamaño (la imagen resultante va a ser de este tamaño
  def glCreateWindow(self,width, height):
    self.width = width
    self.height = height
    self.glClear()
    self.glViewPort(0, 0, width, height)

#(10 puntos)  Deben crear una función glViewPort(x, y, width, height) que defina el área de la imagen sobre la que se va a poder dibujar (hint)
  def glViewPort(self, x, y, width, height):
    self.viewPortX = x
    self.viewPortY = y
    self.viewPortWidth = width
    self.viewPortHeight = height

#(20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
  def clear(self):
    self.framebuffer = [
      [BLACK for x in range(self.width)]
      for y in range(self.height)
    ]
#(10 puntos) Deben crear una función glClearColor(r, g, b) con la que se pueda cambiar el color con el que funciona glClear(). Los parámetros deben ser números en el rango de 0 a 1.
  def glClearColor(self, r, g, b):
    self.clearColor = color(r, g, b)

#(15 puntos) Deben crear una función glColor(r, g, b) con la que se pueda cambiar el color con el que funciona glVertex(). Los parámetros deben ser números en el rango de 0 a 1.
  def glColor(self, r, g, b):
    self.current_color= color(r,g,b)

 
  def render(self):
   self.write('imagen.bmp')
#--Funcion para pintar un pixel
#--Un punto de un color en especidico, coordenadas en x,y y algun color
  def point(self, x, y, color = None):
    self.framebuffer[y][x] = color or self.current_color
  
  #Creación de la función glLine
  def glLine(self, a1, a0, color = None ):
    x0 = a0.x
    x1 = a1.x
    y0 = a0.y
    y1 = a1.y

    #La pendiente de la línea
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    # Dibuja una línea
  

    

#(05 puntos) Deben crear una función glFinish() que escriba el archivo de imagen
  def glFinish(self, filename : str = 'imagen.bmp'):
    with open(filename, "wb") as file:
        #file header 14 bytes
        file.write(char('B'))
        file.write(char('M'))
        file.write(dword(14 + 40 + 3 *(self.width * self.height)))
        file.write(dword(0))
        file.write(dword(14 + 40))

        #info header 40 bytes
        file.write(dword(40))
        file.write(dword(self.width))
        file.write(dword(self.height))
        file.write(word(1))
        file.write(word(24))
        file.write(dword(0))
        file.write(dword( 3 *(self.width * self.height)))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        file.write(dword(0))
        #bitmap
        for y in range(self.height):
            for x in range(self.width):
                file.write(self.framebuffer[y][x])
        

r = Renderer(1024, 768)
r.current_color = color(255, 255, 255)
r.point(10, 10)
r.glFinish()


