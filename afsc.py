from modules import *

con = sqlite3.connect("AFSC.db")
cur =con.cursor()

tod = dt.now().date()
startWeek = tod - timedelta(days=tod.weekday())
endWeek = tod + timedelta(days=6)


class MyState(EventDispatcher):#Stores data that is passed between pages
    usertext = StringProperty()
    passtext = StringProperty()
    taskName = StringProperty()
    taskdate= StringProperty()
    time = StringProperty()
    gender = StringProperty()
    deleteName = StringProperty()
    taskdsc =StringProperty()
    username = StringProperty()
    dept =StringProperty()
    pending =StringProperty()
    notification = StringProperty()
    position = StringProperty()



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
                            self.parent.current ="users"
                cur.execute("Select TaskName from tasks where Action = ?",(self.manager.user.usertext,))
                Tasks  =[]
                for e in cur:
                    for i in e:
                        self.manager.user.position =i
                        Tasks.append(i)
                self.manager.user.pending = str(len(Tasks))
                cur.execute("Select DOF from tasks where Action =?",(self.manager.user.usertext,))
                dates=[]
                for e in cur:
                    for i in e:
                        day = dt.strptime(i,"%Y-%m-%d").date()
                        time = (day -tod).days
                        if time<=2:
                            self.manager.user.notification = "Notification" +"\n" +"You have close Deadlines"



class Users(Screen):#Users Page
    dates = ListProperty([])


    def on_enter(self):

        cur.execute("SELECT DOF from tasks where Action =?",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                day = dt.strptime(i,"%Y-%m-%d").date()
                mindate = (day-tod).days
                if mindate <= 2:
                    self.manager.user.notification ="Notification" +"\n" + "You have close deadlines"










class Admin(Screen):#Admin page
    a = ""

    def __init__(self,**kwargs):
        super(Admin,self).__init__(**kwargs)
        self.a =""
    def on_enter(self):
        self.a = "9"

class SignUp(Screen):#SignUp page
    user = ObjectProperty(None)
    pass1 =ObjectProperty(None)
    pass2 = ObjectProperty(None)

    def clear(self):
        self.user.text = ""
        self.pass1.text = ""
        self.pass2.text =""

    def submit(self):
        if self.pass1.text =="" or self.pass2.text=="" or  self.user.text=="":
            pop = Popup(title="Alert", content=Label(text="Fill up all fields"), size_hint=(None, None), size=(400, 400))
            pop.open()

        elif self.pass1.text != self.pass2.text:
            pop =Popup(title ="Alert", content =Label(text ="Password Mismatch"), size_hint =(None,None), size= (400,400))
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
        self.ids.cale.text =str(the_date)


    def  submit(self):
        self.manager.user.taskdate = self.ids.cale.text
        tasks =[]
        cur.execute("SELECT TaskName FROM TASKS WHERE TaskName =? and Action =?",(self.manager.user.taskName,self.manager.user.usertext,))
        for e in cur:
            for i in e:
                tasks.append(i)
        if len(tasks)!=0:
            pop = Popup(title ="Task Duplication", content =Label(text="Duplication! -Task already recorded"),size =(300,200)
            ,size_hint =(None,None))
            pop.open()
        else:
            cur.execute("INSERT INTO TASKS(Action,TaskName,TaskDescrp,DOF) VALUES(?,?,?,?)",(self.manager.user.usertext,self.manager.user.taskName,self.manager.user.taskdsc,self.manager.user.taskdate,))
            con.commit()
            pop = Popup(title = "Confirmation", content = Label(text = "Task successfully recorded"), size =(200, 200), size_hint =(None,None))
            pop.open()

    def clear(self):
        self.ids.taskNm.text =""
        self.ids.cale.text =""
        self.ids.taskdsr.text =""

    def position(self):
        cur.execute("Select Position from staff where UserName =?",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                self.manager.user.position = i


class AddStaff(Screen):#Page for adding staff
    supervisor =ListProperty([])
    staff =[]

    def on_enter(self):
        cur.execute("SELECT UserName from staff where Capacity = ?",("Supervisor",))
        for e in cur:
            for i in e:
                self.supervisor.append(i)

    def add(self):

        g =self.ids.gender.text
        u =self.ids.name.text
        d =self.ids.department.text
        r =self.ids.role.text
        s =self.ids.supervisor.text

        cur.execute("Select * from staff where UserName =?",(self.ids.name.text,))
        names =[]
        for e in cur:
            for i in e:
                names.append(i)
        if len(names)!=0:
            pop = Popup(title = "Alert", content =Label(text = "UserName already in use try another one"), size = (300,200),size_hint=(None,None))
            pop.open()

        else:
            cur.execute("Insert into staff(UserName,Gender,Department,Capacity,Supervisor)values(?,?,?,?,?)",(u,g,d,r,s,))
            con.commit()
            pop = Popup(title="Confirm", content=Label(text = "Member successfully added"), size=(300, 200),
                        size_hint=(None, None))
            pop.open()






    def back(self):
        self.staff.clear()
        self.parent.current ="admin"

class TaskLayout(Button,Window,RecycleBoxLayout,LayoutSelectionBehavior,Label):#class with definations of how Tasks will look like in the tasks page
    background_color=(0,1,1,1)
    btn =ObjectProperty()
    d1 = ObjectProperty()
    font_size =26


    def on_press(self):
      cur.execute("Select DOF from Tasks where TaskName = ?",(self.btn.text,))
      for e in cur:
          for i in e:
              deadline = i

      cur.execute("Select TaskDescrp from Tasks where TaskName =?",(self.btn.text,))
      for e in cur:
          for i in e:
              description = i

      def pending(instance):
          t1 = FloatLayout()
          d1 = TextInput(hint_text ="yyyy-mm-dd",size_hint=(None,None),pos_hint={"x": 0.1, "y": 0.5}, size=(90, 40))
          t1.add_widget(d1)
          b1 =Button(text="SUBMIT", size_hint=(None, None), pos_hint={"x": 0.2, "y": 0.3}, size=(90, 40))
          t1.add_widget(b1)
          pp = Popup(title ="Set Date", content =t1,size_hint=(None,None),size =(300,300))
          pp.open()

      def done(instance):
          p2.dismiss()
          cur.execute("Select TaskDescrp from tasks where TaskName =? and Action =?",(self.btn.text, self.user.usertext,))
          for e in cur:
              for i in e:
                  descrpt = i
          cur.execute("Insert into Previous VALUES (?,?)",(self.user.usertext, descrpt,))
          con.commit()
          cur.execute("Delete From Tasks where TaskName =? and Action =?",(self.btn.text,self.user.usertext,))
          con.commit()
          p = Popup(title='Confirmation', content=Label(text=self.btn.text + "\n" + "successfully completed"),
                    size=(200, 200), size_hint=(None, None))
          p.open()


      try:
          t = FloatLayout()
          l1 =Label(text ="Task Description:", size_hint =(None,None), pos_hint = {"x":0.1,"y":0.6})
          t.add_widget(l1)
          l2 = Label(text = description, size_hint =(None,None),pos_hint ={"x":0.4,"y":0.5})
          t.add_widget(l2)
          l3 = Label(text="Deadline:", size_hint=(None, None), pos_hint={"x": 0.1, "y": 0.3})
          t.add_widget(l3)
          l2 = Label(text=deadline, size_hint=(None, None), pos_hint={"x": 0.3, "y": 0.3})
          t.add_widget(l2)
          b1 = Button(text = "Done", size =(90,40), pos_hint = {"x":0.1,"y":0.1},size_hint =(None,None), on_press =done)
          t.add_widget(b1)
          b2 =Button(text ="Pending", size=(90,40), pos_hint = {"x":0.5,"y":0.1},size_hint =(None,None),on_press =pending)
          t.add_widget(b2)
          p2 = Popup(title = "Task Assessment", content = t,size =(700,300), size_hint = (None,None))
          p2.open()
      except:
          p = Popup(title="Task Assessment", content=Label(text = "Nothing to select"), size=(400, 300), size_hint=(None, None))
          p.open()






class RV(Screen):# Show Tasks
    staff = ListProperty([])


    def on_enter(self):
        cur.execute("Select TaskName from Tasks where Action =? and Status ='Pending'", (self.manager.user.usertext,))
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

    def position(self):
        cur.execute("Select Position from staff where UserName =?",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                self.manager.user.position = i



    def refresh(self):
        cur.execute("Select TaskName from tasks where Action = ?",(self.manager.user.usertext,))
        done =[]
        for e in cur:
            for i in e:
                done.append(i)
        do = len(done)
        self.manager.user.pending =str(do)



class DeletePop(Popup):

    def delete(self):
        de =DeleteStaff(self)
        de.delete()


class DeleteStaff(Screen):# Page/ Screen for deleting staff
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

        if t == "Choose Name":
            pop = Popup(title ="Alert", content =Label(text ="Please Choose A Name"),size =(200,200),size_hint =(None,None))
            pop.open()
        else:
            pass

    def back(self):
        self.u.clear()

class Surbodinates(Screen):#screen viewed by Supervisor of His Surbodinates
    surbodinates = ListProperty([])

    def on_enter(self):
        cur.execute("Select UserName from staff where Supervisor = ?",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                self.surbodinates.append(i)

class SurbodinatesList(Button):
    color = (0, 0, 1, 1)
    background_color = (255, 255, 255, 255)


class NewDate(Screen):

    def show_date(self):
        picker =MDDatePicker(callback =self.got_date)
        picker.open()

    def got_date(self,the_date):
        self.ids.cale.text =str(the_date)




kv =Builder.load_file("afsc.kv")

class AFSC(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Cyan"
    theme_cls.accent_palette = "Blue"
    theme_cls.theme_style ="Light"
    title = "AFSC ZIMBABWE"


    def build(self):
        return kv

if __name__ =="__main__":
    AFSC().run()


