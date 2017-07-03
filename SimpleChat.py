import socket
from tkinter import Tk,Entry,END,StringVar,Text

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind(('0.0.0.0', 11719))

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

root = Tk()
text = StringVar()
name = StringVar()

name.set('User')
text.set('')
root.title('SimpleChat')
root.geometry('400x300')

log = Text(root)
msg = Entry(root, textvariable=text)
nick = Entry(root, textvariable=name)

msg.pack(side='bottom', fill='x', expand='true')
nick.pack(side='bottom', fill='x', expand='true')
log.pack(side='top', fill='both', expand='true')


def loopproc():
    log.see(END)
    s.setblocking(False)
    try:
        message = s.recv(128)
        log.insert(END, message.decode() + '\n')
    except:
        root.after(1, loopproc)
        return
    root.after(1, loopproc)
    return


def sendproc(event):
    send_msg = '%s:%s' % (name.get(), text.get())
    sock.sendto(send_msg.encode(), ('255.255.255.255', 11719))
    text.set('')

msg.bind('<Return>', sendproc)
msg.focus_get()
root.after(1, loopproc)
root.mainloop()
