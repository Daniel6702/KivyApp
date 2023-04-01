from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.carousel import Carousel
from kivy.graphics import *
from math import *
import random
from kivy.config import Config
import operator
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

width = 1280
height = 720

class Menu1(Widget):
    def __init__(self, main, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.num_of_buttons = 5
        self.button_width = 75
        self.button_height = 75
        self.layout = GridLayout(cols=self.num_of_buttons, rows=1)
        self.layout.size = (self.layout.cols * self.button_width, self.layout.rows * self.button_height)
        
        self.layout.x=0
        self.layout.y=height-self.button_height
        
        self.names = ["1","2","3","4","5"]
        self.funcs = {"1" : self.func1, "2" : self.func2, "3" : self.func3, "4" : self.func4, "5" : self.func5}
    
    def setup(self):
        for i in range(0,self.num_of_buttons):
            btn = Button(text = self.names[i], on_press=self.callback, width=self.button_width, height=self.button_height)
            self.layout.add_widget(btn)
        return self.layout

    def callback(self,event):
        for name in self.names:
            if name == event.text:
                self.funcs[name]()
    
    def func1(self):
        print("1")
        self.main.add(Object(self.main,Rect))
    
    def func2(self):
        print("2")
    
    def func3(self):
        print("3")
    
    def func4(self):
        print("4")
    
    def func5(self):
        print("5")
        
class Menu2(Widget):
    def __init__(self, main,x,y, **kwargs):
        super().__init__(**kwargs)
        self.main = main
        self.num_of_buttons = 5
        self.button_width = 50
        self.button_height = 25
        self.layout = GridLayout(cols=1, rows=self.num_of_buttons)
        self.layout.size = (self.layout.cols * self.button_width, self.layout.rows * self.button_height)
        
        self.layout.x=x
        self.layout.y=y
        
        self.names = ["1a","2a","3a","4a","5a"]
        self.funcs = {"1a" : self.func1, "2a" : self.func2, "3a" : self.func3, "4a" : self.func4, "5a" : self.func5}
    
    def setup(self):
        for i in range(0,self.num_of_buttons):
            btn = Button(text = self.names[i], on_press=self.callback, width=self.button_width, height=self.button_height)
            self.layout.add_widget(btn)
        return self.layout

    def callback(self,event):
        for name in self.names:
            if name == event.text:
                self.funcs[name]()
    
    def func1(self):
        print("change pos")
        self.main.pos = (100,100)
        self.main.obj.update_pos(self.main.pos)
        self.main.unselect()
        self.main.close_menu()
    
    def func2(self):
        print("change color")
        self.main.obj.update_color((0,255,0))
        self.main.unselect()
        self.main.close_menu()
    
    def func3(self):
        print("rotate")
        self.main.obj.angle+=30
        self.main.obj.update_angle(self.main.obj.angle)
        self.main.unselect()
        self.main.close_menu()
    
    def func4(self):
        print("4")
    
    def func5(self):
        print("5")
        
        
class SelectMarker(Widget):
    def __init__(self, main,pos,size, **kwargs):
        super(SelectMarker, self).__init__(**kwargs)
        self.main = main
        self.pos = pos
        self.size = size
        self.margin = 8
        self.points = (pos[0]-self.margin,pos[1]-self.margin,
                         pos[0]+size[0]+self.margin,pos[1]-self.margin,
                         pos[0]+size[0]+self.margin,pos[1]+size[1]+self.margin,
                         pos[0]-self.margin,pos[1]+size[1]+self.margin,
                         pos[0]-self.margin,pos[1]-self.margin)

        with self.canvas:
            Color(1,1,0, mode="rgba")
            Line(points=self.points, width = 1)
            for point in zip(self.points[::2],self.points[1::2]):
                Ellipse(pos=map(operator.sub, point, (self.margin/1.8,self.margin/1.8)), 
                        size=(self.margin,self.margin))        


class Object(Widget):
    def __init__(self, main,type,pos=(0,0),size=(50,50), **kwargs):
        super(Object, self).__init__(**kwargs)
        self.pos = pos
        self.size = size
        self.main = main
        self.selected = False
        self.move = False
        self.menu = False
        self.obj = type(pos,size)
        self.main.add(self.obj)
        
        self.temp_angle = 0
        self.has_moved = False
        self.resize = False
        
    def on_touch_down(self, touch):
        if self.selected:
            points = self.select_widget.points
            for i, point in enumerate(zip(points[::2],points[1::2])):
                if dist(touch.pos, point) < 8:
                    self.resize = True
                
        if dist(self.pos, touch.pos) < 8:
            print("2")
        
        if self.mouse_over(self.pos,self.size,touch.pos):
            self.clicked_on(touch.button)
        else:
            if self.selected:
                self.unselect()
            if self.menu:
                self.close_menu()
        
    def mouse_over(self,pos,size,mouse_pos):
        return (mouse_pos[0] > pos[0] and mouse_pos[0] < pos[0] + size[0]       
                and mouse_pos[1] > pos[1] and mouse_pos[1] < pos[1] + size[1])
         
    def unselect(self):
        self.selected = False
        self.main.remove(self.select_widget)
        
    def select(self):
        self.selected = True
        self.select_widget = SelectMarker(self.main,self.pos,self.size)
        self.main.add(self.select_widget)
        
    def clicked_on(self,button):
        if button == "left":
            if self.selected:
                self.move = True
                self.unselect()
            else:
                self.select()
            if self.menu:
                    self.close_menu()
        elif button == "right":
            if self.selected:
                self.open_menu()
            else:
                self.select()
                self.open_menu()
    
    def open_menu(self):
        self.menu = True
        self.menu_widget = Menu2(self,self.pos[0]+self.size[0],self.pos[1]+self.size[1]).setup()
        self.main.add(self.menu_widget)
                
    def close_menu(self):
        self.menu = False
        self.main.remove(self.menu_widget)
           
    def on_touch_up(self, touch):
        if self.temp_angle != 0:
            self.obj.update_angle(self.temp_angle)     
            self.temp_angle = 0
        if self.mouse_over(self.pos,self.size,touch.pos) and not self.selected and self.has_moved:
            self.select()
        self.has_moved = False
        self.move = False

    def on_touch_move(self, touch):
        if self.obj.angle != 0:
            self.temp_angle = self.obj.angle
            self.obj.update_angle(0)
            
        if self.move: 
            self.pos = tuple([touch.pos[0]-self.size[0]/2,
                              touch.pos[1]-self.size[1]/2])
            self.obj.update_pos(self.pos)
            self.has_moved = True
            
        if self.resize:
            difX = self.pos[0]+self.size[0]-touch.pos[0]
            size = (self.size[0]-difX,self.size[1])
            self.obj.update_size(size)
            
    def change_size(self):
        pass
            
class Rect(Widget):
    def __init__(self,pos,size,**kwargs):
        super(Rect, self).__init__(**kwargs)
        self.color = (255,0,0)
        self.angle = 0
        with self.canvas:
            Color(rgb=(self.color))
            self.rect = Rectangle(pos=pos, size=size)
        
    def update_pos(self,pos):
        self.rect.pos = pos
        
    def update_size(self,size):
        self.rect.size = size
        
    def update_color(self,color):
        self.color = color
        self.re_draw()
    
    def update_angle(self,angle):
        self.angle = angle
        self.re_draw()
            
    def re_draw(self):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            origin = self.rect.pos[0]+self.rect.size[0]/2, self.rect.pos[1]+self.rect.size[1]/2
            Rotate(origin=origin, angle=self.angle)
            Color(rgb=(self.color)) 
            self.rect = Rectangle(pos=self.rect.pos, size=self.rect.size)
            PopMatrix()
            
    
class Main(Widget):
    def setup(self):
        self.menu = Menu1(self)
        self.add_widget(self.menu.setup()) 
        self.widgets = []
        
    def add(self, widget):
        self.widgets.append(widget)
        self.add_widget(widget)  
    
    def remove(self, widget):
        self.remove_widget(widget)        

    def update(self, dt):
        pass
        

class DiagramApp(App):
    def build(self):
        Window.size = (width, height)
        instance = Main()
        instance.setup()
        Clock.schedule_interval(instance.update, 1.0 / 60.0)

        return instance


if __name__ == '__main__':
    root = DiagramApp()
    root.run()
    