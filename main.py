from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
 
class FirstScr(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name) 
        start_btn = Button(text="Начало",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.6})
        start_btn.on_press = self.next_game
        shop_btn = Button(text="Магазин",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.4})
        shop_btn.on_press = self.next_shop
        self.add_widget(start_btn)
        self.add_widget(shop_btn)

    def next_game(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'

    def next_shop(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'Shop'
 
class Shop(Screen):
    def __init__(self, name='Shop'):
        super().__init__(name=name)
        
        
    def next(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'
 
class Square:
    def __init__(self,*lines):
        self.value = None
        self.button = Button() #потом попробуем покрасить
        self.button.on_press = self.click
 
        self.lines = lines
        for line in lines:
            line.append(self)
 
    def click(self):
        global player

        if self.value is None:
            self.value = player
            self.button.text = player

        if player == "X":
            player = "O"
        else:
            player = "X"


 
class GameScr(Screen):
    def __init__(self, name='game'):
        super().__init__(name=name)
        #наполнить кнопками
        up_layout = BoxLayout(orientation="horizontal")
        mid_layout = BoxLayout(orientation="horizontal")
        down_layout = BoxLayout(orientation="horizontal")

        up = []
        mid = []
        down = []
        left = []
        vertical_mid = []
        right = []
        diagonal1 = []
        diagonal2 = []
 
        #верхняя
        Square(up,left,diagonal1)
        Square(up,vertical_mid)
        Square(up,right,diagonal2)
 
        #средний
        Square(mid,left)
        Square(mid,vertical_mid,diagonal1,diagonal2)
        Square(mid,right)
 
        #нижний
        Square(down,left,diagonal2)
        Square(down,vertical_mid)
        Square(down,right,diagonal1)
 
        for square in up:
            up_layout.add_widget(square.button)
        for square in mid:
            mid_layout.add_widget(square.button)
        for square in down:
            down_layout.add_widget(square.button)
 
        vertical_layout = BoxLayout(orientation="vertical")
        vertical_layout.add_widget(up_layout)
        vertical_layout.add_widget(mid_layout)
        vertical_layout.add_widget(down_layout)
        self.add_widget(vertical_layout)
 
class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(FirstScr())
        sm.add_widget(GameScr())
        sm.add_widget(Shop())
        return sm
 
player = "X"
app = MyApp()
app.run()
