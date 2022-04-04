import random
from pprint import pprint

from PyQt5 import QtWidgets, uic
import APIHandler
import html


class Ui(QtWidgets.QMainWindow):
    questionList = []

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('MainWindow.ui', self)
        self.categories.addItem("None")
        self.bg_style.buttonClicked.connect(self.styleChange)
        for obj in APIHandler.get_categories():
            self.categories.addItem(obj['name'])
        self.getQuestionsLinkButton.clicked.connect(self.fetchquestions)
        self.questionTable.clicked.connect(self.questionSelector)
        self.qs_millionaire.setEnabled(False)  # gotta work this one out
        self.show()

    def fetchquestions(self):
        a = self.amount.value()
        c = None if self.categories.currentIndex() == 0 \
            else self.categories.currentIndex() + 8
        d = None if self.bg_diff.checkedButton().text() == "Any" \
            else self.bg_diff.checkedButton().text().lower()
        t = None if self.bg_type.checkedButton().text() == "Any" \
            else "multiple" if self.bg_type.checkedButton().text() == "Multiple" \
            else "boolean"
        self.questionList = []
        for question in APIHandler.get_questions(a, c, d, t):
            question['userAnswer'] = None
            self.questionList.append(question)
        self.addQuestionstoTable()

    def addQuestionstoTable(self):
        self.questionTable.setRowCount(0)
        self.questionTable.setRowCount(len(self.questionList))
        for idx in range(self.questionList.__len__()):
            self.questionTable.setItem(idx, 0, QtWidgets.QTableWidgetItem(self.questionList[idx]['category']))
            self.questionTable.setItem(idx, 1, QtWidgets.QTableWidgetItem(self.questionList[idx]['difficulty']))
            self.questionTable.setItem(idx, 2, QtWidgets.QTableWidgetItem(self.questionList[idx]['type']))
            self.questionTable.setItem(idx, 3, QtWidgets.QTableWidgetItem(""))
            pprint(self.questionList[idx])

    def styleChange(self):
        style = self.bg_style.checkedButton().text().lower()
        print(style)
        if style == "random":
            self.categories.setCurrentIndex(0)
            self.categories.setEnabled(False)
            self.qt_any.setChecked(True)
            self.qd_any.setChecked(True)
            for rb1 in self.bg_type.buttons():
                rb1.setEnabled(False)
            for rb2 in self.bg_diff.buttons():
                rb2.setEnabled(False)
        elif style == "custom":
            self.categories.setEnabled(True)
            for rb1 in self.bg_type.buttons():
                rb1.setEnabled(True)
            for rb2 in self.bg_diff.buttons():
                rb2.setEnabled(True)

    def questionSelector(self, item):
        answerpool = []
        self.selectedQuestion.setText(html.unescape(self.questionList[item.row()]['question']))
        for wrong in self.questionList[item.row()]['incorrect_answers']:
            answerpool.append(wrong)
        answerpool.append(self.questionList[item.row()]['correct_answer'])
        random.shuffle(answerpool)
        hbox = QtWidgets.QHBoxLayout()
        self.answerBox.setLayout(hbox)
        for i in reversed(range(self.answerBox.layout().count())):
            self.answerBox.layout().itemAt(i).widget().deleteLater()
        for answer in answerpool:
            button = QtWidgets.QPushButton(html.unescape(answer))
            if self.questionTable.item(item.row(), 3).text() != "":
                button.setEnabled(False)
            if answer == self.questionList[item.row()]['userAnswer']:
                if answer == self.questionList[item.row()]['correct_answer']:
                    button.setStyleSheet("background-color: #00ff00")
                else:
                    button.setStyleSheet("background-color: #ff0000")
            button.clicked.connect(self.answerCheck)
            self.answerBox.layout().addWidget(button)
            self.answerBox.update()


    def answerCheck(self):
        userAnswer = self.sender().text()
        self.questionList[self.questionTable.currentRow()]['userAnswer'] = userAnswer
        correctAnswer = self.questionList[self.questionTable.currentRow()]['correct_answer']
        print("Answer: ", userAnswer)
        print("Correct: ", correctAnswer)
        if userAnswer == correctAnswer:
            print("Correct!")
            self.sender().setStyleSheet("background-color: #00FF00")
            self.questionTable.setItem(self.questionTable.currentRow(), 3, QtWidgets.QTableWidgetItem("Correct"))
        else:
            print("Incorrect!")
            self.sender().setStyleSheet("background-color: #FF0000")
            self.questionTable.setItem(self.questionTable.currentRow(), 3, QtWidgets.QTableWidgetItem("Incorrect"))
        for i in reversed(range(self.answerBox.layout().count())):
            self.answerBox.layout().itemAt(i).widget().setEnabled(False)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()  # show window
    sys.exit(app.exec_())
