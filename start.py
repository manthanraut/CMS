import Login
from NewMenu import NewMenuScreen
from Bill import BillScreen
from Admin import AdminScreen
from SignUp import SignUpScreen
from Section import SectionScreen
from Resturant import ResScreen
from sys import path
path.append('/usr/lib/python3/dist-packages/')
from kivy.uix.screenmanager import ScreenManager
from kivy.app import App
from kivy.clock import Clock

class SwitchScreen(ScreenManager):
    #Switch Screen is the main screen manager of the application
    def loginC(self):
        self.L = Login.LoginScreen()
        self.L.set()
        self.add_widget(self.L)
        self.current = 'login'
        self.SU = SignUpScreen()
        self.SU.set()
        self.add_widget(self.SU)
        self.SE = SectionScreen()
        self.SE.set()
        self.add_widget(self.SE)
        self.RS = ResScreen()
        self.RS.set()
        self.add_widget(self.RS)
        self.AS = AdminScreen()
        self.AS.set()
        self.add_widget(self.AS)
        self.BS=BillScreen()
        self.BS.set()
        self.add_widget(self.BS)
        self.NM=NewMenuScreen()
        self.NM.set()
        self.add_widget(self.NM)
        
    def update(self,dt):
        #this method swicthes the screen depending on the result of click event on a button
        if self.SE.m.R.RSel == True and self.L.B.LMB.LM.LoginT == True :
            self.current = "CustResScreen"
        elif self.AS.X.SL.next == True:
            self.current='menu'
        elif self.RS.rb.o.bk == True:
            self.current = 'login'
        elif self.RS.rb.o.bl == True:
            self.current="Bill"
        elif self.L.B.LMB.LM.AdminT==True:
            self.current='admin'
        elif self.L.B.LMB.LM.LoginT == True :
            self.current = 'CustResScreen'
        elif self.NM.Y.ML.pre==True:
            self.current='admin'
        elif self.L.B.LMB.LM.SignUpT == True :
            self.current = 'signup'
            if self.SU.X.SL.su.backtl == True or self.SU.X.SL.su.signupT == True:
                self.L.B.LMB.LM.SignUpT = False
                self.current = 'login'
                self.SU.X.SL.su.backtl = False
                self.SU.X.SL.su.signupT = False

class HotelManagementSystemApp(App):
    # main application
    def build (self):
        self.a = SwitchScreen()
        self.a.loginC()
        Clock.schedule_interval(self.a.update, 1.0 / 60.0)
        return self.a

if __name__== '__main__':
    HotelManagementSystemApp().run()
