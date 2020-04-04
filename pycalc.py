import sys
import PyQt5
#import QApplications and the required widgets from 
#PyQt5.QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt
from functools import partial


ERROR_MSG = 'ERROR'

def evaluateExpression(expression):
        #Evaluate an expression
        try:
            result = str(eval(expression, {}, {}))
        except Exception:
            result = ERROR_MSG

        return result

#create a subclass of QMainWindow to setup the calculators GUI
class pyCalcUi(QMainWindow):
    #pycalc's View (GUI).
    def __init__ (self):
        super().__init__()
        
        #set some main window's properties
        self.setWindowTitle('Scientific Calculator')
        self.setFixedSize(250,250)

        #set the central widget
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        #create the display and the buttons
        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        #Create the Display widget
        self.display = QLineEdit()

        #set some display's properties
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        #Add the display to the general layout
        self.generalLayout.addWidget(self.display)
        
    def _createButtons(self):
        #Create the buttons
        self.buttons = {}
        buttonsLayout = QGridLayout()

        #Buttons text | position on the QGridLayout
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                  }

        #Create the buttons and add them to the grid layout
        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText],pos[0], pos[1])

            #Add buttonsLayout to the general layout
            self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        #Set display's text
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        #Get display's text
        return self.display.text()

    def clearDisplay(self):
        #Clears the display
        self.setDisplayText('')


#Create a controller class to connect the GUI and the model
class pyCalcCtrl:
    def __init__(self, model, view):
        #Controller Initializer
        self._evaluate = model
        self.view = view

        #connect signals and slots
        self._connectSignals()
    
    def _calculateResult(self):
        #Evaluates expressions
        result = self. _evaluate(expression=self.view.displayText())
        self.view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        #Build Expression
        if self.view.displayText() == ERROR_MSG:
            self.view.clearDisplay()

        expression = self.view.displayText() + sub_exp
        self.view.setDisplayText(expression)
    
    def _connectSignals(self):
        #Connects signals and slots
        for btnText, btn in self.view.buttons.items():
            if btnText not in {'=','C'}:
                btn.clicked.connect(partial(self._buildExpression, btnText))

        self.view.buttons['='].clicked.connect(self._calculateResult)
        self.view.display.returnPressed.connect(self._calculateResult)
        self.view.buttons['C'].clicked.connect(self.view.clearDisplay)



#Client code
def main():
    #Main function

    #Create an instance of QApplication
    pycalc = QApplication(sys.argv)

    #show the calculator's GUI
    view = pyCalcUi()
    view.show()

    #Create instances of the model and the controller
    model = evaluateExpression
    pyCalcCtrl(model=model, view=view)

    #Execute the calculator's main loop
    sys.exit(pycalc.exec_())


if __name__ == '__main__':
    main()
