from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.audio import SoundLoader

Squares = []

def clear():
    global Squares
    for square in Squares:
        square.button.background_normal = "standart.png"
        square.value = None



class FirstScr(Screen):
    def __init__(self, name='first'):
        super().__init__(name=name)
        background = Image(source="background.jpg", allow_stretch = True, keep_ratio = False)
        start_btn = Button(text="Начало",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.6})
        start_btn.on_press = self.next_game
        shop_btn = Button(text="Магазин",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.4})
        shop_btn.on_press = self.next_shop
        self.add_widget(background)
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
        background = Image(source="background.jpg", allow_stretch = True, keep_ratio = False)
        self.add_widget(background)


    def next(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'main_menu'



class Square:
    def __init__(self,*lines):
        self.value = None
        self.button = Button(background_normal = "standart.png",background_disabled_down = ("white")) #потом попробуем покрасить
        self.button.on_press = self.click
        global Squares
        Squares.append(self)
        self.lines = lines
        for line in lines:
            line.append(self)

    def click(self):
        global player
        global Squares

        if self.value is None:
            self.value = player
            self.win_check()
            self.draw_check()
            if player == "X":
                self.button.background_normal = "x.png"
                player = "O"
            else:
                player = "X"
                self.button.background_normal = "0.png"

    def win_check(self):
        for line in self.lines:
            n = 0
            for square in line:
                if square.value == player:
                    n += 1

            if n == 3:
                global sm, end_screen
                end_screen.label.text = "победил " + player
                sm.current = "end"

    def draw_check(self):
        k = 0
        for square in Squares:
            if square.value != None:
                k += 1

        if k == 9:
            global sm, end_screen
            end_screen.label.text = "Ничья!"
            sm.current = "end"



class GameScr(Screen):
    def __init__(self, name='game'):
        super().__init__(name=name)
        background = Image(source="background.jpg", allow_stretch = True, keep_ratio = False)
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
        self.add_widget(background)
        self.add_widget(vertical_layout)



class End_screen(Screen):
    def __init__(self, name='end'):
        super().__init__(name=name)
        background = Image(source="background.jpg", allow_stretch = True, keep_ratio = False)
        self.label = Label(text = "QQ",color = (0,0,0),size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.7})
        start_btn = Button(text="Меню",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.5})
        start_btn.on_press = self.next_menu
        shop_btn = Button(text="Перезапуск",size_hint = (0.3,0.2),pos_hint = {'center_x' : 0.5, 'center_y' : 0.3})
        shop_btn.on_press = self.next_game
        self.add_widget(background)
        self.add_widget(self.label)
        self.add_widget(start_btn)
        self.add_widget(shop_btn)

    def next_menu(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'first'
        clear()

    def next_game(self):
        self.manager.transition.direction = 'left'
        self.manager.current = 'game'
        clear()



class MyApp(App):
    def build(self):
        global sm,end_screen
        sm = ScreenManager()
        sm.add_widget(FirstScr())
        sm.add_widget(GameScr())
        sm.add_widget(Shop())
        end_screen = End_screen()
        sm.add_widget(end_screen)
        return sm

player = "X"
app = MyApp()
app.run()
