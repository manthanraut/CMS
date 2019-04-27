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
<NewMenuBg>:  
    canvas:
        Color:
            rgba : hex('28B14A')
        Rectangle:
            size : self.size
            pos : self.pos

<Title>:
    orientation: 'vertical'
    size_hint : 1, .1
    pos_hint : {'top' : 1,'center_x' : 0.5}
    canvas:
        Color :
            rgba : 1,.8353,.3098,1
        Rectangle:
            size : self.size
            pos : self.pos
    Label:
        text : "Canteen Management System"
        color : 0,0,0,1
        bold : True
        font_size : 35

''')
class Title(BoxLayout):
    # Sign up title
    pass

class MenuList(FloatLayout):
    # Consist of Frames at the right side of the screen
    def set(self):
        self.sectionLabel=Label(text="Section : ",font_name="candara",color=(0,0,0,1),size_hint=(.3,.1),pos_hint={"x":0,"top":.8},font_size=30)
        self.add_widget(self.sectionLabel)
        self.example=Label(text="(Ex: Maincourse, Starter, Breads, Extras)",font_name="candara",italic=True,color=(0,0,0,.2),size_hint=(.5,.08),pos_hint={"x":.4,"y":.7},font_size=25)
        self.add_widget(self.example)
        self.section=TextInput(hint_text='section',size_hint=(.2,.08),pos_hint={"x":0.25,"top":0.78},font_size=25)
        self.add_widget(self.section)
        self.itemLabel=Label(text="Item Name : ",font_name="candara",color=(0,0,0,1),size_hint=(.3,.1),pos_hint={"x":0,"top":.65},font_size=30)
        self.add_widget(self.itemLabel)
        self.itemname=TextInput(hint_text='Item name',size_hint=(.2,.08),pos_hint={"x":0.25,"top":0.65},font_size=25)
        self.add_widget(self.itemname)
        self.priceLabel=Label(text="Item Price : ",font_name="candara",color=(0,0,0,1),size_hint=(.3,.1),pos_hint={"x":0,"top":.5},font_size=30)
        self.add_widget(self.priceLabel)
        self.price=TextInput(hint_text='Item price',size_hint=(.2,.08),pos_hint={"x":0.25,"top":0.5},font_size=25)
        self.add_widget(self.price)
        self.btn=Button(text = 'Insert',font_name="candara",background_color=(.56,0,1,.55),bold=True,size_hint=(.2,.1),pos_hint={"x":0.05,"top":.3},font_size=25,on_press=self.insert)
        self.add_widget(self.btn)
        self.btn1=Button(text = 'Update',font_name="candara",background_color=(.56,0,1,.55),bold=True,size_hint=(.2,.1),pos_hint={"x":0.3,"top":.3},font_size=25,on_press=self.update)
        self.add_widget(self.btn1)
        self.btn2=Button(text = 'Delete',font_name="candara",background_color=(.56,0,1,.55),bold=True,size_hint=(.2,.1),pos_hint={"x":0.55,"top":.3},font_size=25,on_press=self.delete)
        self.add_widget(self.btn2)
        self.btn3=Button(text = 'Back',font_name="candara",background_color=(.56,0,1,.55),bold=True,size_hint=(.2,.1),pos_hint={"x":0.8,"top":.3},font_size=25,on_press=self.back)
        self.add_widget(self.btn3)
        self.items=TextInput(hint_text="(Item name,price)",cursor=True,size_hint=(.35,.38),font_size=20,pos_hint={"x":0.5,"y":0.33})
        self.add_widget(self.items)
        self.btn4=Button(text = 'Show',font_name="candara",background_color=(.56,0,1,.55),bold=True,size_hint=(.1,.1),pos_hint={"x":0.86,"y":.33},font_size=25,on_press=self.show)
        self.add_widget(self.btn4)
        self.pre=False
        
    def show(self,a):
        self.sect=self.section.text
        cursor.execute("select * from {}".format(self.sect))
        self.d=str(cursor.fetchall())
        total=[]
        for i in self.d:
            if(i=="'" or i=="]" or i=='['):
                continue
            total.append(i)
        self.list1="".join(total)
        self.items.text=str(self.list1)
        hmdb.commit()
    def update(self,a):
        self.sect=self.section.text
        self.item=self.itemname.text
        self.pr=self.price.text
        cursor.execute("update {} set price={} where name='{}'".format(self.sect,self.pr,self.item))
        cursor.execute("update ordermenu set price={} where item_name='{}'".format(self.pr,self.item))
        self.p = PopUp()
        self.p.set("Item price successfully \n updated")
        self.p.open()
        hmdb.commit()
        
    def delete(self,a):
        self.sect=self.section.text
        self.item=self.itemname.text
        self.pr=self.price.text
        cursor.execute("delete from {} where name='{}'".format(self.sect,self.item))
        cursor.execute("delete from ordermenu where item_name='{}'".format(self.item))
        self.p = PopUp()
        self.p.set("Item deleted")
        self.p.open()
        hmdb.commit()
        
    def insert(self,a):
        self.sect=self.section.text
        self.item=self.itemname.text
        self.pr=self.price.text
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (name varchar(15),price int)".format(self.sect))
        cursor.execute("insert into {} values ('{}',{})".format(self.sect,self.item,self.pr))
        cursor.execute("insert into ordermenu values ('{}',{})".format(self.item,self.pr))
        self.p = PopUp()
        self.p.set("New Item Given \n to Menu")
        self.p.open()
        hmdb.commit()
        
    def back(self,a):
        self.pre=True
        
class PopUp(Popup):
    # Show pop up if encounter error in the login
    def set(self,msg):
        self.title = 'Hello Admin!'
        self.content = Label(text = msg)
        self.size_hint = (None,None)
        self.size = (200,200)


class NewMenuBg(BoxLayout):
    # Background for SignUP page
    def set(self):
        self.orientation = 'horizontal'
        self.size_hint  = (1,1)
        self.ML = MenuList()
        self.ML.set()
        self.add_widget(self.ML)

        
class NewMenuScreen(Screen,BoxLayout):
    # main screen for sign up
    def set(self):
        self.name = 'menu'
        self.orientation = 'vertical'
        self.add_widget(Title(),index = 0)
        self.Y = NewMenuBg()
        self.Y.set()
        self.add_widget(self.Y,index = 1)


class NewMenuApp(App):
    # Create local app
    def build(self):
        self.sm = ScreenManager()
        self.a = NewMenuScreen()
        self.a.set()
        self.sm.add_widget(self.a)
        inspector.create_inspector(Window, self.a)
        return self.sm

if __name__ == '__main__':
    NewMenuApp().run()
