import tkinter
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  #PIL=PYTHON IMAGE LIBRARY
from tkcalendar import Calendar
from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import Image
import copy
import tkinter
from tkinter import *

from tkinter import messagebox
from tkinter. messagebox import askyesno
from PIL import ImageTk  #PIL=PYTHON IMAGE LIBRARY
import mysql.connector
import copy
# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table,TableStyle,colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, PageBreak, Image, Spacer, Table, TableStyle)
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import LETTER, inch
from reportlab.graphics.shapes import Line, LineShape, Drawing
from reportlab.lib.colors import Color
from datetime import *
from datetime import datetime
import time

#con9=mysql.connector.connect(host='localhost',user='root',password='test123', database='feasted')#helps commiting changes
#mycursor9=con9.cursor()
#query='create table IF NOT EXISTS USERDATA( email varchar(50) PRIMARY KEY ,username varchar(100) UNIQUE NOT NULL,password varchar(20) NOT NULL)'
#mycursor.execute(query)


#INVOICE GENERATION
class FooterCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
        self.width, self.height = LETTER

    def showPage(self):                           
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if (self._pageNumber > 1):
                self.draw_canvas(page_count)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_canvas(self, page_count):
        page = "Page %s of %s" % (self._pageNumber, page_count)
        x = 128
        self.saveState()
        self.setStrokeColorRGB(0, 0, 0)
        self.setLineWidth(0.5)
        # self.drawImage("static/lr.png", self.width - inch * 8 - 5, self.height - 50, width=100, height=20,
        #                preserveAspectRatio=True)
        # self.drawImage("static/ohka.png", self.width - inch * 2, self.height - 50, width=100, height=30,
        #                preserveAspectRatio=True, mask='auto')
        self.line(30, 740, LETTER[0] - 50, 740)
        self.line(66, 78, LETTER[0] - 66, 78)
        self.setFont('Times-Roman', 10)
        self.drawString(LETTER[0] - x, 65, page)
        self.restoreState()


class PDFPSReporte:

    customeremail = ""
    customername = ""
    customerphone1 = 0
    customerphone2 = 0
    orderlist = ""
    orderdate = ""
    eventdate = ""
    headcount = 0
    location = ""
    total = 0
    Cutlery = ""
    livecooking = ""
    res=[[]]

    def __init__(self, path, orderid):
        self.path = path
        self.orderid = orderid
        self.styleSheet = getSampleStyleSheet()
        self.elements = []

        # colors - Azul turkeza 367AB3
        self.colorOhkaGreen0 = Color((45.0 / 255), (166.0 / 255), (153.0 / 255), 1)
        self.colorOhkaGreen1 = Color((182.0 / 255), (227.0 / 255), (166.0 / 255), 1)
        self.colorOhkaGreen2 = Color((140.0 / 255), (222.0 / 255), (192.0 / 255), 1)
        # self.colorOhkaGreen2 = Color((140.0/255), (222.0/255), (192.0/255), 1)
        self.colorOhkaBlue0 = Color((54.0 / 255), (122.0 / 255), (179.0 / 255), 1)
        self.colorOhkaBlue1 = Color((122.0 / 255), (180.0 / 255), (225.0 / 255), 1)
        self.colorOhkaGreenLineas = Color((50.0 / 255), (140.0 / 255), (140.0 / 255), 1)

        self.getOrderDetails(orderid)
        self.firstPage()
        self.nextPagesHeader(True)
        self.remoteSessionTableMaker()
        self.nextPagesHeader(False)


        # self.inSiteSessionTableMaker()
        # self.nextPagesHeader(False)
        # self.extraActivitiesTableMaker()
        # self.nextPagesHeader(False)
        # self.summaryTableMaker()
        # Build
        self.doc = SimpleDocTemplate(path, pagesize=LETTER)
        self.doc.multiBuild(self.elements)
        #self.doc.multiBuild(self.elements, canvasmaker=FooterCanvas)

    def getOrderDetails(self, orderid):
        mydb = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
        mycursor = mydb.cursor()
        query = 'SELECT * FROM CUSTORDERINFO where order_id=%s'
        mycursor.execute(query, [orderid])
       # mycursor.execute(query)
        rows = mycursor.fetchall()
        for row in rows:
            print(row)
            print(orderid)
            #orderid = row[0]
            self.customeremail = row[1]
            self.customername = row[4]
            self.customerphone1 = row[5]
            self.customerphone2 = row[6]
            self.orderlist = row[7]
            self.orderdate = row[8]
            self.eventdate = row[9]
            self.headcount = row[10]
            self.location = row[11]
            self.total = row[12]
            self.Cutlery = row[13]
            self.livecooking = row[14]
            self.res=eval(self.orderlist)



    def firstPage(self):
        # img = Image('static/lr.png', kind='proportional')
        # img.drawHeight = 0.5 * inch
        # img.drawWidth = 2.4 * inch
        # img.hAlign = 'LEFT'
        # self.elements.append(img)

        spacer = Spacer(30, 100)
        self.elements.append(spacer)

        # img = Image.open('static/ohka.png')
        # img.drawHeight = 2.5 * inch
        # img.drawWidth = 5.5 * inch
        # self.elements.append(img)

        spacer = Spacer(10, 250)
        self.elements.append(spacer)

        psDetalle = ParagraphStyle('Resumen', fontSize=12, leading=14, justifyBreaks=1, alignment=TA_LEFT,
                                   justifyLastLine=1)
        text = """Feasted Catering services<br/>
        Invoice for: """ + self.customername + " / " + self.customeremail + """<br/>
        Phone Numbers: """ + str(self.customerphone1) + " / " + str(self.customerphone2) + """<br/>
        Location: """ + str(self.location) + """<br/>
        Date of invoice: """ + self.orderdate.strftime("%d %B %Y") + """<br/>
        Date of Event: """ + self.eventdate.strftime("%d %B %Y") + """<br/>
        No of people attending: """ + str(self.headcount) + """<br/>
        Cutlery Needed: """ + str(self.Cutlery) + """<br/>
        Live cooking in the venue: """ + str(self.livecooking) + """<br/>
        Order ID for enquiry: """ + str(self.orderid) + """<br/>
        
        """
        paragraphReportSummary = Paragraph(text, psDetalle)
        self.elements.append(paragraphReportSummary)
        self.elements.append(PageBreak())

    def nextPagesHeader(self, isSecondPage):
        if isSecondPage:
            psHeaderText = ParagraphStyle('Hed0', fontSize=16, alignment=TA_LEFT, borderWidth=3,
                                          textColor=self.colorOhkaGreen0)
            text = 'Invoice Details'
            paragraphReportHeader = Paragraph(text, psHeaderText)
            self.elements.append(paragraphReportHeader)

            spacer = Spacer(10, 10)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 2
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 1)
            self.elements.append(spacer)

            d = Drawing(500, 1)
            line = Line(-15, 0, 483, 0)
            line.strokeColor = self.colorOhkaGreenLineas
            line.strokeWidth = 0.5
            d.add(line)
            self.elements.append(d)

            spacer = Spacer(10, 22)
            self.elements.append(spacer)



    def remoteSessionTableMaker(self):
        psHeaderText = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                      textColor=self.colorOhkaBlue0)
        text = ''
        paragraphReportHeader = Paragraph(text, psHeaderText)
        self.elements.append(paragraphReportHeader)

        spacer = Spacer(10, 22)
        self.elements.append(spacer)
        """
        Create the line items
        """
        d = []
        textData = ["ID", "Dish Name", "Veg/Non Veg", "Unit Price", "Qty", "Total"]

        fontSize = 8
        centered = ParagraphStyle(name="centered", alignment=TA_CENTER)
        for text in textData:
            ptext = "<font size='%s'><b>%s</b></font>" % (fontSize, text)
            titlesTable = Paragraph(ptext, centered)
            d.append(titlesTable)

        data = [d]
        lineNum = 1
        formattedLineData = []

        alignStyle = [ParagraphStyle(name="01", alignment=TA_CENTER),
                      ParagraphStyle(name="02", alignment=TA_LEFT),
                      ParagraphStyle(name="03", alignment=TA_CENTER),
                      ParagraphStyle(name="04", alignment=TA_CENTER),
                      ParagraphStyle(name="05", alignment=TA_CENTER),
                      ParagraphStyle(name="06", alignment=TA_CENTER)]
        tot=0
        for sublist in self.res:
            lineData = sublist
            tot+=lineData[-1]
            # data.append(lineData)
            columnNumber = 0
            for item in lineData:
                ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
                p = Paragraph(ptext, alignStyle[columnNumber])
                formattedLineData.append(p)
                columnNumber = columnNumber + 1
            data.append(formattedLineData)
            formattedLineData = []

        # Row for total
        totalRow = ["Total ", "", "", "", "", str(tot)]
        for item in totalRow:
            ptext = "<font size='%s'>%s</font>" % (fontSize - 1, item)
            p = Paragraph(ptext, alignStyle[1])
            formattedLineData.append(p)
        data.append(formattedLineData)




        # print(data)
        table = Table(data, colWidths=[50, 200, 80, 80, 80])
        tStyle = TableStyle([  # ('GRID',(0, 0), (-1, -1), 0.5, grey),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            # ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
            ('LINEABOVE', (0, 0), (-1, -1), 1, self.colorOhkaBlue1),
            ('BACKGROUND', (0, 0), (-1, 0), self.colorOhkaGreenLineas),
            ('BACKGROUND', (0, -1), (-1, -1), self.colorOhkaBlue1),
            ('SPAN', (0, -1), (-2, -1))
        ])
        table.setStyle(tStyle)
        self.elements.append(table)

        text2 = '''TOTAL COST FOR ''' + str(self.headcount) + 'PEOPLE   :' + str(tot * (self.headcount))

        pstext2 = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                 textColor=self.colorOhkaBlue0)
        tex = Paragraph(text2, pstext2)
        self.elements.append(tex)
        if (self.Cutlery).lower() =='yes':
            cuttot=(self.headcount)*10
        else:
            cuttot=0

        if (self.livecooking).lower()=='yes':
            servicetot=(self.headcount)*100
        elif (self.livecooking).lower()=='no':
            servicetot=0

        text3 = '''TOTAL INCLUDING TRANSPORTATION, CUTLERY, SERVICE     :''' + str(tot * (self.headcount))+'+'+str(cuttot+servicetot)+'='+str(tot * (self.headcount)+cuttot+servicetot)

        pstext3 = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                 textColor=self.colorOhkaBlue0)
        tex34 = Paragraph(text3, pstext3)
        self.elements.append(tex34)


        if self.headcount <= 40:
            noofservers = 4
            #cost = noofservers * 1500
        elif 100 <= self.headcount <= 500:
            noofservers = 12
            #cost = 12 * 1500
        else:
            noofservers = int(12 + (self.headcount / 200))
            #cost = noofservers * 1500
        text4 = '''NUMBER OF SERVERS  :   ''' + str(noofservers)
        pstext4 = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                 textColor=self.colorOhkaBlue0)
        tex45 = Paragraph(text4, pstext4)
        self.elements.append(tex45)

        text5 = '''ADVANCE 30% OF COST  :   ''' +str(0.3*(tot * (self.headcount)+cuttot+servicetot))
        pstext5 = ParagraphStyle('Hed0', fontSize=12, alignment=TA_LEFT, borderWidth=3,
                                 textColor=self.colorOhkaBlue0)
        tex56 = Paragraph(text5, pstext5)
        self.elements.append(tex56)











#Functionality
CARRYFORWARDDATA = []
def connect_DATABASE():
    try:
        con = mysql.connector.connect(host='localhost', user='root', password='test123',database='feasted')  # helps commiting changes
        mycursor = con.cursor()
    except:
        messagebox.showerror('Error', 'Database Connectivity issue')
    query = 'use feasted'
    mycursor.execute(query)
    #mycursor.execute('SELECT * from USERDATA')
    #ROW=mycursor.fetchall()
    C = tUsN.get()
    D = tPASW.get()

    sql = "select * from userdata where username = %s and password = %s"
    mycursor.execute(sql, [(C), (D)])
    ROW = mycursor.fetchall()

    if ROW:
        for i in ROW:
            messagebox.showinfo('Info','ACCOUNT EXISTS')
            messagebox.showinfo('INFO', 'LOGIN SUCCESSFUL')
            #CARRYFORWARDDATA=copy.deepcopy(i)
            #print(CARRYFORWARDDATA,'INSIDE ROW')
            #print('Successful')
    else:
        #print('failed')
        messagebox.showerror('Error',"THE CREDENTIALS ARE NOT CORRECT/ ACCOUNT DOESN'T EXIST")
        con.close()
    x=(C,D)
    '''
    if x in ROW:
        print('LOGIN SUCCESSFUL')
        messagebox.showinfo('INFO','LOGIN SUCCESSFUL')
    '''

    sql = "select * from userdata where username = %s"
    mycursor.execute(sql, [C])
    ROW2 = mycursor.fetchall()
    for i in ROW2:
        for y in i:
            CARRYFORWARDDATA.append(y)

    Loginwindow.destroy()












def user_enter(event):
    if tUsN.get()=='Username':
        tUsN.delete(0,END)
def pass_enter(event):
    if tPASW.get()=='Password':
        tPASW.delete(0,END)

def hide():
    openeye.config(file="C:\\Users\\aweso\\OneDrive\\Desktop\\\FEASTED\\feasted pics\\INVISIBLE.png") #CONFIG MODIFIES
    tPASW.config(show='*')
    eyebutton.config(command=show)

def show():
    openeye.config(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\VISIBLE.png")
    tPASW.config(show='')
    eyebutton.config(command=hide)
def signup_page():
    Loginwindow.destroy()
    import Signin
#GUI

Loginwindow=Tk()
Loginwindow.resizable(0,0)
Loginwindow.title("LOGIN")
#Loginwindow.wm_attributes('-toolwindow')
bgimage=ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\BACKWEL.png")
RL = Label(Loginwindow, image=bgimage)
RL.grid(column=0, row=0)
heading=Label(Loginwindow,text='LOG IN',font=("Dosis ExtraBold",30,'bold',),bg='#663300',fg="#ffffff")
heading.place(x=890,y=40)
#welcome=Label(Loginwindow,text='Welcome back!',font=("Times New Roman",30,'bold','italic'),bg='#FAB615',fg="#000000")
#welcome.place(x=150,y=180)
#USERN=Label(Loginwindow,text='USER-NAME:',font=("Times New Roman",20,'bold',),bg='#323752',fg="#ffffff")
#USERN.place(x=650,y=165)


tUsN = Entry(Loginwindow, width=20,font=("Courier New",28,'bold'),fg='#ffffff',bg='#663300',bd=0)
tUsN.place(x=720,y=200)
tUsN.insert(0,'Username')
#pasd=Label(Loginwindow,text='PASSWORD:',font=("Times New Roman",20,'bold',),bg='#323752',fg="#ffffff")
#pasd.place(x=650,y=230)
tPASW = Entry(Loginwindow, width=20,font=("Courier New",28,'bold',),bg='#663300',fg="#ffffff",bd=0)
tPASW.place(x=720,y=325)
tPASW.insert(0,'Password')
tUsN.bind('<FocusIn>',user_enter)
tPASW.bind('<FocusIn>',pass_enter)
RL.pack()
frame1=Frame(Loginwindow,width=345,height=2).place(x=720,y=236)
frame2=Frame(Loginwindow,width=345,height=2).place(x=720,y=359)
closeeye=PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\INVISIBLE.png")
openeye=PhotoImage(file='C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\VISIBLE.png')
eyebutton=Button(Loginwindow,image=openeye,bd=0,bg='#663300',activebackground='#663300',cursor='hand2',command=hide)
eyebutton.place(x=1170,y=320)

bt_frame=tkinter.Frame(Loginwindow,highlightthickness=1,highlightbackground='#ffffff')

#Forgotbutton=Button(Loginwindow,text='Forgot password?',width=20,font=("Courier New",15,'bold'),bd=0,bg='#663300',fg="#ffffff",activebackground='#663300',activeforeground='#ffffff'cursor='hand2')
bt_frame.pack()
#Forgotbutton.place(x=990,y=390)
loginbutton=Button(Loginwindow,text='LOGIN',width=20,font=("Dosis ExtraBold",25,'bold'),bd=0,bg='#ffffff',fg="#663300",activebackground='#663300',activeforeground='#ffffff'
                    ,cursor='hand2',command=connect_DATABASE)
loginbutton.place(x=790,y=450)
orlabel=Label(Loginwindow,text='--------------OR--------------',width=20,font=("Dosis ExtraBold",10,'bold'),bd=0,bg='#663300',fg="#ffffff",activebackground='#663300',activeforeground='#ffffff')
orlabel.place(x=890,y=537)

DsignUp=Label(Loginwindow,text="Don't have an account?",width=25,font=("Courier New",11,'bold'),bd=0,bg='#663300',fg="#ffffff",activebackground='#663300',activeforeground='#ffffff')
DsignUp.place(x=710,y=565)


signUp=Button(Loginwindow,text="Create new account",width=25,font=("Courier New",12,'bold'),bd=0,bg='#663300',fg="#FEB101",activebackground='#FEB101',activeforeground='#663300',command=signup_page)
signUp.place(x=940,y=560)




Loginwindow.mainloop()

import tkinter as tk
from tkinter import PhotoImage
import PIL
from PIL import ImageTk, Image
from tkinter import ttk

def GOTOMENUPAGE():
    root.destroy()
print('CARRY FORWARD DATA',CARRYFORWARDDATA)

root=tk.Tk()
root.geometry('1300x720')
root.resizable(0,0)


main_frame=tk.Frame(root)
main_frame.pack(fill='both', expand=1)

main_canvas=tk.Canvas(main_frame)
main_canvas.pack(side='left', fill='both', expand=1)

main_scrollbar=ttk.Scrollbar(main_frame, orient='vertical', command=main_canvas.yview)
main_scrollbar.pack(side='right', fill='y')

main_canvas.configure(yscrollcommand=main_scrollbar.set)
main_canvas.bind('<Configure>', lambda e: main_canvas.configure(scrollregion=main_canvas.bbox('all')))

main_2frame=tk.Frame(main_canvas)

main_canvas.create_window((0,0), window=main_2frame, anchor='nw')

image1_mainpage=Image.open("C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\slide1.png")
image1_mainpage_=ImageTk.PhotoImage(image1_mainpage)
main_canvas.create_image(0,0,image=image1_mainpage_,anchor='nw')

image2_mainpage=ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\SLIDE2.PNG")
main_canvas.create_image(0,720,image=image2_mainpage,anchor='nw')

image3_mainpage=ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\Slide4.png")
main_canvas.create_image(0,1440,image=image3_mainpage,anchor='nw')

topframe=tk.Label(main_canvas,text='Feasted!                                                         About Us             Members             Contact Us', bg='white',width=77 ,font=('Script MT Bold',20))
topframe.pack(padx=19,pady=0)

ordernowbutton=tk.Button(main_canvas, text='ORDER NOW', font=('Rockwell', 25,'bold'), bg='#1fc2db',cursor='hand2', activebackground='white',highlightthickness=7, highlightbackground='#f0d613' ,activeforeground='#0d0c0d',command=GOTOMENUPAGE)
ordernowbutton.place(x=985, y=470)

usericon=ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\usericon3.png")
profileimage=tk.Button(main_canvas,image=usericon, borderwidth=0, border=0)
profileimage.place(x=1180,y=3)




root.mainloop()
from tkinter import ttk
import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk  # PIL=PYTHON IMAGE LIBRARY
from tkcalendar import Calendar
from tkcalendar import DateEntry
from tkinter import messagebox
from PIL import *
import copy

# FUNCTION DEFINITIONS
# insert an item to the list.



ORDERTOUSE = []


def INSERTITEM():
    try:
        w = str(DISHIDENTRY.get())
        e = int(QUANTITYNO.get())
        te = int(DISHIDENTRY.get())

        db = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
        cur = db.cursor(prepared=True)

        query = "SELECT DISHID,DISHNAME,VORNV,PRICE FROM MASTERTABLE where DISHID = %s "
        cur.execute(query, (w,))
        row3 = cur.fetchall()
        for i in row3:
            l = []
            for t in i:
                l.append(t)
            l.extend([e])
            print(l)

            if l in order:
                messagebox.showerror("ERROR", 'ALREADY IN LIST')

            else:
                order.append(l)
                print(order)

            count = 0
            for item in order:
                if item[0] == te:
                    count = count + 1
                    if count > 1:
                        order.remove(item)
                        messagebox.showerror("ERROR", 'ALREADY IN LIST,UPDATE')
                        print('NEW', order)
            """

            for coun in range(len(order)):
                if (l[0])==(order[coun][0]):
                    messagebox.showerror("ERROR", 'ALREADY IN LIST')
                else:
                    order.append(l)
                    print(order)
            """
            """
            if (len(order))>0:
                for ITEM in order:
                    if (l[0])==(ITEM[0]):
                        messagebox.showerror("ERROR", 'ALREADY IN LIST')
                    else:
                        order.append(l)
                        print(order)
            """

    except Exception as e:
        if not ((DISHIDENTRY.get()).isdigit()) or not ((QUANTITYNO.get()).isdigit()) or (
                (int(QUANTITYNO.get())) < 0) == TRUE:
            messagebox.showerror('Error', 'GIVE VALID ENTRY ')


def ORDERLISTIT():
    REVIEWwindow = Toplevel()
    REVIEWwindow.title('SEE ITEMS')
    REVIEWwindow.resizable(0, 0)
    REVIEWwindow.configure(bg='WHITE')

    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    # Add a Treeview widget
    tree2 = ttk.Treeview(REVIEWwindow, column=("DISHID", "DISHNAME", "VORNV", 'PRICEPER', 'QUANTITY', 'COST'),
                         show='headings', height=5)
    tree2.column("DISHID", anchor=CENTER)
    tree2.heading("DISHID", text="DISHID")
    tree2.column("DISHNAME", anchor=CENTER)
    tree2.heading("DISHNAME", text="DISHNAME")
    tree2.column("VORNV", anchor=CENTER)
    tree2.heading("VORNV", text="VORNV")
    tree2.column("PRICEPER", anchor=CENTER)
    tree2.heading("PRICEPER", text="PRICEPER")
    tree2.column("QUANTITY", anchor=CENTER)
    tree2.heading("QUANTITY", text="QUANTITY")
    tree2.column("COST", anchor=CENTER)
    tree2.heading("COST", text="COST")
    tree2.pack()
    try:
        orderdisplay = copy.deepcopy(order)
        DISHIDNUMBER = DISHIDENTRY.get()

        def DISPLAYTHEORDER():
            for S in orderdisplay:
                if len(S) == 5:
                    # print(S)
                    f = S[-2]
                    # print(f)
                    c = S[-1]
                    # print(c)
                    S.append(f * c)
                tree2.insert('', tk.END, values=S)



    except Exception as e:
        messagebox.showerror('ERROR', 'INTERNAL ERROR')
        # else:
        #    f=S[-3]
        #    c=S[-2]
        #    S[-1]=(f*c)
    DISPLAYTHEORDER()
    REVIEWwindow.mainloop()


def DELETEITEM():
    en = DISHIDENTRY.get()
    length = len(order)
    if length == 0:
        messagebox.showerror("Error", 'NO ITEM TO DELETE, LIST EMPTY ')
    else:
        try:
            for i in range(length):
                if (order[i][0]) == int(en):
                    order.remove((order[i]))
                    print('NEW', order)
            # else:
            # messagebox.showerror('Error', "DISH NOT INSERTED, HENCE NOT DELETED")
        except Exception as e:
            messagebox.showerror('Error', "DISH NOT INSERTED, HENCE NOT DELETED")


def UPDATEITEM():
    en = DISHIDENTRY.get()
    ennum = QUANTITYNO.get()
    length = len(order)
    if length == 0:
        messagebox.showerror("Error", 'NO ITEM TO DELETE, LIST EMPTY ')
    else:
        try:
            for i in range(length):
                if (order[i][0]) == int(en):
                    if len(order[i]) == 5:
                        order[i][-1] = int(ennum)
                        print('NEW', order)
        except Exception as e:
            messagebox.showerror('Error', "DISH NOT INSERTED, HENCE NOT DELETED")

messagebox.showinfo('INFO','THE QUANTITY YOU ARE ENTERING IS FOR EACH SERVING')
menuwindow = tk.Tk()

order = []

menuwindow.geometry('1530x700+0+0')
menuwindow.resizable(0, 0)
menuwindow.configure(bg='WHITE')
menuwindow.title('MENU AND ORDER')
s = ttk.Style()
s.configure('Treeview', rowheight=40)

tree = ttk.Treeview(menuwindow, column=("DISHID", "DISHNAME", "DESCRIPTION", 'V OR NV', 'PRICE'), show='headings',
                    height=10)
tree.column("DISHID", anchor=tk.CENTER)
tree.heading('DISHID', text="DISHID")
tree.column("DISHNAME", anchor=tk.CENTER)
tree.heading("DISHNAME", text="DISHNAME")
tree.column("DESCRIPTION", anchor=tk.CENTER, width=500)
tree.heading("DESCRIPTION", text="DESCRIPTION")
tree.column("V OR NV", anchor=tk.CENTER)
tree.heading("V OR NV", text="V OR NV")
tree.column("PRICE", anchor=tk.CENTER)
tree.heading("PRICE", text="PRICE")
tree.pack()


def connect():
    con1 = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
    cur1 = con1.cursor()
    con1.commit()
    cur1.execute("SELECT * FROM MASTERTABLE")
    rows = cur1.fetchall()
    for row in rows:
        # print(row)
        tree.insert('', tk.END, values=row)
    con1.close()


connect()


def SEARCHBOXENTRY(event):
    k = SEARCHBYCMB.get()

    db = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
    cur = db.cursor()
    cur.execute("SELECT* FROM CUISINES")

    qCUISINELIST = []
    for i in cur:
        qCUISINELIST.append(i)
    print(qCUISINELIST)

    qCUISINELIST.append('VEG')
    qCUISINELIST.append('NON VEG')
    # print(qCUISINELIST)

    cur.execute('SELECT DISHID, DISHNAME FROM MASTERTABLE')

    if k == 'NORTH INDIAN':
        print('NORTH INDIAN')
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '2__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()




    elif k == 'SOUTH INDIAN':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '1__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'INDO-CHINESE':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '4__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'WESTERN':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '3__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'BEVERAGES':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '6__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'SNACKABLES':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where DISHID like '5__'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'VEG':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where VORNV like 'V'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    elif k == 'NON VEG':
        print(k)
        # for u in qCUISINELIST:
        #    if k in u:
        #        m=str(u[0])
        #        print(m)
        cur.reset()
        tree.delete(*tree.get_children())
        cur.execute("SELECT * FROM MASTERTABLE where VORNV like 'NV'")

        rows2 = cur.fetchall()

        for p in rows2:
            print(p)
            tree.insert('', tk.END, values=p)
            db.close()
    # for o in cur:
    # print(o)


Bottomframe = Frame(menuwindow, background='#ffffff')
Bottomframe.place(x=0, y=430, width=1530, height=555)

SEARCHBY = Label(Bottomframe, text='SEARCH BY', font=('Raleway Black', 18, 'bold'), background='#ffffff',
                 foreground='#000000')
SEARCHBY.place(x=0, y=150)

SEARCHBYCMB = ttk.Combobox(Bottomframe, values=(
    'SOUTH INDIAN', 'NORTH INDIAN', 'INDO-CHINESE', 'WESTERN', 'BEVERAGES', 'SNACKABLES', 'VEG', 'NON VEG'),
                           font=('Raleway Black', 18, 'bold'), state='readonly')
SEARCHBYCMB.place(x=150, y=150)
SEARCHBYCMB.bind('<FocusIn>', SEARCHBOXENTRY)

DISHIDLABEL = Label(Bottomframe, text='DISH ID', font=('Raleway Black', 18, 'bold'), background='#ffffff',
                    foreground='#000000')
DISHIDLABEL.place(x=0, y=20)

DISHIDENTRY = Entry(Bottomframe, width=20, font=("Raleway Black", 18, 'bold'), fg='#000000', bg='#ffffff', bd=0,
                    borderwidth=1, relief='solid')
DISHIDENTRY.place(x=100, y=20)

QUANTITY = Label(Bottomframe, text='QUANTITY', font=('Raleway Black', 18, 'bold'), background='#ffffff',
                 foreground='#000000')
QUANTITY.place(x=0, y=80)

QUANTITYNO = Entry(Bottomframe, width=20, font=("Raleway Black", 18, 'bold'), fg='#000000', bg='#ffffff', bd=0,
                   borderwidth=1, relief='solid')
QUANTITYNO.place(x=130, y=80)

INSERTBUT = Button(Bottomframe, text='INSERT ITEM', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0, bg='#000000',
                   fg="#ffffff", activebackground='#ffffff', activeforeground='#000000'
                   , cursor='hand2', command=INSERTITEM)
INSERTBUT.place(x=500, y=50)

ORDERLIST = Button(Bottomframe, text='ORDER LIST', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0, bg='#000000',
                   fg="#ffffff", activebackground='#ffffff', activeforeground='#000000'
                   , cursor='hand2', command=ORDERLISTIT)
ORDERLIST.place(x=500, y=150)

# orderdisplay=order

DELETEBUT = Button(Bottomframe, text='DELETE', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0, bg='#000000',
                   fg="#ffffff", activebackground='#ffffff', activeforeground='#000000'
                   , cursor='hand2', command=DELETEITEM)
DELETEBUT.place(x=800, y=50)

UPDATE = Button(Bottomframe, text='UPDATE', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0, bg='#000000',
                fg="#ffffff", activebackground='#ffffff', activeforeground='#000000'
                , cursor='hand2', command=UPDATEITEM)
UPDATE.place(x=800, y=150)




def WHENORDERCONFORMED():
    ordertocarry = copy.deepcopy(order)
    print('FIRST STATEMENT', order)
    #ordertocarry=copy.deepcopy(order)
    #print('SECOND STATEMENT', order)
    #print('ODER TO CARRY IST STATEMENT',ordertocarry)

    if len(ordertocarry) == 0:
        messagebox.showerror('ERROR', 'INSERT ITEMS')
    elif len(ordertocarry) < 5:
        messagebox.showwarning('ERROR', 'MINIMUM 5 ITEMS MUST BE INSERTED')
    else:
        REVIEW2window = Tk()
        REVIEW2window.title('CONFIRM THE ORDER FINAL')
        REVIEW2window.resizable(0, 0)
        REVIEW2window.configure(bg='WHITE')
        REVIEW2window.geometry('1530x700+0+0')

        bottomfram2 = Frame(REVIEW2window)
        bottomfram2.place(x=0, y=440, width=1530, height=555)
        bottomfram2.configure(bg='white')

        style2 = ttk.Style()
        style2.configure('Treeview', rowheight=40)

        # Add a Treeview widget
        tree3 = ttk.Treeview(REVIEW2window, column=("DISHID", "DISHNAME", "VORNV", 'PRICEPER', 'QUANTITY', 'COST'),
                             show='headings', height=10)
        tree3.column("DISHID", anchor=CENTER)
        tree3.heading("DISHID", text="DISHID")
        tree3.column("DISHNAME", anchor=CENTER)
        tree3.heading("DISHNAME", text="DISHNAME")
        tree3.column("VORNV", anchor=CENTER)
        tree3.heading("VORNV", text="VORNV")
        tree3.column("PRICEPER", anchor=CENTER)
        tree3.heading("PRICEPER", text="PRICEPER")
        tree3.column("QUANTITY", anchor=CENTER)
        tree3.heading("QUANTITY", text="QUANTITY")
        tree3.column("COST", anchor=CENTER)
        tree3.heading("COST", text="COST")
        tree3.pack()

        def ACTUALLYCONFIRM():
            ORDERTOUSE = copy.deepcopy(ordertocarry)
            menuwindow.destroy()
            REVIEW2window.destroy()

            # import PROFILEPAGE2

        for ST in ordertocarry:
            if len(ST) == 5:
                # print(S)
                f = ST[-2]
                # print(f)
                c = ST[-1]
                # print(c)
                ST.append(f * c)

        for yem in ordertocarry:
            tree3.insert('',tk.END,values=yem)
                # tree3.insert('', tk.END, values=ST)

        print(ordertocarry,'ORDERTOCARRY AFTER ITERATION')
        print(order,'AFTER INSERTION OF COST')
        """
            # menuwindow.destroy()
            # REVIEW2window.destroy()
            # import PROFILEPAGE2

        print(order, 'INSIDE WHENORDERCONFIRMED: BEFORE ITERATION')
        """
        """
        for ST in ordertocarry:
            if len(ST) == 5:
                # print(S)
                f = ST[-2]
                # print(f)
                c = ST[-1]
                # print(c)
                ST.append(f * c)
            tree3.insert('', tk.END, values=ST)
        """

        print('ORDERTOUSE',ORDERTOUSE,id(ORDERTOUSE))
        total = 0
        for item in ordertocarry:
            total = total + item[-1]
        print(total)
        print(order,'INSIDE WHENORDERCONFIRMED')
        print(ordertocarry,'ORDERTOCARRY')

        TOTAALLABEL = Label(bottomfram2, text='TOTAL PRICE PER PERSON', font=('Raleway Black', 20, 'bold'),
                            background='#ffffff',
                            foreground='#000000')
        TOTAALLABEL.place(x=700, y=20)

        TOTALDISPLAY = Label(bottomfram2, text=total, font=('Raleway Black', 20, 'bold'), background='#ffffff',
                             foreground='#000000')
        TOTALDISPLAY.place(x=1100, y=20)

        CONFIRMACTUAL = Button(bottomfram2, text='FINAL CONFIRM', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0,
                               bg='#000000', fg="#ffffff", activebackground='#ffffff', activeforeground='#000000'
                               , cursor='hand2', command=ACTUALLYCONFIRM)
        CONFIRMACTUAL.place(x=0, y=20)

        def MAKECHANGESDEF():
            global ordertocarry
            del ordertocarry
            REVIEW2window.destroy()

        MAKECHANGES = Button(bottomfram2, text='MAKE CHANGES', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0,bg='#ffffff', fg="#ff1303", activebackground='#ff1303', activeforeground='#ffffff', cursor='hand2', command=MAKECHANGESDEF)
        MAKECHANGES.place(x=350, y=20)

        REVIEW2window.mainloop()



CONFIRMORDER = Button(Bottomframe, text='CONFIRM', width=15, font=("MONTSERRAT BLACK", 20, 'bold'), bd=0, bg='#fc0303',fg="#ffffff", activebackground='#ffffff', activeforeground='#fc0303', cursor='hand2', command=WHENORDERCONFORMED)
CONFIRMORDER.place(x=1150, y=100)

# connect to the database

menuwindow.mainloop()


#from LOGIN_PAGE import CARRYFORWARDDATA
#from LOGIN_PAGE import *
#CARRYTHEDATA2=copy.deepcopy()

#if CARRYTHEDATA2 !=0:
#    import ABOUTUS_PAGE2
#from MENUPAGE_ORDER import *
#ORDERTOUSE2=copy.deepcopy(ORDERTOUSE)
#print(ORDERTOUSE2)
#print(CARRYTHEDATA2)

THEFINALLIST=[]
orderid=0
#CARRYFORWARDTHEORDER=ORDERTOUSE


def NOOFGUESTS():
    #print(value)
    try:
        if NOOFATTENDEES.get():
            return int(NOOFATTENDEES.get())
    except:
        messagebox.showerror('Error','ENTER VALID INTEGER VALUE')
        return


print(order,'nocost')
print(CARRYFORWARDDATA,'before profile')
if len(order)>=5:

    '''
    def display_details():
        for i in CARRYFORWARDDATA:
            profilewindow
    '''

    print()
    ordertocarry=copy.deepcopy(order)
    profilewindow=Tk()
    profilewindow.resizable(0,0)
    profilewindow.title("CUSTOMER AND EVENT DETAILS")
    bgrd=ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\FEASTED\\feasted pics\\PROFILE.png")
    BG = Label(profilewindow, image=bgrd)
    BG.grid(column=0, row=0)
    framep=Frame(profilewindow,bg="#f5dfeb")
    framep.place(x=100,y=150)

    Nameofuser=Label(framep,text='NAME',font=("Footlight MT Light",30,'bold'), bg="#f5dfeb", fg="#5e0396",anchor='w',bd=0)
    Nameofuser.grid(row=1,column=0,sticky='w',pady=(10,0))

    emailLabelp=Label(framep,text='EMAIL',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    emailLabelp.grid(row=6,column=0,sticky='w',pady=(10,0))

    #emailentryp=Label(framep,width=25,font=("Footlight MT Light",18,'bold',),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    #emailentryp.grid(row=6, column=1,sticky='w',pady=(10,0),padx=(10,0))

    emailentryp =Label(framep, width=25, text=CARRYFORWARDDATA[0],font=("Footlight MT Light", 18, 'bold',), bg="#f5dfeb", fg="#000000", bd=0,borderwidth=1, relief='solid')
    emailentryp.grid(row=6, column=1,sticky='w',pady=(10,0),padx=(10,0))

    NameofuserENT=Entry(framep,width=25,font=("Footlight MT Light",18,'bold',),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    NameofuserENT.grid(row=1, column=1,sticky='w',pady=(10,0),padx=(10,0))

    EVENTDATE=Label(framep,text='EVENT DATE',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    EVENTDATE.grid(row=2,column=0,sticky='w',pady=(10,0))

    EVENTDATEENTRY=DateEntry(framep,width=25, state='readonly',date_pattern='yyyy-mm-dd')
    EVENTDATEENTRY.grid(row=2, column=1,sticky='w',pady=(10,0),padx=(10,0))

    EVENTTIME=Label(framep,text='TIME',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    EVENTTIME.place(x=600,y=65)

    EVENTTIMEENTRY=Entry(framep,width=9,font=("Footlight MT Light",18,'bold',),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    EVENTTIMEENTRY.place(x=745, y=70)


    NOOFATTENDEES_label=Label(framep,text='NUMBER OF GUESTS',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    NOOFATTENDEES_label.grid(row=3,column=0,sticky='w',pady=(10,0))

    check=IntVar()

    NOOFATTENDEES=Entry(framep, width=25,font=("Footlight MT Light",18,'bold'),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid',textvariable=check)
    NOOFATTENDEES.grid(row=3,column=1,sticky='w',pady=(10,0), padx=(10,0))

    PHONENO1_label=Label(framep,text='PHONE NO. 1',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    PHONENO1_label.grid(row=4,column=0,sticky='w',pady=(10,0), padx=(0,0))

    PHONENO1_ENTRY=Entry(framep, width=25,font=("Footlight MT Light",18,'bold'),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    PHONENO1_ENTRY.grid(row=4,column=1,sticky='w',pady=(10,0), padx=(10,0))

    PHONENO2_label=Label(framep,text='PHONE NO. 2',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    PHONENO2_label.grid(row=5,column=0,sticky='w',pady=(10,0), padx=(0,0))

    PHONENO2_ENTRY=Entry(framep, width=25,font=("Footlight MT Light",18,'bold'),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    PHONENO2_ENTRY.grid(row=5,column=1,sticky='w',pady=(10,0), padx=(10,0))

    VENUE_label=Label(framep,text='VENUE',font=("Footlight MT Light",30,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    VENUE_label.grid(row=7,column=0,sticky='w',pady=(10,0), padx=(0,0))

    VENUE_ENTRY=Entry(framep, width=40,font=("Footlight MT Light",18,'bold'),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    VENUE_ENTRY.grid(row=7,column=1,sticky='w',pady=(10,0), padx=(10,0))


    check2=IntVar()

    COOKONSPOTQ_yes=Checkbutton(framep,bg="#f5dfeb", text='COOK ON SPOT?',font=("Gill Sans MT",18,'bold'),activebackground="#f5dfeb",activeforeground='#000000',cursor='hand2',variable=check2,offvalue='')
    COOKONSPOTQ_yes.grid(row=8,column=1,sticky='w',pady=(10,0), padx=(10,0))

    CUTLERYYESNO=Label(framep,text='DO YOU WANT CUTLERY?',font=("Gill Sans MT Condensed",20,'bold'),bg="#f5dfeb",fg="#5e0396",anchor='w',bd=0)
    CUTLERYYESNO.grid(row=8,column=0,sticky='w',pady=(10,0))

    CUTLERYENTRY=Entry(framep,width=7,font=("Footlight MT Light",18,'bold',),bg="#f5dfeb",fg="#000000",bd=0,borderwidth=1,relief='solid')
    CUTLERYENTRY.get()
    CUTLERYENTRY.insert(0,'Yes/No')
    CUTLERYENTRY.grid(row=8, column=0,sticky='w',pady=(10,0),padx=(224,0))

    def totalcal():
        total=0
        for item in ordertocarry:
            p=item[-2]
            q=item[-1]
            total = total + (p * q)
            item.append(p*q)
        return total


    TOADDINSQL = []
    orderid=0
    def WHENSUBMITTED():
        if NameofuserENT==0:
            messagebox.showerror('Error','ENTER VALID NAME')
        elif VENUE_ENTRY=='':
            messagebox.showerror('Error','Enter valid LOCATION')
        elif NOOFATTENDEES==0:
            messagebox.showerror('Error','Minimum 25 people must be present')
        e=CARRYFORWARDDATA[0]
        u=CARRYFORWARDDATA[1]
        P=CARRYFORWARDDATA[2]
        N=NameofuserENT.get()
        P1=int(PHONENO1_ENTRY.get())
        P2=int(PHONENO2_ENTRY.get())
        ORDERLIST=ordertocarry
        eventdt=EVENTDATEENTRY.get()
        NOA=int(NOOFATTENDEES.get())
        L=VENUE_ENTRY.get()
        #COSTFORSERVICE=NOA*100
        CUT=CUTLERYENTRY.get()

        if (CUTLERYENTRY.get()).lower()=='yes':
            CUTPRICE=(10)*NOA
        else:
            CUTPRICE=0


        if check2.get()==1:
            ons='yes'
            onscost=NOA*100
        elif check2.get()==0:
            ons='no'
            onscost=0

        cos = totalcal()
        pr = (cos * NOA)+onscost+CUTPRICE
        TOADDINSQL=(e,u,P,N,P1,P2,str(ORDERLIST),eventdt,NOA,L,pr,CUT,ons)
        mydb=mysql.connector.connect(host='localhost',user='root',password='test123', database='feasted')
        mycursor=mydb.cursor()
        query = 'create table IF NOT EXISTS CUSTORDERINFO(order_id MEDIUMINT primary key AUTO_INCREMENT NOT NULL,email varchar(50),username varchar(100),password varchar(20),NAME VARCHAR(100) NOT NULL, PHONENO1 int,PHONENO2 int, ORDERLIST TEXT NOT NULL, ORDER_DATE DATE NOT NULL,EVENT_DATE DATE NOT NULL,NOOFPEOPLE int not null,LOCATION varchar(255) not null,PRICE int not null,CUTLERY varchar(3) not null,ONSPOTORNO varchar(3) not null,FOREIGN KEY (username) references userdata(username),FOREIGN KEY (email) references userdata(email));'
        mycursor.execute(query)
        query='INSERT INTO CUSTORDERINFO(email,username,password,NAME,PHONENO1,PHONENO2,ORDERLIST,ORDER_DATE,EVENT_DATE,NOOFPEOPLE,LOCATION,PRICE,CUTLERY,ONSPOTORNO) VALUES(%s,%s,%s,%s,%s,%s,%s,CURRENT_DATE,%s,%s,%s,%s,%s,%s)'
        mycursor.execute(query,TOADDINSQL)
        toiterate=mycursor.fetchall()
        for vc in toiterate:
            for h in vc:
                if (h[1]==e) and (h[2]==u) and (h[9]==eventdt):
                    orderid=h[0]
                    print(orderid,'orderid')
        mydb.commit()
        mydb.close()
        #profilewindow.destroy()

        mydb = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
        mycursor = mydb.cursor()
        query = 'SELECT * FROM CUSTORDERINFO where username like %s and event_date like %s'
        mycursor.execute(query, [(u), (eventdt)])
        rows = mycursor.fetchall()

        for row in rows:
            print(row)
            orderid = row[0]
            print(orderid)
        mydb.close()
        tade=date.today()
        tme=time.localtime()
        tmea=time.strftime("%H:%M:%S", tme).replace(':','')
        FN=N+'_'+str(tade)+tmea

        #createpdf(row5)
        fileName = f"C:\\Users\\aweso\\Invoice_{FN.replace(' ', '_')}.pdf"
        print(fileName)
        report = PDFPSReporte(fileName,orderid)
        messagebox.showinfo('Info','INVOICE GENERATED : '+fileName)
        messagebox.showinfo('INFORMATION','DIRECTING TO PAYMENT PAGE')
        profilewindow.destroy()

        PAYMENTPAGE = Tk()
        PAYMENTPAGE.title('Servers and cutlery')
        PAYMENTPAGE.geometry('1280x720')
        PAYMENTPAGE.resizable(0, 0)

        def mode():
            accepted1 = accept_var1.get()
            if accepted1 == '':
                messagebox.showinfo('Required field', 'Please choose mode of payment')
            else:
                messagebox.showinfo('PAYMENT STATUS', 'PAYMENT DONE')
                PAYMENTPAGE.destroy()


        mydb = mysql.connector.connect(host='localhost', user='root', password='test123', database='feasted')
        mycursor = mydb.cursor()
        query = 'SELECT PRICE FROM CUSTORDERINFO where order_id like %s '
        mycursor.execute(query, (orderid,))
        row9 = mycursor.fetchall()
        for lrow in row9:
            money = lrow[0]
            print(money)
        mydb.close()
        advancemoney = 0.3 * money

        paypage = Frame(PAYMENTPAGE, highlightbackground='#3c0cab', highlightthickness=3)
        paypage_header = Label(paypage, text='COST & PAYMENT ', bg='#3c0cab', fg='white', font=('Eras Demi ITC', 26))
        paypage_header.place(x=0, y=0, width=840)
        paypage.pack(pady=30)
        paypage.pack_propagate(False)
        paypage.configure(width=780, height=850)
        totalcost_lb = Label(paypage, text='Total cost =', fg='black', font=('Bahnschrift Light Condensed', 32))
        totalcost_lb.place(x=0, y=90)
        totalcost_lbamt = Label(paypage, text=str(money), fg='black', font=('Bahnschrift Light Condensed', 32))
        totalcost_lbamt.place(x=250, y=90)
        payment_advance1 = Label(paypage, text='ADVANCE PAYMENT', fg='#3c0cab', bg='#85beed',
                                 font=('Berlin Sans FB', 20))
        payment_advance = Label(paypage, text='Advance payment amount=', fg='black',
                                font=('Bahnschrift Light Condensed', 17))
        payment_advanceamt = Label(paypage, text=str(advancemoney), fg='black',
                                   font=('Bahnschrift Light Condensed', 17))

        payment_advanceoptions = Label(paypage, text='Payment options:', fg='black', bg='#b4c4d1',
                                       font=('Bahnschrift Light Condensed', 16))
        payment_advance1.place(x=0, y=200)
        payment_advance.place(x=0, y=240)
        payment_advanceoptions.place(x=0, y=280)
        payment_advanceamt.place(x=300, y=240)

        var = StringVar()
        checkbox_1 = Checkbutton(paypage, text='Cash', font=14, variable=var, onvalue='Cash ', offvalue='')
        checkbox_2 = Checkbutton(paypage, text='Card', font=14, variable=var, onvalue='Card', offvalue='')
        checkbox_3 = Checkbutton(paypage, text='UPI', font=14, variable=var, onvalue='UPI', offvalue='')
        checkbox_1.place(x=10, y=320)
        checkbox_2.place(x=10, y=350)
        checkbox_3.place(x=10, y=380)
        payment_advancebutton = Button(paypage, text='PROCEED TO PAY', fg='white', bg='#3127ba',
                                       font=('Britannic Bold', 16),
                                       cursor='hand2', activebackground='white', highlightthickness=3,
                                       highlightbackground='#200f85', activeforeground='black')
        payment_advancebutton.place(x=30, y=420)

        mainpayment_header = Label(paypage, text='Please select MODE OF TOTAL PAYMENT* ', fg='#3c0cab', bg='#85beed',
                                   font=('Berlin Sans FB', 20))
        accept_var1 = StringVar(value='')
        checkbox_mp1 = Checkbutton(paypage, text='Cash on spot after event', font=15, variable=accept_var1,
                                   onvalue='Cash on spot after event', offvalue='')
        checkbox_mp2 = Checkbutton(paypage, text='UPI payment on spot after event', font=15, variable=accept_var1,
                                   onvalue='UPI payment on spot after event ', offvalue='')
        mainpayment_header.place(x=0, y=475)
        checkbox_mp1.place(x=10, y=520)
        checkbox_mp2.place(x=10, y=560)

        final_button = Button(paypage, text='PROCEED', fg='white', bg='#2920a1', font=('Britannic Bold', 21),
                              cursor='hand2',
                              activebackground='white', highlightthickness=5, highlightbackground='#200f85',
                              activeforeground='black', command=mode)
        final_button.place(x=555, y=582)

        starlabel = Label(paypage, text='*Required field', fg='#d44c4c', font=('Dubai Medium', 13))
        starlabel.place(x=10, y=614)
        PAYMENTPAGE.mainloop()
        messagebox.showinfo('INFO','PAYMENT PROCEDURES DONE')
        LOGOUTPAGE = Tk()
        LOGOUTPAGE.title('logout page')
        LOGOUTPAGE.geometry('1280x720')
        LOGOUTPAGE.resizable(0, 0)

        def logout():
            ans = askyesno(title='Logout', message='Do you want to Exit?')
            if ans:
                LOGOUTPAGE.destroy()
                messagebox.showinfo('INFO', 'LOGGED OUT')
        image_logoutpage = ImageTk.PhotoImage(file="C:\\Users\\aweso\\OneDrive\\Desktop\\\FEASTED\\feasted pics\\LOGOUT2.png")
        canvas_logout = Canvas(LOGOUTPAGE)
        canvas_logout.pack(side='left', fill='both', expand=True)
        canvas_logout.create_image(0, 0, image=image_logoutpage, anchor='nw')
        logoutbutton = Button(canvas_logout, text='LOGOUT', font=('Eras Bold ITC', 48), bg='#6610ad', cursor='hand2',
                              fg='white', activebackground='white', highlightthickness=7, highlightbackground='#f0d613',
                              activeforeground='#0d0c0d', command=logout)
        logoutbutton.place(x=810, y=522)
        LOGOUTPAGE.mainloop()




    SUBMIT_BUTTON=Button(framep,text='SUBMIT DETAILS',width=20,font=("MONTSERRAT BLACK",25,'bold'),bd=0,bg='#000000',fg="#ffffff",activebackground="#f5dfeb",activeforeground='#000000'
                        ,cursor='hand2',command=WHENSUBMITTED)
    SUBMIT_BUTTON.grid(row=9,column=1,sticky='w',pady=(10,0), padx=(10,0))

    profilewindow.mainloop()
else:
    messagebox.showerror('ERROR','AN ERROR HAS OCCURED')
    #import MENUPAGE_ORDER
    pass


