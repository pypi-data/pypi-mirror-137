from flask import Flask, render_template, request
import flask_socketio as f_socket
from PIL import Image
from threading import Thread
import urllib
import random as r
app = Flask('app', static_url_path="", static_folder="/")
socket = f_socket.SocketIO(app)
#kaboom!
endstring = '<div id="boody">'
script = '<script src="https://code.jquery.com/jquery-3.6.0.js"></script><script>' + """$(document).keydown(function(key) {
  fetch(`/keydown/${key.key}`).then(function(r) {
    r.text().then(function(t) {
      if(t.includes('BODY:ERRCOL')) {
        t = t.replace('BODY:ERRCOL', '')
        $(document.body).css('background-color', 'black')
      }
      $('#boody').html(t)
    })
  })
})
"""
keysandfuncs = {'ArrowUp':[], 'ArrowDown':[], 'ArrowLeft':[], 'ArrowRight':[], 'w':[], 'a':[], 's':[], 'd':[]}
socketevents = {}
keydownfunc = None
actions = []
headstring = ''
screenobjs = []
scobids = []
filetouse = 'index.html'
def kablooey(title=False, file=False):
  global headstring, filetouse
  if title:
    headstring += '<title>' + title + '</title>'
  if file:
    filetouse = file
def add(item, x, y, outline=False, opacity=False, z=False, tags=[], comps=[]):
  global endstring
  endstr = endstring[:]
  endstr = ''
  item.x = x
  item.y = y
  morestyls = outline.add_style() if outline else ''
  morestyls += opacity.add_style() if opacity else ''
  morestyls += z.add_style() if z else ''
  taggies = ' '.join(tags)
  idtogib = r.randint(0, 10000)
  while idtogib in scobids:
    idtogib = r.randint(0, 10000)
  if type(item) == Sprite:
    endstr += f"<img id='{idtogib}' {item.get_img_attrs().replace('morestyles', morestyls)}></img>"
  elif type(item) in [Rect, Circle]:
    endstr += f"<div id='{idtogib}' {item.get_div_attrs().replace('morestyles', morestyls)}></div>"
  elif type(item) == Text:
    endstr += f"<p id='{idtogib}' {item.get_p_attrs().replace('morestyles', morestyls)}>{item.text}</p>"
  theobj = ScreenObj(endstr, x, y, '__', taggies)
  theobj.id_ = idtogib
  if type(item) in [Sprite, Rect]:
    theobj.size = {'width':item.width, 'height':item.height}
  elif type(item) == Circle:
    theobj.size = {'width':item.radius, 'height':item.radius}
  elif type(item) == Text:
    pass
  if Area() in comps:
    theobj.area = Area(theobj)
  if Body() in comps:
    theobj.body = Body(theobj)
  if ArrowMove() in comps:
    inst = comps[comps.index(ArrowMove())]
    theobj.mover = ArrowMove(inst.move, theobj)
  if LetterMove() in comps:
    inst = comps[comps.index(LetterMove())]
    theobj.mover = LetterMove(inst.move, theobj)
  endstring += endstr
  return theobj
#Screen objects
class ScobDict:
  def __init__(self, data, scob):
    self.data = data
    self.scob = scob
  def __setitem__(self, name, value):
    global endstring
    fel = self.scob.el[:]
    if name == 'y':
      self.scob.el = self.scob.el.replace('top:'+str(self.data[name])+'px;', 'top:'+str(value)+'px;')
    elif name == 'x':
      self.scob.el = self.scob.el.replace('left:'+str(self.data[name])+'px;', 'left:'+str(value)+'px;')
    elif name == 'width':
      self.scob.el = self.scob.el.replace('width:'+str(self.data[name])+'px;', 'width:'+str(value)+'px;')
    elif name == 'height':
      self.scob.el = self.scob.el.replace('height:'+str(self.data[name])+'px;', 'height:'+str(value)+'px;')
    endstring = endstring.replace(fel, self.scob.el)
    self.data[name] = value
  def __getitem__(self, name):
    return self.data[name]
class ScreenObj:
  def __init__(self, el, x, y, size, tags):
    self.el = el
    self.pos = ScobDict({'x':x, 'y':y}, self)
    self.tags = tags
    self.size = {'width':size[0], 'height':size[1]}
    screenobjs.append(self)
  def kill(self):
    global endstring
    endstring = endstring.replace(self.el, '')
    self.tags = []
    scobids.remove(self.id_)
    screenobjs.remove(self)
class Sprite:
  def __init__(self, path, width=False, height=False):
    self.path = path
    self.width = width
    self.height = height
    if not self.width and not self.height:
      self.width, self.height = Image.open(path).size
  def get_img_attrs(self):
    end = f"src='{self.path}' style='top:{self.y}px; left:{self.x}px; position:absolute; morestyles'"
    if self.width:
      end += f' width={self.width}'
    if self.height:
      end += f' height={self.height}'
    return end
class Rect:
  def __init__(self, width, height, color=(255, 255, 255)):
    self.width = width
    self.height = height
    self.color = color
  def get_div_attrs(self):
    end = f'style="width: {self.width}px; height: {self.height}px; background-color: rgb{self.color}; top:{self.y}px; left:{self.x}px; position:absolute; morestyles"'
    return end
class Circle:
  def __init__(self, radius, color=(255, 255, 255)):
    self.radius = radius
    self.color = color
  def get_div_attrs(self):
    end = f'style="border-radius: 50%; background-color: rgb{self.color}; width: {self.radius}px; height: {self.radius}px; position:absolute; top:{self.y}px; left:{self.x}px; morestyles"'
    return end
class Text:
  def __init__(self, text, size=16, font='sans-serif', color=(0, 0, 0)):
    self.text = text
    self.size = size
    self.font = font
    self.color = color
  def get_p_attrs(self):
    end = f'style="font-size: {self.size}px; position:absolute; top:{self.y}px; left:{self.x}px; margin: 0px; font-family: {self.font}; color:rgb{self.color}; morestyles"'
    return end
#Styling classes
class Outline:
  def __init__(self, thickness, color=(0, 0, 0)):
    self.thickness = thickness
    self.color = color
  def add_style(self):
    return f'border-width: {self.thickness}px; border-color: rgb{self.color}; border-style: solid;'
class Opacity:
  def __init__(self, opacity):
    self.opacity = opacity
  def add_style(self):
    return f'opacity: {self.opacity};'
class Z:
  def __init__(self, z):
    self.z = z
  def add_style(self):
    return f'z-index: {self.z}'
#Components
class Area:
  def __init__(self, me=None):
    self.me = me
    self.iss = 'area'
  def is_colliding(self, tag):
    elswtag = []
    for i in screenobjs:
      if tag in i.tags:
        elswtag.append(i)
    for i in elswtag:
      xin = i.pos['x']-self.me.size['width'] < self.me.pos['x'] < i.pos['x']+self.me.size['width']
      yin = self.me.pos['y'] in range(i.pos['y']-self.me.size['height'], i.pos['y']+self.me.size['height'])
      if xin and yin:
        return True
  def __eq__(self, other):
    return self.iss == other.iss
class Body:
  def __init__(self, me=None):
    self.me = me
    self.iss = 'body'
  def __eq__(self, other):
    return self.iss == other.iss
class ArrowMove:
  def __init__(self, move=10, me=None):
    self.me = me
    self.move = move
    self.iss = 'arrowmove'
    def upp():
      self.me.pos['y'] -= move
    def down():
      self.me.pos['y'] += move
    def left():
      self.me.pos['x'] -= move
    def right():
      self.me.pos['x'] += move
    if me == None:
      return
    keysandfuncs['ArrowUp'] += [upp]
    self.ufi = len(keysandfuncs['ArrowUp'])-1
    keysandfuncs['ArrowDown'] += [down]
    self.dfi = len(keysandfuncs['ArrowDown'])-1
    keysandfuncs['ArrowRight'] += [right]
    self.rfi = len(keysandfuncs['ArrowLeft'])-1
    keysandfuncs['ArrowLeft'] += [left]
    self.lfi = len(keysandfuncs['ArrowRight'])-1
  def change_speed(self, newspeed):
    def upp():
      self.me.pos['y'] -= newspeed
    def down():
      self.me.pos['y'] += newspeed
    def left():
      self.me.pos['x'] -= newspeed
    def right():
      self.me.pos['x'] += newspeed
    keysandfuncs['ArrowUp'][self.ufi] = upp
    keysandfuncs['ArrowDown'][self.dfi] = down
    keysandfuncs['ArrowRight'][self.rfi] = right
    keysandfuncs['ArrowLeft'][self.lfi] = left
  def __eq__(self, other):
    return self.iss == other.iss
class LetterMove:
  def __init__(self, move=10, me=None):
    self.me = me
    self.move = move
    self.iss = 'lettermove'
    def upp():
      self.me.pos['y'] -= move
    def down():
      self.me.pos['y'] += move
    def left():
      self.me.pos['x'] -= move
    def right():
      self.me.pos['x'] += move
    if me == None:
      return
    keysandfuncs['w'] += [upp]
    self.ufi = len(keysandfuncs['w'])-1
    keysandfuncs['s'] += [down]
    self.dfi = len(keysandfuncs['s'])-1
    keysandfuncs['d'] += [right]
    self.rfi = len(keysandfuncs['d'])-1
    keysandfuncs['a'] += [left]
    self.lfi = len(keysandfuncs['a'])-1
  def change_speed(self, newspeed):
    def upp():
      self.me.pos['y'] -= newspeed
    def down():
      self.me.pos['y'] += newspeed
    def left():
      self.me.pos['x'] -= newspeed
    def right():
      self.me.pos['x'] += newspeed
    keysandfuncs['w'][self.ufi] = upp
    keysandfuncs['s'][self.dfi] = down
    keysandfuncs['d'][self.rfi] = right
    keysandfuncs['a'][self.lfi] = left
  def __eq__(self, other):
    return self.iss == other.iss
#Events
def key_down(key):
  def inner(func):
    if key in keysandfuncs:
      keysandfuncs[key].append(func)
    else:
      keysandfuncs[key] = [func] 
  return inner
def action():
  def inner(func):
    actions.append(func)
  return inner
#Multiplayer
def client_event(name, js=''):
  def i(f):
    global script
    script += """suckit.on('{0}', (data) => {{
  fetch(`/socketio?event={0}&data=${JSON.stringify(data)}`).then(function(r) {{
    {1}
    r.text().then(function(t) {{
      if(t.includes('BODY:ERRCOL')) {{
        t = t.replace('BODY:ERRCOL', '')
        $(document.body).css('background-color', 'black')
      }}
      $('#boody').html(t)
    }})
  }})
}})
}})
""".format(name, js, '{', '}')
    socketevents[name] = f
  return i
#Routes
@app.route('/')
def hello_world():
  return render_template(filetouse, kaboom=endstring+'</div>', scrpt=script+'</script>', headstf=headstring)
@app.route('/keydown/<key>')
def keydown(key):
  try:
    for i in keysandfuncs[key]:
      try:
        i()
      except Exception as e:
        global endstring
        endstring = f'<div id="boody" style="color:red; font-family:monospace;"><h1>{e}</h1> BODY:ERRCOL'
  except KeyError:
    pass
  return endstring+'</div>'
@app.route('/socketio')
def socketioroute():
  if request.method == 'GET':
    if str(request.query_string)[2:-1] != '':
      query_string = str(request.query_string)[2:-1].split('&')
      for i in range(0, len(query_string)):
        query_string[i] = query_string[i].split('=')
      form = dict(query_string)
      for i in form:
        form[i] = urllib.parse.unquote(form[i]).replace('+', ' ')
    else:
      form = {}
  socketevents[form['event']](form['data'])
#ROON
def runner():
  open('templates/' + filetouse, 'w').write("""<!doctype html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <style>
  </style>
  {{ headstf|safe }}
</head>
<body>
{{ kaboom|safe }}
{{ scrpt|safe }}
</body>
  """)
  socket.run(app, host='0.0.0.0', port=8080)
def run():
  server = Thread(target=runner)
  server.start()