import time
import serial
import sys
import datetime
import pyttsx3
import mysql.connector
from PyQt5 import QtWidgets, QtGui, QtCore

# DIAGNOSE PART
import speech_recognition as sr
import operator
import re
import _thread
from playsound import playsound





'''
                                                NOTES
                                                ------

    [1]                 --->    I AM ALTERING RESTRICTIONS IN InfoForm, AND IT MUST BE MODIFIED BEFORE DEPLOYMENT
    [2]                 --->    exist_ variable in (EnterID class) most be tested when database is finished
    [3]                 --->    Give A look at (Patient class) and (Visitor class), and see if there is a need to modify them
    [4]                 --->    Moving from FollowMe window will be automatically, not by clicking a button
    [5]                 --->
    [6]                 --->


'''




PLATFORM = ''
SPEAK = False

DATABASE = False



'''
                                    What's New In This Version
                                    --------------------------

    [1]                 --->    DIAGNOSING PART: DID WHAT IBRAHIM WANT
    [2]                 --->
    [3]                 --->
    [4]                 --->
    [5]                 --->
    [6]                 --->
    [7]                 --->
    [8]                 --->


'''


'''
                                        Error Codes
                                        -----------

    [I]                 --->    error in sensors
    [MI]                --->    error in serial communication between Muhammad and Ibrahim
    [skipped]           --->    user could not use sensor
    [T]                 --->    received more than 510 temperature values, and it is supposed to receive only 510 values
    [PE]                --->    error in arduino (software/hardware)

'''


class Patient:
    def __init__(self, name=None, iid=None, address=None, phone=None, birth_date=None, heart=None, sugar=None,
                 temp=None, pressure=None):
        # Personal Info
        self.Name = name
        self.ID = iid
        self.Addr = address
        self.Phone = phone
        self.Birth_Date = birth_date

        # Metrics
        self.Heart_Beats = heart
        self.Sugar = sugar
        self.Temperature = temp
        self.Pressure = pressure

    def print_personal_info(self):
        print('  Name : ', self.Name)
        print('  ID   : ', self.ID)
        print('  Addr : ', self.Addr)
        print('  Mobil: ', self.Phone)
        print('  Birth: ', self.Birth_Date)

    def print_metrics(self):
        print('  Heart: ', self.Heart_Beats)
        print('  Sugar: ', self.Sugar)
        print('  Temp : ', self.Temperature)
        print('  Press: ', self.Pressure)

    def __str__(self):
        print('Patient Info: ')
        self.print_personal_info()
        print('')
        self.print_metrics()
        return ''


class Visitor:
    def __init__(self, name=None, iid=None, address=None, phone=None, birth_date=None):
        # Personal Info
        self.Name = name
        self.ID = iid
        self.Addr = address
        self.Phone = phone
        self.Birth_Date = birth_date

    def __str__(self):
        print('Visitor Info: ')
        print('  Name : ', self.Name)
        print('  ID   : ', self.ID)
        print('  Addr : ', self.Addr)
        print('  Mobil: ', self.Phone)
        print('  Birth: ', self.Birth_Date)
        return ''


# GLOBAL VARIABLES
last_patient = Patient()
last_visitor = Visitor()



class Root:

    def __init__(self):

        # WIDGET
        self.w = QtWidgets.QWidget()
        self.w.setWindowTitle(" ZU Hospital ")
        self.w.setWindowIcon(QtGui.QIcon('Icons/Hospital'))
        self.w.setGeometry(100, 50, 400, 500)
        # self.w.setFixedSize(400, 500)
        # self.w.setStyleSheet("""background-color: #494162""")
        self.w.keyPressEvent = self.esc
        self.w.mouseDoubleClickEvent = self.start_click

        # IMAGE
        image = QtGui.QImage("Icons/img/hos_1.jpg")
        sImage = image.scaled(QtCore.QSize(1365, 777))  # resize Image to widgets size

        # PALETTE
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))  # 10 = Windowrole

        # SET PALETTE TO THE WIDGET
        self.w.setPalette(palette)

        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("Welcome To ZU Hospital")
        lbl.setStyleSheet("color: white; font-size: 44px")  # 22px
        lbl.move(50, 80)  # 580, 250

        # LABEL
        lbl2 = QtWidgets.QLabel(self.w)
        lbl2.setText("Double click to start")
        lbl2.setStyleSheet("color: yellow; font-size: 16px")
        lbl2.move(386, 70)

        # START BUTTON
        btn = QtWidgets.QPushButton(self.w)
        btn.setText("Start")
        btn.setGeometry(550, 500, 300, 80)
        btn.setStyleSheet("""
                                        .QPushButton{
                                                background-color: #BCACEC;
                                                color: white;
                                                font-size: 50px;
                                                border-radius: 40px;

                                        }

                                        .QPushButton:pressed {

                                                background-color: #0CACEC;
                                                border-style: inset;
                                        }

                                        .QPushButton:hover{
                                                background-color: rgb(255, 0, 0);
                                                color: ;
                                                padding-right: 10px;
                                        }

                                  """)
        btn.clicked.connect(self.start_click)
        btn.setVisible(False)

        # SHOW WIDGET AS FULLSCREEN
        self.w.showFullScreen()


    def start_click(self, e):
        self.type2 = Type2()

    def esc(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.w.close()



class Type2:

    def __init__(self):

        # DIALOG
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle("Patient/Visitor")
        self.w.setWindowIcon(QtGui.QIcon('Icons/Two'))
        self.w.setFixedSize(400, 500)
        self.w.setStyleSheet(""".QDialog{background: white; border: 4px solid #0CACEC;}""")  # 494162
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)



        # STYLESHEET FOR PATIENT/VISITOR BUTTONS
        ss = """
                                .QPushButton{
                                        background-color: #0CACEC;
                                        font: 30px;
                                        color: white;
                                        border-radius: 40px;
                                }

                                .QPushButton:hover{
                                        background-color: blue;
                                        color: white;
                                }

                                .QPushButton:pressed {
                                        border-style: inset;
                                        padding-right: 5px;
                                        background-color: blue;
                                }


                     """
        # BCACEC  # 0CACEC


        # HOME BUTTON
        self.home = QtWidgets.QPushButton('×', self.w)
        self.home.setGeometry(370, 5, 20, 20)
        self.home.setStyleSheet(""".QPushButton{background: white; color: ; font: 24px; border: 0px solid;}""")
        self.home.clicked.connect(self.w.close)


        # PATIENT BUTTON
        btn_patient = QtWidgets.QPushButton(self.w)
        btn_patient.setText("Patient")  # Patient
        btn_patient.setGeometry(88 + 5, 120, 220, 80)
        btn_patient.setStyleSheet(ss)
        btn_patient.clearFocus()
        btn_patient.clicked.connect(self.btn_patient_click)

        # VISITOR BUTTON
        btn_visitor = QtWidgets.QPushButton(self.w)
        btn_visitor.setText("Visitor")  # Visitor
        btn_visitor.setGeometry(88 + 5, 260, 220, 80)
        btn_visitor.setStyleSheet(ss)
        btn_visitor.clearFocus()
        btn_visitor.clicked.connect(self.btn_visitor_click)

        # SET FOCUS TO DIALOG
        self.w.setFocus()

        # SHOW DIALOG
        self.w.show()


    def btn_patient_click(self):
        # self.patient_info = InfoForm('Patient Info')

        self.entter_id = EnterID('Patient Info')
        self.w.close()

    def btn_visitor_click(self):
        # self.visitor_info = InfoForm('Visitor Info')

        self.entter_id = EnterID('Visitor Info')
        self.w.close()



# src
class EnterID:

    def __init__(self, src):
        # TO KEEP TRACK OF THE USER  (IS HE PATIENT OR VISITOR?)
        self.src = src

        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.resize(400, 200)
        self.w.setStyleSheet(""".QDialog{background-color: #494162; border: 1px solid white}""")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("Enter Your National ID")
        lbl.move(30, 50)
        lbl.setStyleSheet("color: white; font-size: 24px")

        # STYLESHEET FOR LINE EDIT
        input_ss = """
                                            QLineEdit{
                                                        background-color: #f16a70;
                                                        font: 26px;

                                                        color: white;
                                                        border-width: 3px;
                                                        border-style: solid;
                                                        border-color: #f16a70 #f16a70 #F2D6CB #f16a70;
                                            }
                                    """


        # LiNE EDIT
        self.input_id0 = QtWidgets.QLineEdit(self.w)
        self.input_id0.setGeometry(30, 100, 245, 40)
        self.input_id0.setPlaceholderText('National ID')
        self.input_id0.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d+')))
        self.input_id0.setMaxLength(14)
        self.input_id0.setStyleSheet(input_ss)


        # NEXT BUTTON
        btn = QtWidgets.QPushButton(self.w)
        btn.setText("Next")
        btn.setGeometry(280, 100, 100, 40)
        btn.setStyleSheet("""
                                .QPushButton{
                                        background-color: #BCACEC;
                                        color: white;
                                        font-size: 30px;
                                        border-radius: 40px;

                                }

                                .QPushButton:hover{
                                        background-color: rgb(255, 0, 0);
                                        color: ;
                                        padding-left: 10px;
                                }

                          """)
        btn.clicked.connect(self.next_click)

        # Exit BUTTON
        btn_x = QtWidgets.QPushButton(self.w)
        btn_x.setText("×")
        btn_x.setGeometry(345, 1, 50, 40)
        btn_x.setStyleSheet("""
                                                        background-color: #494162;
                                                        color: white;
                                                        font-size: 30px;
                                                        border-radius: 40px;
                                    """)
        btn_x.clicked.connect(self.w.close)

        # SHOW DIALOG
        self.w.show()


    def next_click(self, e):

        # MESSAGE BOX
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Warning')
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        button_ok = self.msg.button(QtWidgets.QMessageBox.Ok)
        button_ok.setStyleSheet(""" background-color: #BCACEC; color: black;""")
        self.msg.setStyleSheet("""background-color: #494162; color: white; font: 24px""")
        # self.msg.move(300, 200)


        # MAKE SURE NATIONAL ID IS 14 DIGIT
        if len(self.input_id0.text()) < 14:
            self.msg.setText('Please enter your full ID   ')
            returned_val = self.msg.exec_()

            # RETURN THE FOCUS TO LINE EDIT
            self.input_id0.setFocus()


        else:

            # WIDGET
            self.conf = QtWidgets.QDialog()
            self.conf.setModal(True)
            self.conf.resize(400, 200)
            self.conf.setStyleSheet(""".QDialog{background-color: #494162; border: 1px solid white}""")
            self.conf.setWindowFlags(QtCore.Qt.FramelessWindowHint)

            # LABEL
            self.lbl_is = QtWidgets.QLabel(' Your National ID Is ', self.conf)
            self.lbl_is.move(5, 10)
            self.lbl_is.setStyleSheet(""" font: 24px; color: white; border-bottom: 0px solid red""")

            # LABEL
            lbl_id = QtWidgets.QLabel(self.conf)
            lbl_id.move(100, 50)
            lbl_id.setText(
                "{} {} {} {}".format(self.input_id0.text()[0:3], self.input_id0.text()[3:6], self.input_id0.text()[6:10],
                                     self.input_id0.text()[10:14]))
            lbl_id.setStyleSheet("color: yellow; font-size: 30px; border: 1px solid white")


            # LABEL
            self.lbl_qest = QtWidgets.QLabel("Are you sure it's correct?", self.conf)
            self.lbl_qest.move(20, 100)
            self.lbl_qest.setStyleSheet('font: 32px; color: red')

            # BUTTON EDIT
            btn_edit = QtWidgets.QPushButton(self.conf)
            btn_edit.setText('Edit')
            btn_edit.setGeometry(195, 159, 100, 40)
            btn_edit.setStyleSheet('color: red; font: 24px; ')         # background-color: #BCACEC;
            btn_edit.clicked.connect(self.edit_id_clicked)

            # BUTTON CORRECT
            btn_correct = QtWidgets.QPushButton(self.conf)
            btn_correct.setText('Correct')
            btn_correct.setGeometry(299, 159, 100, 40)
            btn_correct.setStyleSheet(' color: green; font: 24px; ')   # background-color: #BCACEC;
            btn_correct.clicked.connect(self.correct_id_clicked)

            # HIDE AND SHOW
            self.w.hide()
            self.conf.show()


    def edit_id_clicked(self):
        # self.input_id.setText("")
        self.w.show()
        self.input_id0.setFocus()
        self.conf.hide()


    # ABOVE IS OK
    # ABOVE IS OK
    # ABOVE IS OK

    def correct_id_clicked(self):

        self.conf.close()


        """
        check if this patient is in DB...,
        if true : Show his data and ask him if he wants to change it!
        if false: Take his data
        """


        # هنا تعديل واقف على الداتابيز

        exist_ = get_patient_data_from_db(int(self.input_id0.text()))

        exist_ = True


        if exist_:

            """
                خليه يتعرف على الشخص الواقف قدام الكاميرا ويرجعلك رقمه
            """

            self.cnf= ConfirmationForm_Exist(self.src, 'Name from DB', 'ID from DB', 'Address from DB', 'Mobile from DB',
                                      'birth_date from DB')
        else:

            """
                خدله صورة
            """

            self.cnf = InfoForm(self.src, self.input_id0.text())







# title, id
class InfoForm:

    def __init__(self, title, ID):

        # WINDOW
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle(title)
        self.w.setFixedSize(410, 500)
        self.w.setWindowIcon(QtGui.QIcon('Icons/lock'))
        self.w.setStyleSheet(""".QDialog{background-color: #f16a70; border: 3px solid white;}""")
        self.w.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.FramelessWindowHint)


        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("Please Enter Your Information ")
        lbl.setStyleSheet('color: yellow; font: 20px')
        lbl.move(80, 40)


        #############################################################################
        #############################################################################

        # STYLESHEET FOR LINE EDIT
        line_edit_ss = """
                                    QLineEdit{
                                                background-color: #f16a70;
                                                font: 20px;

                                                color: white;
                                                border-width: 3px;
                                                border-style: solid;
                                                border-color: #f16a70 #f16a70 #F2D6CB #f16a70;
                                    }
                            """

        # STYLESHEET FOR COMBOBOX                       # 6a70f1
        combo_ss = """
                                    .QComboBox{
                                                background-color: #f16a70;
                                                font: 20px;
                                                color: white;
                                                border-width: 3px;
                                                border-style: solid;
                                                border-color: #f16a70 #f16a70 #F2D6CB #f16a70;
                                    }
                            """

        # STYLESHEET FOR BUTTON SUBMIT
        btn_submit_ss = """
                                    .QPushButton{
                                                background-color: #0CACEC;
                                                font: 16px;
                                                color:  ;
                                                border-radius: 4px;

                                                border-top: 2px solid white;
                                                border-left: 2px solid white;
                                            }

                                    .QPushButton:hover {
                                            background-color: #0CACEC;
                                            color: white;
                                    }

                                    .QPushButton:pressed {
                                            border-style: inset;
                                            padding-right: 5px;
                                            background-color: red;
                                    }


                        """

        # STYLESHEET FOR BUTTON CANCEL
        btn_cancel_ss = """
                                            .QPushButton{
                                                background-color: #f16a70;
                                                font: 16px;
                                                color:  white;
                                                border-radius: 4px;

                                                border-top: 2px solid white;
                                                border-right: 2px solid white;
                                            }

                                            .QPushButton:hover {
                                                    background-color: #0CACEC;
                                                    color: white;
                                            }

                                            .QPushButton:pressed {
                                                    border-style: inset;
                                                    padding-right: 5px;
                                                    background-color: red;
                                            }


                                """

        #############################################################################
        #############################################################################


        # LiNE EDIT
        self.input_name = QtWidgets.QLineEdit(self.w)
        self.input_name.setGeometry(30, 97 + 30, 350, 30)
        self.input_name.setPlaceholderText('Full Name')
        self.input_name.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("([a-zأ-يA-Z]{2}[a-zأ-يA-Z]*[\s-]{0,1})+")))
        self.input_name.setMaxLength(85)
        self.input_name.setStyleSheet(line_edit_ss)

        # LiNE EDIT
        self.input_id = QtWidgets.QLineEdit(self.w)
        self.input_id.setText(ID[0:3] + " " + ID[3:6] + " " + ID[6:10] + " " + ID[10:14])
        self.input_id.setGeometry(30, 137 + 40, 350, 30)
        self.input_id.setPlaceholderText('National ID')
        self.input_id.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('\d+')))
        self.input_id.setMaxLength(17)
        self.input_id.setStyleSheet(line_edit_ss)
        self.input_id.setEnabled(False)

        # LiNE EDIT
        self.input_add = QtWidgets.QLineEdit(self.w)
        self.input_add.setGeometry(30, 177 + 50, 350, 30)
        self.input_add.setPlaceholderText('Address')
        self.input_add.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("([a-zأ-يA-Z]{2}[a-zأ-يA-Z]*[\s-]{0,1})+")))
        self.input_add.setMaxLength(85)
        self.input_add.setStyleSheet(line_edit_ss)

        # LiNE EDIT
        self.input_moile = QtWidgets.QLineEdit(self.w)
        self.input_moile.setGeometry(30, 217 + 60, 350, 30)
        self.input_moile.setPlaceholderText('Mobile Number')
        self.input_moile.setValidator(QtGui.QIntValidator())
        self.input_moile.setMaxLength(11)
        self.input_moile.setStyleSheet(line_edit_ss)
        # self.input_moile.setAlignment(QtCore.Qt.AlignCenter)

        # COMBO BOX FOR YEARS
        self.combo_year = QtWidgets.QComboBox(self.w)
        self.combo_year.setGeometry(30, 257 + 70, 115, 30)
        self.combo_year.setStyleSheet(combo_ss)

        self.combo_year.addItem('Date')
        now = datetime.datetime.now()
        for i in range(0, 151): self.combo_year.addItem(str(now.year - i))
        self.combo_year.addItem('Before {}'.format(now.year - 150))

        # COMBO BOX FOR MONTHS
        self.combo_month = QtWidgets.QComboBox(self.w)
        self.combo_month.setGeometry(158, 257 + 70, 130, 30)
        self.combo_month.setStyleSheet(combo_ss)

        self.months = ['OF', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                       'October', 'November', 'December']
        for i in self.months: self.combo_month.addItem(i)

        # COMBO BOX FOR DAYS
        self.combo_day = QtWidgets.QComboBox(self.w)
        self.combo_day.setGeometry(298, 257 + 70, 80, 30)
        self.combo_day.setStyleSheet(combo_ss)

        self.combo_day.addItem('Birth')
        for i in range(1, 10): self.combo_day.addItem('0' + str(i))
        for i in range(10, 32): self.combo_day.addItem(str(i))

        # BUTTON SUBMIT
        btn_submit = QtWidgets.QPushButton("Submit", self.w)
        btn_submit.setGeometry(205, 462, 202, 35)  # 110, 465, 200, 30
        btn_submit.setStyleSheet(btn_submit_ss)
        btn_submit.clicked.connect(self.btn_submit_click)

        # BUTTON CANCEL
        btn_cancel = QtWidgets.QPushButton("Cancel", self.w)
        btn_cancel.setGeometry(3, 462, 202, 35)
        btn_cancel.setStyleSheet(btn_cancel_ss)
        btn_cancel.clicked.connect(self.btn_cancel_click)

        # SHOW INFO FORM
        self.w.show()

    def btn_submit_click(self):

        # Map months names to numbers
        # Similar to switch case in java
        self.month_n = {
            "January": '01',
            "February": '02',
            "March": '03',
            "April": '04',
            "May": '05',
            "June": '06',
            "July": '07',
            "August": '08',
            "September": '09',
            "October": '10',
            "November": '11',
            "December": '12'
        }.get(self.combo_month.currentText(), "Invalid month")


        # ALTER RESTRICTIONS DURING TESTING
        # MUST BE EDITED BEFORE DEPLOYMENT
        if False:
            self.restrictions()
        else:
            test_without_restrictions_1(self)


    def btn_cancel_click(self):
        self.w.close()


    def restrictions(self):

        # MESSAGE BOX
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Warning')
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        button_ok = self.msg.button(QtWidgets.QMessageBox.Ok)
        button_ok.setStyleSheet(""" background-color: #BCACEC; color: black;""")
        self.msg.setStyleSheet("""background-color: #494162; color: white; font: 24px""")
        # self.msg.move(300, 200)


        # FULL NAME RESTRICTIONS
        if len(self.input_name.text()) - space_count(self.input_name.text()) < 12:
            self.msg.setText('Please enter your full name')
            returned_val = self.msg.exec_()

        # ID RESTRICTIONS
        elif len(self.input_id.text()) < 14:
            self.msg.setText('Please enter your full ID   ')
            returned_val = self.msg.exec_()

        # ADDRESS RESTRICTIONS
        elif len(self.input_add.text()) - space_count(self.input_add.text()) < 12:
            self.msg.setText('Please enter your full address')
            returned_val = self.msg.exec_()

        # MOBILE RESTRICTIONS
        elif len(self.input_moile.text()) < 11:
            self.msg.setText('Please enter your full phone')
            returned_val = self.msg.exec_()

        elif self.input_moile.text()[0] == '-' or self.input_moile.text()[0] == '+':
            self.msg.setText("Please enter your phone in just numbers. (without: '+' or '-')")
            returned_val = self.msg.exec_()

        # BIRTH DATE RESTRICTIONS
        elif self.combo_year.currentText() == 'Date':
            self.msg.setText('Please choose your year of birth')
            returned_val = self.msg.exec_()

        elif self.combo_month.currentText() == 'OF':
            self.msg.setText('Please choose your month of birth')
            returned_val = self.msg.exec_()

        elif self.combo_day.currentText() == 'Birth':
            self.msg.setText('Please choose your day of birth')
            returned_val = self.msg.exec_()


        else:
            # FORMAT BIRTH DATE LIKE 2019-01-05
            formal_date = self.combo_year.currentText() + '-' + self.month_n + '-' + self.combo_day.currentText()

            self.w.hide()

            self.cnfMSG = ConfirmationForm_Not_Exist(self, self.input_name.text(), self.input_id.text(), self.input_add.text(),
                                          self.input_moile.text(), formal_date)



# parent, title
class UpdateForm:


    def __init__(self, parent, title):
        # TO ACCESS PARENT PROPERTIES
        self.parent = parent

        # WINDOW
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle(title)
        self.w.setFixedSize(410, 380)
        self.w.move(480, 100)
        self.w.setWindowIcon(QtGui.QIcon('Icons/lock'))
        self.w.setStyleSheet(""".QDialog{background-color: #f16a70; border: 3px solid white;}""")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("Please Update Your Information ")
        lbl.setStyleSheet('color: yellow; font: 20px')
        lbl.move(60, 40)

        ############################################################################
        ############################################################################

        # STYLESHEET FOR LINE EDIT
        line_edit_ss = """
                                            QLineEdit{
                                                        background-color: #f16a70;
                                                        font: 24px;

                                                        color: white;
                                                        border-width: 3px;
                                                        border-style: solid;
                                                        border-color: #f16a70 #f16a70 #F2D6CB #f16a70;
                                            }
                                    """

        # STYLESHEET FOR BUTTON UPDATE
        btn_update_ss = """
                                            .QPushButton{
                                                        background-color: #0CACEC;
                                                        font: 16px;
                                                        color:  ;
                                                        border-radius: 4px;

                                                        border-top: 2px solid white;
                                                        border-left: 2px solid white;
                                                    }

                                            .QPushButton:hover {
                                                    background-color: #0CACEC;
                                                    color: white;
                                            }

                                            .QPushButton:pressed {
                                                    border-style: inset;
                                                    padding-right: 5px;
                                                    background-color: red;
                                            }


                                """

        # STYLESHEET FOR BUTTON CANCEL
        btn_cancel_ss = """
                                                    .QPushButton{
                                                        background-color: #f16a70;
                                                        font: 16px;
                                                        color:  white;
                                                        border-radius: 4px;

                                                        border-top: 2px solid white;
                                                        border-right: 2px solid white;
                                                    }

                                                    .QPushButton:hover {
                                                            background-color: #0CACEC;
                                                            color: white;
                                                    }

                                                    .QPushButton:pressed {
                                                            border-style: inset;
                                                            padding-right: 5px;
                                                            background-color: red;
                                                    }


                                        """

        ############################################################################
        ############################################################################

        # LiNE EDIT
        self.input_add = QtWidgets.QLineEdit(self.w)
        self.input_add.setGeometry(30, 97 + 30, 350, 40)
        self.input_add.setPlaceholderText('Address')
        self.input_add.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("([a-zأ-يA-Z]{2}[a-zأ-يA-Z]*[\s-]{0,1})+")))
        self.input_add.setMaxLength(85)
        self.input_add.setStyleSheet(line_edit_ss)
        # self.input_add.setFocusPolicy(QtCore.Qt.ClickFocus)


        # LiNE EDIT
        self.input_moile = QtWidgets.QLineEdit(self.w)
        self.input_moile.setGeometry(30, 137 + 40+ 30, 350, 40)
        self.input_moile.setPlaceholderText('Mobile Number')
        self.input_moile.setValidator(QtGui.QIntValidator())
        self.input_moile.setMaxLength(11)
        self.input_moile.setStyleSheet(line_edit_ss)
        # self.input_moile.setFocusPolicy(QtCore.Qt.ClickFocus)


        # BUTTON UPDATE
        self.btn_update = QtWidgets.QPushButton("Update", self.w)
        self.btn_update.setGeometry(205, 345, 202, 35)  # 110, 465, 200, 30
        self.btn_update.setStyleSheet(btn_update_ss)
        self.btn_update.clicked.connect(self.btn_update_click)

        # BUTTON CANCEL
        self.btn_cancel = QtWidgets.QPushButton("Cancel", self.w)
        self.btn_cancel.setGeometry(3, 345, 202, 35)
        self.btn_cancel.setStyleSheet(btn_cancel_ss)
        self.btn_cancel.clicked.connect(self.btn_cancel_click)


        # RADIO BUTTON
        self.chk_add = QtWidgets.QRadioButton(self.w)
        self.chk_add.move(10, 300)
        self.chk_add.setText('Update Address')
        self.chk_add.setStyleSheet('font: 16px; color: white')
        self.chk_add.toggled.connect(self.ch_add_clicked)

        # RADIO BUTTON
        self.chk_mobile = QtWidgets.QRadioButton(self.w)
        self.chk_mobile.move(160, 300)
        self.chk_mobile.setText('Update Mobile')
        self.chk_mobile.setStyleSheet('font: 16px; color: white')
        self.chk_mobile.toggled.connect(self.ch_mobile_clicked)

        # RADIO BUTTON
        self.chk_both = QtWidgets.QRadioButton(self.w)
        self.chk_both.move(295, 300)
        self.chk_both.setText('Update Both')
        self.chk_both.setStyleSheet('font: 16px; color: white')
        self.chk_both.setChecked(True)
        self.chk_both.toggled.connect(self.ch_both_clicked)


        # SHOW WIDGET
        self.w.show()



    def btn_update_click(self):

        up = self.restrictions()


        if up:
            # UPDATE DATA
            if self.parent.src == 'Patient Info':
                ''
                print('Update patient data')

                if self.chk_add.isChecked():
                    update_patient_address_into_db(self.input_add.text())

                elif self.chk_mobile.isChecked:
                    update_patient_mobile_into_db(self.input_moile.text())

                elif self.chk_both.isChecked():
                    update_patient_address_into_db(self.input_add.text())
                    update_patient_mobile_into_db(self.input_moile.text())


            else:
                print('Update visitor data')

                if self.chk_add.isChecked():
                    update_visitor_address_into_db(self.input_add.text())

                elif self.chk_mobile.isChecked:
                    update_visitor_mobile_into_db(self.input_moile.text())

                elif self.chk_both.isChecked():
                    update_visitor_address_into_db(self.input_add.text())
                    update_visitor_mobile_into_db(self.input_moile.text())


    def btn_cancel_click(self):
        self.w.hide()
        self.parent.w.show()


    def restrictions(self):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle('Warning')
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        button_ok = self.msg.button(QtWidgets.QMessageBox.Ok)
        button_ok.setStyleSheet(""" background-color: #BCACEC; color: black;""")
        self.msg.setStyleSheet("""background-color: #494162; color: white; font: 24px""")
        # self.msg.move(300, 200)


        if (self.chk_add.isChecked() or self.chk_both.isChecked()) and (len(self.input_add.text()) - space_count(self.input_add.text()) < 12):
            self.msg.setText('Please enter your full address')
            returned_val = self.msg.exec_()

        elif (self.chk_mobile.isChecked() or self.chk_both.isChecked()) and (len(self.input_moile.text()) < 11):
            self.msg.setText('Please enter your full phone')
            returned_val = self.msg.exec_()

        elif  (self.chk_mobile.isChecked() or self.chk_both.isChecked()) and (self.input_moile.text()[0] == '-' or self.input_moile.text()[0] == '+'):
            self.msg.setText("Please enter your phone in just numbers. (without: '+' or '-')")
            returned_val = self.msg.exec_()

        else:
            self.parent.keep_it_clicked()
            self.w.close()

            # TO KNOW WHEN ALL RESTRICTION IS SATSIFIED, SO UPDATE THE DATA
            return True


    ########################################
    ########################################


    def ch_add_clicked(self, e):
        # print('add: ', e)

        # RESET TEXT
        self.input_add.setText('')
        self.input_moile.setText('')


        if e:

            # SHOW ONLY ADDRESS LINE EDIT
            self.input_add.setVisible(True)
            self.input_moile.setVisible(False)

            # RESIZE
            self.w.setFixedSize(410, 340-50)

            self.btn_update.move(205, 255)
            self.btn_cancel.move(3, 255)

            self.chk_add.move(10, 300-40-50)
            self.chk_mobile.move(160, 300-40-50)
            self.chk_both.move(295, 300-40-50)

    def ch_mobile_clicked(self, e):
        # print('mob: ', e)

        # RESET TEXT
        self.input_add.setText('')
        self.input_moile.setText('')


        if e:

            # SHOW ONLY MOBILE LINE EDIT
            self.input_add.setVisible(False)
            self.input_moile.setVisible(True)

            # RESIZE
            self.w.setFixedSize(410, 340 - 50)

            self.btn_update.move(205, 255)
            self.btn_cancel.move(3, 255)

            self.chk_add.move(10, 300 - 40 - 50)
            self.chk_mobile.move(160, 300 - 40 - 50)
            self.chk_both.move(295, 300 - 40 - 50)

            self.input_moile.move(30, 97 + 30)

    def ch_both_clicked(self, e):
        # print('both: ', e)

        # RESET TEXT
        self.input_add.setText('')
        self.input_moile.setText('')


        if e:

            # SHOW BOTH LINE EDIT
            self.input_add.setVisible(True)
            self.input_moile.setVisible(True)

            # RESIZE
            self.w.setFixedSize(410, 380)

            self.btn_update.move(205, 345)
            self.btn_cancel.move(3, 345)

            self.chk_add.move(10, 300)
            self.chk_mobile.move(160, 300)
            self.chk_both.move(295, 300)

            self.input_moile.move(30, 137 + 40+ 30)



# src, name, id, address, mobile, birth_date
class ConfirmationForm_Exist:

    def __init__(self, src, name, idd, address, mobile, birth_date):
        # TO KEEP TRACK OF THE USER  (IS HE PATIENT OR VISITOR?)
        self.src = src

        # this list used to sort info fields by its string length تصاعديا
        arr = [str(name), str(idd), str(address), str(mobile), str(birth_date)]
        arr.sort(key=len)


        self.width = len(arr[4]) * 15   # character width  in "Courier New" font = 15

        # TO KEEP IT SUITABLE
        if self.width < 260:
            self.width = 260


        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.resize(140 + self.width + 10, 500)
        self.w.setStyleSheet(" QDialog{background: white;} ")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)


        # LABEL
        self.lbl_name = QtWidgets.QLabel(' Name ', self.w)
        self.lbl_name.move(30, 97 + 30)
        self.lbl_name.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER NAME
        self.p_name = QtWidgets.QLabel(self.w)
        self.p_name.move(140, 97 + 30)
        # self.input_name.setStyleSheet("""background-color: #494162; font: 20px; color: white; border-left: px;""")
        self.p_name.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ###########################################################################

        # LABEL
        self.lbl_id = QtWidgets.QLabel(' ID ', self.w)
        self.lbl_id.move(30, 137 + 40)
        self.lbl_id.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER ID
        self.p_id = QtWidgets.QLabel(self.w)
        self.p_id.move(140, 137 + 40)
        self.p_id.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        #############################################################################

        # LABEL
        self.lbl_add = QtWidgets.QLabel(' Addr ', self.w)
        self.lbl_add.move(30, 177 + 50)
        self.lbl_add.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER ADDRESS
        self.p_add = QtWidgets.QLabel(self.w)
        self.p_add.move(140, 177 + 50)
        self.p_add.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        #############################################################################

        # LABEL
        self.lbl_phone = QtWidgets.QLabel(' Mobile ', self.w)
        self.lbl_phone.move(30, 217 + 60)
        self.lbl_phone.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER MOBILE NUMBER
        self.p_moile = QtWidgets.QLabel(self.w)
        self.p_moile.move(140, 217 + 60)
        # self.p_moile.setAlignment(QtCore.Qt.AlignCenter)
        self.p_moile.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ############################################################################

        # LABEL
        self.lbl_birth = QtWidgets.QLabel(' Birth Date ', self.w)
        self.lbl_birth.move(30, 257 + 70)
        self.lbl_birth.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER BIRTH DATE
        self.p_birth_date = QtWidgets.QLabel(self.w)
        self.p_birth_date.move(140, 257 + 70)
        # self.input_birth_date.setAlignment(QtCore.Qt.AlignCenter)
        self.p_birth_date.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ############################################################################

        # ______________________________________________________________________#

        # SET USER DATA ON LABELS
        self.p_name.setText(name)
        self.p_id.setText(idd)
        self.p_add.setText(address)
        self.p_moile.setText(mobile)
        self.p_birth_date.setText(birth_date)
        # ______________________________________________________________________#



        # LABEL
        self.lbl = QtWidgets.QLabel("This is your information", self.w)
        self.lbl.move((self.width - 200) / 2, 20)
        self.lbl.setStyleSheet('font: 32px; color: green')

        # LABEL
        self.lbl2 = QtWidgets.QLabel("Do you want to update it?", self.w)
        self.lbl2.move((self.width - 200) / 2, 60)
        self.lbl2.setStyleSheet('font: 32px; color: green')

        # BUTTON UPDATE
        btn_edit = QtWidgets.QPushButton(self.w)
        btn_edit.setText('Update')
        btn_edit.setGeometry(self.width - 115, 370 + 70, 100, 40)
        btn_edit.setStyleSheet('color: red; font: 24px; ')
        btn_edit.clicked.connect(self.update_clicked)

        # BUTTON KEEP IT
        btn_correct = QtWidgets.QPushButton(self.w)
        btn_correct.setText('Keep It')
        btn_correct.setGeometry(self.width - 10, 370 + 70, 100, 40)
        btn_correct.setStyleSheet('color: green; font: 24px; ')
        btn_correct.clicked.connect(self.keep_it_clicked)

        # SHOW WIDGET
        self.w.show()


    def update_clicked(self):
        self.w.hide()
        self.update = UpdateForm(self, 'Update Your Info')


    def keep_it_clicked(self):
        'next step'

        if self.src == 'Patient Info':

            self.w.hide()
            self.dep = Metrics()

        else:
            self.patient_room = PatientRoom()
            self.w.close()




# parent, name, idd, address, mobile, birth_date
class ConfirmationForm_Not_Exist:

    def __init__(self, parent, name, idd, address, mobile, birth_date):
        # TO ACCESS PARENT PROPERTIES
        self.parent = parent

        # this list used to sort info fields by its string length تصاعديا
        arr = [str(name), str(idd), str(address), str(mobile), str(birth_date)]
        arr.sort(key=len)


        self.width = len(arr[4]) * 15  # character width  in "Courier New" font = 15

        # TO KEEP IT SUITABLE
        if self.width < 260:
            self.width = 260

        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.resize(140 + self.width + 10, 500)
        self.w.setStyleSheet(" QDialog{background: white;} ")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # LABEL
        self.lbl_name = QtWidgets.QLabel(' Name ', self.w)
        self.lbl_name.move(30, 97 + 30)
        self.lbl_name.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER NAME
        self.p_name = QtWidgets.QLabel(self.w)
        self.p_name.move(140, 97 + 30)
        # self.input_name.setStyleSheet("""background-color: #494162; font: 20px; color: white; border-left: px;""")
        self.p_name.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ###########################################################################

        # LABEL
        self.lbl_id = QtWidgets.QLabel(' ID ', self.w)
        self.lbl_id.move(30, 137 + 40)
        self.lbl_id.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER ID
        self.p_id = QtWidgets.QLabel(self.w)
        self.p_id.move(140, 137 + 40)
        self.p_id.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        #############################################################################

        # LABEL
        self.lbl_add = QtWidgets.QLabel(' Addr ', self.w)
        self.lbl_add.move(30, 177 + 50)
        self.lbl_add.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER ADDRESS
        self.p_add = QtWidgets.QLabel(self.w)
        self.p_add.move(140, 177 + 50)
        self.p_add.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        #############################################################################

        # LABEL
        self.lbl_phone = QtWidgets.QLabel(' Mobile ', self.w)
        self.lbl_phone.move(30, 217 + 60)
        self.lbl_phone.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER MOBILE NUMBER
        self.p_moile = QtWidgets.QLabel(self.w)
        self.p_moile.move(140, 217 + 60)
        # self.p_moile.setAlignment(QtCore.Qt.AlignCenter)
        self.p_moile.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ############################################################################

        # LABEL
        self.lbl_birth = QtWidgets.QLabel(' Birth Date ', self.w)
        self.lbl_birth.move(30, 257 + 70)
        self.lbl_birth.setStyleSheet(""" font: 20px; color: red; border-left: 2px solid;""")

        # LABEL TO DISPLAY USER BIRTH DATE
        self.p_birth_date = QtWidgets.QLabel(self.w)
        self.p_birth_date.move(140, 257 + 70)
        # self.input_birth_date.setAlignment(QtCore.Qt.AlignCenter)
        self.p_birth_date.setStyleSheet('font-family: Courier New; font: 24px; border: 2px dashed;')
        ############################################################################

        # ______________________________________________________________________#

        # SET USER DATA ON LABELS
        self.p_name.setText(name)
        self.p_id.setText(idd)
        self.p_add.setText(address)
        self.p_moile.setText(mobile)
        self.p_birth_date.setText(birth_date)
        # ______________________________________________________________________#



        # LABEL
        # the width of this label = 240             (I knew it by try and error)
        self.lbl = QtWidgets.QLabel("Are you sure it's correct?", self.w)
        self.lbl.move((self.width - 200) / 2, 20)
        self.lbl.setStyleSheet('font: 32px; color: green')

        # BUTTON EDIT
        btn_edit = QtWidgets.QPushButton(self.w)
        btn_edit.setText('Edit')
        btn_edit.setGeometry(self.width - 115, 370 + 70, 100, 40)
        btn_edit.setStyleSheet('color: red; font: 24px; ')
        btn_edit.clicked.connect(self.edit_clicked)

        # BUTTON CORRECT
        btn_correct = QtWidgets.QPushButton(self.w)
        btn_correct.setText('Correct')
        btn_correct.setGeometry(self.width - 10, 370 + 70, 100, 40)
        btn_correct.setStyleSheet('color: green; font: 24px; ')
        btn_correct.clicked.connect(self.correct_clicked)

        # SHOW WIDGET
        self.w.show()


    def edit_clicked(self):
        self.parent.w.show()
        self.w.hide()


    def correct_clicked(self):
        # self.w.close()

        if self.parent.w.windowTitle() == 'Patient Info':

            # save data that user entered into patient object
            last_patient.Name       = self.p_name.text()
            last_patient.ID         = self.p_id.text()
            last_patient.Addr       = self.p_add.text()
            last_patient.Phone      = self.p_moile.text()
            last_patient.Birth_Date = self.p_birth_date.text()


            # SAVE DATA THAT USER ENTERED INTO DATABASE
            save_patient_data_into_db(last_patient)


            ############################## TEMPORARY ########################################
            ###...

            self.followme = FollowMe()
            self.w.close()

            if SPEAK:
                # TEXT TO SPEECH
                engine = pyttsx3.init()
                voices = engine.getProperty('voices')
                engine.setProperty('voice', voices[1].id)
                engine.setProperty('rate', 150)
                # engine.say("Now I will guide you to the diagnosis, Please Follow me ")
                engine.say(" Please Follow me ")
                engine.runAndWait()


            # BUTTON ADDED TO FOLLOW ME WIDGET TO MOVE THE USER TO NEXT WIDGET WHEN CLICKED
            self.btn_new = QtWidgets.QPushButton("UuuNEXTuuU", self.followme.w)
            self.btn_new.setGeometry(600, 600, 200, 30)
            self.btn_new.clicked.connect(self.btn_uu_click)
            self.btn_new.show()

            ###...
            ############################## END TEMPORARY ########################################


        else:

            # save data that user entered into visitor object
            last_visitor.Name       = self.p_name.text()
            last_visitor.ID         = self.p_id.text()
            last_visitor.Addr       = self.p_add.text()
            last_visitor.Phone      = self.p_moile.text()
            last_visitor.Birth_Date = self.p_birth_date.text()

            # SAVE DATA THAT USER ENTERED INTO DATABASE
            save_visitor_data_into_db(last_visitor)

            # next
            self.patient_room = PatientRoom()
            self.w.close()



    def btn_uu_click(self):
        self.followme.w.hide()
        self.dep = Metrics()





class Metrics:

    def __init__(self):


        # DIALOGE
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle('Metrics')
        self.w.setWindowIcon(QtGui.QIcon('Icons/metrics.png'))
        self.w.setFixedSize(400, 500)
        self.w.setStyleSheet("""background-color: ;""")
        self.w.setWindowFlags(QtCore.Qt.SubWindow)
        # self.w.setEnabled(False)
        # self.w.move(900, 150)

        # TO DISPLAY HEART BEAT VALUE
        self.heart_beats = QtWidgets.QSplitter(self.w)
        self.heart_beats.setGeometry(16, 200, 100, 100)
        self.heart_beats.setStyleSheet("""background-color: #F16A70; border-radius: 50px;""")

        # # TO DISPLAY SUGAR VALUE
        # self.sugar = QtWidgets.QSplitter(self.w)
        # self.sugar.setGeometry(112, 150, 80, 80)
        # self.sugar.setStyleSheet("""background-color: #B1D877; border-radius: 40px;""")

        # TO DISPLAY TEMPERATURE VALUE
        self.temperature = QtWidgets.QSplitter(self.w)
        self.temperature.setGeometry(208, 200, 100, 100)
        self.temperature.setStyleSheet("""background-color: #8CDCDA; border-radius: 50px;""")

        # TO DISPLAY PRESSURE VALUE
        self.pressure = QtWidgets.QSplitter(self.w)
        self.pressure.setGeometry(304, 150, 80, 80)
        self.pressure.setStyleSheet("""background-color: #B1D877; border-radius: 40px;""")


        # LABEL
        self.heart_beats_lbl = QtWidgets.QLabel('Heart Beats', self.heart_beats)
        self.heart_beats_lbl.setStyleSheet('background-color: #F16A70; font: 14px')
        self.heart_beats_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # # LABEL
        # self.sugar_lbl = QtWidgets.QLabel('Sugar', self.sugar)
        # self.sugar_lbl.setStyleSheet('background-color: #B1D877; font: 14px')
        # self.sugar_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # LABEL
        self.temperature_lbl = QtWidgets.QLabel('Temperature', self.temperature)
        self.temperature_lbl.setStyleSheet('background-color: #8CDCDA; font: 14px')
        self.temperature_lbl.setAlignment(QtCore.Qt.AlignCenter)

        # LABEL
        self.pressure_lbl = QtWidgets.QLabel('Pressure', self.pressure)
        self.pressure_lbl.setStyleSheet('background-color: #B1D877; font: 14px')
        self.pressure_lbl.setAlignment(QtCore.Qt.AlignCenter)


        # BUTTON NEXT
        btn_next = QtWidgets.QPushButton("Next", self.w)
        btn_next.setGeometry(210, 465, 150, 30)  # 110, 465, 200, 30
        btn_next.setStyleSheet(StyleSheets().btn_next)
        btn_next.setVisible(False)
        btn_next.clicked.connect(self.btn_next_click)

        # BUTTON CANCEL
        btn_cancel = QtWidgets.QPushButton("Cancel", self.w)
        btn_cancel.setGeometry(50, 465, 150, 30)
        btn_cancel.setStyleSheet(StyleSheets().btn_next)
        btn_cancel.setVisible(False)
        btn_cancel.clicked.connect(self.w.close)

        # SHOW
        self.w.show()

        if SPEAK:
            # SPEAKER
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.setProperty('rate', 150)
            engine.say("Now I will take your metrics. Please follow instructions ")
            engine.runAndWait()


        # GET METRICS
        self.get_metrics()

        # SET BUTTONS VISIBLE
        # self.w.setEnabled(True)
        btn_next.setVisible(True)
        btn_cancel.setVisible(True)


    def btn_next_click(self):
        self.w.hide()
        self.patient_case = PatientCase()





    def msg(self, flash_color):
        msg = QtWidgets.QMessageBox()
        msg.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        msg.setText(
            '\nPut your finger on the sensor that flashes on {} and wait. \n\nBut FIRST click OK'.format(flash_color))
        msg.setWindowTitle('How To Use Heart Beat Sensor')
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        button_ok = msg.button(QtWidgets.QMessageBox.Ok)
        button_ok.setStyleSheet(""" background-color: #BCACEC; color: black;""")
        # msg.setStyleSheet("""background-color: #F16A70; color: white; font: 24px""")

        msg_lbl = QtWidgets.QLabel('But FIRST click OK', msg)
        msg_lbl.resize(200, 30)
        msg_lbl.setStyleSheet('color: blue;')
        msg_lbl.move(65, 140)

        if flash_color == 'yellow':
            msg.setStyleSheet("""background-color: #B1D877; color: white; font: 24px""")
        elif flash_color == 'green':
            msg.setStyleSheet("""background-color: green; color: white; font: 24px""")
            msg_lbl.setStyleSheet('color: yellow;')
        elif flash_color == 'blue':
            msg.setStyleSheet("""background-color: blue; color: white; font: 24px""")
            msg_lbl.setStyleSheet('color: red;')  # Aquamarine Purple
        else:
            # if 'red'
            msg.setStyleSheet("""background-color: #F16A70; color: white; font: 24px""")

        rtrn = msg.exec_()

        return rtrn

    def get_metrics(self):
        # NEXT LINE:
        # [1] CALL [self.msg('red')] TO SHOW MESSAGE,
        # [2] MAKE SURE THAT YOU CLICKED "OK" BUTTONS ON THE MESSAGE WIDGET

        if self.msg('red') == QtWidgets.QMessageBox.Ok:
            last_patient.Heart_Beats = get_heart_beats()  # call function --> get_heart_beats() & stores returned value in last_patient.Heart_Beats
            self.heart_beats_lbl.setText(last_patient.Heart_Beats)  # display that value on a label

        if self.msg('green') == QtWidgets.QMessageBox.Ok:
            last_patient.Temperature = get_temperature()
            self.temperature_lbl.setText(last_patient.Temperature)

        if self.msg('blue') == QtWidgets.QMessageBox.Ok:
            prsr = get_pressure()

            if prsr[0] == 'DONE':
                high = prsr[1]
                low = prsr[2]

                last_patient.High_Pressure = high
                last_patient.Low_Pressure = low

                self.pressure_lbl.setText('\n' + last_patient.High_Pressure + ' / ' + last_patient.Low_Pressure)

            else:

                high = prsr
                low = prsr

                last_patient.High_Pressure = high
                last_patient.Low_Pressure = low

                self.pressure_lbl.setText('\n' + prsr)







class FollowMe:

    def __init__(self):

        # WIDGET
        self.w = QtWidgets.QWidget()
        # self.w.setModal(True)
        self.w.setWindowTitle("Follow Me")
        self.w.setWindowIcon(QtGui.QIcon('Icons/location.png'))
        self.w.setFixedSize(400, 500)
        self.w.setStyleSheet("""background-color: white""")
        self.w.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.w.keyPressEvent = self.esc

        # LABEL FOR THE GIF IMAGE
        self.lbl = QtWidgets.QLabel(self.w)
        self.lbl.setStyleSheet("color: white; font: 44px")
        self.lbl.move(500, 200)

        # GIF IMAGE
        self.gif = QtGui.QMovie('Icons/follow.gif')  # G:/sh.mp4
        self.gif.start()

        # ADD GIT IMAGE TO LABEL
        self.lbl.setMovie(self.gif)

        # SHOW WIDGET
        self.w.showFullScreen()


    def esc(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.w.close()






class PatientRoom:

    def __init__(self):

        # DIALOG
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle("Patient Room")
        self.w.setWindowIcon(QtGui.QIcon('Icons/search.png'))
        self.w.setFixedSize(400, 500)
        self.w.setStyleSheet("""background-color: #494162""")
        self.w.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("Please enter patient name ")
        lbl.setStyleSheet('color: cyan; font: 20px')
        lbl.move(85, 60)

        # LABEL
        lbl2 = QtWidgets.QLabel(self.w)
        lbl2.setText("Or enter room number ")
        lbl2.setStyleSheet('color: cyan; font: 16px')
        lbl2.move(130, 200)



        # LABEL
        lbl_name = QtWidgets.QLabel("Patient Name", self.w)
        lbl_name.setGeometry(15, 121, 105, 28)
        lbl_name.setStyleSheet("background-color: #B1D877; color: black; font: 16px; border: 1px solid white;border-radius: 14px")


        #####################################################################################
        #####################################################################################

        # THE COMPLETER PART
        # Resources:
        # https://wiki.python.org/moin/PyQt/Adding%20auto-completion%20to%20a%20QLineEdit
        self.lst = ['Khalid Hamada', 'Ibrahim Mahmoud', 'Ahmad Abdelrahmaan', 'Huessin Tarek', 'Mohamad Abdelhameed',
                    'Aya Samir', 'Enas', 'Heba', 'Helmy', 'Hanan']


        # CREATE MODEL FOR THE COMPLETER
        self.model = QtCore.QStringListModel()
        self.model.setStringList(self.lst)

        # CREATE COMPLETER OBJECT
        input_name_completer = QtWidgets.QCompleter()
        # SET MODEL TO THE COMPLETER
        input_name_completer.setModel(self.model)
        input_name_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)

        # SET STYLESHEET TO THE POP-UP MENU OF THE COMPLETER
        c = input_name_completer.popup()
        c.resize(300, 900)
        c.setStyleSheet(
            "background-color: #61BC79; color: white; font: 18px; border: 1px solid white; padding-left: 5px; padding-right: 30px;")

        #####################################################################################
        #####################################################################################


        # LINE EDIT
        self.input_name = QtWidgets.QLineEdit(self.w)
        self.input_name.setGeometry(125 + 5, 120, 252, 30)
        self.input_name.setStyleSheet("background-color: #948BB1; color: white; font: 20px; border: 1px solid white; border-radius: 15px; padding-left: 5px; padding-right: 30px;")
        self.input_name.textEdited.connect(self.on_text_edit)

        # ADD COMPLETER TO THE LINE EDIT
        self.input_name.setCompleter(input_name_completer)


        # LABEL
        self.lbl_room = QtWidgets.QLabel("Room Number", self.w)
        self.lbl_room.setGeometry(14, 241, 112, 28)
        self.lbl_room.setStyleSheet(
            "background-color: #B1D877; color: black; font: 16px; border: 1px solid white; border-radius: 14px")

        # LINE EDIT
        self.input_room = QtWidgets.QLineEdit(self.w)
        self.input_room.setGeometry(127 + 5, 240, 250, 30)
        self.input_room.setValidator(QtGui.QIntValidator())
        self.input_room.setMaxLength(4)
        self.input_room.setStyleSheet(
            "background-color: #948BB1; color: white; font: 20px; border: 1px solid white; border-radius: 15px; padding-left: 100px; padding-right: 100px")


        # BUTTON
        btn_search_by_name = QtWidgets.QPushButton("Go", self.w)
        btn_search_by_name.setGeometry(352, 120, 30, 30)
        btn_search_by_name.setStyleSheet(StyleSheets().btn_search)
        # btn_search_by_name.clicked.connect(self.btn_search_by_name_click)


        # BUTTON
        btn_search_by_room = QtWidgets.QPushButton("Go", self.w)
        btn_search_by_room.setGeometry(352, 240, 30, 30)
        btn_search_by_room.setStyleSheet(StyleSheets().btn_search)
        # btn_search_by_room.clicked.connect(self.btn_self.btn_search_by_room_click_click)

        # SHOW WIDGET
        self.w.show()


    def on_text_edit(self, e):

        if DATABASE:
            # cursor.execute('SELECT Name FROM patient WHERE Name LIKE "%{}%" '.format(self.input_name.text()))
            cursor.execute('SELECT Name, Room_ID FROM patient WHERE Name LIKE "%{}%" '.format(e))

            # DATA FROM DATABASE
            lst = cursor.fetchall()  # list of tuples, each tuple has only one string ==> ('Mo Salah', )
            print(lst)

        else:
            lst = ['Khalid Hamada', 'Ibrahim Mahmoud', 'Ahmad Abdelrahmaan', 'Huessin Tarek', 'Mohamad Abdelhameed',
                   'Aya Samir', 'Enas', 'Heba', 'Helmy', 'Hanan']


        model_lst = []

        " THIS FOR LOOP NEEDED TO BE IN A THREAD "
        for i in lst:  # for each tuple in the list
            model_lst.append(i[0])  # add its first element to another list
            print('$: ', i[0])


        # update the list of the MODEL of the completer
        self.model.setStringList(model_lst)


#####################################################################################
#                       INTERFACE WITH DIAGNOSE PART                                #
#####################################################################################



dep = [0] * 13          #separtment array of values
depart = ["Abdomen", "Heart", "Surgery", "Bones", "Teeth", "Therapy", "Psycho",
          "Nerve", "Chest", "Nose", "Eyes", "Skin", "Stomach"]



def search_head(cmplnt):
    eye = open("ai/head_eye.txt", "r")  # open the keywords file
    file_contents = eye.read()  # read the whole file content
    for i in file_contents.split('\n'):  # loop for every word in the file
        if i in cmplnt:
            dep[10] += 4                             # gain points

    nose = open("ai/head_nose.txt", "r")
    file_contents = nose.read()
    for i in file_contents.split('\n'):
        if i in cmplnt:
            dep[9] += 4

    nerve = open("ai/head_nerve.txt", "r")
    file_contents = nerve.read()
    for i in file_contents.split('\n'):
        if i in cmplnt:
            dep[7] += 4

    teeth = open("ai/head_teeth.txt", "r")
    file_contents = teeth.read()
    for i in file_contents.split('\n'):
        if i in cmplnt:
            dep[4] += 4

    Skin = open("ai/head_skin.txt", "r")
    file_contents = Skin.read()
    for i in file_contents.split('\n'):
        if i in cmplnt:
            dep[11] += 4

    Bones = open("ai/head_bones.txt", "r")
    file_contents = Bones.read()
    for i in file_contents.split('\n'):
        if i in cmplnt:
            dep[3] += 4


def max_equality():
    i = 0
    j = i + 1
    maximum = max(dep)
    # print(maximum)
    while i < len(dep):
        while j < len(dep):

            if dep[i] == dep[j] != 0 and dep[j] == maximum:
                return 1
            j = j + 1

        i = i + 1
        j = i + 1


def head(f, g):


    search_head(f)


    # zero equal
    while(max(dep) == 0):
        playsound('sound/details.mp3')
        f = respond('', '')
        # f = respond('frommyeye.wav', '')
        print(f)
        search_head(f)



    while max_equality() == 1:

        # speak("مزيدٌ مِنَ التفاصيل لو سمحت", '')

        playsound('sound/details.mp3')
        f = respond('', '')
        # f = respond('frommyeye.wav', '')
        print(f)
        # print(f)
        search_head(f)



    #Get the highest value and it’s index in the array
    index, value = max(enumerate(dep), key=operator.itemgetter(1))
    print("القسم الأقرب بقيمة", value)

    i = 0
    while i < len(dep):
        dep[i] = 0
        i = i + 1

    return depart[index]


def respond(a, b):
    r = sr.Recognizer()                     #taking object from SpeechRecognition
    # print('here', r.__str__())
    with sr.Microphone() as source:         #existing audio file as source of talk
        # print("أجب بالكلام:")
        audio = r.listen(source, timeout= 10, phrase_time_limit=5)                #listen and save what said
        # print('audio')
        try:
            text = r.recognize_google(audio, language='en')      #transform speech to text
            print('You siad: ', text)
        except:
            print("I don't hear you !!")
            playsound('sound/notunderstand.mp3')
            return respond('', '')
    return text


def get_body_part(m):

    if "head" in m:
        return 'head_part'
    elif "chest" in m:
        print('Chest_dep')
        return "Chest"
    elif "abdomen" in m or "belly" in m or "stomach" in m:
        print("Abdomen_dep")
        return "Abdomen"
    elif 'feet' in m or 'leg' in m or 'hand' in m or 'toe' in m:
        print('Therapy_dep')
        return "Therapy"
    elif "back" in m:
        print("Bones_dep")
        return "Bones"
    else:
        return "1"



class PatientCase:

    def __init__(self):

        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setWindowTitle(" ZU Hospital ")
        self.w.setWindowIcon(QtGui.QIcon('Icons/Hospital'))
        self.w.resize(400, 500)
        self.w.setFixedSize(400, 450)
        # self.w.setStyleSheet(""".QWidget{border: 1px solid red}""")
        self.w.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        self.w.keyPressEvent = self.esc


        # IMAGE
        image = QtGui.QImage("Icons/img/hos_1.jpg")
        sImage = image.scaled(QtCore.QSize(1365, 900))  # resize Image to widgets size

        # PALETTE
        palette = QtGui.QPalette()
        palette.setBrush(10, QtGui.QBrush(sImage))  # 10 = Windowrole

        self.w.setPalette(palette)


        # LABEL
        lbl = QtWidgets.QLabel(self.w)
        lbl.setText("What is the case of the patient?")
        lbl.setStyleSheet("color: yellow; font-size: 24px")  # 22px
        lbl.move(5, 10)  # 580, 250

        self.btn_baby = QtWidgets.QRadioButton('Patient is a Baby', self.w)
        self.btn_baby.move(30, 70)
        self.btn_baby.setStyleSheet('color: white; font: 22px')

        self.btn_pregnancy = QtWidgets.QRadioButton('Pregnancy', self.w)
        self.btn_pregnancy.move(30, 120)
        self.btn_pregnancy.setStyleSheet('color: white; font: 22px')

        self.btn_womenhood = QtWidgets.QRadioButton('Special Womanhood Complaint', self.w)
        self.btn_womenhood.move(30, 170)
        self.btn_womenhood.setStyleSheet('color: white; font: 22px')

        self.btn_surgery = QtWidgets.QRadioButton('Surgery or Wound appurtenances', self.w)
        self.btn_surgery.move(30, 220)
        self.btn_surgery.setStyleSheet('color: white; font: 22px')

        self.btn_genitalia = QtWidgets.QRadioButton('Genitalia', self.w)
        self.btn_genitalia.move(30, 270)
        self.btn_genitalia.setStyleSheet('color: white; font: 22px')

        self.btn_others = QtWidgets.QRadioButton('Others', self.w)
        self.btn_others.move(30, 320)
        self.btn_others.setStyleSheet(""".QRadioButton{ color: white; font: 22px}""")

        # NEXT BUTTON
        btn = QtWidgets.QPushButton(self.w)
        btn.setText("Next")
        btn.setGeometry(310, 350, 300, 80)  # BCACEC
        btn.setStyleSheet("""
                                .QPushButton{
                                        background-color: rgb(255, 0, 0);
                                        color: white;
                                        font-size: 20px;
                                        border-radius: 40px;
                                        padding-right: 190px;

                                }

                                .QPushButton:pressed {

                                        background-color: #0CACEC;
                                        border-style: inset;
                                }

                                .QPushButton:hover{
                                        background-color: #BCACEC;
                                        color: ;
                                        padding-right: 190px;
                                }

                          """)
        btn.clicked.connect(self.next_click)


        self.w.show()



    def next_click(self, e):

        # checked = self.btn_baby.isChecked() or self.btn_pregnancy.isChecked() or self.btn_womenhood.isChecked() or self.btn_surgery.isChecked() or self.btn_genitalia.isChecked() or self.btn_others.isChecked()


        if self.btn_baby.isChecked():

            loc = get_department_location('Baby')
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print("baby_dep")
            return "Baby"

        elif self.btn_pregnancy.isChecked():

            loc = get_department_location('Womanhood')
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print("womanhood_dep")
            return "Womanhood"

        elif self.btn_womenhood.isChecked():

            loc = get_department_location('Womanhood')
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print("womanhood_dep")
            return "Womanhood"

        elif self.btn_surgery.isChecked():

            loc = get_department_location('Surgery')
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print("surgery_dep")
            return "Surgery"

        elif self.btn_genitalia.isChecked():

            loc = get_department_location('Urine')
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print("urine_dep")
            return "Urine"

        elif self.btn_others.isChecked():

            self.pain_source = PainSource()
            self.w.close()

        else:
            msg = QtWidgets.QMessageBox()
            msg.setText('Please choose one of the above cases. If not matched, choose [Others]')
            msg.setWindowTitle('Warning')
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
            button_ok = msg.button(QtWidgets.QMessageBox.Ok)
            button_ok.setStyleSheet(""" background-color: #BCACEC; color: black;""")
            msg.setStyleSheet("""background-color: #494162; color: white; font: 24px""")
            # msg.move(300, 200)
            msg.exec_()


    def esc(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.w.close()



class PainSource:

    def __init__(self):

        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle(" ZU Hospital ")
        self.w.setWindowIcon(QtGui.QIcon('Icons/Hospital'))
        self.w.resize(400, 500)
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.w.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.w.keyPressEvent = self.esc



        '''
        # NO BUTTON
        self.btn_no = QtWidgets.QPushButton(self.w)
        self.btn_no.setText("Click Me")
        self.btn_no.resize(300, 300)
        self.btn_no.move(560, 220)
        # self.btn_no.setStyleSheet(ss)
        self.btn_no.setStyleSheet("""
                                        .QPushButton{
                                                background-color: blue;
                                                color: white;
                                                font-size: 70px;
                                                border-radius: 150px;
                                                padding-right: 0px;

                                        }

                                        .QPushButton:pressed {

                                                background-color: #0CACEC;
                                                border-style: inset;
                                        }

                                        .QPushButton:hover{
                                                background-color: rgb(255, 0, 0);
                                                color: ;
                                                padding-right: 0px;
                                        }

                                  """)
        self.btn_no.clicked.connect(self.no_click)
        '''



        # LABEL
        self.lbl = QtWidgets.QLabel('CLICK ON THE MIC\n FOR DIAGNOSING', self.w)
        self.lbl.move(350, 285)
        self.lbl.setStyleSheet('color: orange; font: 60px;')


        # BUTTON
        self.btn_no = QtWidgets.QPushButton(self.w)
        self.btn_no.setText("Click Me..")
        self.btn_no.setIcon(QtGui.QIcon('Icons/mic.png'))
        self.btn_no.setIconSize(QtCore.QSize(600, 600))
        self.btn_no.resize(300, 300)
        self.btn_no.move(930, 220)
        self.btn_no.setStyleSheet("""
                                                .QPushButton{
                                                        background-color: white;
                                                        color: white;
                                                        font-size: 70px;
                                                        border-radius: 150px;
                                                        padding-right: 0px;

                                                }

                                                .QPushButton:pressed {

                                                        background-color: white;
                                                        border-style: inset;
                                                }

                                                .QPushButton:hover{
                                                        background-color: white;
                                                        color: ;
                                                        padding-right: 0px;
                                                }

                                          """)
        self.btn_no.clicked.connect(self.no_click)


        if False:
            # HIDE LABELS
            self.mlbl = QtWidgets.QLabel(self.w)
            self.mlbl.resize(60, 200)
            self.mlbl.move(980, 260)
            # self.mlbl.setStyleSheet('background: orange')


            self.uplbl = QtWidgets.QLabel(self.w)
            self.uplbl.resize(20, 20)
            self.uplbl.move(960, 285)
            # self.uplbl.setStyleSheet('background: red')

            self.dwnlbl = QtWidgets.QLabel(self.w)
            self.dwnlbl.resize(20, 20)
            self.dwnlbl.move(960, 420)
            # self.dwnlbl.setStyleSheet('background: red')



        # SHOW WIDGET
        self.w.showFullScreen()


    def no_click(self, e):

        playsound('sound/pain.mp3')

        txt = respond('', '')
        # txt = respond('frommyhead.wav')
        print(txt)
        dprt = get_body_part(txt)
        if dprt == "1":
            playsound('sound/notunderstand.mp3')
            # speak("لم افهمك، اعد المحاولة", '')
            self.no_click('')

        elif dprt == 'head_part':

            playsound('sound/complain.mp3')

            txt = respond('', '')
            # txt = respond('headeaq.wav')
            print(txt)
            dprt = head(txt, '')


            #
            loc = get_department_location(dprt)
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print('Go to {} department'.format(dprt))




        else:

            #
            loc = get_department_location(dprt)
            self.followme = FollowMe()
            self.w.close()
            set_destination(loc)

            print('Go to {} department'.format(dprt))


    def esc(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.w.close()





######################################################################################
#                   END INERFACE WITH DIAGNOSE PART                                  #
######################################################################################


# Interface with Medical Part
def get_heart_beats(call=0):
    # print("\n*...Tell Patient How To Use Heart_Beats Sensor...*")

    """
            *get Heart Beats*
            *from Ibrahim*
    """

    # Demo2
    try:
        arduino = serial.Serial('COM5', '9600', timeout=45)
        print('>> Serial port opened')
        time.sleep(2)
        chk = True
    except serial.serialutil.SerialException:
        print('@ Can not open serial communication with Ibrahim')
        arduino = None
        chk = False



    if chk:
        print('>> sent h to arduino')
        arduino.write('h'.encode())
        time.sleep(.1)
        print('>> waiting heartbeats measurement...')
        s = arduino.readline().decode().rstrip('\r\n')
        print('Received: ', s)
        # arduino.close()
        if s == '0':
            print('@ Heart sensor not working!!')
            # arduino.close()
            return '-I-'
        elif s == '2':
            call += 1
            print('@ Patient can not use heart beat sensor [{}]'.format(call))
            if call == 3:
                # >> print('Please ask staff for help') <<
                # arduino.close()
                return '-skipped-'
            else:
                # arduino.close()!!
                return get_heart_beats(call)

        elif s.startswith("10Ok01"):
            print('Heart beat value: ', s[6:])
            # arduino.close()
            return s[6:]

        else:
            print('@ Protocol Error!!')
            # arduino.close()
            return '-PE-'

    elif not chk:
        return '-MI-'

    else:
        assert 0 != 0, 'Fatal error!!'

    # End demo2


def get_temperature(call=0):
    # print("\n*...Tell Patient How To Use Temperature Sensor...*")

    """
            *get Temperature*
            *from Ibrahim*
    """

    # Demo2
    try:
        arduino = serial.Serial('COM5', '9600', timeout=2)
        print('>> Serial port opened')
        time.sleep(2)
        chk = True
    except serial.serialutil.SerialException:
        print('@ Can not open serial communication with Ibrahim')
        arduino = None
        chk = False

    if chk:

        count = 0                                     # used to count num of received values

        print('>> sent t to arduino')
        arduino.write('t'.encode())
        time.sleep(.1)

        while 1:
            # print('sent t to arduino')
            # arduino.write('t'.encode())
            # time.sleep(.1)
            s = arduino.readline().decode().rstrip('\r\n')

            if s == '0':
                print('Received: ', s)
                print('@ Temperature sensor not working!!')
                # arduino.close()
                return '-I-'

            elif s == '2':
                call += 1
                print('Received: ', s)
                print('@ Patient can not use temp sensor [{}]'.format(call))
                if call == 3:
                    # >> print('Please ask staff for help') <<
                    # arduino.close()
                    return '-skipped-'
                else:
                    # count = 0             # we must reset count
                    continue
                    # arduino.close()!!
                    return get_temperature(call)

            elif s.startswith("10Ok01"):
                curr = s[6:]
                if curr.startswith('150'):
                    return curr[3:]
                else:
                    count += 1
                    print('Temp num[{}] : '.format(count), curr)
                    if count > 150:
                        print(
                            '@ Error: received more than 150 temperature values, and it is supposed to receive only 150 values!!')
                        return '-T-'

            else:
                print('@ Protocol Error!!')
                return '-PE-'

    elif not chk:
        return '-MI-'

    else:
        assert 0 != 0, 'Fatal error!!'

    # End demo2


def get_pressure(call=0):

    # Demo2
    try:
        arduino = serial.Serial('COM5', '9600', timeout=45)
        print('>> Serial port opened')
        time.sleep(2)
        chk = True
    except serial.serialutil.SerialException:
        print('@ Can not open serial communication with Ibrahim')
        arduino = None
        chk = False

    if chk:
        print('>> sent p to arduino')
        arduino.write('p'.encode())
        time.sleep(.1)
        print('>> waiting pressure measurement...')
        s = arduino.readline().decode().rstrip('\r\n')
        print('Received: ', s)
        # arduino.close()
        if s == '0':
            print('@ Pressure sensor not working!!')
            # arduino.close()
            return '-I-'
        elif s == '2':
            call += 1
            print('@ Patient can not use pressure sensor [{}]'.format(call))
            if call == 3:
                # >> print('Please ask staff for help') <<
                # arduino.close()
                return '-skipped-'
            else:
                # arduino.close()!!
                return get_pressure(call)

        elif s.startswith("10Ok01"):
            print('High Pressure value: ', s[6:9])
            print('Low Pressure value: ', s[9:12])

            high = s[6:9]
            low  = s[9:12]
            # arduino.close()
            return ['DONE', high, low]

        else:
            print('@ Protocol Error!!')
            # arduino.close()
            return '-PE-'

    elif not chk:
        return '-MI-'

    else:
        assert 0 != 0, 'Fatal error!!'

    # End demo2



# NOT USED IN CURRENT CODE STRUCTURE
def get_metrics(pa):
    pa.Heart_Beats = get_heart_beats()
    pa.Temperature = get_temperature()
    pa.Pressure = get_pressure()
    return pa





# Interface with DB
def get_patient_data_from_db(ID):

    """

    Get Patient Info From Database; If Exist

    :param ID:
    :return:
    """

    return ['Patient Name', 'Patient ID', 'Patient Address', 'Patient Mobile', 'Patient Birth_Date']
def get_visitor_data_from_db(ID):
    """

    Get Visitor Info From Database; If Exist

    :param ID:
    :return:
    """

    return ['Visitor Name', 'Visitor ID', 'Visitor Address', 'Visitor Mobile', 'Visitor Birth_Date']




def save_patient_data_into_db(lst_ptnt):

    """

    :param lst_ptnt:
    :return:
    """



    '''
                ###################################################################################
                #                                [DATABASE]                                       #        #
                ###################################################################################

                # INSERT PATIENT DATA INTO DATABASE
                sql =   """
                            INSERT INTO patient (Name, ID, Address, Mobile, Birth_Date) VALUES (%s, %s, %s, %s, %s)
                        """

                val = (last_patient.Name, last_patient.ID, last_patient.Addr, last_patient.Phone, last_patient.Birth_Date)
                cursor.execute(sql, val)
                conn.commit()

                ###################################################################################
                #                                [END] [DATABASE]                                 #             #
                ###################################################################################
    '''
def save_visitor_data_into_db(lst_vstr):

    """

    :param lst_vstr:
    :return:
    """

    '''
                ###################################################################################
                #                                [DATABASE]                                       #        #
                ###################################################################################

                # INSERT VISITOR DATA INTO DATABASE
                sql =   """
                                INSERT INTO visitor (Name, ID, Address, Mobile, Birth_Date) VALUES (%s, %s, %s, %s, %s)
                        """
                val = (last_visitor.Name, last_visitor.ID, last_visitor.Addr, last_visitor.Phone, last_visitor.Birth_Date)
                cursor.execute(sql, val)
                conn.commit()

                ###################################################################################
                #                                [END] [DATABASE]                                 #             #
                ###################################################################################
    '''



def update_patient_address_into_db(ptnt_addr):
    ''
def update_patient_mobile_into_db(ptnt_mob):
    ''


def update_visitor_address_into_db(vstr_addr):
    ''
def update_visitor_mobile_into_db(vstr_mob):
    ''



def get_department_location(dprt):
    ''

    return ''




def search_by_name():
    ptn = input("Enter patient name: ")

    '''
            *search in database for ptn*
            *from DB*
    '''

    # Demo
    print('Now Robo will send *search_by_name* request to the Database with name = "{}"'.format(ptn))
    time.sleep(3)
    print('The Database is supposed to send back response{[Patient_Info] or NOT_FOUND} ')
    time.sleep(3)
    print('Robo will Extract "{}" location from Info he get from DB\n\n'.format(ptn))
    time.sleep(5)
    # End demo

    return '{}_room'.format(ptn)  # *destination*
def search_by_room():
    room = input("Enter room number:  ")

    '''
            *search in database for room*
            *from DB*
    '''

    # Demo
    print('Now, Robo will send *search_by_room* request to the Database with room_num = "{}"'.format(room))
    time.sleep(5)
    print('The Database is supposed to send back response{[Patient_Info] or NO_SUCH_ROOM} ')
    time.sleep(5)
    print('Robo will Extract room_num "{}" location from Info he get from DB\n\n'.format(room))
    time.sleep(5)
    # End demo

    return 'room number {}'.format(room)  # *destination*




# Interface with Khalid
def set_destination(destination):
    """
            *send Destination*
            *to Khalid*
    """

    # Demo

    print('\nNow, Robo is sending destination to Khalid')
    # time.sleep(.1)
    print('Khalid supposed to send acknowledgment back and move Robo to  "{}"'.format(destination))
    # time.sleep(.1)
    # End demo

    return 'ACK'  # *acknowledgment*
def go_home():
    set_destination('''*Home*''')
def is_destination(destination):
    """
            *get Current_Location*
            *from Khalid*
    """

    # Demo
    time.sleep(1)
    print('\nNow, Robo is asking Khalid for Current_Location every while')
    time.sleep(3)
    print('Khalid is supposed to send Current_Location every while')
    time.sleep(3)
    print('When Current_Location is same as "{}"'.format(destination), ' Robo will Stop')
    time.sleep(5)
    # End demo

    return True  # *true or false*
def is_home():
    check = is_destination('''*Home*''')
    return check


#############################################################################
#############################################################################


# Helper Functions
def space_count(lis):
    count = 0
    for i in lis:
        if i == ' ':
            count += 1
    # print('count:', count)
    return count


class StyleSheets:
    def __init__(self):
        self.btn_next = """
                                    .QPushButton{
                                        background-color: #BCACEC;
                                        font: 16px;
                                        color:  ;
                                        border-radius: 4px;
                                    }

                                    .QPushButton:hover {
                                            background-color: #0CACEC;
                                            color: white;
                                    }

                                    .QPushButton:pressed {
                                            border-style: inset;
                                            padding-right: 5px;
                                            background-color: red;
                                    }


                        """

        self.btn_search = """
                                    .QPushButton{
                                            background-color: #F16A70;
                                            font: 16px;
                                            color:  ;
                                            border: 1px solid #F16A70;
                                            border-radius: 15px
                                    }

                                    .QPushButton:hover {
                                            background-color: ;
                                            color: white;
                                    }

                                    .QPushButton:pressed {
                                            border-style: inset;
                                            padding-left: 5px;
                                            background-color: red;
                                    }


                            """




#############################################################################
#############################################################################











########################################################################################
# الكام سطر الجايين دول عظمة على عظمة
########################################################################################

'''
                    TO DO
                    -----
        [1]     Wrap it in a function, so you can reuse it easily

'''

# بدل ما يطلعلك كده
'Process finished with exit code -1073740791 (0xC0000409)'
# الكام سطر ده بيخلي ال pyqt تطلع exceptions
# stackoverflow link: https://stackoverflow.com/questions/34363552/python-process-finished-with-exit-code-1-when-using-pycharm-and-pyqt5/37837374#


sys._excepthook = sys.excepthook
def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)
# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


##########################################################################################
#                                   END الكام سطر                                        #
##########################################################################################











def test_without_restrictions_1(self):
    formal_date = self.combo_year.currentText() + '-' + self.month_n + '-' + self.combo_day.currentText()

    self.w.hide()
    self.cnfMSG = ConfirmationForm_Not_Exist(self, self.input_name.text(), self.input_id.text(), self.input_add.text(), self.input_moile.text(), formal_date)


if __name__ == '__main__':

    if DATABASE:
        " THIS CONNECTION NEEDED TO BE IN A THREAD "
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ZU_DB"
        )

        cursor = conn.cursor()

    app = QtWidgets.QApplication(sys.argv)
    Root()
    sys.exit(app.exec_())
