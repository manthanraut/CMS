from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
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
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="thechamp16",database='application')
cursor = hmdb.cursor(buffered=True)
Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
<AdminBg>:  
    canvas:
        Color:
            rgba : hex('EC4D37')
        Rectangle:
            size : self.size
            pos : self.pos
      

''')


class SecondList(FloatLayout):
    # Consist of Frames at the right side of the screen
    def set(self):
        self.L=Label(text="Orders-->(Order ID, Item Name, Qtn)",pos_hint={"right":.35,"y":0.9},size_hint=(.4,.05),font_size=25,color=(0,0,0,.2))
        self.add_widget(self.L)
        self.L1=Label(text="Payment-->(OrderID,Paid,Received,Amt.)",pos_hint={"right":.37,"y":0.95},size_hint=(.4,.05),font_size=25,color=(0,0,0,.2))
        self.add_widget(self.L1)
        self.displaydata=TextInput(text="",cursor=True,size_hint=(.17,.7),font_size=20,pos_hint={"x":0.08,"y":0.1})
        self.add_widget(self.displaydata)
        self.btn1=Button(text="Show Orders",font_name="candara",size_hint=(.4,.1),font_size=22,pos_hint={"x":0.46,"y":0.88},background_color=(0,0,1,.7),bold=True,on_press=self.showOrders)
        self.add_widget(self.btn1)
        self.btn2=Button(text="Show Payment",font_name="candara",size_hint=(.4,.1),pos_hint={"x":0.46,"y":0.75},background_color=(0,0,1,.7),bold=True,font_size=25,on_press=self.showPayments)
        self.add_widget(self.btn2)
        self.tb1p=TextInput(hint_text="Order ID",size_hint=(.16,.1),pos_hint={"x":0.37,"y":0.54},font_size=28,multiline=False)
        self.add_widget(self.tb1p)
        self.label1=Label(text="Check Payment Details",font_name="candara",color=(0,0,0,1),size_hint=(.3,.1),pos_hint={"x":.53,"y":.64},bold=True,font_size=30)
        self.add_widget(self.label1)
        self.label2=Label(text="Check Order Details",font_name="candara",color=(0,0,0,1),size_hint=(.3,.1),pos_hint={"x":.53,"y":.34},bold=True,font_size=30)
        self.add_widget(self.label2)
        self.btn3p=Button(text = 'Check',font_name="candara",size_hint=(.16,.1),pos_hint={"x":0.6,"y":0.54},background_color=(0,0,1,.7),bold=True,font_size=25,on_press=self.checkp)
        self.add_widget(self.btn3p)
        self.tb3p=TextInput(readonly=True,size_hint=(.1,.1),pos_hint={"x":0.83,"y":0.54},font_size=35)
        self.add_widget(self.tb3p)
        self.btn3r=Button(text = 'Received',font_name="candara",size_hint=(.3,.1),pos_hint={"x":0.535,"y":0.14},background_color=(0,0,1,.7),bold=True,font_size=25,on_press=self.receive)
        self.add_widget(self.btn3r)
        self.tb2r=TextInput(hint_text="Order ID",size_hint=(.16,.1),pos_hint={"x":0.37,"y":0.25},font_size=25,multiline=False)
        self.add_widget(self.tb2r)
        self.btn4p=Button(text = 'Paid',font_name="candara",background_color=(0,0,1,.7),bold=True,size_hint=(.3,.08),pos_hint={"x":0.535,"y":0.44},font_size=25,on_press=self.paid)
        self.add_widget(self.btn4p)
        self.btn4r=Button(text = 'Check',font_name="candara",background_color=(0,0,1,.7),bold=True,size_hint=(.16,.1),pos_hint={"x":0.6,"y":0.25},font_size=25,on_press=self.checkr)
        self.add_widget(self.btn4r)
        self.tb4r=TextInput(readonly=True,size_hint=(.1,.1),pos_hint={"x":0.83,"y":0.25},font_size=35)
        self.add_widget(self.tb4r)
        self.btn=Button(text = 'Click Here To Make changes in Menu',font_name="candara",background_color=(0,0,1,.7),bold=True,size_hint=(.3,.1),pos_hint={"x":0.555,"y":0.02},font_size=25,on_press=self.create)
        self.add_widget(self.btn)
        self.next=False
    

    def showOrders(self,a):
        cursor.execute("select order_id,item_name,count(item_name) as qtn from orderinfo group by order_id,item_name")
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='[' or i==","):
                continue
            total.append(i)
        self.list1="".join(total)
        self.displaydata.text=str(self.list1)
        hmdb.commit()
        
    def create(self,a):
        self.next=True
    
    def showPayments(self,a):
        cursor.execute("select * from orderdetails")
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='[' or i==","):
                continue
            total.append(i)
        self.list1="".join(total)
        self.displaydata.text=str(self.list1)
        hmdb.commit()
        
    def checkp(self,a):
        self.id1=self.tb1p.text
        y=[]
        cursor.execute("select paid from orderdetails where order_id={}".format(self.id1))
        self.q=str(cursor.fetchone())
        for i in self.q:
            if(i=="'" or i==")" or i=="]" or i=='(' or i=='[' or i==','):
                continue
            y.append(i)
        self.y1="".join(y)
        if self.y1=='Y':
            self.tb3p.text=str(self.y1)
        else:
            self.p = PopUp()
            self.p.set("Payment not done".format(self.id1))
            self.p.open()
        hmdb.commit()
        
    def checkr(self,a):
        self.id=self.tb2r.text
        y=[]
        cursor.execute("select received from orderdetails where order_id={}".format(self.id))
        self.q=str(cursor.fetchone())
        for i in self.q:
            if(i=="'" or i==")" or i=="]" or i=='(' or i=='[' or i==','):
                continue
            y.append(i)
        self.y1="".join(y)
        if self.y1=='Y':
            self.tb4r.text=str(self.y1)
        else:
            self.p = PopUp()
            self.p.set("Order Not delivered".format(self.id))
            self.p.open()
        hmdb.commit()
        
    def receive(self,a):
        cursor.execute("update orderdetails set received='Y' where order_id={}".format(self.id))
        hmdb.commit()
        self.p = PopUp()
        self.p.set("Order Successfully \n delivered".format(self.id))
        self.p.open()
        cursor.execute("select * from orderdetails")
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='['):
                continue
            total.append(i)
        self.list1="".join(total)
        self.displaydata.text=str(self.list1)
        
        

    def paid(self,a):
        self.id=self.tb1p.text
        cursor.execute("update orderdetails set paid='Y' where order_id={}".format(self.id))
        hmdb.commit()
        self.p = PopUp()
        self.p.set("Payment successfully \n done for Order_ID {}".format(self.id))
        self.p.open()
        cursor.execute("select * from orderdetails")
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='['):
                continue
            total.append(i)
        self.list1="".join(total)
        cursor.execute("select * from orderdetails")
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='['):
                continue
            total.append(i)
        self.list1="".join(total)
        self.displaydata.text=str(self.list1)

class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,msg):
        self.title = 'Hello Admin!'
        self.content = Label(text = msg)
        self.size_hint = (None,None)
        self.size = (200,200)


class AdminBg(BoxLayout):
    # Background for SignUP page
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint  = (1,1)
        self.SL = SecondList()
        self.SL.set()
        self.add_widget(self.SL)

        
class AdminScreen(Screen,BoxLayout):
    # main screen for sign up
    def set(self):
        self.name = 'admin'
        self.orientation = 'vertical'
        self.X = AdminBg()
        self.X.set()
        self.add_widget(self.X,index = 1)


class AdminApp(App):
    # Create local app
    def build(self):
        self.sm = ScreenManager()
        self.a = AdminScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        inspector.create_inspector(Window, self.a)
        return self.sm

if __name__ == '__main__':
    AdminApp().run()
