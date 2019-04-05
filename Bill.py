from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from Resturant import *
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="thechamp16",database='application')
cursor = hmdb.cursor(buffered=True)
Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
<BillBg>:  
    canvas:
        Color:
            rgba : hex('#FFE67C')
        Rectangle :
            size : self.size
            pos : self.pos
<BillTitle>:
    orientation: 'vertical'
    size_hint : 1, .1
    pos_hint : {'top' : 1,'center_x' : 0.5}
    canvas:
        Color :
            rgba : hex('#295F2D')
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "BILL"
        color : 1,1,1,1
        bold : True
        font_size : 35
      

''')
class BillList(FloatLayout):
    def set(self):
        self.ord=Orders()
        self.L=Label(text="Bill No. :",pos_hint={"right":0.3,"y":0.8},font_name="candara",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L)
        self.L1=Label(text="",pos_hint={"right":0.38,"y":0.8},font_name="candara",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L1)
        self.L2=Label(text="Particulars",pos_hint={"right":0.5,"y":0.7},font_name="candara",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L2)
        self.L3=Label(text="Total No. of items",pos_hint={"right":0.7,"y":0.7},size_hint=(.4,.05),font_name="candara",font_size=30,color=(0,0,0,1))
        self.add_widget(self.L3)
        self.itembox=TextInput(hint_text="Items",readonly=True,cursor=True,size_hint=(.13,.5),font_size=20,pos_hint={"x":0.25,"y":0.18})
        self.add_widget(self.itembox)
        self.qtnbox=TextInput(readonly=True,cursor=True,size_hint=(.02,.5),font_size=20,pos_hint={"x":0.48,"y":0.18})
        self.add_widget(self.qtnbox)
        self.btn=Button(text = 'View Bill',font_name="candara",background_color=(0,.8,0,1),bold=True,size_hint=(.15,.1),pos_hint={"x":0.6,"y":0.5},font_size=25,on_press=self.show)
        self.add_widget(self.btn)
        self.L5=Label(text="TOTAL (Rs.)",pos_hint={"x":0.4,"y":0.3},font_name="candara",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L5)
        self.L6=Label(text="",pos_hint={"x":0.5,"y":0.3},font_name="candara",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L6)
        self.L3=Label(text="Thank You !! Visit Again",pos_hint={"x":0.5,"y":0.1},font_name="ravie",size_hint=(.4,.05),font_size=30,color=(0,0,0,1))
        self.add_widget(self.L3)
        
    def show(self,a):
        self.L1.text=str(g_orderid)
        cursor.execute("select total from orderdetails where order_id={}".format(g_orderid))
        self.d=str(cursor.fetchone())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='[' or i=="(" or i=="," or i==')'):
                continue
            total.append(i)
        self.list1="".join(total)
        self.L6.text=self.list1
        cursor.execute("select distinct item_name from orderinfo where order_id={}".format(g_orderid))
        self.d1=str(cursor.fetchall())
        total1=[]
        for i in self.d1:
            if(i=="'" or i=="]" or i=='[' or i==","):
                continue
            total1.append(i)
        self.list2="".join(total1)
        self.itembox.text=self.list2
        cursor.execute("select count(item_name) from orderinfo where order_id={} group by item_name".format(g_orderid))
        self.d2=str(cursor.fetchall())
        total2=[]
        for i in self.d2:
            if(i=="'" or i=="]" or i=='[' or i=="," or i=="(" or i==")"):
                continue
            total2.append(i)
        self.list3="".join(total2)
        self.qtnbox.text=self.list3
        hmdb.commit()
        
        
class BillTitle(BoxLayout):
    # Sign up title
    pass

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,msg):
        self.title = 'Hello Admin!'
        self.content = Label(text = msg)
        self.size_hint = (None,None)
        self.size = (200,200)

        
class BillBg(BoxLayout):
    # Background for SignUP page
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint  = (1,1)
        self.BL = BillList()
        self.BL.set()
        self.add_widget(self.BL)

        
class BillScreen(Screen,BoxLayout):
    # main screen for sign up
    def set(self):
        self.name = 'Bill'
        self.orientation = 'vertical'
        self.add_widget(BillTitle(),index = 0)
        self.X = BillBg()
        self.X.set()
        self.add_widget(self.X,index = 1)


class BillApp(App):
    # Create local app
    def build(self):
        self.sm = ScreenManager()
        self.a = BillScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        inspector.create_inspector(Window, self.a)
        return self.sm

if __name__ == '__main__':
    BillApp().run()

	
