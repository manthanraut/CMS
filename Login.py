from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="thechamp16",database="application")
cursor = hmdb.cursor()
Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
<LoginScreen>:
    BoxLayout:
<Title>:
    orientation: 'vertical'
    size_hint : 1, .1
    canvas:
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Canteen Management System"
        color : 1,0,0,1
        bold : True
        italic: True
        font_size : 50
<LoginBg>:
    Image:
        source:'food.jpg'
        allow_stretch: True
        keep_ratio: False    
<LoginMenu>:
    orientation : 'vertical'
    canvas:
        Color :
            rgba :hex('#292826')
        Rectangle:
            size : self.size
            pos : self.pos
<LoginMenuB>:
    canvas:
        Color:
            rgba :hex('#F9D342')
        Rectangle :
            size : self.size
            pos : self.pos
<UP>:
    orientation : 'horizontal'
<AccType>:
    Button:
        text : 'Customer'
        size_hint_y : None
        height : 36
        on_release : root.select('Customer')
        background_normal: ''
        background_color : 1,.75,0,.96
        color : 0,0,0,1
    Button:
        text : 'Admin'
        size_hint_y : None
        height : 36
        on_release : root.select('Admin')
        background_normal: ''
        background_color : 1,.75,0,.96
        color : 0,0,0,1
''')
class UP(BoxLayout):
    # Frame grouping label and input for login
    def set(self):
        self.padding = (5,5)
        self.spacing = 10
    def aset(self):
        self.add_widget(Label(text = 'Account Type',font_name="candara", color = (1,1,1,1),font_size=25))
        self.Account = AccType()
        self.acc = Button(text = 'Select Acc. Type',font_name="candara",background_normal= '',background_color = (1,.75,0,.96),font_size=25,color = (0,0,0,1))
        self.acc.bind(on_release = self.Account.open)
        self.Account.bind(on_select = lambda instance, x : setattr( self.acc ,'text', x))
        self.add_widget(self.acc)
        self.set()
    def oset(self,t,f):
        self.add_widget(Label(text = t + ' : ', color = (1,1,1,1),font_name="candara",font_size=25))
        self.I = TextInput(hint_text = t, multiline = False, padding = (10,10),background_color=(1,1,1,.9),font_size=25,password = f)
        self.add_widget(self.I)
        self.set()


class Title(BoxLayout):
    # Main title of the Application
    def set(self):
        self.size_hint = (1,.1)
        self.pos_hint = {'top' : 1,'center_x' : 0.5}

class LoginBg(AnchorLayout):
    #Background which consist of image background
    def set(self):
        self.size_hint = (1,1)
        self.LMB = LoginMenuB()
        self.LMB.set()
        self.LoginT = self.LMB.LoginT
        self.SignUpT = self.LMB.SignUpT
        self.add_widget(self.LMB)

class LoginMenuB(BoxLayout):
    # Square background of login menu
    def set(self):
        self.size_hint=(.6,.6)
        self.pos_hint={'center_x' : 0.5,'center_y' : 0.5}
        self.padding = (6,6)
        self.LM = LoginMenu()
        self.LM.set()
        self.LoginT = self.LM.LoginT
        self.SignUpT = self.LM.SignUpT
        self.add_widget(self.LM)


    def aw(self, ob):
        self.add_widget(ob)

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self):
        self.title = 'Wrong Login Details'
        self.content = Label(text = 'You have entered \n wrong Login Details',font_name="candara")
        self.size_hint = (None,None)
        self.size = (200,200)

class LoginMenu(BoxLayout):
    # Login Menu with all the input and button widgets
    def logincheck(self,instance):
        global g_user
        g_user=self.UN.I.text
        self.query = "SELECT * FROM logindetails WHERE username = '{}' AND acctype='{}' ".format(self.UN.I.text,self.AS.acc.text)
        cursor.execute(self.query)
        self.validcheck = cursor.fetchone()
        if self.PW.I.text == ''or self.validcheck == None:
            self.p = PopUp()
            self.p.set()
            self.p.open()
        else :
            if self.PW.I.text == self.validcheck[1]:
                self.LoginT = True
                hmdb.close()
                if self.PW.I.text=='admin123' and self.UN.I.text=='admin':
                    self.AdminT=True
                    hmdb.close()
            else :
                self.p = PopUp()
                self.p.set()
                self.p.open()
        

    def signupcheck(self,instance):
        self.SignUpT = True

    def set(self):
        self.LoginT = False
        self.AdminT=False
        self.SignUpT = False
        self.padding = (10,10)
        self.pos_hint={'center_x' : 0.5,'center_y' : 0.5}
        self.aw(Label(text='Login',font_name="candara",font_size=25,color =(1,1,1,1), bold = True))
        self.AS = UP()
        self.AS.aset()
        self.aw(self.AS)
        self.UN = UP()
        self.UN.oset('Username',False)
        self.aw(self.UN)
        self.PW = UP()
        self.PW.oset('Password',True)
        self.aw(self.PW)
        self.lg = Button(text = 'Login',font_name="candara",font_size=25,background_normal= '',background_color = (1,.75,0,.96),color = (0,0,0,1))
        self.lg.bind(on_press = self.logincheck)
        self.aw(self.lg)
        self.signup = BoxLayout(orientation = 'horizontal', padding = (5,5),spacing = 10)
        self.orl = Label(text = 'Or', font_size=22,size_hint = (.5,.2),color = (1,1,1,1))
        self.signupb = Button(on_press = self.signupcheck,text = 'Sign Up',font_name="candara", size_hint = (.7,1),font_size=25,background_normal= '',background_color = (1,.75,0,.96),color = (0,0,0,1))
        self.signup.add_widget(self.orl)
        self.signup.add_widget(self.signupb)
        self.aw(self.signup)



    def aw(self,ob):
        self.add_widget(ob)

class LoginScreen(Screen,BoxLayout):
    # main login screen
    def set(self):
        self.name = 'login'
        self.orientation = 'vertical'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T)
        self.B = LoginBg()
        self.B.set()
        self.LoginT = self.B.LoginT
        self.SignUpT = self.B.SignUpT
        self.add_widget(self.B,index = 1)


class AccType(DropDown):
    # To create drop down list
    pass



class Main():
    # crete local login application
    def Start(self):
        self.sm = ScreenManager()
        self.L = LoginScreen()
        self.L.set()
        self.sm.add_widget(self.L)
        return self.sm

class HotelMangementSystemApp(App):
    def build(self):
        inspector.create_inspector(Window,Main)
        X = Main()
        return X.Start()

if __name__ == '__main__':
    HotelMangementSystemApp().run()
