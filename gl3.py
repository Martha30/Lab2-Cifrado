#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#Ejercicio 1
#26/07/2021

#Universidad del Valle de Guatemala
#Laurelinda Gómez 19501
#26/07/2021

import struct 



def char(c):
  return struct.pack("=c", c.encode('ascii'))

# 2 byte
def word(n):
  return struct.pack("=h", n)

# 4 bytes
def dword(n):
  return struct.pack("=l", n)

def color(r, g, b):
  if (r <= 1 and g <= 1 and b <= 1):
    return bytes([int(b*255), int(g*255), int(r*255)])
  return bytes([b, g, r])

#MIS VARIABLES GLOBALES
BLACK = color(3,3,3)
WHITE = color(255,255,255)

class Renderer(object):
  def __init__(self, width, height):
    self.glInit(width, height)
  #(05 puntos) Deben crear una función glInit() que inicialice cualquier objeto interno que requiera su software renderer
  def glInit(self, width, height):
    self.current_color = WHITE
    self.clear_color = BLACK
    self.glCreateWindow(width, height)
#(20 puntos) Deben crear una función glClear() que llene el mapa de bits con un solo color
  def glClear(self):
    self.framebuffer = [
      [self.clear_color for x in range(self.width)]
      for y in range(self.height)
    ]
#(10 puntos) Deben crear una función glClearColor(r, g, b) con la que se pueda cambiar el color con el que funciona glClear(). Los parámetros deben ser números en el rango de 0 a 1.
  def glClearColor(self, r, g, b):
    self.clear_color = color(r, g, b)

#05 puntos) Deben crear una función glCreateWindow(width, height) que inicialice su framebuffer con un tamaño (la imagen resultante va a ser de este tamaño
  def glCreateWindow(self, width, height):
    self.width = width
    self.height = height
    self.glClear()
    self.glViewPort(0, 0, self.width, self.height)

#(10 puntos)  Deben crear una función glViewPort(x, y, width, height) que defina el área de la imagen sobre la que se va a poder dibujar (hint) 
  def glViewPort(self, x, y, width, height):
    self.vpx = int(x) 
    self.vpy = int(y) 
    self.vpwidth = int(width)
    self.vpheight = int(height)

#(15 puntos) Deben crear una función glColor(r, g, b) con la que se pueda cambiar el color con el que funciona glVertex(). Los parámetros deben ser números en el rango de 0 a 1.
  def glColor(self, r, g, b):
    self.current_color = color(r, g, b)

  def glVertex(self, x, y):
    x = int( (x+1)*(self.vpwidth/2)+self.vpx )
    y = int( (y+1)*(self.vpheight/2)+self.vpy )
    self.framebuffer[y-1][x-1] = self.current_color

  #Creación de la función glLine
 #Codigo basado en la clase
   
  def glLine(self, x0, y0, x1, y1):
    x0 = int( (x0+1)*(self.vpwidth/2)+self.vpx )
    y0 = int( (y0+1)*(self.vpheight/2)+self.vpy )
    x1 = int( (x1+1)*(self.vpwidth/2)+self.vpx )
    y1 = int( (y1+1)*(self.vpheight/2)+self.vpy )
    dy = abs(y1 - y0)
    dx = abs(x1 - x0)

    steep = dy > dx
    if x1 < x0:
      t,t1 = x0,y0
      x0, y0 = x1, y1
      x1, y1 = t, t1
      

    if steep:
      x0, y0 = y0, x0
      x1, y1 = y1, x1

      dy = abs(y1 - y0)
      dx = abs(x1 - x0)

    offset = 0 * 2 * dx
    threshold = 0.5 * 2 * dx
    y = y0
     #La pendiente de la línea
    # y = mx + b
    points = []
    for x in range(x0, x1):
      if steep:
        points.append((y, x))
      else:
        points.append((x, y))

      offset += (dy/dx) * 2 * dx
      if offset >= threshold:
        y += 1 if y0 < y1 else -1
        threshold += 1 * 2 * dx
    for point in points:
      self.glVertex(((point[0]-self.vpx)*(2/self.vpwidth)-1), ((point[1]-self.vpy)*(2/self.vpheight)-1))

 
  
#Método para escribir un archivo 
  def write(self, filename):   
    with open(filename, 'bw') as file:
      #file header 14 bytes
      file.write(char('B'))
      file.write(char('M'))      
      file.write(dword(14 + 40 + (self.width * self.height * 3))) 
      file.write(dword(0))
      file.write(dword(14 + 40))
       #info header 40 bytes
      file.write(dword(40))
      file.write(dword(self.width))
      file.write(dword(self.height))
      file.write(word(1))
      file.write(word(24))
      file.write(dword(0))
      file.write(dword(self.width * self.height * 3))
      file.write(dword(0))
      file.write(dword(0))
      file.write(dword(0))
      file.write(dword(0))

      #bitmap
      for y in range(self.height):
        for x in range(self.width):
          file.write(self.framebuffer[y][x])

#(05 puntos) Deben crear una función glFinish() que escriba el archivo de imagen   
  def glFinish(self, fileName):
    self.write(fileName + ".bmp")

    
r = Renderer(500, 500)
r.glColor(255, 255, 255)
r.glLine(-1, -1, 0.5, 0.5)
r.glFinish("imagen")
