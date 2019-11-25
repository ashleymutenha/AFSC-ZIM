from modules import *

con = sqlite3.connect("AFSC.db")
cur =con.cursor()


class MyState(EventDispatcher):
    usertext = StringProperty()
    passtext = StringProperty()
    taskName = StringProperty()
    taskd = StringProperty()
    time = StringProperty()
    gender = StringProperty()
    deleteName = StringProperty()



class Window(ScreenManager):
   user =ObjectProperty(MyState())

class Dispatch:
    user = ObjectProperty(MyState())





class Main(Screen):

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

class Tasks(Screen):
    pass

class Admin(Screen):

    pass

class SignUp(Screen):
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


class AddTask(Screen):

    def  submit(self):
        cur.execute("INSERT INTO TASKS VALUES(?,?,?,?)",(self.manager.user.usertext,self.manager.user.taskName,self.manager.user.taskd,self.manager.user.time))
        con.commit()
        pop = Popup(title = "Confirmation", content = Label(text = "Task successfully recorded"), size =(200, 200), size_hint =(None,None))
        pop.open()


class AddStaff(Screen):
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

class Ty(Label):
    color =(0,0,1,1)
    size =(240,190)




    def on_press(self):
        show_pop()


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
class DeletePop(FloatLayout):
    pass

    def delete(self):
        cur.execute("Delete from staff where UserName =? ",())
        con.commit
        p = Popup(title = "Confirmation", content =Label(text =  +"successfully deleted"), size =(200,200),size_hint =(None,None))
        p.open()


class DeleteStaff(Screen):
    spi = ObjectProperty()
    u = ListProperty([])
    def on_enter(self):
        cur.execute("SELECT UserName FROM STAFF ")
        for e in cur:
            for i in e:
                self.u.append(i)

    def delete(self):#functionality for delete on popup
        t = self.spi.text
        cur.execute("Delete from staff where UserName =?",(t,))
        con.commit()
        p = Popup(title = "Confirmation", content =t +"successfully deleted", size =(200,200), size_hint =(None,None))
        p.open()


    def add(self): #functionality to call popup
        t = self.spi.text
        d =DeletePop()


        if t == "Choose Name":
            pop = Popup(title ="Alert", content =Label(text ="Please Choose A Name"),size =(200,200),size_hint =(None,None))
            pop.open()
        else:
            pop = Popup(content=d, size=(399, 200), size_hint=(None, None))
            pop.open()

    def back(self):
        self.u.clear()

class SpinnerOptions(SpinnerOption):
    pass


def show_pop():
    show = TestCheckbox()

    pop = Popup(content=show,size=(200, 200), size_hint=(None, None))
    pop.open()





kv =Builder.load_file("afsc.kv") 

class AFSC(App):
    title = "AFSC ZIMBABWE"
    de = DeleteStaff()
    def build(self):

        return kv

if __name__ =="__main__":
    AFSC().run()
