"""
Учебный чат для ознакомления работы с сокетами, написанный после прочтения
статьи на Хабре
"""
import socket
from time import strftime, localtime
from tkinter import Tk, Entry, END, StringVar, Text, Frame, Label


# TODO Оформить все как классы. Доработать интефейс. Ввести настройку IP.
# TODO Возможно стоит подумать над созданием единого сервера и добавлением комнат.
# TODO Нужно снизить нагрузку на процессор.

# прием по всем каналам
host = '0.0.0.0'
# свободный порт и простое число
port = 11917

sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock_recv.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock_recv.bind((host, port))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

root = Tk()
root.title('SimpleChat')
root.geometry('400x300')

text = StringVar()
name = StringVar()
name.set('Fox')
text.set('')


log = Text(root)
log.tag_config('time', foreground='green')
log.tag_config('nick', foreground='red')
frame1 = Frame(root)

msg = Entry(root, textvariable=text)
nick = Entry(frame1, textvariable=name)

msg.pack(side='bottom', fill='x', expand='true')
frame1.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both', expand='true')
Label(frame1, text='Your nick: ').pack(side='left')
nick.pack(side='left', fill='x', expand='true')


def init_application():
    None


def print_msg(message, root=log):

    root.insert(END, strftime("%H:%M ", localtime()), 'time')
    nick_end = message.find(':')
    root.insert(END, message[:nick_end] + ':\n', 'nick')
    root.insert(END, message[nick_end+1:] + '\n')


def loopproc():
    log.see(END)
    sock_recv.setblocking(False)
    try:
        message = sock_recv.recv(128).decode()
        print_msg(message)
    except:
        root.after(1, loopproc)
        return
    root.after(1, loopproc)
    return


def sendproc(event):
    send_msg = '%s:%s' % (name.get(), text.get())
    text.set('')
    # broadcast # TODO для корректной работы нужен сервер
    sock.sendto(send_msg.encode('utf-8'), ('255.255.255.255', port))

msg.bind('<Return>', sendproc)
msg.focus_get()
root.after(1, loopproc())
root.mainloop()
