from modules import *

tod = dt.now().date()
start = tod - timedelta(days=tod.weekday())
end = start + timedelta(days=4)


class MyState(EventDispatcher):#Stores data that is passed between pages
    usertext = StringProperty()
    passtext = StringProperty()
    taskName = StringProperty()
    taskdate= StringProperty()
    gender = StringProperty()
    deleteName = StringProperty()
    taskdsc =StringProperty()
    username =StringProperty()
    notification1 = StringProperty()
    position = StringProperty()
    pending = StringProperty()
    supervisor = StringProperty()
    staff = ListProperty([])
    notification = StringProperty()
    dept =StringProperty()
    userName = ObjectProperty()
    notifications = ListProperty([])
    people =[]

class State(EventDispatcher):
    usert = ""
    emp =""



class Window(ScreenManager):#Manages all proceeses of all Pages
   user =ObjectProperty(MyState())


class Main(Screen):#Login Page
     def Login(self):
        self.manager.user.staff.clear()
        if self.manager.user.usertext =="" or self.manager.user.passtext=="":
            pop = Popup(title = "AFSC  says" ,title_color =(0,0,0,1),title_size =22,
                        content =Label(text ="Fill up all fields",color =(0,0,1,1),font_size =22),
                        size_hint =(None,None), size= (400,200),background ="",background_color =(0,0,0,0.1),border =(14,14,14,14))
            pop.open()
            u  =self.manager.user.usertext
        else:
            users=[]
            pas = self.manager.user.passtext
            try:
                pass1 = hashlib.sha256(pas.encode('ascii')).hexdigest()
                cur.execute("SELECT * from staff where UserName =%s and Password =%s ",(self.manager.user.usertext,pass1,))
                for e in cur:
                    users.append(e)
                if len(users) == 0:
                    pop = Popup(title="AFSC says", title_color=(0, 0, 0, 1),title_size =22,
                                    content=Label(text="Wrong Credentials, please verify and try again",
                                                  color=(0, 0, 1, 1),font_size =22), size_hint=(None, None), size=(450, 200),
                                   background="",background_color =(0,0,0,0.1),)
                    pop.open()
                else:
                    cur.execute("SELECT Role from staff where UserName =%s", (self.manager.user.usertext,))
                    for e in cur:
                        for i in e:
                            if i == "Admin":
                                self.parent.current = "admin"
                            else:
                                self.parent.current = "users"

                    State.usert= self.manager.user.usertext
                    cur.execute("Select TaskName from tasks where Action = %s", (self.manager.user.usertext,))
                    Tasks = []
                    for e in cur:
                        for i in e:
                            self.manager.user.position = i
                            Tasks.append(i)
                            self.manager.user.pending = str(len(Tasks))


                    cur.execute("Select TaskName from tasks where Action =%s", (self.manager.user.usertext,))
                    st =[]
                    for e in cur:
                        for i in e:
                            st.append(i)

                    if len(st)==0:
                        self.manager.user.staff.append("NO PENDING TASKS")
                        self.manager.user.pending = "0"
                    else:
                        for e in st:
                            self.manager.user.staff.append(e)
                            self.manager.user.pending = str(len(self.manager.user.staff))
                    cur.execute("SELECT UserName FROM staff WHERE Supervisor = %s ", (self.manager.user.usertext,))
                    for e in cur:
                        for i in e:
                            self.manager.user.people.append(i)


            except Exception:
               pop = Popup(title="AFSC says", title_color=(0, 0, 0, 1),title_size =22,
                            content=Label(text="Server is currently down inform the Admin",
                                          color=(0, 0, 1, 1),font_size =22), size=(420, 200), size_hint=(None, None),background ="",background_color =(0,0,0,0.1),)
               pop.open()

class SpinnerOpt(SpinnerOption):
    background_color=(0,0,0,1)
    size =(190,40)
    font_size=22


class Users(Screen):#Users Page
    dates = ListProperty([])
    noti =[]
    def on_enter(self):
        Notifications()
    def notify(self):
        Notifications()


    def open(self):
        ntf = FloatLayout()

        t = Label(text =self.manager.user.notification1,color =(0,0,0,1),
                  pos_hint ={"x":0.3,"y":0.5},size_hint =(None,None))
        ntf.add_widget(t)

        t1 = Label(text =self.manager.user.notification2,color =(0,0,0,1),
                   pos_hint ={"x":0.3,"y":0.4},size_hint =(None,None))
        ntf.add_widget(t1)

        t2 = Label(text =self.manager.user.notification3,color =(0,0,0,1),
                   pos_hint ={"x":0.3,"y":0.3},size_hint =(None,None))
        ntf.add_widget(t2)

        p = Popup(title ="AFSC says",title_color =(0,0,0,1),background ="",
                  size =(450,250),size_hint =(None,None),content = ntf,background_color =(0,0,0,0.1),)
        p.open()

    def supervise(self):
        Supervise()


class Admin(Screen):#Admin page


    def supervise(self):
        Supervise()





class SignUp(Screen):#SignUp page
    user = ObjectProperty()
    pass1 =ObjectProperty()
    pass2 = ObjectProperty()



    def clear(self):
        self.user.text = ""
        self.pass1.text = ""
        self.pass2.text =""



    def submit(self):
        if self.pass1.text =="" or self.pass2.text=="" or  self.user.text=="":
            pop = Popup(title="Alert", content=Label(text="Fill up all fields"), size_hint=(None, None), size=(400, 400))
            pop.open()

        elif self.pass1.text != self.pass2.text:
            pop =Popup(title ="Alert",title_color =(0,0,0,1),title_size =22,content =Label(text ="Password Mismatch",
                                                                                           color = (0,0,1,1),font_size =22),
                       size_hint =(None,None), size= (400,200), background ="")
            pop.open()



        else:
            cur.execute("SELECT * from staff where UserName =%s",(self.user.text,))
            users =[]
            for e in cur:
                users.append(e)
            if len(users)==0:
                pop = Popup(title="AFSC says",title_color =(0,0,0,1),title_size =22, content=Label(text="Your are not a recognised employee" +\
                                                                                     "\n" +\
                                                                                     " of this organisation", color =(0,0,1,1),font_size =22),
                             size_hint=(None, None),
                             size=(400, 300),background ="",background_color =(0,0,0,0.1),)
                pop.open()
            else:
                cur.execute("SELECT Password from staff where UserName =%s",(self.user.text,))
                for e in cur:
                    for i in e:
                        if i == None:
                            pas = self.pass1.text
                            pass1 = hashlib.sha256(pas.encode("ascii")).hexdigest()
                            cur.execute("Update staff  set Password =%s where UserName =%s",
                                             (pass1, self.user.text,))
                            con.commit()
                            pop = Popup(title="AFSC says", title_color=(0, 0, 0, 1),title_size =22,
                                        content=Label(
                                            text="Registration Complete"+ "\n"+" you can proceed to log into the system",
                                            color=(0, 0, 1, 1),font_size =22),
                                        size_hint=(None, None),
                                        size=(400, 300), background="",background_color =(0,0,0,0.1),)
                            pop.open()
                        else:
                            pop = Popup(title="AFSC says", title_color=(0, 0, 0, 1),
                                        content=Label(text="Your have already registered into the system",
                                                      color=(0, 0, 0, 1)),
                                        size_hint=(None, None),
                                        size=(400, 400), background="",background_color =(0,0,0,0.1), )
                            pop.open()



class AddTask(Screen):#Page for adding Tasks


    def show_date(self):
            MDDatePicker(callback =self.day,background_color =(0,0,0,0.1),).open()


    def day(self,the_date):
         self.ids.cale.text = str(the_date)


    def  submit(self):
        if self.ids.cale.text =="" or self.manager.user.taskName=="" or self.manager.user.taskdsc=="":
            p =Popup(background ="", title = "AFSC says",title_color =(0,0,0,1),title_size =22,content =Label(text = "Fill all fields",
                                                                                                              color =(0,0,1,1),font_size =22),
                     size =(250,200),size_hint =(None,None),background_color =(0,0,0,0.1),)
            p.open()
        else:
            self.manager.user.taskdate = self.ids.cale.text
            day = dt.strptime(self.manager.user.taskdate,"%Y-%m-%d").date()
            if day< tod:
                pop =Popup(background ="", title = "AFSC says",title_color =(0,0,0,1),title_size =22,content =Label(text = "Date Selection Void",
                      color =(0,0,1,1),font_size =22),
                     size =(230,200),size_hint =(None,None),background_color =(0,0,0,0.1),)
                pop.open()
            else:
                tasks =[]
                cur.execute("SELECT TaskName FROM TASKS WHERE TaskName =%s and Action =%s",(self.manager.user.taskName,self.manager.user.usertext,))
                for e in cur:
                    for i in e:
                        tasks.append(i)
                if len(tasks)!=0:
                    pop = Popup(title ="Task Duplication",title_color =(0,0,0,1),title_size =22, content =Label(text="Duplication! -Task already recorded",
                           color =(0,0,1,1),font_size =22),size =(350,200)
                     ,size_hint =(None,None),background ="",background_color =(0,0,0,0.1),)
                    pop.open()
                else:
                    cur.execute("INSERT INTO TASKS(Action,TaskName,TaskDescrpt,DOF) VALUES(%s,%s,%s,%s)",(self.manager.user.usertext,self.manager.user.taskName,
                                     self.manager.user.taskdsc,self.manager.user.taskdate,))
                    con.commit()
                    pop = Popup(title = "AFSC says" ,title_color=(0,0,0,1),title_size =22,
                        content =Label(text = "Task successfully recorded",color =(0,0,1,1),font_size =22),
                        size =(300, 200), size_hint =(None,None),background ="",background_color =(0,0,0,0.1))
                    pop.open()
                    self.manager.user.staff.clear()
                    cur.execute("Select TaskName  from tasks Where Action = %s",(self.manager.user.usertext,))
                    for e in cur:
                        for i in e:
                            self.manager.user.staff.append(i)
                            self.manager.user.pending = str(len(self.manager.user.staff))

    def clear(self):
        self.ids.taskNm.text =""
        self.ids.cale.text =""
        self.ids.taskdsr.text =""

    def position(self):
        cur.execute("Select Role from staff where UserName =%s",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                self.manager.user.position = i
class SpiOption(SpinnerOption):
    background_color =(0,0,1,1)
    font_size =22

class AddStaff(Screen):#Page for adding staff

    nm = ObjectProperty()
    superv = ListProperty([])
    supervisor = StringProperty()

    def dept(self):
        self.superv.clear()
        self.manager.user.dept = self.ids.department.text
        cur.execute("Select UserName from staff where Department = %s and Supervision ='Yes'",
                    (self.manager.user.dept,))
        for i in cur:
            for e in i:
                self.superv.append(e)
        self.ids.sup.values = self.superv



    def add(self):
        d = self.ids.department.text
        r = self.ids.role.text
        c = self.ids.sup.text
        staff =[]

        cur.execute("Select UserName from staff where UserName = %s",(self.nm.text,))
        for e in cur:
            for i in e:
                staff.append(i)
        if len(staff)>0:
            pop = Popup(title ="AFSC says",title_color =(0,0,0,1),title_size =22,content = Label(text = "UserName already in use try another one",
                                                                                  color =(0,0,1,1),font_size=22),background ="",size =(350,200)
                                                                                   ,size_hint =(None,None),background_color =(0,0,0,0.1),)
            pop.open()
            staff.clear()
        else:
            cur.execute("Insert into staff(UserName,Department,Role,Supervision,Supervisor) VALUES(%s,%s,%s,%s,%s)",(self.nm.text,d,r,self.supervisor,c))
            con.commit()
            self.manager.user.staff.clear()
            pop = Popup(title="AFSC says", title_color=(0, 0, 0, 1),title_size =22,
                        content=Label(text= self.nm.text +"\n"+"successfully added",
                                      color=(0, 0, 1, 1),font_size =22,), background="", size=(350, 200)
                        , size_hint=(None, None),background_color =(0,0,0,0.1),)
            pop.open()


    def back(self):

        self.parent.current ="admin"

class TaskLayout(Button,Window):#class with definations of how Tasks will look like in the tasks page
    background_color =(0,0,1,1)
    btn =ObjectProperty()
    d1 = ObjectProperty()
    color = (1,1,1,1)
    font_size =26


    def on_press(self):
      if self.btn.text!= "NO PENDING TASKS":
          cur.execute("Select DOF from Tasks where TaskName = %s",(self.btn.text,))
          for e in cur:
              for i in e:
                  deadline = i
          cur.execute("Select TaskDescrpt from Tasks where TaskName =%s",(self.btn.text,))
          for e in cur:
              for i in e:
                  description = i

          def done(instance):
              p2.dismiss()
              cur.execute("Select TaskDescrpt from tasks where TaskName =%s and Action =%s",(self.btn.text, self.user.usertext,))
              for e in cur:
                  for i in e:
                      descrpt = i
              date= dt.strftime(tod,"%Y-%m-%d")
              cur.execute("Insert into previous(Action,TaskDescrpt,DOF) values (%s,%s,%s)",(self.user.usertext, descrpt,date))
              con.commit()
              cur.execute("Delete From Tasks where TaskName =%s and Action =%s",(self.btn.text,self.user.usertext,))
              con.commit()
              self.user.staff.clear()
              cur.execute("Select TaskName from tasks where Action =%s",(self.user.usertext,))
              for e in cur:
                  for i in e:
                      self.user.staff.append(i)
              self.user.pending = str(len(self.user.staff))
              if len(self.user.staff)==0:
                  self.user.staff.clear()
                  self.user.staff.append("NO PENDING TASKS")
                  p = Popup(title='Confirmation',title_color=(0,0,0,1),title_size =22,
                            content=Label(text=self.btn.text + "\n" + "successfully completed",
                                          color =(0,0,1,1),font_size =22),
                    size=(250, 200),
                    size_hint=(None, None),
                            background ="",background_color =(0,0,0,0.1),)
                  p.open()
          cur.execute("Select TaskDescrpt from tasks where Action = %s and TaskName = %s",(self.user.usertext,self.btn.text,))
          for e in cur:
              for i in e:
                  description = i
          try:
              date = dt.strptime(deadline,"%Y-%m-%d").date()
              days = (date -tod).days
              t = FloatLayout()
              l1 =Label(text ="Task Description:", size_hint =(None,None), pos_hint = {"x":0.1,"y":0.6},color =(0,0,0,1),font_size=21)
              t.add_widget(l1)
              l2 = Label(text = description, size_hint =(None,None),pos_hint ={"x":0.4,"y":0.5},color= (0,0,1,1),font_size=21)
              t.add_widget(l2)
              l3 = Label(text="Deadline:", size_hint=(None, None), pos_hint={"x": 0.1, "y": 0.3},color =(0,0,0,1),font_size=21)
              t.add_widget(l3)
              l2 = Label(text=deadline, size_hint=(None, None), pos_hint={"x": 0.3, "y": 0.3},color= (0,0,1,1),font_size=21)
              t.add_widget(l2)
              l4 = Label(text="Days left:", size_hint=(None, None), pos_hint={"x": 0.1, "y": 0.1}, color=(0,0,0,1),font_size=21)
              t.add_widget(l4)
              l3 = Label(text=str(days), size_hint=(None, None), pos_hint={"x": 0.3, "y": 0.1}, color=(0,0,1,1),font_size=21)
              t.add_widget(l3)
              b1 = Button(text = "Done", size =(100,40), pos_hint = {"x":0.1,"y":0.0},size_hint =(None,None), on_press =done,
                      background_color =(0,0,0,1), font_size=21)
              t.add_widget(b1)
              b2 =Button(text ="Pending", size=(100,40), pos_hint = {"x":0.5,"y":0.0},size_hint =(None,None),on_press =Pending,
                     background_color =(1,0,0,1),font_size=21)
              t.add_widget(b2)
              p2 = Popup(title = "Task Assessment",title_color=(0,0,0,1), content = t,size =(680,300),
                         size_hint = (None,None),background ="",background_color =(0,0,0,0.1),)
              p2.open()
          except Exception:
              p2 = Popup(title="Alert", title_color=(0, 0, 0, 1),title_size=22, content=Label(text  ="SOMETHING WRONG",color =(1,0,0,1)
                                                                                ,font_size =22), size=(680, 300),
                         size_hint=(None, None), background="",background_color =(0,0,0,0.1),)
              p2.open()
      else:
          pass


class RV(Screen):# Show Tasks
    percentage = StringProperty()


    def on_enter(self):
        deadlines =[]
        completed =[]
        cur.execute("SELECT DOF FROM tasks where Action =%s",(self.manager.user.usertext,))
        for i in cur:
            for e in i:
                date = dt.strptime(e,"%Y-%m-%d").date()
                if date>=start and date<=end:
                    deadlines.append(date)

        cur.execute("SELECT DOF FROM previous where Action =%s", (self.manager.user.usertext,))
        for i in cur:
            for e in i:
                date = dt.strptime(e,"%Y-%m-%d").date()
                if date >= start and date <= end:
                    deadlines.append(date)


        cur.execute("SELECT DOF FROM previous WHERE Action =%s",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                 datecom =dt.strptime(i,"%Y-%m-%d").date()
                 if datecom >= start and datecom <= end:
                     completed.append(datecom)
        all = len(deadlines)
        complete = len(completed)
        try:
            completeper = int((complete/all)*100)
            self.percentage = str(completeper)
        except Exception:
            pass

    def clear(self):
        self.manager.user.staff.clear()

    def position(self):
        self.manager.user.staff.clear()
        cur.execute("Select Role from staff where UserName =%s",(self.manager.user.usertext,))
        for e in cur:
            for i in e:
                self.manager.user.position = i



    def refresh(self):
        self.parent.current ="view"





class DeleteStaff(Screen):# Page/ Screen for deleting staff
    spi = ObjectProperty()
    u = ListProperty([])


    def on_enter(self):#Retrieving UserNames from the Server for deletion
        cur.execute("SELECT UserName FROM STAFF ")
        for e in cur:
            for i in e:
                if  i =="afsc":
                    pass
                else:
                    self.u.append(i)

    def delete(self):#functionality for delete on popup

        name =self.spi.text

        def remove(instance):
            po.dismiss()
            cur.execute("Delete from staff where UserName = %s",(name,))
            con.commit()
            p = Popup(title ="AFSC says",title_color = (0,0,1,1),title_size =22,content =Label(text = name +"\n" + "was successfully removed from the server",
                                                                                               color =(0,0,1,1),font_size =22)
                      ,size_hint =(None,None),size =(450,200),background ="",background_color =(0,0,0,0.1))
            p.open()

        def close(instance):
            po.dismiss()

        t2 = FloatLayout()

        L1 = Label(text = "Do you really want to delete this employee",color =(0,0,0,1),size_hint=(None,None),pos_hint ={"x":0.4,"y":0.5},font_size =22)
        t2.add_widget(L1)

        b1 =MDFillRoundFlatIconButton(text = "Yes",md_bg_color =(0,1,1,1),text_color=(0,0,0,1),
                                  pos_hint={"x":0.1,"y":0.4},size_hint=(None,None),icon ="check",font_size =22,on_release =remove)
        t2.add_widget(b1)

        b2 = MDFillRoundFlatIconButton(text ="No", md_bg_color =(1,0,0,1),text_color =(0,0,0,1), pos_hint={"x":0.6,"y":0.4},
                                   size_hint =(None,None),icon ="xbox",font_size =22,on_release =close)

        t2.add_widget(b2)

        po = Popup(title ="AFSC says",title_color = (0,0,0,1),content =t2,title_size =22,size=(490,270),
                   size_hint =(None,None),background ="",background_color =(0,0,0,0.1),)
        po.open()



    def back(self):
        self.u.clear()


def Supervise():

    class Supervise(FloatLayout):
        people =[]
        cur.execute("SELECT UserName from staff WHERE Supervisor =%s",(State.usert))
        for e in cur:
            for i in e:
                people.append(i)
        if len(people)==0:
            people.append("Operation void")
        else:
            pass

        def clear(self):
            p.dismiss()

    class Employee(Button):
        font_size =22
        background_color=(1,1,1,0.0)
        btn = ObjectProperty()
        user = StringProperty()
        color =(0,0,0,1)

        def on_press(self):
            p.dismiss()
            self.user = self.btn.text
            State.emp =self.user
            class EmployeeTasks(FloatLayout):
                tasks = []
                cur.execute("SELECT TaskName from tasks WHERE Action =%s",(self.user,))
                for e in cur:
                    for i in e:
                        tasks.append(i)
                if len(tasks)==0:
                    tasks.append("Operation Void")


                def assign(self):
                    class Assign(FloatLayout):

                        def dismiss(self):
                            p.dismiss()

                        def show_date(self):
                            MDDatePicker(callback=self.day).open()

                        def day(self, the_date):
                            self.ids.cale.text = str(the_date)

                        def done(self):
                            cur.execute("INSERT INTO TASKS(Action,TaskName,TaskDescrpt,DOF) VALUES(%s,%s,%s,%s)",
                                        (State.emp, self.ids.tname.text,
                                         self.ids.description.text, self.ids.cale.text,))
                            con.commit()
                            p1 = Popup(content=Label(text ="Task Assignment to"+"\n"+State.emp +"Successfull",color =(0,0,1,1),font_size =22),
                                                                          background="", title="Confirmation",
                                      title_color=(0, 0, 1, 1), title_size=22, size=(300, 300),size_hint=(None,None),background_color =(0,0,0,0.1),)

                            p1.open()

                    a =Assign()
                    p =Popup(content =a,background ="",title ="Assign task to" +"\n" +State.emp,
                             title_color =(0,0,1,1),title_size =22,size =(500,300),background_color =(0,0,0,0.1),)
                    p.open()







            class Tasks(Button):
                font_size=22
                lab = ObjectProperty()
                background_color =(1,1,1,0.0)
                color = (0,0,0,1)
                user =self.user


                def on_press(self):
                    p1.dismiss()
                    t = FloatLayout()
                    try:
                        cur.execute("SELECT TaskDescrpt from Tasks where Action =%s and TaskName =%s",
                                (self.user, self.lab.text,))
                        for e in cur:
                            for i in e:
                                description = i

                        cur.execute("SELECT DOF from Tasks where Action =%s and TaskName =%s",
                                (self.user, self.lab.text,))
                        for e in cur:
                            for i in e:
                                deadline = i

                        l1 = Label(text="TaskDescription", font_size=22, color=(0, 0, 0, 1), size_hint=(None, None),
                               pos_hint={"x": 0.1, "y": 0.5})
                        t.add_widget(l1)

                        l2 = Label(text=description, font_size=20, color=(0, 0, 1, 1), size_hint=(None, None),
                               pos_hint={"x": 0.4, "y": 0.4})
                        t.add_widget(l2)

                        l3 = Label(text="Deadine", font_size=22, color=(0, 0, 0, 1), size_hint=(None, None),
                               pos_hint={"x": 0.0, "y": 0.2})
                        t.add_widget(l3)

                        l4 = Label(text=deadline, font_size=22, color=(0, 0, 1, 1), size_hint=(None, None),
                               pos_hint={"x": 0.4, "y": 0.2})

                        t.add_widget(l4)

                        y = t
                        p2 = Popup(size=(550, 370), title="Task Description", title_size=22, title_color=(0, 0, 0, 1),
                               content=y,
                               size_hint=(None, None), background="",background_color =(0,0,0,0.1))
                        p2.open()
                    except:
                        p2 = Popup(size=(350, 370), title="Error", title_size=22, title_color=(0, 0, 0, 1),
                                   content=Label(text ="Operation Void",color =(1,0,0,1),font_size =22),
                                   size_hint=(None, None), background="", background_color =(0,0,0,0.1),)
                        p2.open()




            em  =EmployeeTasks()
            p.dismiss()
            p1 = Popup(size=(500, 370), title="Tasks Pending",title_size =22, title_color=(0, 0, 0, 1), content=em,
                      size_hint=(None, None), background="",background_color =(0,0,0,0.1),)
            p1.open()


    r =Supervise()
    p =Popup(size =(500,370),title ="Supervision",title_size =22 ,title_color=(0,0,0,1),content =r,
             size_hint=(None,None),background="",background_color =(0,0,0,0.1),)
    p.open()


def Pending(instance):
    class Pend(FloatLayout):

        def show_date(self):
            MDDatePicker(callback=self.day,background_color =(0,0,0,0.1)).open()

        def day(self, the_date):
            cur.execute("Update tasks Set DOF =%s where Action = %s",(str(the_date),State.usert,))
            con.commit()
            p.dismiss()
            p1= Popup(title="Confirmation", title_color=(0, 0, 0, 1),title_size =22, size=(200, 200), size_hint=(None, None),
                      background="", content=Label(text = "New Deadline set to" +"\n"\
                                                   +str(the_date),color =(0,0,0,1)),background_color =(0,0,0,0.1))
            p1.open()


    d =Pend()

    p = Popup(title ="SET NEW DEADLINE",title_color =(0,0,0,1),size= (350,200),size_hint =(None,None),
              background ="",content =d,background_color =(0,0,0,0.1),)
    p.open()

def Notifications():
    class Notify:
        notifications =[]
        cur.execute("SELECT DOF from tasks WHERE Action = %s",(State.usert))
        for e in cur:
            for i in e:
                day = dt.strptime(i,"%Y-%m-%d").date()
                if day>=start and day<=end:
                    pass




kv =Builder.load_file("afsc.kv")

class AFSC(App):
    theme_cls = ThemeManager()
    theme_cls.primary_palette = "Indigo"
    theme_cls.accent_palette = "Blue"
    theme_cls.theme_style ="Light"
    title = "AFSC ZIMBABWE"
    
    def build(self):
        return kv

if __name__ =="__main__":
    AFSC().run()


