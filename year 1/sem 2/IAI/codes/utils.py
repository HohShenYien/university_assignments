# This Python file uses the following encoding: utf-8
from PyQt5.QtCore import QObject, Qt, QEvent
from PyQt5.QtGui import QCursor, QFont, QIcon, QPixmap
from PyQt5.QtWidgets import QLabel, QPlainTextEdit, QPushButton, QScrollArea, QWidget, QHBoxLayout
from PyQt5.QtTest import QTest

from itertools import chain

import rsc
import scan_symptom
import ai

def get_knowledge():
    # This function will read all the knowledge into dictionaries
    symptom_nutrient = {}
    symptom_avoid = {}
    nutrient_food = {}
    with open("symptoms-to_eat.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            symptoms = tmp[0].split("/")
            nutrients = tmp[1].split("/")
            for symptom in symptoms:
                if symptom in ["AIDS", "HIV"]:
                    # special case
                    symptom_nutrient[symptom] = (symptom, nutrients)
                    continue
                # Process the symptom name
                symptom_nutrient[scan_symptom.lemmatize(symptom.lower())] = (symptom, nutrients)

    with open("symptoms-not_to_eat.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            symptoms = tmp[0].split("/")
            food = tmp[1].split("/")
            for symptom in symptoms:
                if symptom in ["AIDS", "HIV"]:
                    # special case
                    symptom_avoid[symptom] = (symptom, food)
                    continue
                # Process the symptom name
                symptom_avoid[scan_symptom.lemmatize(symptom.lower())] = (symptom, food)

    with open("nutrient-food.txt", "r") as file:
        for line in file.readlines():
            tmp = line.strip().split("|")
            nutrients = tmp[0].split("/")
            food = tmp[1].split("/")
            for nutrient in nutrients:
                # Process the symptom name
                nutrient_food[nutrient] = food
    
    return symptom_nutrient, symptom_avoid, nutrient_food

class Chat():
    """
    # This class will help to implement all GUI chatting functionalities
    """
    def __init__(self, widget, layout):
        self.robot = QPixmap(":/img/robot.png") # Load this image as icon
        self.widget = widget
        self.layout = layout

        # Getting widgets from UI
        self.scrollArea = widget.findChild(QScrollArea, "scrollArea")
        scrollBar = self.scrollArea.verticalScrollBar()
        scrollBar.rangeChanged.connect(self.scrollDown)
        self.chatbox = widget.findChild(QPlainTextEdit, "chatbox")
        self.textBtn = widget.findChild(QPushButton, "submitTextBtn")
        self.textBtn.setIcon(QIcon(":/img/sendIcon.png"))
        self.textBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.textBtn.clicked.connect(self.receiveMessage)

        self.font = QFont("Arial", 12) # Arial size 12 will be the fonts used
        self.sendMessage("Hello world")
        self.sendMessage("I am NutriBot, your friendly personal nutrient advisor!")
        self.sendMessage("You may ask me what to eat or not to eat if you are facing a disease or a symptom.")
        self.sendMessage("However, I am not that intelligent, I would appreciate if you will state your question in full like 'What should I eat if I have diabetes?'")
        self.model = ai.train()
        self.symptom_nutrient, self.symptom_avoid, self.nutrient_food = get_knowledge()

        self.waiting = False # indicates if the chatbot is waiting for options

    def sendMessage(self, message):
        # This display a message sent by the chatbot
        # First create a horizontal layout and fit robot icon and text into it
        horizontalLayout = QHBoxLayout()

        img = QLabel()
        img.setPixmap(self.robot)
        horizontalLayout.addWidget(img)

        chat = self.createChat(message)
        chat.setStyleSheet("""
        QLabel {
            padding:5px;
            background-color: #fff;
            border-radius:10px;
            min-width: 300px;
            }
        """)
        horizontalLayout.addWidget(chat)

        horizontalLayout.setAlignment(Qt.AlignLeft) # Not centre, but left
        self.layout.addLayout(horizontalLayout)

    def receiveMessage(self, text = ""):
        # This function will receive chat message from user
        # Display it, and chatbot will respond accordingly
        horizontalLayout = QHBoxLayout()
        if text == "":
            text = self.chatbox.toPlainText()

        if text == "":
            # Not going to display anything when blank
            return
        elif text == False:
            text = "No"
        chat = self.createChat(text)
        chat.setStyleSheet("""
        QLabel {
            padding:5px;
            background-color: #98FB98;
            border-radius:10px;
            min-width: 350px;
            }
        """)
        horizontalLayout.addWidget(chat)
        horizontalLayout.setAlignment(Qt.AlignRight) # Not centre, but right
        self.layout.addLayout(horizontalLayout)

        self.chatbox.setPlainText("")
        if self.waiting:
            # Already gotten tag from user
            if text == "No":
                # Do nothing
                self.sendMessage("I am sorry, can you restate your question again?")
            else:
                self.respond([text], self.tag)
            # Resets the variable
            self.waiting = False
            self.chatbox.setReadOnly(False)
            self.chatbox.setStyleSheet("QPlainTextEdit {background-color: #FFFFFF;}")
            self.curryFunction("", self.tmp)() # Clears the options
            return

        tag, response = ai.predict(self.model, text)
        # 5 and 6 are food to eat and food to avoid respectively
        if int(tag) < 5:
            self.sendMessage(response)
        else:
            self.scan_nutrient(text, int(tag))


    def options(self, opts:'list[str]'):
        """
        # This is a function that create multiple buttons to send to the chatbot
        # It will first create a horizontal layout, and populate it with buttons
        # And add the layout into the main window
        # Also connected some functions to the buttons
        """
        horizontalLayout = QHBoxLayout()
        self.tmp = []
        for message in opts:
            self.tmp.append(QPushButton(message))
            self.tmp[-1].setStyleSheet("""
            QPushButton {padding:5px;
            background-color: #98FB98;
            border-radius:12px;
            min-height:40px;}
            """)
            self.tmp[-1].setCursor(QCursor(Qt.PointingHandCursor))

        for i in range(len(opts)):
            horizontalLayout.addWidget(self.tmp[i])
            tmpFunc = self.curryFunction(opts[i], self.tmp)
            self.tmp[i].clicked.connect(tmpFunc)
        
        self.layout.addLayout(horizontalLayout)


    def createChat(self, message):
        """
        # A helper function that returns a QLabel object with certain style
        # And properties
        """
        chat = QLabel(message)
        chat.setWordWrap(True) # New line when too long
        chat.setTextInteractionFlags(Qt.TextSelectableByMouse) # Can be highlighted
        chat.setCursor(QCursor(Qt.IBeamCursor))
        chat.setFont(self.font)
        return chat

    def scrollDown(self):
        # A simple helper function to scroll to the bottom of the window
        target = self.scrollArea.verticalScrollBar().maximum()
        self.scrollArea.verticalScrollBar().setValue(target)

    def curryFunction(self, message, targets):
        # A curry function that helps for option function
        def clicked():
            try:
                self.clearAll(targets)
            except:
                pass
            self.receiveMessage(message)
                            
        return clicked

    def clearAll(self, targets:'list[QWidget]'):
        # This function will remove all the widgets in targets from
        # the app
        for widget in targets:
            widget.deleteLater()

    def possible(self, options, tag):
        # This function will start creating options for user
        # Doesn't allow user to write anything for now
        self.waiting = True
        self.tag = tag
        self.chatbox.setReadOnly(True)
        self.chatbox.setStyleSheet("QPlainTextEdit {background-color: #C0C0C0;}")
        # letting user to type no
        self.chatbox.setPlainText("No") 
        self.sendMessage("I don't quite get it, did you mean any of the following?")
        self.options(options)

    def respond(self, keys:'list[symptoms]', tag):
        self.chatbox.setReadOnly(True) # Don't let user inputs anything for now
        self.chatbox.setStyleSheet("QPlainTextEdit {background-color: #C0C0C0;}")
        if tag == 5:
            # This is for symptoms to food to eat
            for key in keys:
                nutrients = self.symptom_nutrient[key]
                self.sendMessage(f"For your {nutrients[0]}, you should consider consuming more: ")
                QTest.qWait(500)
                for ind, nutrient in enumerate(nutrients[1]):
                    self.sendMessage(f"{ind + 1}. {nutrient}")
                    food = ", ".join(self.nutrient_food[nutrient])
                    self.sendMessage(f"This includes food like {food}.")
                    QTest.qWait(3000)

        elif tag == 6:
            for key in keys:
                oriSymptom = self.symptom_avoid[key][0]
                food = ", ".join(self.symptom_avoid[key][1])
                self.sendMessage(f"For your {oriSymptom}, you should consider avoiding the following food:")
                QTest.qWait(500)
                self.sendMessage(f"{food}.")
                QTest.qWait(3000)

        self.sendMessage("Any other question?")
        self.chatbox.setReadOnly(False)
        self.chatbox.setStyleSheet("QPlainTextEdit {background-color: #FFF;}")

    def scan_nutrient(self, message, tag):
        res = []
        if tag == 5:
            possibleSet, rootWordSet, synonymSymptomsDict, correctionDict = scan_symptom.scan(message,
                                                            self.symptom_nutrient)
        elif tag == 6:
            possibleSet, rootWordSet, synonymSymptomsDict, correctionDict = scan_symptom.scan(message,
                                                            self.symptom_avoid)
        for symptom in possibleSet:
            if tag == 5:
                if scan_symptom.lemmatize(symptom) in self.symptom_nutrient:
                    res.append(scan_symptom.lemmatize(symptom))
            elif tag == 6:
                if scan_symptom.lemmatize(symptom) in self.symptom_avoid:
                    res.append(scan_symptom.lemmatize(symptom))
        if not res:
            # If res is empty
            for symptom in rootWordSet:
                if tag == 5:
                    if scan_symptom.lemmatize(symptom) in self.symptom_nutrient:
                        res.append(scan_symptom.lemmatize(symptom))
                elif tag == 5:
                    if scan_symptom.lemmatize(symptom) in self.symptom_avoid:
                        res.append(scan_symptom.lemmatize(symptom))

        if not res:
            if not synonymSymptomsDict:
                self.sendMessage("I am sorry, can you restate your question again?")
            else:
                self.possible(list(chain(*synonymSymptomsDict.values()))[:3], tag)

        else:
            self.respond(res, tag)