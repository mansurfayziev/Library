import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3 as sq3
from PyQt5.QtWidgets import QMessageBox




with sq3.connect('DBLibrary.db') as con:
    cur=con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        leasing_books TEXT DEFAULT "w",
        balanc LOGINT DEFAULT 0
    ) """)
    cur.execute("""CREATE TABLE IF NOT EXISTS books(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        class INTEGER DEFAULT 0,
        amount LOGINT NOT NULL,
        leased LOGINT DEFAULT 0
    )""")
    con.commit()
    
    def id_to_balanc(id_client):
        try:
            d=list(cur.execute(f"SELECT balanc FROM clients WHERE id={id_client}").fetchone())
            return d[0]
        except Exception as e:
            cv=QMessageBox()
            cv.setWindowTitle("Хатоги хангоми гирифтани Баланси Мизоч аз Анбор")
            cv.setText(str(e))
            cv.setIcon(QMessageBox.Warning)
            cv.exec_()
            return 'Дар АНБОР нест.'

    def id_to_str(id_book):
        try:
            ff=list(cur.execute(f"SELECT name FROM books WHERE id={id_book}").fetchone())
            return ff
        except Exception as e:
            cv=QMessageBox()
            cv.setWindowTitle("Хатоги хангоми гирифтани китоб аз Анбор")
            cv.setText(str(e))
            cv.setIcon(QMessageBox.Warning)
            # cv.exec_()
            return "Дар АНБОР нест."

    def get_books_ofClinet(id_Client):
        clt=[s for s in cur.execute(f"SELECT * FROM clients WHERE id={int(id_Client)}").fetchone()]
        return clt


    def new_book(nom,sinf,miqdor):
        if nom.strip()=='' or miqdor.strip()=='' or (sinf.strip()!='' and sinf.isalpha()) or (miqdor.strip()!='' and miqdor.isalpha()):
            err=QMessageBox()
            err.setWindowTitle("Хатоги дар пур кардани майдонхо")
            err.setText("  Лутфан майдонхоро дуруст пур кунед!")
            err.setIcon(QMessageBox.Warning)
            err.setStandardButtons(QMessageBox.Ok )
            err.setDetailedText(f"*Номи китоб: {nom}, бояд сатр бошад (Хатмист) \n Синф: {sinf}, бояд ракам бошад!\n *Микдор: {miqdor}, бояд ракам бошад (Хатмист)\n\n Дар кадоме аз инхо шумо хато кардаед!")
            err.exec_()
        else:
            if sinf.strip()=='':
                sinf=0
            try:
                rrr=list(cur.execute(f"SELECT name,class FROM books WHERE name='{nom}' AND class={sinf}").fetchone())
            except:
                rrr=['nest']

            if rrr[0]=='nest':
                cur.execute(f"INSERT INTO books(name,class,amount,leased) VALUES (?,?,?,0)",(nom,sinf,miqdor))
                con.commit()
            else:
                cur.execute(f"UPDATE books SET amount=amount+{miqdor} WHERE name='{nom}' AND class={sinf}")
                con.commit()


    def click_cv(i):
        if i.text()=='Ok':
            try:
                cur.execute(f"DELETE FROM books WHERE id={id}")
                con.commit()
                cv=QMessageBox()
                cv.setWindowTitle("Нест карда шуд.")
                cv.setText(f"Бо муввафакият аз Анбор нест карда шуд")
                cv.setIcon(QMessageBox.Information)
                cv.exec_()
            except sq3.Error as err:
                cv=QMessageBox()
                cv.setWindowTitle("Хатоги хангоми нест кардани китоб")
                cv.setText("Хатоги хангоми нест кардани китоб аз Анбор \n "+str(err))
                cv.setStandardButtons(QMessageBox.Ok )
                cv.setIcon(QMessageBox.Warning)
                cv.exec_()


    def remove_book(id):
        try:
            # count=list(cur.execute(f"SELECT leased FROM books WHERE id={id}").fetchone())[0]
            # if count>0:
            #     cv=QMessageBox()
            #     cv.setWindowTitle("Огохи")
            #     cv.setText(f"Китобе ки Шумо нест карда истодаед,\n айни хол {count}-то китоб дар ичора карор дорад.")
            #     cv.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            #     cv.setIcon(QMessageBox.Information)
            #     cv.buttonClicked.connect(click_cv)
            #     cv.exec_()
                cur.execute(f"DELETE FROM books WHERE id={id}")
                con.commit()

        except Exception as err:
            cv=QMessageBox()
            cv.setWindowTitle("Хатоги хангоми нест кардан китоб")
            cv.setText(err)
            cv.setIcon(QMessageBox.Warning)
            cv.exec_()

    def reverse_listBookDB():
        df=cur.execute("SELECT * FROM books WHERE id>0")
        df=cur.execute("SELECT * FROM books WHERE id>0")

        ff=[]
        for k in df:
            for x in k:
                ff.append(len(str(x)))
                

        dfd=cur.execute("SELECT * FROM books WHERE id>0")
        listDB=[]
        for v in dfd:
            r=''
            # 
            for q in v:
                de=' '*((max(ff)+3)-len(str(q)))
                r+=str(q)+de
            listDB.append(r)

        return listDB

    def list_Clients():
        df=cur.execute("SELECT * FROM clients")
        j=[]

        for x in df:
            k=''
            for i in x:
                try:
                        
                    if i[0]=='w':
                        i=str(i)
                        i=i.replace('w','')
                        i=i.replace('m','<--')
                        i=i.replace('id',' | ')
                        i=i[:100]
                except:
                    pass
                k+=str(i)+'    |||     '
            j.append(k)
        return j

    def list_Clients_getLease():
        df=cur.execute("SELECT name FROM clients")
        j=[]

        for x in df:
            k=''
            for i in x:
                try:
                        
                    if i[0]=='w':
                        i=str(i)
                        i=i.replace('w','')
                        i=i.replace('m','<--')
                        i=i.replace('id',' | ')
                        i=i[:100]
                except:
                    pass
                k+=str(i)
            j.append(k)
        return j
    
    # def list_books_getLease():
    #     d=cur.execute("SELECT name FROM books WHERE ")

    def remove_Client(id):
        try:
            cur.execute(f"DELETE FROM clients WHERE id={id}")
            con.commit()
        except sq3.Error as er:
            err=QMessageBox()
            err.setText(str(er))
            err.setIcon(QMessageBox.Warning)
            err.setWindowTitle("Хатоги хангоми нест кардан аз руйхат ")
            err.exec_()

    def new_client(name):  
        if cur.execute(f"SELECT * FROM clients WHERE name='{name}'").fetchone():
            cv=QMessageBox()
            cv.setWindowTitle("Чунин Мизоч вучуд дорад!")
            cv.setText("Бо чунин ном мизоч алакай хаст!!!")
            cv.setIcon(QMessageBox.Warning)
            cv.exec_()
            return False
        else:
            try:
                cur.execute(f"INSERT INTO clients(name) VALUES('{name}')")
                con.commit()
                cv=QMessageBox()
                cv.setWindowTitle(f"{name} сабт шуд!")
                cv.setText(f"{name} дар руйхат кайд карда шуд!")
                cv.setIcon(QMessageBox.Information)
                cv.exec_()
                return True
            except sq3.Error as er:
                cv=QMessageBox()
                cv.setWindowTitle("Хатоги хангоми сабти Мизоч!")
                cv.setText(er)
                cv.setIcon(QMessageBox.Warning)
                cv.exec_()
                return False

    def getBook_setCilent(id_book,id_client,amount_of_book,balanc):
        mi=list(cur.execute(f"SELECT amount FROM books WHERE id={id_book}").fetchone())
        if int(mi[0])< int(amount_of_book):
            cv=QMessageBox()
            cv.setWindowTitle("Микдори китоб кам!")
            cv.setText("Микдори китоби интихобшуда аз микдори Шумо ворид карда кам аст. ")
            cv.setIcon(QMessageBox.Warning)
            cv.exec_()
            return False
        else:
            try:
                ff_last=list(cur.execute(f"SELECT leasing_books FROM clients WHERE id={int(id_client)}").fetchone())
                
                ff=str(ff_last[0])+"id"+str(int(id_book))+"m"+str(amount_of_book)   
                
                bal=int((int(amount_of_book)*float(balanc)))
                cur.execute(f"UPDATE books SET amount=amount-{int(amount_of_book)} WHERE id={int(id_book)}")
                cur.execute(f"UPDATE clients SET balanc=balanc-{int(bal)} WHERE id={int(id_client)}")
                cur.execute(f"UPDATE books SET leased=leased+{int(amount_of_book)} WHERE id={int(id_book)}")
                cur.execute(f"UPDATE clients SET leasing_books='{str(ff)}' WHERE id={int(id_client)}")
                con.commit()
                cv=QMessageBox()
                cv.setWindowTitle("Ба ичора додан бо хуби анчом дод")
                cv.setText(f"{amount_of_book}-то китоб ба ичора дода шуд!")
                cv.setIcon(QMessageBox.Information)
                cv.exec_()
                return True
            except sq3.Error as er:
                cv=QMessageBox()
                cv.setWindowTitle("Хатоги хангоми додани китоб ба ичора")
                cv.setText(str(er))
                cv.setIcon(QMessageBox.Warning)
                cv.exec_()
                return False
       

class Ui_GiriftaniKitob(object):
    def setupUi(self, GiriftaniKitob):
        GiriftaniKitob.setObjectName("GiriftaniKitob")
        GiriftaniKitob.resize(500, 445)
        GiriftaniKitob.setStyleSheet("background-color: white;")
        self.listWidget = QtWidgets.QListWidget(GiriftaniKitob)
        self.listWidget.setGeometry(QtCore.QRect(20, 40, 221, 281))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(GiriftaniKitob)
        self.listWidget_2.setGeometry(QtCore.QRect(250, 40, 231, 281))
        self.listWidget_2.setObjectName("listWidget_2")
        self.pushButton = QtWidgets.QPushButton(GiriftaniKitob)
        self.pushButton.setGeometry(QtCore.QRect(70, 390, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(28, 186, 0);")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(GiriftaniKitob)
        self.label.setGeometry(QtCore.QRect(20, 4, 461, 31))
        self.label.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.pushButton_2 = QtWidgets.QPushButton(GiriftaniKitob)
        self.pushButton_2.setGeometry(QtCore.QRect(280, 390, 201, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("border:1px solid black;")
        self.pushButton_2.setObjectName("pushButton_2")
        self.spinBox = QtWidgets.QSpinBox(GiriftaniKitob)
        self.spinBox.setGeometry(QtCore.QRect(267, 340, 91, 22))
        self.spinBox.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.spinBox.setMaximum(10000)
        self.spinBox.setObjectName("spinBox")
        self.label_2 = QtWidgets.QLabel(GiriftaniKitob)
        self.label_2.setGeometry(QtCore.QRect(20, 335, 245, 31))
        self.label_2.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.label_2.setObjectName("label_2")
        self.retranslateUi(GiriftaniKitob)
        QtCore.QMetaObject.connectSlotsByName(GiriftaniKitob)

        self.func()

    def retranslateUi(self, GiriftaniKitob):
        _translate = QtCore.QCoreApplication.translate
        GiriftaniKitob.setWindowTitle(_translate("GiriftaniKitob", "Аз иҷора гирифтан"))
        self.pushButton.setText(_translate("GiriftaniKitob", "Иҷро кардан"))
        self.label.setText(_translate("GiriftaniKitob", "Рӯйхати Мизоҷон              Руйхати китобҳои мизоҷ"))
        self.pushButton_2.setText(_translate("GiriftaniKitob", "Баргаштан"))
        self.label_2.setText(_translate("GiriftaniKitob", "Миқдори гирифташаванда:"))

    def func(self):
        print(list_Clients_getLease())


# Dialog Set Lease
class Ui_setLeaseWindow(object):
    def setupUi(self, setLeaseWindow):
        setLeaseWindow.setObjectName("setLeaseWindow")
        setLeaseWindow.resize(604, 337)
        font = QtGui.QFont()
        font.setPointSize(12)
        setLeaseWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(setLeaseWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listBooks = QtWidgets.QListWidget(self.centralwidget)
        self.listBooks.setGeometry(QtCore.QRect(10, 40, 291, 161))
        self.listBooks.setObjectName("listBooks")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(8, 10, 201, 31))
        self.label.setObjectName("label")
        self.listClients = QtWidgets.QListWidget(self.centralwidget)
        self.listClients.setGeometry(QtCore.QRect(300, 40, 291, 161))
        self.listClients.setObjectName("listClients")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(306, 10, 231, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 220, 181, 21))
        self.label_3.setObjectName("label_3")
        self.text_amount_of_book = QtWidgets.QSpinBox(self.centralwidget)
        self.text_amount_of_book.setGeometry(QtCore.QRect(174, 219, 61, 24))
        self.text_amount_of_book.setObjectName("text_amount_of_book")
        self.btn_setBook = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setBook.setGeometry(QtCore.QRect(250, 290, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.btn_setBook.setFont(font)
        self.btn_setBook.setStyleSheet("background-color: rgb(46, 199, 0);\n"
"color: rgb(255, 238, 250);")
        self.btn_setBook.setObjectName("btn_setBook")
        self.btn_Cancle = QtWidgets.QPushButton(self.centralwidget)
        self.btn_Cancle.setGeometry(QtCore.QRect(467, 290, 125, 41))
        self.btn_Cancle.setStyleSheet("background-color: rgb(255, 59, 0);")
        self.btn_Cancle.setObjectName("btn_Cancle")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 220, 271, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(443, 218, 51, 24))
        self.lineEdit.setText("0")
        self.lineEdit.setObjectName("lineEdit")
        setLeaseWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(setLeaseWindow)
        QtCore.QMetaObject.connectSlotsByName(setLeaseWindow)

        self.func()

    def retranslateUi(self, setLeaseWindow):
        _translate = QtCore.QCoreApplication.translate
        setLeaseWindow.setWindowTitle(_translate("setLeaseWindow", "Ба ичора додани китоб"))
        self.label.setText(_translate("setLeaseWindow", "Китобро интихоб намоед:"))
        self.label_2.setText(_translate("setLeaseWindow", "Муштариро интихоб намоед:"))
        self.label_3.setText(_translate("setLeaseWindow", "Микдори додашаванда:"))
        self.btn_setBook.setText(_translate("setLeaseWindow", "Ичро кардан"))
        self.btn_Cancle.setText(_translate("setLeaseWindow", "Бекор кардан"))
        self.label_4.setText(_translate("setLeaseWindow", "Маблаги 1 китоб:            сомон."))



    def func(self):
        self.listBooks.addItems(reverse_listBookDB())
        self.listClients.addItems(list_Clients())
        self.btn_setBook.clicked.connect(self.setBook)

    def setBook(self):
        try:
            id_b=self.listBooks.currentIndex().data()[:4]
            id_c=self.listClients.currentIndex().data()[:4]
            miq=self.text_amount_of_book.text()
            money=self.lineEdit.text()  
        except:
            confirm=QMessageBox()
            confirm.setWindowTitle("Интихоб нашудааст.")
            confirm.setIcon(QMessageBox.Warning)
            confirm.setText("Лутфан китобро ва баъдан мизочро интихоб кунед!")
            confirm.exec_()

        if miq=='0' or money.isalpha():
                cfm=QMessageBox()
                cfm.setWindowTitle("Микдор ё Нарх нодуруст ворид шудааст.")
                cfm.setIcon(QMessageBox.Warning)
                cfm.setText("Лутфан микдор ва нархро дуруст ворид кунед!")
                cfm.exec_()
        else:
                if getBook_setCilent(id_b,id_c,miq,money):
                    self.close()
                    self.twoWindow = TwoWindow()
                    self.twoWindow.show()

        

# Dialog add Client

class Ui_dialog_addClient(object): 
    def setupUi(self, dialog_addClient):
        dialog_addClient.setObjectName("dialog_addClient")
        dialog_addClient.resize(535, 144)
        self.centralwidget = QtWidgets.QWidget(dialog_addClient)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(150, 30, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(150, 80, 180, 41))
        self.pushButton.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";\n"
"background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));\n"
"background-color: rgb(0, 255, 42);")
        self.btn_Cancel= QtWidgets.QPushButton(self.centralwidget)
        self.btn_Cancel.setGeometry(335, 80, 120,41)
        self.btn_Cancel.setStyleSheet("font-size: 16px; border: 1px solid ;")
        self.btn_Cancel.setText("Баргаштан")
        
        dialog_addClient.setCentralWidget(self.centralwidget)
        
        self.func()

        self.retranslateUi(dialog_addClient)
        QtCore.QMetaObject.connectSlotsByName(dialog_addClient)

    def retranslateUi(self, dialog_addClient):
        _translate = QtCore.QCoreApplication.translate
        dialog_addClient.setWindowTitle(_translate("dialog_addClient", "Илова кардани Мизоҷ"))
        self.label.setText(_translate("dialog_addClient", "Номи Мизоҷ"))
        self.pushButton.setText(_translate("dialog_addClient", "Илова кардан"))

    def func(self):
        self.pushButton.clicked.connect(self.addClient)

    def addClient(self):
        try:
            if new_client(self.lineEdit.text()):
                self.close()
                self.twoWindow = TwoWindow()
                self.twoWindow.show()

        except ValueError as er:
            confirm=QMessageBox()
            confirm.setWindowTitle("Хато хангоми илова кардани Мизоч")
            confirm.setIcon(QMessageBox.Warning)
            confirm.setText(er)
            confirm.exec_()


#  Clients
class Ui_Cilent(object):
    def setupUi(self, CilentWindow):
        CilentWindow.setObjectName("CilentWindow")
        CilentWindow.resize(584, 500)
        font = QtGui.QFont()
        font.setPointSize(12)
        CilentWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(CilentWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.list_Cilents = QtWidgets.QListWidget(self.centralwidget)
        self.list_Cilents.setGeometry(QtCore.QRect(0, 0, 341, 501))
        self.list_Cilents.setObjectName("list_Cilents")
        self.btn_addClient = QtWidgets.QPushButton(self.centralwidget)
        self.btn_addClient.setGeometry(QtCore.QRect(360, 10, 201, 31))
        self.btn_addClient.setStyleSheet("background-color: rgb(12, 255, 0);")
        self.btn_addClient.setObjectName("btn_addClient")
        self.btn_deleteClient = QtWidgets.QPushButton(self.centralwidget)
        self.btn_deleteClient.setGeometry(QtCore.QRect(360, 41, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btn_deleteClient.setFont(font)
        self.btn_deleteClient.setStyleSheet("border-color: rgb(255, 80, 185);\n"
"color: rgb(0, 0, 0);\n"    
"background-color: rgb(255, 0, 4);")
        self.btn_deleteClient.setObjectName("btn_deleteClient")
        self.btn_setLease = QtWidgets.QPushButton(self.centralwidget)
        self.btn_setLease.setGeometry(QtCore.QRect(360, 90, 201, 31))
        self.btn_setLease.setStyleSheet("background-color: rgb(255, 255, 110);")
        self.btn_setLease.setObjectName("btn_setLease")
        self.btn_getLease = QtWidgets.QPushButton(self.centralwidget)
        self.btn_getLease.setGeometry(QtCore.QRect(360, 120, 201, 31))
        self.btn_getLease.setStyleSheet("background-color: rgb(223, 171, 255);")
        self.btn_getLease.setObjectName("btn_getLease")
        self.list_booksClient = QtWidgets.QListWidget(self.centralwidget)
        self.list_booksClient.setGeometry(QtCore.QRect(340, 211, 241, 291))
        self.list_booksClient.setObjectName("list_booksClient")
        self.btn_link_to_Sclad=QtWidgets.QPushButton(self)
        self.btn_link_to_Sclad.setGeometry(360,150,201,31)
        self.btn_link_to_Sclad.setText("Анбори китобхо")
        self.btn_link_to_Sclad.show()

        CilentWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CilentWindow)
        QtCore.QMetaObject.connectSlotsByName(CilentWindow)

        self.new_funtion()

    def retranslateUi(self, CilentWindow):
        _translate = QtCore.QCoreApplication.translate
        CilentWindow.setWindowTitle(_translate("CilentWindow", "Руйхати мизочон - Мудири Китобхона v1.0"))
        self.btn_addClient.setText(_translate("CilentWindow", "Илова кардани  Мизоч"))
        self.btn_deleteClient.setText(_translate("CilentWindow", "Нест кардани Мизоч"))
        self.btn_setLease.setText(_translate("CilentWindow", "Ба ичора додан"))
        self.btn_getLease.setText(_translate("CilentWindow", "Аз ичора гирифтан"))
    
    def new_funtion(self):
        self.list_Cilents.clicked.connect(self.click_listClients)
        self.revres_listClients()
        self.btn_deleteClient.clicked.connect(self.rmd_Clt)

    def click_listClients(self):
        id_c=self.list_Cilents.currentIndex().data().split()[0]
        l=get_books_ofClinet(id_c)[2]
        
        l=l[1:]
             
        l=l.split('id')[1:]
        arr=[]

        for x in l:
            x=x.split('m')
            arr.append(x)
        lk=['Таърхи гир. ктбхои ичорави']
        i=0
        max_book_amount=0
        for x in arr:
            i+=1
            
            max_book_amount+=int(x[1])
            lk.append(f"{i}. {' '.join(id_to_str(x[0]))} ({x[1]})")

        lk.append("----------------------------------")
        lk.append(f"Баланси Мизоч:   {id_to_balanc(id_c)}")
        lk.append(f"Хама китобхо:  {max_book_amount}")
        self.list_booksClient.clear()
        self.list_booksClient.addItems(lk)
        return max_book_amount
     
    def rmd_Clt(self):
        try:
            id=self.list_Cilents.currentIndex().data()[:4]
            remove_Client(int(id))
            self.revres_listClients()
        except TypeError as er:
            err=QMessageBox()
            err.setText(str(er))
            err.setIcon(QMessageBox.Warning)
            err.setWindowTitle("Хатоги хангоми нест кардан аз руйхат ")
            err.exec_()


    def revres_listClients(self):
        self.list_Cilents.clear()
        self.list_Cilents.addItems(list_Clients())

# Sclad
class Ui_Sclad(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(725, 400)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 331, 360))
        self.listWidget.setObjectName("listWidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 30, 121, 31))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(390, 60, 61, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(370, 90, 71, 31))
        self.label_3.setObjectName("label_3")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(470, 30, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("text-align:center;")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(470, 60, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("text-align:center;")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(470, 90, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit_3.setFont(font)
        self.lineEdit_3.setStyleSheet("text-align:center;")
        self.lineEdit_3.setText("")
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(470, 130, 201, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 360, 101, 31))
        self.pushButton_2.setFixedWidth(230)
        self.pushButton_2.setStyleSheet("background: rgb(255, 4, 4);")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(360, 170,340, 40)
        self.pushButton_3.setStyleSheet("background: rgb(10, 255, 10)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText("Руйхати Мизочон")




        

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.reverse_listBookDB()
        self.pushButton.clicked.connect(self.newbook)
        self.pushButton_2.clicked.connect(self.remove_book)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Анбори китобхо - Мудири Китобхона v1.1"))
        self.label.setText(_translate("MainWindow", "Номи китоб:"))
        self.label_2.setText(_translate("MainWindow", "Синф:"))
        self.label_3.setText(_translate("MainWindow", "Микдор:"))
        self.pushButton.setText(_translate("MainWindow", "Илова кардан ба АНБОР"))
        self.pushButton_2.setText(_translate("MainWindow", "Нест кардани интихобшуда"))
   
    def reverse_listBookDB(self):
            self.listWidget.clear()
            df=reverse_listBookDB()
            self.listWidget.addItems(df)

    def newbook(self):
        nom=str(self.lineEdit.text())
        sinf=self.lineEdit_2.text()
        miq=self.lineEdit_3.text()
        new_book(nom,sinf,miq)
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit.setText('')
        reverse_listBookDB()
        self.reverse_listBookDB()
        
    def remove_book(self):
        
        try:
            id=self.listWidget.currentIndex().data()[:4]
            remove_book(id)
            reverse_listBookDB()
            self.reverse_listBookDB()
        except TypeError as er:
            err=QMessageBox()
            err.setText(str(er))
            err.setIcon(QMessageBox.Warning)
            err.setWindowTitle("Хатоги хангоми нест кардан аз руйхат ")
            err.exec_()



class dSSS(QtWidgets.QMainWindow, Ui_GiriftaniKitob):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.check2)
    
    def check2(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()

class dAddCWindow(QtWidgets.QMainWindow, Ui_dialog_addClient):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_Cancel.clicked.connect(self.check2)
    
    def check2(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()

class dAddCWindow(QtWidgets.QMainWindow, Ui_dialog_addClient):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_Cancel.clicked.connect(self.check2)
    
    def check2(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()



class dAddCWindow(QtWidgets.QMainWindow, Ui_dialog_addClient):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_Cancel.clicked.connect(self.check2)
    
    def check2(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()

class dSetLeaseWindow(QtWidgets.QMainWindow, Ui_setLeaseWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_Cancle.clicked.connect(self.check2)
    
    def check2(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()   


class TwoWindow(QtWidgets.QMainWindow, Ui_Cilent):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_link_to_Sclad.clicked.connect(self.check2)
        self.btn_addClient.clicked.connect(self.check3)
        self.btn_setLease.clicked.connect(self.check4)
        self.btn_getLease.clicked.connect(self.check5)
    
    def check2(self):
        self.close()
        self.twoWindow = OneWindow()
        self.twoWindow.show()
    
    def check3(self):
        self.close()
        self.twoWindow = dAddCWindow()
        self.twoWindow.show()
    
    def check4(self):
        self.close()
        self.twoWindow = dSetLeaseWindow()
        self.twoWindow.show()
    
    def check5(self):
        self.close()
        self.twoWindow = dSSS()
        self.twoWindow.show()
        

class OneWindow(QtWidgets.QMainWindow, Ui_Sclad):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.twoWindow = None
        self.pushButton_3.clicked.connect(self.check)

    def check(self):
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()


    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = OneWindow()
    window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()