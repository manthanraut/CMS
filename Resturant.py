from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.clock import Clock
import random
import mysql.connector as db
hmdb = db.connect(host="localhost",user="root",password="thechamp16",database="application")
cursor = hmdb.cursor(buffered=True)

Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex
<ResTitle>:
    orientation: 'vertical'
    size_hint : 1, .1
    canvas:
        
        Rectangle:
            size : self.size
            pos : self.pos
            source:'background1.jpg'
    Label:
        text : "Resturant"
        color : 0,0,0,1
        bold : True
        italic: True
        font_size : 50
<Orders>:
    canvas:
        Color:
            rgba : hex('#FFF748')
        Rectangle:
            size : self.size
            pos : self.pos
    
<ResMenu>:
    canvas:
        
        Rectangle:
            size : self.size
            pos : self.pos
            source:'sixth.png'
                
<Item>:
    canvas:
        Color:
            rgba : 1,.75,0,.96
        Rectangle:
            size : self.size
            pos : self.pos
            
            
''')
cartitem = []
nud = False
g_orderid=random.randint(99,1000)
class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,x):
        self.title = 'Order status'
        self.content = Label(text = 'OrderID :-{} Your \n Order successfully submitted'.format(g_orderid),font_size=16,font_name="candara")
        self.size_hint = (None,None)
        self.size = (250,200)
class PopUp1(Popup):
    def set(self,msg):
        self.title='Dear Customer'
        self.content = Label(text = msg,font_size=16,font_name="candara")
        self.size_hint = (None,None)
        self.size = (200,200)
        
class  Orders(BoxLayout):
    global cartitem
    global itemname
    global nud
    global g_order_id
    def set(self):
        
        self.orientation = 'vertical'
        self.size_hint = (.5,1)
        self.padding = (10,10)
        self.spacing = 10
        self.cart = Label(text='View my order',font_name="candara",color=(0,0,0,1),size_hint= (1,.1),font_size=20,height=15)
        self.add_widget(self.cart)
        self.t_show=TextInput(readonly=True, pos_hint={'x':0,'y':.4},font_size=14, size_hint=[1, .6], background_color=[1,1,1,.8])
        self.add_widget(self.t_show)
        self.add_widget(Button(text = 'Show',size_hint = (1,.4),font_name="candara",background_color=(.4,0.8,0.5,.7),font_size=20,bold=True,on_press = self.show))
        self.o_total = Label(text='Total :',color=(0,0,0,1),font_name="candara",pos_hint={'right':0.6,'y':.4},size_hint= (1,.2),font_size=20,height=15)
        self.t_total=TextInput(readonly=True,hint_text="Total Amt.", font_size=18, size_hint=[.4, .43],pos_hint={'right':0.4,'y':.7}, background_color=[1,1,1,.8])
        self.add_widget(self.o_total)
        self.add_widget(self.t_total)
        self.t_delete=TextInput(hint_text="Item name",font_size=20, size_hint=[.4, .25], background_color=[1,1,1,.8])
        self.add_widget(self.t_delete)
        self.add_widget(Button(text = 'Delete Item',font_name="candara",background_color=(.4,0.8,0.5,.7),font_size=20,bold=True,size_hint = (.5,.4),on_press = self.delete))
        self.add_widget(Button(text="Submit",size_hint=(.5,.4),font_name="candara",background_color=(.4,0.8,0.5,.7),font_size=20,bold=True,on_press=self.toadmin))
        self.add_widget(Button(text = 'View Bill',background_color=(.4,0.8,0.5,.7),font_name="candara",font_size=20,bold=True,size_hint = (1,.4),on_press = self.viewbill))
        self.add_widget(Button(text = 'Sign out',background_color=(.4,0.8,0.5,.7),font_name="candara",font_size=20,bold=True,size_hint = (1,.4),on_press = self.back))
        self.shown = []
        self.obj = []
        self.bk = False
        self.bl=False
        nud = False

    def delete(self,a):
        cursor.execute("delete from orderdata1 where item_name = '{}' and order_id = {}".format(self.t_delete.text,g_orderid))
        cursor.execute("select item_name from orderdata1 where order_id = {}".format(g_orderid))
        self.d=cursor.fetchall()
        self.t_show.text=str(self.d)
        hmdb.commit()
        
    def viewbill(self,a):
        self.bl=True
        
    def show(self,a):
        cursor.execute("select order_id,item_name,count(item_name) as qtn from orderdata1 group by order_id,item_name having order_id = {}".format(g_orderid))
        self.s=cursor.fetchall()
        self.t_show.text=str(self.s)
        cursor.execute("select sum(m.price) FROM ordermenu as m INNER JOIN orderdata1 as i ON m.item_name=i.item_name where order_id = {}".format(g_orderid))
        self.c=cursor.fetchall()
        self.t=str(self.c)
        total=[]
        for i in self.t:
            if(i=="'" or i==")" or i=="]" or i=='(' or i=='[' or i==','):
                continue
            total.append(i)
        name1="".join(total)
        if name1.find('Decimal') == -1:
            pass
        else:
            self.n=name1.replace('Decimal',"")
        self.t_total.text=self.n
        hmdb.commit()
        
    def back(self,a):
        self.bk = True
        
    def aw(self,t):
        w = IL()
        w.set(t)
        self.add_widget(w)
        return w

    def toadmin(self,a):
        self.p = PopUp1()
        if len(str(self.t_total.text))==0:
            self.p.set('Please make some Order \n to submit!!')
            self.p.open()
        else:
            cursor.execute("CREATE TABLE IF NOT EXISTS orderdetails (order_id int,paid varchar(5),received varchar(5),total varchar(10))")
            cursor.execute("insert into orderdetails(order_id,total) values ({},'{}')".format(g_orderid,self.n))
            cursor.execute("CREATE TABLE IF NOT EXISTS orderinfo (order_id int,item_name varchar(20))")
            cursor.execute("insert into orderinfo select * from orderdata1")
            self.x=random.randint(99,1000)
            self.g_orderid = self.x
            self.p = PopUp()
            self.p.set(self.x)
            self.p.open()
            hmdb.commit()
       
class IL(BoxLayout):
    # Frame which group the label and input for various attributes
    def set(self,t):
        self.t = t
        self.add_widget(Label(text = t + ' : ',font_name="candara", font_size=18,color = (0,0,0,1),size_hint=(.3,.5)))
        self.ti = TextInput(hint_text = t,write_tab = False, size_hint=(.45,.9))
        self.add_widget(self.ti)
        
class Item(BoxLayout):
    global nud
    global g_orderid
    global g_user
    
    def set(self,row):
        self.orientation = 'vertical'
        self.row = row
        self.size_hint = (.3,.2)
        self.name = Button(text=row[0],size_hint=(1,0.5),font_size=20,font_name="candara",color = (1,1,1,1),on_press=self.save)
        self.add_widget(self.name)
        self.bl = BoxLayout(orientation = 'horizontal', size_hint = (1,.5))
        self.price = Label(text='Price :'+str(row[1]),font_name="candara",font_size=20,size_hint = (.5,1),color = (0,0,0,1))
        self.bl.add_widget(self.price)
        self.add_widget(self.bl)
        self.result=TextInput(readonly=True, font_size=18, size_hint=[1, .75], background_color=[1,1,1,.8])
        self.add_widget(self.result)
        return self
    
    def save(self,textval):
        self.result.text = textval.text
        cursor.execute("CREATE TABLE IF NOT EXISTS orderdata1 (order_id int,item_name varchar(20))")
        cursor.execute("insert into orderdata1 (order_id,item_name) values({},'{}')".format(g_orderid,self.result.text))
        hmdb.commit()

class Items(TabbedPanelItem):
    def set(self,text):
        cursor.execute('select * from {}'.format(text))
        row = cursor.fetchone()
        self.sl = StackLayout(orientation = 'lr-tb',padding=(10,10),spacing = 10)
        self.l = []
        i = 0
        while row is not None:
            self.l.append(Item())
            self.l[i] = self.l[i].set(row)
            self.sl.add_widget(self.l[i])
            i += 1
            row = cursor.fetchone()
        self.add_widget(self.sl)
        
class ResMenu(TabbedPanel,BoxLayout):
    def set(self):
        self.orientaion = 'horizontal'
        self.do_default_tab = False
        self.starter = Items(text='Starter')
        self.starter.set('starter')
        self.add_widget(self.starter)
        self.default_tab = self.starter
        self.maincourse = Items(text= 'Main Course')
        self.maincourse.set('maincourse')
        self.add_widget(self.maincourse)
        self.breads = Items(text='Breads')
        self.breads.set('breads')
        self.add_widget(self.breads)
        self.extras = Items(text="Extras")
        self.extras.set('extras')
        self.add_widget(self.extras)


class ResBg(BoxLayout,FloatLayout):
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint = (1,.9)
        self.m = ResMenu()
        self.m.set()
        self.o = Orders()
        self.o.set()
        self.add_widget(self.o)
        self.add_widget(self.m)

    def getdata(self):
        global g_orderid
        self.o.getdata()
        self.item = self.o.Itemdetails
        self.total = self.item 
        self.o.su.back = True
        self.x=random.randint(99,1000)
        self.g_orderid = self.x
        self.p = PopUp()
        self.p.set(self.x)
        self.p.open()
        
class ResTitle(BoxLayout):
        # Main title of the Application
    def set(self):
        self.size_hint = (1, .1)
        self.pos_hint = {'top': 1, 'center_x': 0.5}

class ResScreen(Screen,BoxLayout):
    def set(self):
        self.name = "CustResScreen"
        self.orientation = 'vertical'
        self.Ti = ResTitle()
        self.Ti.set()
        self.add_widget(self.Ti)
        self.rb = ResBg()
        self.rb.set()
        self.add_widget(self.rb)
        

class ResScreenM(ScreenManager):
    def set(self):
        self.R = ResScreen()
        self.R.set()
        self.add_widget(self.R)

class ResScreenApp(App):
    def build(self):
        self.s = ResScreenM()
        self.s.set()
        inspector.create_inspector(Window, self.s)
        return self.s


if __name__ == '__main__':
    ResScreenApp().run()
