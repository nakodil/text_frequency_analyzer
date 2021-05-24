# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(729, 594)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.message = QtWidgets.QListWidget(self.centralwidget)
        self.message.setGeometry(QtCore.QRect(10, 150, 701, 81))
        self.message.setWordWrap(True)
        self.message.setObjectName("message")
        self.show_source_select_dialog = QtWidgets.QPushButton(self.centralwidget)
        self.show_source_select_dialog.setGeometry(QtCore.QRect(10, 20, 181, 31))
        self.show_source_select_dialog.setObjectName("show_source_select_dialog")
        self.source_file_path = QtWidgets.QTextEdit(self.centralwidget)
        self.source_file_path.setGeometry(QtCore.QRect(200, 20, 511, 31))
        self.source_file_path.setObjectName("source_file_path")
        self.result = QtWidgets.QListWidget(self.centralwidget)
        self.result.setGeometry(QtCore.QRect(10, 330, 701, 201))
        self.result.setWordWrap(True)
        self.result.setObjectName("result")
        self.label_for_message = QtWidgets.QLabel(self.centralwidget)
        self.label_for_message.setGeometry(QtCore.QRect(10, 120, 172, 16))
        self.label_for_message.setObjectName("label_for_message")
        self.label_for_message_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_for_message_2.setGeometry(QtCore.QRect(10, 300, 64, 20))
        self.label_for_message_2.setObjectName("label_for_message_2")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(290, 70, 425, 22))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.word_type_verb = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.word_type_verb.setChecked(True)
        self.word_type_verb.setObjectName("word_type_verb")
        self.horizontalLayout.addWidget(self.word_type_verb)
        self.word_type_adjective = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.word_type_adjective.setObjectName("word_type_adjective")
        self.horizontalLayout.addWidget(self.word_type_adjective)
        self.word_type_noun = QtWidgets.QCheckBox(self.horizontalLayoutWidget)
        self.word_type_noun.setObjectName("word_type_noun")
        self.horizontalLayout.addWidget(self.word_type_noun)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 70, 241, 26))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_for_words_number = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label_for_words_number.setObjectName("label_for_words_number")
        self.horizontalLayout_2.addWidget(self.label_for_words_number)
        self.words_number = QtWidgets.QSpinBox(self.horizontalLayoutWidget_2)
        self.words_number.setMinimum(1)
        self.words_number.setMaximum(999)
        self.words_number.setObjectName("words_number")
        self.horizontalLayout_2.addWidget(self.words_number)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(60, 550, 591, 30))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.analyze = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.analyze.setEnabled(False)
        self.analyze.setObjectName("analyze")
        self.horizontalLayout_3.addWidget(self.analyze)
        self.save_result_to_file = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.save_result_to_file.setEnabled(False)
        self.save_result_to_file.setFlat(False)
        self.save_result_to_file.setObjectName("save_result_to_file")
        self.horizontalLayout_3.addWidget(self.save_result_to_file)
        self.make_wordcloud = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        self.make_wordcloud.setEnabled(False)
        self.make_wordcloud.setObjectName("make_wordcloud")
        self.horizontalLayout_3.addWidget(self.make_wordcloud)
        self.progress = QtWidgets.QProgressBar(self.centralwidget)
        self.progress.setGeometry(QtCore.QRect(10, 240, 701, 23))
        self.progress.setProperty("value", 0)
        self.progress.setObjectName("progress")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Частотный анализатор текста"))
        self.show_source_select_dialog.setText(_translate("MainWindow", "выбрать источник"))
        self.label_for_message.setText(_translate("MainWindow", "Ход выполнения программы:"))
        self.label_for_message_2.setText(_translate("MainWindow", "Результат:"))
        self.label.setText(_translate("MainWindow", "Части речи:"))
        self.word_type_verb.setText(_translate("MainWindow", "глаголы"))
        self.word_type_adjective.setText(_translate("MainWindow", "прилагательные"))
        self.word_type_noun.setText(_translate("MainWindow", "существительные"))
        self.label_for_words_number.setText(_translate("MainWindow", "Количество слов в результате:"))
        self.analyze.setText(_translate("MainWindow", "анализировать источник"))
        self.save_result_to_file.setText(_translate("MainWindow", "сохранить результат в файл"))
        self.make_wordcloud.setText(_translate("MainWindow", "сохранить облако слов"))
