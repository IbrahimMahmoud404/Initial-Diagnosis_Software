from PyQt5 import QtWidgets, QtGui, QtCore
import sys

# DIAGNOSE PART
import speech_recognition as sr
import operator
import re
import _thread
from playsound import playsound
import threading


dep = [0] * 13          #separtment array of values
depart = ["Abdomen", "Heart", "Surgery", "Bones", "Teeth", "Therapy", "Psycho",
          "Nerve", "Chest", "Nose", "Eyes", "Skin", "Stomach"]

GLOBAL_TEXT = 0
GLOBAL_INSTANCE = None


# Timer Interrupt
def do_you_heard_me_timer():
    global GLOBAL_TEXT

    t = threading.Timer(1.0, do_you_heard_me_timer)
    t.setDaemon(True)
    t.start()

    # print('> ',GLOBAL_TEXT)

    if GLOBAL_TEXT == 0:
        pass
    else:
        txt = GLOBAL_TEXT
        GLOBAL_TEXT = 0
        dprt = get_body_part(txt)

        # print('dprt:                     @@@@@@@: ', dprt)

        t.cancel()
        diagnose(dprt)


def diagnose(dprt):
    global GLOBAL_TEXT
    global GLOBAL_INSTANCE

    if dprt == "1":

        do_you_heard_me_timer()

        playsound('sound/notunderstand.mp3')

        playsound('sound/pain.mp3')

        # _thread.start_new_thread(respond, (GLOBAL_INSTANCE, ''))
        respond(GLOBAL_INSTANCE, '')


    elif dprt == 'head_part':

        playsound('sound/complain.mp3')

        txt = respond(GLOBAL_INSTANCE, '')

        print(txt)
        dprt = head(txt, '')

        #
        print('Go to {} department'.format(dprt))


    else:

        print('Go to {} department'.format(dprt))


def search_head(cmplnt):

    eye = open("ai/head_eye.txt", "r")                     #open the keywords file
    file_contents = eye.read()                          # read the whole file content
    for i in file_contents.split('\n'):                 #loop for every word in the file
        pattern = re.compile(i)                         #compile the word to a regex
        for match in re.finditer(pattern, cmplnt):         #search in the text
            dep[10] += 4                                # gain points


    nose = open("ai/head_nose.txt", "r")
    file_contents = nose.read()
    for i in file_contents.split('\n'):
        pattern = re.compile(i)
        for match in re.finditer(pattern, cmplnt):
            dep[9] += 4


    nerve = open("ai/head_nerve.txt", "r")
    file_contents = nerve.read()
    for i in file_contents.split('\n'):
        pattern = re.compile(i)
        for match in re.finditer(pattern, cmplnt):
            dep[7] += 4


    teeth = open("ai/head_teeth.txt", "r")
    file_contents = teeth.read()
    for i in file_contents.split('\n'):
        pattern = re.compile(i)
        for match in re.finditer(pattern, cmplnt):
            dep[4] += 4


    Skin = open("ai/head_skin.txt", "r")
    file_contents = Skin.read()
    for i in file_contents.split('\n'):
        pattern = re.compile(i)
        for match in re.finditer(pattern, cmplnt):
            dep[11] += 4


    Bones = open("ai/head_bones.txt", "r")
    file_contents = Bones.read()
    for i in file_contents.split('\n'):
        pattern = re.compile(i)
        for match in re.finditer(pattern, cmplnt):
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
    global GLOBAL_INSTANCE

    search_head(f)


    # zero equal
    while(max(dep) == 0):
        playsound('sound/details.mp3')

        f = respond(GLOBAL_INSTANCE, '')
        print(f)
        print(f)
        search_head(f)



    while max_equality() == 1:

        # speak("مزيدٌ مِنَ التفاصيل لو سمحت", '')

        playsound('sound/details.mp3')

        f = respond(GLOBAL_INSTANCE, '')
        print(f)
        print(f)
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
    global GLOBAL_TEXT

    r = sr.Recognizer()                     #taking object from SpeechRecognition


    with sr.Microphone() as source:         #existing audio file as source of talk

        audio = r.listen(source, timeout= 12, phrase_time_limit=6)                #listen and save what said

        try:

            text = r.recognize_google(audio, language='ar-SA')      #transform speech to text


            print('You siad: ', text)

            GLOBAL_TEXT = text
            a.lb.setVisible(True)
            a.lb.setText(text)


        except:
            print("لم اسمعك!!")
            # speak("لم اسمعك، اعد المحاولة", '')
            playsound('sound/notunderstand.mp3')
            return respond(a, '')
    return text




def get_body_part(m):

    if "رأس" in m or "راس" in m:
        return 'head_part'
    elif "صدر" in m:
        print('Chest_dep')
        return "Chest"
    elif "بطن" in m:
        print("Abdomen_dep")
        return "Abdomen"
    elif 'قدم' in m or 'ذراع' in m or 'يد' in m or 'رجل' in m:
        print('Therapy_dep')
        return "Therapy"
    elif "ظهر" in m or "ضهر" in m:
        print("Bones_dep")
        return "Bones"
    else:

        return "1"




class PainSource:

    def __init__(self):

        global GLOBAL_INSTANCE
        GLOBAL_INSTANCE = self

        # WIDGET
        self.w = QtWidgets.QDialog()
        self.w.setModal(True)
        self.w.setWindowTitle(" ZU Hospital ")
        self.w.setWindowIcon(QtGui.QIcon('Icons/Hospital'))
        # self.w.resize(1300, 350)
        self.w.move(20, 0)
        self.w.setStyleSheet("""background-color: white;""")
        self.w.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.w.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.w.keyPressEvent = self.esc


        # LABEL
        self.lbl = QtWidgets.QLabel('CLICK ON THE MIC\n FOR DIAGNOSING', self.w)
        self.lbl.move(350, 285)
        self.lbl.setStyleSheet('color: orange; font: 60px;')
        self.lbl.setWordWrap(True)

        # LABEL
        self.lb = QtWidgets.QLabel(self.w)
        self.lb.move(30, 20)
        self.lb.resize(880, 620)
        self.lb.setStyleSheet('background: white;color: orange; font: 60px;')
        self.lb.setWordWrap(True)
        self.lb.setVisible(False)




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


        if True:
            # HIDE LABELS
            self.mlbl = QtWidgets.QLabel(self.w)
            self.mlbl.resize(60, 200)
            self.mlbl.move(980+20, 260)
            # self.mlbl.setStyleSheet('background: orange')

            self.uplbl = QtWidgets.QLabel(self.w)
            self.uplbl.resize(20, 20)
            self.uplbl.move(960+20, 285)
            # self.uplbl.setStyleSheet('background: red')

            self.dwnlbl = QtWidgets.QLabel(self.w)
            self.dwnlbl.resize(20, 20)
            self.dwnlbl.move(960+20, 420)
            # self.dwnlbl.setStyleSheet('background: red')



        # SHOW WIDGET
        self.w.showFullScreen()



    def no_click(self, e):

        self.btn_no.setEnabled(False)

        self.mlbl.setVisible(False)
        self.uplbl.setVisible(False)
        self.dwnlbl.setVisible(False)


        playsound('sound/pain.mp3')


        _thread.start_new_thread(respond, (self, 'w'))

        # new_thread = threading.Thread(target=respond, args = (self, ''))
        # new_thread.start()


    def esc(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.w.close()











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









if __name__ == '__main__':



    app = QtWidgets.QApplication(sys.argv)

    pew = PainSource()
    do_you_heard_me_timer()
    sys.exit(app.exec_())