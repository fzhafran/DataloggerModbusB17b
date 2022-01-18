from telegram.ext import Updater
import telegram
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, utils
import csv
from datetime import date, timedelta
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

updater = Updater (token = "806075178:AAHnqo_zetbOKhtelc0XkmwAP6-B7_y7rgE", use_context = True)
dispatcher = updater.dispatcher

AHU_or_CSAG, change_preparation, pick_ahu, change_value, namaruang = range(5)
temperature_or_pressure = 0
number_ahu = 0
address = 0
temperature1 = 0
temperature2 = 0

devicetype = 0
def build_menu(buttons,
               n_cols,
               header_buttons,
               footer_buttons):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons == 1:
        menu.insert(0, [header_buttons])
    if footer_buttons == 1:
        menu.append([footer_buttons])
    return menu

def start (update, context) :
    button_list = [
        [telegram.KeyboardButton('/start')],
        [telegram.KeyboardButton('/Cek_status_all')],
        [telegram.KeyboardButton('/Change')],
        [telegram.KeyboardButton('/Trend')],
        [telegram.KeyboardButton('/checkme')]
    ]
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    context.bot.send_message(chat_id = update.effective_chat.id, text="hello", reply_markup = reply_markup)

chatid= []
def stopnotifyme(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "ok, we won't notify you")
    #chatid.append(update.effective_chat.id)
    context.job_queue.stop()

def notifyme(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "we will notify you")
    #chatid.append(update.effective_chat.id)
    context.job_queue.start()
    context.job_queue.run_repeating (checknotif, 1, context = update.effective_chat.id )

def checknotif(context):
    with open('alertlog.csv', 'r') as alert:
        for row in csv.reader(alert, delimiter=','):
            context.bot.send_message(chat_id=context.job.context, text = str(row[1]))

def checkme (update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="hi, your chat id = {}".format(update.effective_chat.id))

def echo (update, context) :
    global temperature1, temperature2
    nomor = []
    listing = []
    listingbaru = []
    listingcond = []
    with open('logging.csv', 'r') as csvfile:
        next(csvfile)
        for row in csv.reader(csvfile, delimiter=','):
            nomor.append(int(row[0]))
        nomorsekarang = len(nomor)
        print(nomorsekarang)

    with open('logging.csv', 'r') as csvfile:
        next(csvfile)
        for x, line in enumerate(csv.reader(csvfile)):
            if x == nomorsekarang - 1:
                for y in line:
                    listing.append(y)
    print(nomorsekarang)
    print(listing)
    with open ('devicelist.csv','r') as namaparam :
        next(namaparam)
        param = []
        for row in csv.reader(namaparam, delimiter = ','):
            param.append(str(row[0]))
    for pos in range (3, 82, 2) :
        listingcond.append(listing[pos])
    for pos in range (2, 82, 2):
        listingbaru.append(listing[pos])

    print(param)
    print(listingcond)
    print(listingbaru)

    allcond = []
    for xxx in range (0, len(param), 1):
        allcond.append (str(param[xxx] + ": " + str(listingcond[xxx] +": " +str(listingbaru[xxx]) )))

    print(allcond)
    for things in allcond :
        context.bot.send_message(chat_id=update.effective_chat.id, text= things)

    isiteks = update.message.text
    nomor = listing = listingbaru = listingcond = None

def changedevicevalue (alamat, jumlah) :
    with open ('request.csv', 'a') as logging :
        logging.write(str(alamat)+','+str(jumlah)+ ','+'\n')

def picktrend (update, context) :
    global barisyangdipilih
    with open('devicelist.csv', 'r') as limitlist:
        next(limitlist)
        listparam = []
        for row in csv.reader(limitlist, delimiter=','):
            listparam.append(str(row[0]))

    button_listtrend = []
    for ahutrend in listparam:
        button_listtrend.append([telegram.KeyboardButton(ahutrend)])

    reply_markup = telegram.ReplyKeyboardMarkup(button_listtrend)
    update.message.reply_text ('pick room', reply_markup = reply_markup)
    button_listtrend = None
    return namaruang


def printtrend (update, context) :
    date2 = []
    with open ('devicelist.csv','r') as limitlist :
        next(limitlist)
        listparam = []
        idbaris = []
        for row in csv.reader(limitlist, delimiter = ','):
            listparam.append(str(row[0]))
            idbaris.append(str(row[5]))
    roomchoosen = update.message.text
    baris = listparam.index(str(roomchoosen))

    with open ('logging.csv', 'r') as csvfiledev1 :
        next(csvfiledev1)
        x = []
        tanggal = []
        tanggaljam =[]
        y = []
        # z = []
        for row in csv.reader (csvfiledev1, delimiter = ',') :
            dateonly = row[1].split()
            dateonly = dateonly[:-1]
            dateonly = ' '.join([str(elem) for elem in dateonly])
            x.append (float(row[0]))
            tanggal.append (dateonly)
            tanggaljam.append(row[1])
            y.append (float(row[int(idbaris[baris])]))
            # z.append (float(row[4]))

    last3days = date.today() - timedelta(days= 2)
    print(last3days)
    # try :
    first = tanggal.index(str(last3days))
    last = len(x) - 1
    print(first,last)
    datestep = []
    stepy = []
    # stepz = []
    for data in range(first, last, 1) :
        datestep.append(tanggaljam[data])
        stepy.append(y[data])
        # stepz.append(z[data])

    # figgraphtemp = plt.figure()
    # figgraphtemp, (x1,x2) = plt.subplots(2,1,sharex=True, figsize=(20,10))
    # x1.plot(datestep, stepy)
    # x1.set_title('temperature ' + str(roomchoosen))
    # x2.plot(datestep,stepz)
    # x2.set_title('pressure ' + str(roomchoosen))
    plt.plot (datestep, stepy)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig('trend.png')

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open("trend.png","rb"))
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=figgraphpres)
    # except :
    #     context.bot.send_message(chat_id=update.effective_chat.id,
    #                              text="date not in list")

    stepz = stepy = datestep = last = first = last3days = x = tanggal = y = tanggaljam = listparam = idbaris =  None
    return ConversationHandler.END

def change1 (update, context) :
    with open ('devicelist.csv','r') as limitlist :
        next(limitlist)
        listparam = []
        for row in csv.reader(limitlist, delimiter = ','):
            listparam.append(str(row[0]))
    button_list=[]
    for ahu in listparam :
        button_list.append([telegram.KeyboardButton(ahu)])
    reply_markup = telegram.ReplyKeyboardMarkup(button_list)
    update.message.reply_text ('??', reply_markup = reply_markup)
    button_list = listparam = None
    return pick_ahu

def ahu_picker (update, context) :
    global number_ahu
    number_ahu = update.message.text
    update.message.reply_text ('what is your desired value ?')
    return change_value
            
def value (update, context) :
    global address, devicetype
    with open ('devicelist.csv','r') as limitlist :
        next(limitlist)
        listahu = []
        address = []
        for row in csv.reader(limitlist, delimiter = ','):
            listahu.append(str(row[0]))
            address.append(int(row[1]))
        
    value = update.message.text
    place = listahu.index(str(number_ahu))
    context.bot.send_message (chat_id = update.effective_chat.id, text = "setting {} with address {} to {} . . . . .".format (str(number_ahu), str(address[place]), str(value)))
    changedevicevalue (address[place], value)
    print(address[place])
    print(value, change_value)
    context.bot.send_message (chat_id = update.effective_chat.id, text = "request sent")
    listahu = address = None
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text('Bye!',reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

start_handler = CommandHandler ('Start', start)  ## <-- add more func for pass job queue to use alarm.
# notifyme_handler = CommandHandler ('notifyme', notifyme, pass_job_queue=True)
# stopnotifyme_handler = CommandHandler ('stop_notifyme', stopnotifyme, pass_job_queue=True)
cek_handler = CommandHandler ('Cek_status_all', echo)
checkme_handler = CommandHandler('checkme', checkme)
change_handler = ConversationHandler (
    entry_points = [CommandHandler ('Change', change1)],
    states = {
        pick_ahu : [MessageHandler(Filters.text, ahu_picker)],
        change_value : [MessageHandler(Filters.text, value)]
    },
    fallbacks = [CommandHandler('Cancel', cancel)])
trend_handler = ConversationHandler (
    entry_points = [CommandHandler ('Trend', picktrend)],
    states = {
        namaruang : [MessageHandler(Filters.text, printtrend)]
    },
    fallbacks = [CommandHandler('cancel', cancel)])

dispatcher.add_handler (start_handler)
# dispatcher.add_handler (notifyme_handler)
# dispatcher.add_handler (stopnotifyme_handler)
dispatcher.add_handler (cek_handler)
dispatcher.add_handler (checkme_handler)
dispatcher.add_handler (change_handler)
dispatcher.add_handler (trend_handler)
updater.start_polling()
updater.idle()