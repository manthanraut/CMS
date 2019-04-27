from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.lang import Builder
from Login import *
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="thechamp16",database='application')
cursor = hmdb.cursor()

Builder.load_string('''
<STitle>:
    orientation: 'vertical'
    size_hint : 1, .08
    pos_hint : {'top' : .9,'center_x' : 0.5}
    canvas:
        Color :
            rgba : hex('#4831D4')
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Sign Up"
        color : 1,1,1,1
        bold : True
        font_size : 35
<SignUpBg>:
    canvas:
        Color:
            rgba : hex('#CCF381')
        Rectangle :
            size : self.size
            pos : self.pos
            

''')
class STitle(BoxLayout):
    # Sign up title
    pass

class RButton(BoxLayout):
    # Radio button for selecting gender
    def set(self):
        self.selectMale = False
        self.selectFemale = False
        self.orientation = 'horizontal'
        self.spacing = 10
        self.padding = (10,10)
        self.l = Label(text = 'Gender',size_hint = (1.5,1),font_name="candara",font_size=25,color = (0,0,0,1))
        self.add_widget (self.l)
        self.m = ToggleButton(text = 'Male',group = 'gender',font_size=18,size_hint=(1,.7),on_press = self.selectM,background_color=(.5,0,1,.6))
        self.add_widget(self.m)
        self.f = ToggleButton(text = 'Female', group = 'gender',font_size=18,size_hint=(1,.7),on_press = self.selectF,background_color=(.5,0,1,.6))
        self.add_widget(self.f)

    def selectM(self,x):
        self.selectMale = True
        self.selectFemale = False

    def selectF(self,x):
        self.selectFemale = True
        self.selectMale = False

class DOB(BoxLayout):
    # Frame of widgets to get date of birth
    def set(self):
        self.orientation = 'horizontal'
        self.padding = (5,5)
        self.spacing = 10
        self.l = Label(text= 'Date Of Birth',font_name="candara",font_size=25, color = (0,0,0,1))
        self.d = TextInput(hint_text = 'DD',multiline=False,size_hint = (.3,.4),font_size=20,write_tab = False,input_filter = 'int')
        self.m = TextInput(hint_text = 'MM',multiline=False,size_hint = (.3,.4),font_size=20,write_tab = False,input_filter = 'int')
        self.yy = TextInput(hint_text = 'YYYY',multiline=False,size_hint = (.5,.4),font_size=20,write_tab = False,input_filter = 'int')
        self.add_widget(self.l)
        self.add_widget(self.d)
        self.add_widget(self.m)
        self.add_widget(self.yy)

class SignUpBg(BoxLayout):
    # Background for SignUP page
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint  = (1,.82)
        self.FL = FirstList()
        self.FL.set()
        self.add_widget(self.FL)
        self.SL = SecondList()
        self.SL.set()
        self.add_widget(self.SL)

class IL(BoxLayout):
    # Frame which group the label and input for various attributes
    def set(self,t,ps = False, input_f = None):
        self.t = t
        self.add_widget(Label(text = t + ' : ',font_name="candara", font_size=25,color = (0,0,0,1)))
        self.ti = TextInput(password = ps,font_size=30,multiline=False,write_tab = False, input_filter = input_f )
        self.add_widget(self.ti)

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,msg):
        self.title = 'Hello Admin!'
        self.content = Label(text = msg)
        self.size_hint = (None,None)
        self.size = (200,200)

class FirstList(BoxLayout):
    # Contais Frames at the left side of screen
    def set(self):
        self.orientation = 'vertical'
        self.padding = (10,10)
        self.spacing = 10
        self.fullname = self.aw('Full Name')
        self.rollno = self.aw('Roll No.')
        self.email = self.aw('Email')
        self.mobileno = self.aw('Mobile No.',inp='int')
        self.username = self.aw('Username')
        self.password = self.aw('Password',ps=True)
        self.cpassword = self.aw('Confirm Password',ps=True)
        self.branch = self.aw('Branch',inp = None)
        self.city = self.aw('City')

    def aw(self,t,ps= False, inp = None):
        self.w = IL()
        self.w.set(t,ps,input_f=inp)
        self.add_widget(self.w)
        return self.w

    def check(self):
        if self.cpassword.ti.text != self.password.ti.text:
            self.PE = PopUp()
            self.PE.set('Password Differ Your\n Password do not match\n with confirm password')
            self.PE.open()
            return False
        return True

    def getdata(self):
        self.FirstListItem = []
        if self.check() == True:
            self.FirstListI = [self.fullname,self.rollno,self.email,self.mobileno,self.username,self.password,self.branch,self.city]
            for i in self.FirstListI:
                self.FirstListItem.append(i.ti.text)
            return self.FirstListItem

class SButton(BoxLayout):
    # Sign up button and back button
    def set(self):
        self.backtl = False
        self.signupT = False
        self.orientation = 'horizontal'
        self.spacing = 10
        self.b = Button(text = 'Sign Up',on_press = self.SignUpButton,font_size=20,size_hint=(1,.7),background_color=(.5,0,1,.6))
        self.add_widget(self.b)
        self.back = Button(text = 'Back', on_press = self.backtologin,font_size=20,size_hint=(1,.7),background_color=(.5,0,1,.6))
        self.add_widget(self.back)

    def SignUpButton(self,a):
        self.signupT = True

    def backtologin(self,x):
        self.backtl = True


class SecondList(BoxLayout):
    # Consist of Frames at the right side of the screen
    def set(self):
        self.padding = (10,10)
        self.spacing = 10
        self.orientation = 'vertical'
        self.pincode = self.aw('Pincode(required)')
        self.aadhaar = self.aw('Aadhaar No.(required)')
        self.g = RButton()
        self.g.set()
        self.add_widget(self.g)
        self.dob = DOB()
        self.dob.set()
        self.add_widget(self.dob)
        self.su = SButton()
        self.su.set()
        self.add_widget(self.su)


    def aw(self,t):
        w = IL()
        w.set(t)
        self.add_widget(w)
        return w

    def check(self):
        self.pincode = int(self.pincode)

    def getdata(self):

        self.SecondListI = [self.pincode,self.aadhaar,]
        self.SecondListItem = []
        for i in self.SecondListI:
            self.SecondListItem.append(i.ti.text)
        if self.g.selectMale == True :
            self.SecondListItem.append('Male')
        elif self.g.selectFemale == True:
            self.SecondListItem.append('Female')
        self.d = self.dob.d.text
        self.m = self.dob.m.text
        self.y = self.dob.yy.text
        self.SecondListItem.append((str(int(self.d))+'/'+str(int(self.m))+'/'+str(int(self.y))))
        return self.SecondListItem


class SignUpScreen(Screen,BoxLayout):
    # main screen for sign up
    def set(self):
        self.name = 'signup'
        self.orientation = 'vertical'
        self.T = Title()
        self.T.set()
        self.add_widget(self.T,index = 0)
        self.add_widget(STitle(),index = 0)
        self.X = SignUpBg()
        self.X.set()
        self.X.SL.su.b.on_press = self.getdata
        self.add_widget(self.X,index = 1)

    def getdata(self):
        self.X.FL.getdata()
        self.fl = self.X.FL.FirstListItem
        self.X.SL.getdata()
        self.sl = self.X.SL.SecondListItem
        self.total = self.fl + self.sl
        self.X.SL.su.backtl = True
        cursor.execute("CREATE TABLE IF NOT EXISTS customerdata(fullname varchar(30),rollno varchar(10),email varchar(40),mobileno bigint,username varchar(15),password varchar(20),branch varchar(20),city varchar(15),pincode bigint,aadhaarno bigint,gender varchar(5),dob varchar(15))")
        self.query = 'INSERT INTO customerdata VALUES ('
        for i in range(len(self.total)):
            self.query += "'"+self.total[i]+"'"
            if i == len(self.total)-1:
                self.query = self.query
            else:
                self.query += ','
        self.query += ')'
        cursor.execute(self.query)
        cursor.execute("CREATE TABLE IF NOT EXISTS logindetails (username varchar(20),password varchar(20),acctype varchar(15))")
        self.q = "insert into logindetails values ('{}','{}','Customer')".format(self.total[4],self.total[5])
        cursor.execute(self.q)
        hmdb.commit()


class SignUpApp(App):
    # Create local app
    def build(self):
        self.sm = ScreenManager()
        self.a = SignUpScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        inspector.create_inspector(Window, self.a)
        return self.sm

if __name__ == '__main__':
    SignUpApp().run()
