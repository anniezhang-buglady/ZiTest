import datetime

import pywintypes
from win32com.client import DispatchEx

from win32com.client import makepy

# from extract import Extract

makepy.GenerateFromTypeLibSpec('Lotus Domino Objects')


makepy.GenerateFromTypeLibSpec('Lotus Notes Automation Classes')

class NotesMail(object):
    """
     发送读取邮件有关的操作
    """

    def __init__(self, server, file):
        print('init mail client')
        # self.session = DispatchEx('Notes.NotesSession')
        # # self.server = self.session.GetEnvironmentString("MailServer", True)
        # self.db = self.session.GetDatabase(server, file)
        # if not self.db.IsOpen:
        #     print('open mail db')
        #     try:
        #         self.db.OPENMAIL
        #     except Exception as e:
        #         print(str(e))
        #         print( 'could not open database: {}'.format('\mail\张丽华') )

        # for notes 8.5 maybe
        self.session = DispatchEx('Notes.NotesSession')
        self.server = self.session.GetEnvironmentString("MailServer", True)
        self.db = self.session.GetDatebase(server, file)
        self.db.OPENMAIL
        print("11111111111111111111")
        print("2222222222222222")
        print(server)
        print(file)
        if not self.db.IsOpen:
            print("3333333333333333333333")
            try:
                self.db.Open()
            except pywintypes.com_error:
                print('could not open database: ')

    def send_mail(self, reciver_list, subject, body=None):
        doc = self.db.CREATEDOCUMENT
        doc.sendto = reciver_list
        doc.Subject = subject
        if body:
            doc.Body = body
        doc.SEND(0, reciver_list)
        print('send success')


def main():
    # recivers = ['User1/szABCtech', 'User2/szABCtech']
    recivers = ['zhangxue/kedacom']
    mail = NotesMail('kedacomtest2@kedacom', 'mail\张丽华.nsf')
    mail.send_mail(recivers, 'test sender', 'This is a test mail body ')


if __name__ == '__main__':
    main()
