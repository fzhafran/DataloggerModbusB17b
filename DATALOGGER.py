import csv
import time
from datetime import datetime
from tkinter import *

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from matplotlib.figure import Figure
import subprocess, os
import psutil
from sys import executable
from subprocess import Popen, CREATE_NEW_CONSOLE

screensizex = 1205
screensizey = 730
root = Tk ()
root.geometry ('%dx%d' % (root.winfo_screenwidth(),root.winfo_screenheight()))
root.title ("Data Logger B17b")
root.config(background = "black")

parenttitle = Label (root, text = "", background = "black", fg = "white", font = (None, 10), anchor = "center")
parenttitle.grid (row = 71, column = 0)
btnahu= Button(root, text="AHU", width=12, height=1, background="white",
                        command=lambda: raiseframe(ahuparent))
btnahu.grid(row=72, column=0)
btncoldstor = Button(root, text="COLD STORAGE", width=12, height=1, background="white",
                        command=lambda: raiseframe(coldstorparent))
btncoldstor.grid(row=73, column=0)
filename = PhotoImage(file='b17.png')

def raiseframe (frame) :
    frame.tkraise()
    if frame == ahuparent :
        parenttitle.configure(text="AHU")
    if frame == coldstorparent :
        parenttitle.configure(text="COLD STORAGE")

coldstorparent = Frame(root, relief=RIDGE)
coldstorparent.grid(row = 1,rowspan = 70, column = 0)
coldstorparent.config(background='black')
bgcoldstor = Label(coldstorparent,image=filename)
bgcoldstor.grid(row = 0, column = 0)

ahuparent = Frame(root, relief=RIDGE)
ahuparent.grid(row = 1,rowspan = 70, column = 0)
ahuparent.config(background='black')
bgahu = Label(ahuparent,image=filename)
bgahu.grid(row = 0, column = 0)

xxx = 0
alerting = []
alarmsent = []
with open ('devicelist.csv','r') as limitlist :
    next(limitlist)
    for row in csv.reader(limitlist, delimiter = ','):
        alerting.append(0)
        alarmsent.append(0)
        
def hitung():
    global xxx
    xxx = xxx + 1
    # if xxx == 10 :
    #     try :
    #         print("starting")
    #         run = Popen('READER.exe', creationflags=CREATE_NEW_CONSOLE)
    #     except Exception as exc:
    #         print(exc)

    # if xxx == 10000 :
    #     try :
    #         print("closing....")
    #         os.system("taskkill /f /im READER.exe")

    #         try :
    #             run1 = Popen('autoerase.exe', creationflags=CREATE_NEW_CONSOLE)
    #         except Exception as exc:
    #             print(exc)
    #         xxx = 0
    #     except :
    #         xxx = 0
    return xxx

def alert (message):
    try :
        if message not in open('alertlog.csv', 'r').read():
            with open ('alertlog.csv', 'a') as alertlogging :
                alertlogging.write(str(message)+','+'\n')
            alertlogging.close()
        else :
            pass
    except :
        pass

def setval(name, alamat):
    def readsv():
        try :
            # instrumentsv = minimalmodbus.Instrument('COM4', int(alamat))
            # instrumentsv.serial.baudrate = 9600
            # instrumentsv.serial.bytesize = 8
            # instrumentsv.serial.parity = serial.PARITY_NONE
            # instrumentsv.serial.stopbits = 2
            # instrumentsv.serial.timeout = 1
            # instrumentsv.mode = minimalmodbus.MODE_RTU
            # datasv = instrumentsv.read_register(0x03eb, 1, 0x04, signed = True)
            svnowlabel.configure(text = "change sv ")

        except :
            svnowlabel.configure(text="change sv device")

    def changesetvalue() :
        data = valinput.get()
        try :
            with open('request.csv', 'a') as logging:
                logging.write(str(int(alamat)) + ',' + str(data) + ',' + '\n')
        except :
             pass

    with open ('devicelist.csv','r') as findalamat :
        next(findalamat)
        roomdetail = []
        alamataddrs = []
        for row in csv.reader(findalamat, delimiter = ','):
            roomdetail.append(str(row[0]))
            alamataddrs.append(float(row[1]))
    findalamat.close()

    alamat = alamataddrs[roomdetail.index(alamat)]

    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    popx = (screenwidth/2) - (screenwidth-screensizex)
    popy = (screenheight/2) - (screenheight-screensizey)
    setvalue = Toplevel()
    setvalue.title(name)
    setvalue.geometry('130x65+%d+%d'% (popx, popy))
    svnowlabel = Button(setvalue, width=10, height=1, text="aaaa", fg="black", font=(None, 8), anchor="center")
    svnowlabel.grid(row=0, column=0)
    valinput = Entry(setvalue, width=21, background="white", justify=RIGHT)
    valinput.grid(row=1, column=0)
    valinputbutton = Button(setvalue, text="enter", width=5, height=1, background="white",
                           command=lambda: changesetvalue())
    valinputbutton.grid(row=2, column=0)
    readsv()

def calendarpickstartend(title, sumbux, sumbuy):
    with open ('devicelist.csv','r') as dataplace :
        next(dataplace)
        parameterandroom = []
        placeofdata = []
        for row in csv.reader(dataplace, delimiter = ','):
            parameterandroom.append(str(row[0]))
            placeofdata.append(float(row[5]))
    dataplace.close()

    sumbux = placeofdata[parameterandroom.index(sumbux)]
    sumbuy = placeofdata[parameterandroom.index(sumbuy)]
    print(sumbux, sumbuy)
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    popx = (screenwidth / 2) - (screenwidth - screensizex)
    popy = (screenheight / 2) - (screenheight - screensizey)
    timepicker = Toplevel()
    timepicker.title("Pick Date and Time")
    timepicker.geometry('130x130+%d+%d' % (popx, popy))
    examplelabel = Label(timepicker, width=20, height=1, text="format : YYYY-MM-DD", fg="black", font=(None, 8), anchor="center")
    examplelabel.grid(row=0, column=0)
    starttimeframe = Frame (timepicker)
    starttimeframe.grid(row = 1, column = 0)
    endtimeframe = Frame (timepicker)
    endtimeframe.grid(row =2, column = 0)
    starttimelabel = Label (starttimeframe, width = 10,height = 1,  text = "start date", fg = "black", font = (None, 8), anchor = "center")
    starttimelabel.grid(row=0, column = 0)
    starttime = Entry(starttimeframe, width=18, background="white", justify=CENTER)
    starttime.grid(row= 1, column=0)
    endtimelabel = Label (endtimeframe, width = 10,height = 1,  text = "end date", fg = "black", font = (None, 8), anchor = "center")
    endtimelabel.grid(row=0, column= 0)
    endtime = Entry(endtimeframe, width=18, background="white", justify=CENTER)
    endtime.grid(row=1, column=0)
    graphbutton = Button(timepicker, text="Draw Graph", width=8, height=1, background="white",
                            command=lambda: monitoringdevice(title, sumbux, sumbuy, starttime.get(), endtime.get()))
    graphbutton.grid(row=3, column=0)
    timepicker.update()


def monitoringdevice (title, sumbux, sumbuy, awal, akhir) :
    def onFrameConfigure(monitorcanv):
        '''Reset the scroll region to encompass the inner frame'''
        monitorcanv.configure(scrollregion=monitorcanv.bbox("all"))

    with open ('logging.csv', 'r') as csvfiledev1 :
        next(csvfiledev1)
        x = []
        date = []
        y = []
        z = []
        for row in csv.reader (csvfiledev1, delimiter = ',') :
            dateonly = row[1].split()
            dateonly = dateonly[:-1]
            dateonly = ' '.join([str(elem) for elem in dateonly])
            x.append (float(row[0]))
            date.append (dateonly)
            y.append (float(row[int(sumbux)]))
            z.append (float(row[int(sumbuy)]))
    csvfiledev1.close()
    print(y)
    print(z)
    startgraph = date.index(awal)
    endgraph = (len(date) - 1) - list(reversed(date)).index(akhir)

    stepx = []
    stepy = []
    stepz = []
    for datatograph in range(startgraph,endgraph+1,1) :
        stepx.append(x[datatograph])
        stepy.append(y[datatograph])
        stepz.append(z[datatograph])

    monitordev1 = Toplevel ()
    monitordev1.title ("Graph")
    monitordev1.geometry ("1300x570")
    monitorcanv = Canvas (monitordev1, bg = 'black', width = 1300, height = 600, scrollregion = (0,0,1300,1500))
    vbar = Scrollbar(monitordev1, orient=VERTICAL, command=monitorcanv.yview)
    vbar.pack(side=RIGHT, fill=Y)
    monitorcanv.configure(yscrollcommand=vbar.set)
    monitorcanv.pack(side = LEFT, fill="both", expand = True)
    framemonitor = Frame(monitorcanv, width=1300, height=1500, background="black")
    framemonitor.pack(side=LEFT, fill=Y)
    monitorcanv.create_window((4, 4), window=framemonitor, anchor="nw")
    framemonitor.bind("<Configure>", lambda event, canvas=monitorcanv: onFrameConfigure(monitorcanv))

    graphtempdev1 = Frame (framemonitor, width = 13, height = 5, background = "white")
    graphtempdev1.grid (row = 0, column = 0, sticky = "nsew", pady = 5)
    # graphtempdev1.pack(side=BOTTOM, fill=Y)
    graphtempdev1label = Label (graphtempdev1, text = title +" Temperature" , anchor = CENTER, background = "white")
    graphtempdev1label.grid (row = 0, column = 0)
    figgraphtempdev1 = Figure (figsize = (13, 2.5), dpi = 100)
    figgraphtempdev1.add_subplot (111).plot (stepx, stepy, 'go-')
    canvas = FigureCanvasTkAgg (figgraphtempdev1, master = graphtempdev1)
    canvas.draw ()
    canvas.get_tk_widget ().grid (row = 1, column = 0)
    graphpresdev1 = Frame (framemonitor, width = 13, height = 5, background = "white")
    graphpresdev1.grid (row = 1, column = 0, sticky = "nsew", pady = 5)
    # graphpresdev1.pack(side=BOTTOM, fill=Y)
    graphpresdev1label = Label (graphpresdev1, text = title + " Pressure", anchor = CENTER, background = "white")
    graphpresdev1label.grid (row = 0, column = 0)
    figgraphpresdev1 = Figure (figsize = (13, 2.5), dpi = 100)
    figgraphpresdev1.add_subplot (111).plot (stepx, stepz, 'bo-')
    canvas = FigureCanvasTkAgg (figgraphpresdev1, master = graphpresdev1)
    canvas.draw ()
    canvas.get_tk_widget ().grid (row = 1, column = 0)

    graphtempall = Frame(framemonitor, width=13, height=5, background="white")
    graphtempall.grid(row=2, column=0, sticky="nsew", pady=5)
    # graphtempall.pack(side=BOTTOM, fill=Y)
    graphtempalllabel = Label(graphtempall, text=title + " Temperature all", anchor=CENTER, background="white")
    graphtempalllabel.grid(row=0, column=0)
    figgraphtempall = Figure(figsize=(13, 2.5), dpi=100)
    figgraphtempall.add_subplot(111).plot(x, y, 'go-')
    canvas = FigureCanvasTkAgg(figgraphtempall, master=graphtempall)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)
    graphpresall = Frame(framemonitor, width=13, height=5, background="white")
    graphpresall.grid(row=3, column=0, sticky="nsew", pady=5)
    # graphpresall.pack(side=BOTTOM, fill=Y)
    graphpresalllabel = Label(graphpresall, text=title + " Pressure all", anchor=CENTER, background="white")
    graphpresalllabel.grid(row=0, column=0)
    figgraphpresall = Figure(figsize=(13, 2.5), dpi=100)
    figgraphpresall.add_subplot(111).plot(x, z, 'bo-')
    canvas = FigureCanvasTkAgg(figgraphpresall, master=graphpresall)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0)
    vbar.config(command= monitorcanv.yview)

    x = y = z = date = stepx = stepy = stepz = None

def read () :
    global alerting
    hitung()
    with open ('realtimedata.csv', 'r') as csvfile :
        listingdata = []
        datain = []
        datacond = []
        for x, line in enumerate (csvfile) :
            if x == valuextemp1 :
                for y in line.split(',') :
                    listingdata.append(y)
                # print(len(listingdata)+1)
                for even in range (2,len(listingdata),2) :
                    datain.append(listingdata[even])
                for odd in range (3,len(listingdata),2) :
                    datacond.append(listingdata[odd])
    csvfile.close()

    with open ('devicelist.csv','r') as limitlist :
        next(limitlist)
        param = []

        minlimit = []
        maxlimit = []
        for row in csv.reader(limitlist, delimiter = ','):
            param.append(str(row[0]))
            minlimit.append(float(row[2]))
            maxlimit.append(float(row[3]))
    limitlist.close()

    dataout = [presentvalue1a, presentvalue1b,
               presentvalue2a, presentvalue2b,
               presentvalue3a, presentvalue3b,
               presentvalue4a, presentvalue4b,
               presentvalue5a, presentvalue5b,
               presentvalue6a, presentvalue6b,
               presentvalue7a, presentvalue7b,
               presentvalue8a, presentvalue8b,
               presentvalue9a, presentvalue9b,
               presentvalue10a, presentvalue10b,
               presentvalue11a, presentvalue11b,
               presentvalue12a, presentvalue12b,
               presentvalue13a, presentvalue13b,
               presentvalue14a, presentvalue14b,
               presentvalue15a, presentvalue15b,
               presentvalue16a, presentvalue16b,
               presentvalue17a, presentvalue17b,
               presentvalue18a, presentvalue18b,
               presentvalue19a, presentvalue19b,
               presentvalue20a, presentvalue20b
               ]
    choose = 0
    for entry in dataout :
        for suhu in range (0, len(dataout)+2, 2):
            if choose == suhu :
                if datacond[choose] == 'ON':
                    if minlimit[choose] < float(datain[choose]) < maxlimit[choose]:
                        entry.configure(bg="white", text="{value:6.2f} degC".format(value=float(datain[choose])))
                        try :
                            lines = []
                            with open('alertlog.csv', 'r') as inp :
                                deleteread = csv.reader(inp, delimiter = ',')
                                for row in deleteread:
                                    lines.append(row)
                                    for field in row:
                                        if field == param[choose]:
                                            lines.remove(row)
                            inp.close()
                            with open('alertlog.csv', 'w', newline = "\n") as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(lines)
                            writeFile.close()
                            alarmsent[choose], alerting[choose] = 0,0
                            lines = None
                        except :
                            pass

                    else:
                        entry.configure(bg="white", text="{value:6.2f} degC".format(value=float(datain[choose])))
                        alerting[choose] = 1
                        if alerting[choose] == 1 and alarmsent[choose] == 0:
                            alert(param[choose] +','+ param[choose] + " tidak sesuai")
                            alarmsent[choose] = 1
                if datacond[choose] == 'OFF':
                    entry.configure(bg="white", text="off")

        for tekanan in range (1, len(dataout)+2,2):
            if choose == tekanan :
                if datacond[choose] == 'ON':
                    if minlimit[choose] < float(datain[choose]) < maxlimit[choose]:
                        entry.configure(bg="white", text="{value:6.2f} pa".format(value=float(datain[choose])))
                        try :
                            lines = []
                            with open('alertlog.csv', 'r') as inp:
                                deleteread = csv.reader(inp, delimiter=',')
                                for row in deleteread:
                                    lines.append(row)
                                    for field in row:
                                        if field == param[choose]:
                                            lines.remove(row)
                            inp.close()
                            with open('alertlog.csv', 'w', newline = "\n") as writeFile:
                                writer = csv.writer(writeFile)
                                writer.writerows(lines)
                            writeFile.close()
                            alarmsent[choose], alerting[choose] = 0, 0
                            lines = None
                        except :
                            pass
                    else:
                        entry.configure(bg="white", text="{value:6.2f} pa".format(value=float(datain[choose])))
                        alerting[choose] = 1
                        if alerting[choose] == 1 and alarmsent[choose] == 0:
                            alert(param[choose] +','+ param[choose] + " tidak sesuai")
                            alarmsent[choose] = 1
                if datacond[choose] == 'OFF':
                    entry.configure(bg="white", text="off")

        choose = choose + 1
    listingdata = choose = datain = datacond = dataout = minlimit = maxlimit = param = None
    time.sleep(0.05)

def frameschedule (targetschedule):
    def schedule(targetschedule, waktumati, waktuhidup):
        with open('schedule.csv', 'a') as writer:
            writer.write(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ',' +
                         str(waktumati) + ',' + str(waktuhidup) + ',' + str(targetschedule) + ',' + '\n')
        writer.close()
        scheduleframe.destroy()

    with open('devicelist.csv', 'r') as scheduling:
        next(scheduling)
        paramlist = []
        addresslist = []
        for row in csv.reader(scheduling, delimiter=','):
            paramlist.append(str(row[0]))
            addresslist.append(int(row[1]))
    scheduling.close()
    print(addresslist)
    targetaddress = addresslist[paramlist.index(targetschedule)]
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    popx = (screenwidth / 2) - (screenwidth - screensizex)
    popy = (screenheight / 2) - (screenwidth - screensizex)
    scheduleframe = Toplevel()
    scheduleframe.title("Pick Date and Time")
    scheduleframe.geometry('130x130+%d+%d' % (popx, popy))
    exampletime = Label(scheduleframe, width=20, height=1, text="YYYY-MM-DD hh:mm:ss", fg="black", font=(None, 8),
                         anchor="center")
    exampletime.grid(row=0, column=0)
    framewaktuawal = Frame(scheduleframe)
    framewaktuawal.grid(row=1, column=0)
    framewaktuakhir = Frame(scheduleframe)
    framewaktuakhir.grid(row=2, column=0)
    labelwaktuawal = Label(framewaktuawal, width=10, height=1, text="start time", fg="black", font=(None, 8),
                           anchor="center")
    labelwaktuawal.grid(row=0, column=0)
    waktuawal = Entry(framewaktuawal, width=18, background="white", justify=CENTER)
    waktuawal.grid(row=1, column=0)
    labelwaktuakhir = Label(framewaktuakhir, width=10, height=1, text="end time", fg="black", font=(None, 8), anchor="center")
    labelwaktuakhir.grid(row=0, column=0)
    waktuakhir = Entry(framewaktuakhir, width=18, background="white", justify=CENTER)
    waktuakhir.grid(row=1, column=0)
    set = Button(scheduleframe, text="set", width=8, height=1, background="white",
                         command=lambda: schedule(targetaddress, waktuawal.get(), waktuakhir.get()))
    set.grid(row=3, column=0)
    paramlist = addresslist = None

########################################################################################################################
############################## FRAME PERSIAPAN 401 225##############################################################################
########################################################################################################################
frameahu1 = Frame (bgahu, width = 15, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu1.place (x = 401, y = 220)
##GRAPH and room name
roomlabel1 = Button (frameahu1, width = 8, height = 1, text = "Persiapan" ,
                     command = lambda : calendarpickstartend("Persiapan", "Suhu Persiapan","Tekanan Persiapan"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel1.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue1a = Button (frameahu1, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Persiapan", "Suhu Persiapan"))
presentvalue1a.grid (row = 1, column = 0)
presentvalue1b = Button (frameahu1, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Persiapan", "Tekanan Persiapan"))
presentvalue1b.grid (row = 2, column = 0)
# sch1 = Button (frameahu1, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch1.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME ALAT STERIL 566 261###############################################################################
########################################################################################################################
frameahu2 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu2.place (x = 566, y = 255)
##GRAPH and room name
roomlabel2 = Button (frameahu2, width = 8, height = 2, text = "Alat Steril" ,
                     command = lambda : calendarpickstartend("Alat Steril", "Suhu Alat Steril","Tekanan Alat Steril"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel2.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue2a = Button (frameahu2, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Alat Steril", "Suhu Alat Steril"))
presentvalue2a.grid (row = 0, column = 1)
presentvalue2b = Button (frameahu2, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Alat Steril", "Tekanan Alat Steril"))
presentvalue2b.grid (row = 1, column = 1)
# sch2 = Button (frameahu2, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch2.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME STERILISASI 540 215###############################################################################
########################################################################################################################
frameahu3 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu3.place (x = 536, y = 220)
##GRAPH and room name
roomlabel3 = Button (frameahu3, width = 8, height = 1, text = "Sterilisasi" ,
                     command = lambda : calendarpickstartend("Sterilisasi", "Suhu Sterilisasi","Tekanan Sterilisasi"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel3.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue3a = Button (frameahu3, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Sterilisasi", "Suhu Sterilisasi"))
presentvalue3a.grid (row = 0, column = 1)
presentvalue3b = Button (frameahu3, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Sterilisasi", "Tekanan Sterilisasi"))
presentvalue3b.grid (row = 0, column = 2)
# sch3 = Button (frameahu3, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch3.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME PRA 1 963 315###############################################################################
########################################################################################################################
frameahu4 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu4.place (x = 963, y = 315)
##GRAPH and room name
roomlabel4 = Button (frameahu4, width = 8, height = 1, text = "PRA 1" ,
                     command = lambda : calendarpickstartend("PRA 1", "Suhu PRA 1","Tekanan PRA 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel4.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue4a = Button (frameahu4, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("PRA 1", "Suhu PRA 1"))
presentvalue4a.grid (row = 1, column = 0)
presentvalue4b = Button (frameahu4, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("PRA 1", "Tekanan PRA 1"))
presentvalue4b.grid (row = 2, column = 0)
# sch4 = Button (frameahu4, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch4.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME PRA 2 755 316###############################################################################
########################################################################################################################
frameahu5 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu5.place (x = 755, y = 316)
##GRAPH and room name
roomlabel5 = Button (frameahu5, width = 8, height = 1, text = "PRA 2" ,
                     command = lambda : calendarpickstartend("PRA 2", "Suhu PRA 2","Tekanan PRA 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel5.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue5a = Button (frameahu5, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("PRA 2", "Suhu PRA 2"))
presentvalue5a.grid (row = 1, column = 0)
presentvalue5b = Button (frameahu5, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("PRA 2", "Tekanan PRA 2"))
presentvalue5b.grid (row = 2, column = 0)
# sch5 = Button (frameahu5, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch5.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME KOR BERSIH 143 303###############################################################################
########################################################################################################################
frameahu6 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu6.place (x = 125, y = 301)
##GRAPH and room name
roomlabel6 = Button (frameahu6, width = 10, height = 1, text = "K Bersih" ,
                     command = lambda : calendarpickstartend("K Bersih", "Suhu K Bersih","Tekanan K Bersih"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel6.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue6a = Button (frameahu6, width = 10,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "center",
                        command = lambda : setval("K Bersih", "Suhu K Bersih"))
presentvalue6a.grid (row = 0, column = 1)
presentvalue6b = Button (frameahu6, width = 10,height = 1, text = "", fg = "black", font = (None, 6), anchor = "center",
                         command = lambda : setval("K Bersih", "Tekanan K Bersih"))
presentvalue6b.grid (row = 0, column = 2)
# sch6 = Button (frameahu6, width = 10, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch6.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME POS INO 2 132 348###############################################################################
########################################################################################################################
frameahu7 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu7.place (x = 140, y = 335)
##GRAPH and room name
roomlabel7 = Button (frameahu7, width = 8, height = 1, text = "Post 2" ,
                     command = lambda : calendarpickstartend("Post 2", "Suhu Post 2","Tekanan Post 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel7.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue7a = Button (frameahu7, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Post 2", "Suhu Post 2"))
presentvalue7a.grid (row = 1, column = 0)
presentvalue7b = Button (frameahu7, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Post 2", "Tekanan Post 2"))
presentvalue7b.grid (row = 2, column = 0)
# sch7 = Button (frameahu7, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch7.grid (row = 0, column = 2, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME INOHARVEST 2 490 448###############################################################################
########################################################################################################################
frameahu8 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu8.place (x = 503, y = 450)
##GRAPH and room name
roomlabel8 = Button (frameahu8, width = 8, height = 2, text = "Inoharvest 2" ,
                     command = lambda : calendarpickstartend("Inoharvest 2", "Suhu Inoharvest 2","Tekanan Inoharvest 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel8.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue8a = Button (frameahu8, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Inoharvest 2", "Suhu Inoharvest 2"))
presentvalue8a.grid (row = 0, column = 1)
presentvalue8b = Button (frameahu8, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Inoharvest 2", "Tekanan Inoharvest 2"))
presentvalue8b.grid (row = 1, column = 1)
# sch8 = Button (frameahu8, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch8.grid (row = 1, column = 1, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME CANDLING 389 446###############################################################################
########################################################################################################################
frameahu9 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu9.place (x = 395, y = 442)
##GRAPH and room name
roomlabel9 = Button (frameahu9, width = 8, height = 1, text = "Candling" ,
                     command = lambda : calendarpickstartend("Candling", "Suhu Candling","Tekanan Candling"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel9.grid (row = 0, column = 0, columnspan = 2)
##PRESENT VALUE
presentvalue9a = Button (frameahu9, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Candling", "Suhu Candling"))
presentvalue9a.grid (row = 1, column = 0)
presentvalue9b = Button (frameahu9, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Candling", "Tekanan Candling"))
presentvalue9b.grid (row = 2, column = 0)
# sch9 = Button (frameahu9, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch9.grid (row = 1, column = 1, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME SEPARATOR 369 335###############################################################################
########################################################################################################################
frameahu10 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu10.place (x = 369, y = 350)
##GRAPH and room name
roomlabel10 = Button (frameahu10, width = 8, height = 2, text = "Separasi" ,
                     command = lambda : calendarpickstartend("Separasi", "Suhu Separasi","Tekanan Separasi"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel10.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue10a = Button (frameahu10, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Separasi", "Suhu Separasi"))
presentvalue10a.grid (row = 0, column = 1)
presentvalue10b = Button (frameahu10, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Separasi", "Tekanan Separasi"))
presentvalue10b.grid (row = 1, column = 1)
# sch10 = Button (frameahu10, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch10.grid (row = 0, column = 2, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME KOR KOTOR 343 417###############################################################################
########################################################################################################################
frameahu11 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu11.place (x = 327, y = 414)
##GRAPH and room name
roomlabel11 = Button (frameahu11, width = 8, height = 1, text = "K Kotor" ,
                     command = lambda : calendarpickstartend("K Kotor", "Suhu K Kotor","Tekanan K Kotor"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel11.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue11a = Button (frameahu11, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("POST K Kotor", "Suhu K Kotor"))
presentvalue11a.grid (row = 0, column = 1)
presentvalue11b = Button (frameahu11, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("POST K Kotor", "Tekanan K Kotor"))
presentvalue11b.grid (row = 0, column = 2)
# sch11 = Button (frameahu11, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch11.grid (row = 0, column = 2, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME DEKONT BSL 2 234 330###############################################################################
########################################################################################################################
frameahu12 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu12.place (x = 230, y = 325)
##GRAPH and room name
roomlabel12 = Button (frameahu12, width = 8, height = 1, text = "Dekont BSL 2" ,
                     command = lambda : calendarpickstartend("Dekont BSL 2", "Suhu Dekont BSL 2","Tekanan Dekont BSL 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel12.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue12a = Button (frameahu12, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Dekont BSL 2", "Suhu Dekont BSL 2"))
presentvalue12a.grid (row = 1, column = 0)
presentvalue12b = Button (frameahu12, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Dekont BSL 2", "Tekanan Dekont BSL 2"))
presentvalue12b.grid (row = 2, column = 0)
# sch12 = Button (frameahu12, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch12.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME DEKONT BSL 3 233 376###############################################################################
########################################################################################################################
frameahu13 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu13.place (x = 230, y = 380)
##GRAPH and room name
roomlabel13 = Button (frameahu13, width = 8, height = 1, text = "Dekont BSL 3" ,
                     command = lambda : calendarpickstartend("Dekont BSL 3", "Suhu Dekont BSL 3","Tekanan Dekont BSL 3"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel13.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue13a = Button (frameahu13, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Dekont BSL 3", "Suhu Dekont BSL 3"))
presentvalue13a.grid (row = 1, column = 0)
presentvalue13b = Button (frameahu13, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Dekont BSL 3", "Tekanan Dekont BSL 3"))
presentvalue13b.grid (row = 2, column = 0)
# sch13 = Button (frameahu13, width = 6, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch13.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME INOHV 1 237 447###############################################################################
########################################################################################################################
frameahu14 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu14.place (x = 237, y = 450)
##GRAPH and room name
roomlabel14 = Button (frameahu14, width = 8, height = 2, text = "Inoharvest 1" ,
                     command = lambda : calendarpickstartend("Inoharvest 1", "Suhu Inoharvest 1","Tekanan Inoharvest 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel14.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue14a = Button (frameahu14, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Inoharvest 1", "Suhu Inoharvest 1"))
presentvalue14a.grid (row = 0, column = 1)
presentvalue14b = Button (frameahu14, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Inoharvest 1", "Tekanan Inoharvest 1"))
presentvalue14b.grid (row = 1, column = 1)
# sch14 = Button (frameahu14, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch14.grid (row = 0, column = 2, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME KOR BERSIH 2 518 511###############################################################################
########################################################################################################################
frameahu15 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu15.place (x = 518, y = 508)
##GRAPH and room name
roomlabel15 = Button (frameahu15, width = 8, height = 1, text = "K Bersih 2" ,
                     command = lambda : calendarpickstartend("K Bersih 2", "Suhu K Bersih 2","Tekanan K Bersih 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel15.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue15a = Button (frameahu15, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "center",
                        command = lambda : setval("Kor K Bersih 2", "Suhu K Bersih 2"))
presentvalue15a.grid (row = 0, column = 1)
presentvalue15b = Button (frameahu15, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "center",
                         command = lambda : setval("Kor K Bersih 2", "Tekanan K Bersih 2"))
presentvalue15b.grid (row = 0, column = 2)
# sch15 = Button (frameahu15, width = 7, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch15.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME post ino 1 632 355###############################################################################
########################################################################################################################
frameahu16 = Frame (bgahu, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu16.place (x = 645, y = 335)
##GRAPH and room name
roomlabel16 = Button (frameahu16, width = 8, height = 1, text = "Post 1" ,
                     command = lambda : calendarpickstartend("Post 1", "Suhu Post 1","Tekanan Post 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel16.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue16a = Button (frameahu16, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Post 1", "Suhu Post 1"))
presentvalue16a.grid (row = 1, column = 0)
presentvalue16b = Button (frameahu16, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Post 1", "Tekanan Post 1"))
presentvalue16b.grid (row = 2, column = 0)
# sch16 = Button (frameahu16, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch16.grid (row = 0, column = 2, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME CHILL 1###############################################################################
########################################################################################################################
frameahu17 = Frame (bgcoldstor, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu17.place (x = 235, y = 453)
##GRAPH and room name
roomlabel17 = Button (frameahu17, width = 8, height = 2, text = "Chilling 1" ,
                     command = lambda : calendarpickstartend("Chilling 1", "Suhu Chilling 1","Tekanan Chilling 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel17.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue17b = Button (frameahu17, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Chilling 1", "Tekanan Chilling 1"))
presentvalue17b.grid (row = 0, column = 1)
presentvalue17a = Button (frameahu17, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Chilling 1", "Suhu Chilling 1"))
presentvalue17a.grid (row = 1, column = 1)

# sch17 = Button (frameahu17, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch17.grid (row = 0, column = 2, rowspan = 2)
# ########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME chill 2##############################################################################
########################################################################################################################
frameahu18 = Frame (bgcoldstor, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu18.place (x = 527, y = 398)
##GRAPH and room name
roomlabel18 = Button (frameahu18, width = 8, height = 2, text = "Chilling 2" ,
                     command = lambda : calendarpickstartend("Chilling 2", "Suhu Chilling 2","Tekanan Chilling 2"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel18.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue18b = Button (frameahu18, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "e",
                         command = lambda : setval("Chilling 2", "Tekanan Chilling 2"))
presentvalue18b.grid (row = 0, column = 1)
presentvalue18a = Button (frameahu18, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "e",
                        command = lambda : setval("Chilling 2", "Suhu Chilling 2"))
presentvalue18a.grid (row = 1, column = 1)

# sch18 = Button (frameahu18, width = 5, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch18.grid (row = 0, column = 3, rowspan = 2)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME BULK###############################################################################
########################################################################################################################
frameahu19 = Frame (bgcoldstor, width = 10, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu19.place (x = 560, y = 332)
##GRAPH and room name
roomlabel19 = Button (frameahu19, width = 8, height = 1, text = "Bulk 1" ,
                     command = lambda : calendarpickstartend("Bulk 1", "Suhu Bulk 1","Tekanan Bulk 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel19.grid (row = 0, column = 0)
##PRESENT VALUE
presentvalue19b = Button (frameahu19, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "center",
                         command = lambda : setval("Bulk 1", "Tekanan Bulk 1"))
presentvalue19b.grid (row = 1, column = 0)
presentvalue19a = Button (frameahu19, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "center",
                        command = lambda : setval("Bulk 1", "Suhu Bulk 1"))
presentvalue19a.grid (row = 2, column = 0)

# sch19 = Button (frameahu19, width = 10, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch19.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################

########################################################################################################################
############################## FRAME SIMPAN TELOR###############################################################################
########################################################################################################################
frameahu20 = Frame (bgcoldstor, width = 15, height = 4, borderwidth = 0, relief = RAISED, bg = "black")
frameahu20.place (x = 634, y = 561)
##GRAPH and room name
roomlabel20 = Button (frameahu20, width = 8, height = 2, text = "Simpan Telur 1" ,
                     command = lambda : calendarpickstartend("Simpan Telur 1", "Suhu Simpan Telur 1","Tekanan Simpan Telur 1"), font= (None, 6), anchor = "center", bg = "black", fg="white")
roomlabel20.grid (row = 0, column = 0, rowspan = 2)
##PRESENT VALUE
presentvalue20b = Button (frameahu20, width = 8,height = 1, text = "", fg = "black", font = (None, 6), anchor = "center",
                         command = lambda : setval("Simpan Telur 1", "Tekanan Simpan Telur 1"))
presentvalue20b.grid (row = 0, column = 1)
presentvalue20a = Button (frameahu20, width = 8,height = 1,  text = "", fg = "black", font = (None, 6), anchor = "center",
                        command = lambda : setval("Simpan Telur 1", "Suhu Simpan Telur 1"))
presentvalue20a.grid (row = 1, column = 1)

# sch1 = Button (frameahu20, width = 10, height = 1, text = "Sch" ,
#                command = lambda : frameschedule(1), font= (None, 6), anchor = "center", bg = "black", fg="white")
# sch1.grid (row = 3, column = 0)
########################################################################################################################
########################################################################################################################


while True :
    global valuextemp1
    try:
        with open('realtimedata.csv', 'r') as carivaluextemp1:
            nomortemp1 = []
            for row in csv.reader(carivaluextemp1, delimiter=','):
                nomortemp1.append(int(row[0]))
        carivaluextemp1.close()
        valuextemp1 = len(nomortemp1) - 1
        read()
        # checkingsch()
        nomortemp1 = None
    except Exception as exc:
        print(exc)

    # root.update_idletasks()
    root.update()

# read_every_second ()
# root.mainloop ()