from modules import *

con = sqlite3.connect("AFSC.db")
cur =con.cursor()


class MyState(EventDispatcher):#Stores data that is passed between pages
    usertext = StringProperty()
    passtext = StringProperty()
    taskName = StringProperty()
    taskd = StringProperty()
    time = StringProperty()
    gender = StringProperty()
    deleteName = StringProperty()
    task =StringProperty()



class Window(ScreenManager):#Manages all proceeses of all Pages
   user =ObjectProperty(MyState())




class Main(Screen):#Login Page

     def Login(self):
        if self.manager.user.usertext =="" or self.manager.user.passtext=="":
            pop = Popup(title = "Alert", content =Label(text ="Fill up all fields"),size_hint =(None,None), size= (400,400))
            pop.open()
            u  =self.manager.user.usertext
        else:
            users=[]
            cur.execute("SELECT * FROM staff where UserName =? and Password =?",(self.manager.user.usertext, self.manager.user.passtext))
            for e in cur:
                users.append(e)
            if len(users)==0:
                pop = Popup(title="Alert", content=Label(text="Wrong Credentials, please verify and try again"),size_hint=(None,None), size=(400,400))
                pop.open()
            else:
                cur.execute("SELECT Position from staff where Username =?", (self.manager.user.usertext,))
                for e in cur:
                    for i in e:
                        if i =="Admin":
                            self.parent.current ="admin"
                        else:
                            self.parent.current ="tasks"

class Tasks(Screen):#Users Page
    pass

class Admin(Screen):#Admin page

    pass

class SignUp(Screen):#SignUp page
    user = ObjectProperty(None)
    pass1 =ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def clear(self):
        self.user.text = ""
        self.pass1.text = ""
        self.pass2.text =""

    def submit(self):

        if self.pass1.text != self.pass2.text:
            pop =Popup(title ="Alert", content =Label(text ="Password Mismatch"), size_hint =(None,None), size= (400,400))
            pop.open()
        elif self.pass1.text =="" or self.pass2.text=="" or  self.user.text=="":
            pop = Popup(title="Alert", content=Label(text="Fill up all fields"), size_hint=(None, None), size=(400, 400))
            pop.open()

        else:
            cur.execute("SELECT * from staff where UserName =?",(self.user.text,))
            users =[]
            for e in cur:
                users.append(e)
            if len(users)==0:
                pop = Popup(title="Alert", content=Label(text="Your are not a recognised employee of this organisation"), size_hint=(None, None),
                             size=(400, 400))
                pop.open()
            else:
                cur.execute("SELECT Password from staff where UserName =?",(self.user.text,))
                for e in cur:
                    if e == (None,):
                        cur.execute("Update staff  set Password =? where UserName =?",(self.pass1.text,self.user.text,))
                        con.commit()
                        pop = Popup(title="Alert",
                                    content=Label(text="Registration Complete, you can proceed to log into the system"),
                                    size_hint=(None, None),
                                    size=(400, 400))
                        pop.open()
                    else:
                        pop = Popup(title="Alert",
                                    content=Label(text="Your have already registered into the system, "),
                                    size_hint=(None, None),
                                    size=(400, 400))
                        pop.open()
                        webbrowser.open('http://www.google.com')


class AddTask(Screen):#Page for adding Tasks

    def show_date(self):
        picker =MDDatePicker(callback =self.got_date)
        picker.open()

    def got_date(self,the_date):
        print(the_date)

    def  submit(self):
        cur.execute("INSERT INTO TASKS VALUES(?,?,?,?)",(self.manager.user.usertext,self.manager.user.taskName,self.manager.user.taskd,self.manager.user.time))
        con.commit()
        pop = Popup(title = "Confirmation", content = Label(text = "Task successfully recorded"), size =(200, 200), size_hint =(None,None))
        pop.open()


class AddStaff(Screen):#Page for adding staff
    nam =ObjectProperty(None)
    spi =ObjectProperty(None)

    def add(self):
        t =self.nam.text
        s= self.spi.text

        if t =="" or s =="Gender":
            p =Popup(title ="Alert",content =Label(text= "Fill up details"),size_hint =(None,None), size =(200,200))
            p.open()
        else:
            cur.execute("SELECT UserName FROM STAFF WHERE UserName =?",(t,))
            user =(cur.fetchall())
            if len(user)==0:
                cur.execute("INSERT INTO STAFF(UserName,Gender) VALUES(?,?)", (t, s,))
                con.commit()
                p = Popup(title="Confirmation", content=Label(text="Employee addition successfull"),
                          size_hint=(None, None), size=(300, 180))
                p.open()
            else:
                p = Popup(title="Alert", content=Label(text="Employee Code is in use try another one"),
                          size_hint=(None, None), size=(300, 180))
                p.open()

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''

class TestCheckbox(FloatLayout):
    pass

class TaskLayout(Button):
    color =(0,0,1,1)
    background_color=(255,255,255,255)

    def  on_press(self):
      self.t =GridLayout()
      self.t.cols =2
      b1 = Button(text ="Completed",size_hint =(0.4,0.1),pos_hint ={"x":0.2,"y":0.6})
      b2 = Button(text = "Pending",size_hint =(0.4,0.1),pos_hint = {"x":0.4,"y":0.6})
      self.t.add_widget(b1)
      self.t.add_widget(b2)
      pop =Popup(title ="Assess", content =self.t,size=(200,200),size_hint =(None,None))
      pop.open()




class RV(Screen):
    staff = ListProperty([])
    def on_enter(self, *args):
        cur.execute("Select TaskName from Tasks where Action =?", (self.manager.user.usertext,))
        staff =[]
        for e in cur:
            staff.append(e)
        if len(staff)>=1:
            for e in staff:
                for i in e:
                    self.staff.append(i)
        else:
            T = "NO PENDING TASKS"
            self.staff.append(T)
    def clear(self):
        self.staff.clear()
class DeletePop(Popup):

    def delete(self):
        de =DeleteStaff(self)
        de.delete()


class DeleteStaff(Screen):
    spi = ObjectProperty()
    u = ListProperty([])

    def on_enter(self):#Retrieving UserNames from the Server for deletion
        cur.execute("SELECT UserName FROM STAFF ")
        for e in cur:
            for i in e:
                self.u.append(i)

    def delete(self):#functionality for delete on popup

        t = self.spi.text
        self.Pop = GridLayout()


        self.Pop.cols =1
        t1 = Label(text = "Are you sure You want to delete"+t,size_hint =(0.4,0.1),pos_hint ={"x":0.2,"y":0.8},font_size =26,color =(0,1,0,1))
        self.Pop.add_widget(t1)
        self.p =GridLayout()
        self.p.cols=2
        b1 =Button(text = "YES",size= (100,60),pos_hint={"x":0.2,"y":0.6},width =100,font_size =26,size_hint=(None,None))
        b2 = Button(text="NO", size=(100,60),pos_hint={"x":0.9,"y":0.6},width =100,font_size =26,size_hint=(None,None))
        b1.bind(on_press =self.yes)
        self.p.add_widget(b1)
        self.p.add_widget(b2)
        self.Pop.add_widget(self.p)
        pop = Popup(title="Alert", content=self.Pop, size=(500, 200), size_hint=(None,None))
        pop.open()

    def yes(self,instance):

        cur.execute("Delete from staff where UserName =?", (self.spi.text,))
        con.commit()
        p = Popup(title="Confirmation", content=self.spi.text + "successfully deleted", size=(200, 200), size_hint=(None, None))
        p.open()

    def add(self): #functionality to call popup
        t = self.spi.text


        if t == "Choose Name":
            pop = Popup(title ="Alert", content =Label(text ="Please Choose A Name"),size =(200,200),size_hint =(None,None))
            pop.open()
        else:
            pass

    def back(self):
        self.u.clear()



kv =Builder.load_file("afsc.kv") 

class AFSC(App):
    title = "AFSC ZIMBABWE"
    theme_cls = ThemeManager()
    def build(self):

        return kv

if __name__ =="__main__":
    AFSC().run()
