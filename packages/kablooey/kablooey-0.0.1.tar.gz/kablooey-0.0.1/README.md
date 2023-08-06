# Kaboom...
# In python!
[Original Kaboom(JS)](https://kaboomjs.com)  
I created a version of kaboom in python, for people who don't want to use JS.  
[Open docs in browser](https://kaboom-in-python.shivankchhaya.repl.co/docs)
# Start Game
### `kablooey(title=False, file=False) => None`
##### Title sets the title of the window. File is the file to write the content in
```py
import kaboompython as k
k.kablooey("Kaboom... in python!", "templates/index.html")
#This would name the window "Kaboom... in python!" and would write the content in "templates/index.html"
#...
#Your code here...
#Your code must have these lines at the end!
k.run()
while True:
  for action in k.actions:
    action()
```
# Screen Objects
### `add(item, x, y, outline=False, opacity=False, z=False, tags=[], comps=[]) => ScreenObj`
##### Add an object to the screen.
```py
k.add(k.Sprite('/dod.jpeg'), 0, 0, outline=k.Outline(10), opacity=k.Opacity(0.5), z=k.Z(2), tags=['dod', 'jpeg'], comps=[k.ArrowMove()])
#This would add:
#The "dod.jpeg" image
#At x: 0, y: 0
#with a black outline of 10 pixels
#with 50% opacity
#at a z-index of 2
#with tags of "dod" and "jpeg"
#with the ArrowMove component
```
### `Sprite(path, width=False, height=False) => Sprite`
##### Returns a sprite. Width and height will be the dimensions of the image unless otherwise said.
```py
s = k.Sprite('/dod.jpeg', 30, 30)
#Use k.add to add to screen
k.add(s, 0, 0)
```
### `Rect(width, height, color=(255, 255, 255)) => Rect`
##### Returns a rectangle. Color must be a tuple with 3 items being these accordingly: red, green, blue
```py
r = k.Rect(50, 50)
k.add(r, 0, 0)
#This adds a white rectangle thats 50 px wide and 50 px high
```
### `Circle(radius, color=(255, 255, 255)) => Circle`
##### Returns a circle. Radius is radius of circle, and color is color of circle.
```py
c = k.Circle(50)
k.add(c, 0, 0)
#This adds a white circle with 50 radius
```
### `Text(text, size=16, font='sans-serif', color=(0, 0, 0)) => Text`
##### Returns text. Text is what to display, size is in pixels, font must be a valid css font, and color is color of text.
```py
t = k.Text('KABOOM!')
k.add(t, 0, 0)
#This would add a 16 pixels, black "KABOOM!" in the sans-serif font
```
# Styles
### `Outline(thickness, color=(0, 0, 0)) => Outline`
##### Returns an outline. Thickness is how thick the outline should be in pixels, and color is color of the outline.
```py
c = k.Circle(50)
k.add(c, 0, 0, outline=k.Outline(50))
#This would add a 50 px thick black outline to the circle.
```
### `Opacity(opacity) => Opacity`
##### Returns opacity. Opacity is how opaque the object should be.
```py
s = k.Sprite('/kablooey.png', 30, 30)
k.add(s, 0, 0, opacity=k.Opacity(0.5))
#This would make the image 50% opaque
```
### `Z(z) => Z`
##### Returns Z. Z is the z-index of the object.
```py
r = k.Rect(20, 20)
k.add(r, 0, 0, z=k.Z(2))
c = k.Circle(20)
k.add(c, 0, 0, z=k.Z(1))
#Even though the circle is being told to be put above the rectangle, the rectangle will come first because of the higher Z-index.
```
# Components
### `Area() => Area`
##### Adds a collider to object
```py
c = k.Circle(50)
c2 = k.Circle(20)
k.add(c, 0, 0, comps=[k.Area()])
k.add(c2, 50, 0, tags=['c2'])
#Now you can use this function
if(c.area.is_colliding('c2')) {
  print('Collideed')
}
```
### `ArrowMove(speed=10) => ArrowMove`
##### Makes the object movable with arrow keys
```py
r = k.Rect(50, 50)
k.add(r, 0, 0, comps=[k.ArrowMove()])
#The rectangle can now be moved with the arrow keys.
#This function comes with the component:
r.mover.change_speed(50)
```
### `LetterMove(speed=10) => LetterMove`
##### ArrowMove, but with wasd
```py
r = k.Rect(50, 50)
k.add(r, 0, 0, comps=[k.LetterMove()])
#Same thing as ArrowMove, but with wasd keys.
```
# Events(decorators)
### `key_down(key) => None`
##### Adds a function to be executed when key goes down
```py
@k.key_down('c')
def cdown():
  print('someboody preesed da cee keyy')
```
### `action() => None`
##### Adds a function to be executed every frame
```py
@k.action()
def uneaction():
  print('fwefwef')
```
# Have fun with ...
+ kaboom.py _or_
+ kablooey _or_
+ kaboom... in python
###### I really don't know, help me here