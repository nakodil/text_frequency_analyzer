import re
import sys
import time
import pymorphy2  # pip install pymorphy2
from collections import Counter
from PyQt5.QtWidgets import QFileDialog  # pip install pyside2
from PyQt5 import QtTest  # pip install pyside2
from interface import *


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()


def show_source_select_dialog():
    """
    Показывает диалог выбора файла.
    Сохраняет выбранный файл в source_file_path.
    """
    source_file_path = QFileDialog.getOpenFileName(filter="*.txt")
    ui.source_file_path.setText(source_file_path[0])


def check_source_file_path():
    """
    Проверяет выбранный путь до файла-источника.
    Если путь введен, активирует кнопку «Анализировать источник».
    Если путь пустой, блокирует кнопку «Анализировать источник».
    TODO: валидация типа файла
    """
    source_file_path = ui.source_file_path.toPlainText()
    if source_file_path:
        ui.analyze.setEnabled(True)
    else:
        ui.analyze.setEnabled(False)


def interface_is_active(condition: bool):
    """
    Активирует/блокирует интерфейс:
    кнопку «Выбрать источник»
    поле выбора пути до файла-источника текста
    кнопку «Анализировать источник»
    виджет «Количество слов в результате»
    виджет «Часть речи»
    """
    ui.analyze.setEnabled(condition)
    ui.source_file_path.setEnabled(condition)
    ui.show_source_select_dialog.setEnabled(condition)
    ui.save_result_to_file.setEnabled(condition)
    ui.words_number.setEnabled(condition)


def get_text_str() -> str:
    """
    Открывает файл и забирает содержимое в строку.
    """
    source_file_path = ui.source_file_path.toPlainText()
    source_file = open(source_file_path, "r", encoding="utf-8")
    text_str = source_file.read()
    source_file.close()
    return text_str


def get_word_type() -> list:
    """
    Создает список и добавляет в него части речи из виджета «Части речи»
    """
    word_type_list = []
    if ui.word_type_verb.isChecked():
        word_type_list.append("VERB")
    if ui.word_type_adjective.isChecked():
        word_type_list.append("ADJF")
        word_type_list.append("ADJS")
    if ui.word_type_noun.isChecked():
        word_type_list.append("NOUN")
    return word_type_list


def prepare_text(text_str: str) -> list:
    """
    Делает все буквы строчными.
    Заменяет букву «ё» на «е».
    Разбирает текст на слова и делает из них список.
    """
    text_str = text_str.lower()
    text_str = re.sub("ё", "е", text_str)
    text_list = re.findall(r"[а-я]+", text_str)
    return text_list


def morph_analyze_text(text_list: list, word_type_list: list) -> list:
    """
    Проходит по всем словам в списке.
    Добавляет все существительные в нормальной форме в новый список.
    TODO: брать парсы с максимальным score
    """
    normal_list = []
    morph = pymorphy2.MorphAnalyzer()

    for word in text_list:
        p = morph.parse(word)[0]
        if "NOUN" in word_type_list:
            if "NOUN" in p.tag:
                normal_list.append(p.normal_form)
        if "VERB" in word_type_list:
            if "VERB" in p.tag:
                normal_list.append(p.normal_form)
        if "ADJF" in word_type_list or "ADJS" in word_type_list:
            if "ADJF" in p.tag or "ADJS" in p.tag:
                normal_list.append(p.normal_form)

    return normal_list


def count_words(normal_list: list) -> dict:
    """
    Считает повторы слов.
    Записывает результат в словарь по убыванию повторов в виде
    слово : количество
    Количество пар в словаре зависит от выбранного пользователем в пункте
    «Количество слов в результате»
    """
    result_dict = dict(
        Counter(normal_list).most_common(ui.words_number.value())
    )
    return result_dict


def result_to_widget(result_dict: dict):
    """
    Записывает пары словаря построчно по убыванию в виджет «Результат»
    """
    for key, value in result_dict.items():
        result_item = f"{key} : {value}\n"
        ui.result.addItem(result_item)


def save_result_to_file():
    """
    Сохраняет содержимое виджета «Результат» в выбранный файл.
    Выдает сообщение в виджет «Ход выполнения программы».
    """
    destination_file = QFileDialog.getOpenFileName(filter="*.txt")
    destination_file_path = destination_file[0]

    with open(destination_file_path, "w", encoding="utf-8") as file:
        for i in range(ui.result.count()):
            line = ui.result.item(i).text()
            file.write(line)

    ui.message.addItem(f"Результат сохранен в {destination_file_path}")


def main():
    """
    Основная функция. Выполняет программу последовательно,
    если удалось получить текстовое содержимое из файла.
    PYQT не обновит интерфейс, пока не завершится функция main().
    Для изменения интерфейса в ходе выполнения функции main()
    используется прерывание на время с помощью QtTest.QTest.qWait(1)
    """
    start_time = time.time()
    word_type_list = get_word_type()
    interface_is_active(False)
    ui.message.clear()
    ui.result.clear()
    ui.message.addItem(f"Идет анализ текста. Пожалуйста, подождите!")
    QtTest.QTest.qWait(1)

    try:
        text_str = get_text_str()
    except Exception as e:
        ui.message.addItem(
            f"Не удалось прочитать текст из файла! "
            f"Проверьте путь!"
        )
        ui.source_file_path.setEnabled(True)
        ui.show_source_select_dialog.setEnabled(True)
        ui.words_number.setEnabled(True)
        return None
        QtTest.QTest.qWait(1)

    if word_type_list:
        text_list = prepare_text(text_str)
        normal_list = morph_analyze_text(text_list, word_type_list)
        result_dict = count_words(normal_list)
        result_to_widget(result_dict)
        end_time = round(time.time() - start_time, 2)
        ui.message.addItem(f"Анализ завершен за {end_time} секунд")
        interface_is_active(True)
        ui.save_result_to_file.setEnabled(True)
        QtTest.QTest.qWait(1)

    else:
        ui.message.addItem(f"Части речи не выбраны, анализ невозможен!")
        ui.source_file_path.setEnabled(True)
        ui.show_source_select_dialog.setEnabled(True)
        ui.words_number.setEnabled(True)
        return None
        QtTest.QTest.qWait(1)


# привязка сигналов к событиям элементов интерфейса
ui.show_source_select_dialog.clicked.connect(show_source_select_dialog)
ui.save_result_to_file.clicked.connect(save_result_to_file)
ui.source_file_path.textChanged.connect(check_source_file_path)
ui.analyze.clicked.connect(main)

sys.exit(app.exec_())
