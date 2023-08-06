import datetime
from imap_tools import MailBox, AND
from mailthon import postman, email
from threading import Thread

smtp = 'smtp.gmail.com'
imap = 'imap.gmail.com'
username = 'pychat01@gmail.com'
password = 'pychat01@pychat01'
alias = input('Welcome to Pychat. Enter your alias: ')

last_fetched_date = datetime.datetime.fromisoformat('2000-01-01 00:00:00-08:00')


def send(msg):
    p = postman(host=smtp, auth=(username, password))
    r = p.send(email(
        content=u'',
        subject=msg,
        sender=f'{alias} <{username}>',
        receivers=[username],
    ))
    return r.ok


def receive():
    global last_fetched_date
    with MailBox(imap).login(username, password) as mailbox:
        msgs = [msg for msg in mailbox.fetch(headers_only=True, bulk=True)]
        for s in msgs:
            if last_fetched_date < s.date:
                yield f"{s.date} {s.from_values.name}: {s.subject}"
                last_fetched_date = s.date


def loop_receive_to_terminal():
    while True:
        for msg in receive():
            print(msg)


def main(argv=None):
    send(f" I've entered room.")

    t = Thread(target=loop_receive_to_terminal)
    t.start()

    while True:
        msg = input("")
        send(msg)



if __name__ == "__main__":
    main()