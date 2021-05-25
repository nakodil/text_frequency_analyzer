import re
import sys
import time
from collections import Counter
from PyQt5.QtWidgets import QFileDialog  # pip install pyside2
from PyQt5 import QtTest  # pip install pyside2
from interface import *

# для разбора документов MS Word
import docx

# для морфологического анализа
import pymorphy2  # pip install pymorphy2

# для облака слов
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# нормализация для файлов с разной кодировкой
from charset_normalizer import CharsetNormalizerMatches as cnm  # pip install


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

# настройка изображения WordCloud
wc_arguments_dict = {
    "background_color": "black",
    "max_words": 1000,
    "width": 2000,
    "height": 1000,
    "relative_scaling": 0.25,
    "normalize_plurals": False
}


def show_source_select_dialog():
    """
    Показывает диалог выбора файла, доступны только *.txt и *.docx.
    Сохраняет путь выбранного файла в source_file_path.
    """
    source_file_path = QFileDialog.getOpenFileName(filter="*.txt *.docx")
    ui.source_file_path.setText(source_file_path[0])


def check_source_file_path():
    """
    Проверяет выбранный путь до файла-источника.
    Если путь введен, активирует кнопку «Анализировать источник».
    Если путь пустой, блокирует кнопку «Анализировать источник».
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
    ui.make_wordcloud.setEnabled(condition)


def get_text_str() -> str:
    """
    Берет путь к файлу и определяет его тип.
    У *.txt нормализует кодировку его текстового содержимого и
    записывает его в строку.
    У *.docx парсит содержимое и записывает его в строку.
    """
    # TODO: определить тип файла по пути
    source_file_type = "txt"
    source_file_path = ui.source_file_path.toPlainText()
    if source_file_type == "docx":
        doc = docx.Document('example.docx')
        text = []
        # FIXME: Здесь три одинаковых параграфа в виде списка
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
            print(text)
        text_str = text(' '.join(text))
        print(text_str)
    else:
        text_str = str(cnm.from_path(source_file_path).best().first())
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

    # задаем максимум для прогресс-бара
    progress_max_value = len(text_list)
    ui.progress.setMaximum(progress_max_value)
    progress_i = 0

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

        # добавляем единицу к прогресс-бару
        QtTest.QTest.qWait(0)
        ui.progress.setValue(progress_i)
        progress_i += 1
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
        result_item = f"{key} : {value}"
        ui.result.addItem(result_item)


def save_result_to_file():
    """
    Сохраняет содержимое виджета «Результат» в выбранный файл.
    Выдает сообщение в виджет «Ход выполнения программы».
    """
    destination_file = QFileDialog.getSaveFileName(filter="*.txt")
    destination_file_path = destination_file[0]

    with open(destination_file_path, "w", encoding="utf-8") as file:
        for i in range(ui.result.count()):
            line = ui.result.item(i).text()
            file.write(line)

    ui.message.addItem(f"Результат сохранен в {destination_file_path}")


def make_wordcloud():
    """
    Открывает диалог выбора файла-изображения
    и сохраняет в него результат в виде облака слов.
    Сначала WordCloud генерирует изображение width×height,
    потом «вписывает» его в plot.
    У изображения удалены границы, оно получится меньше, чем мы задали.
    https://stackoverflow.com/questions/28786534/increase-resolution-with-word-cloud-and-remove-empty-border
    """
    image_file = QFileDialog.getSaveFileName(filter="*.png")
    image_file_path = image_file[0]

    wc = WordCloud(**wc_arguments_dict).generate_from_frequencies(result_dict)
    plt.figure(figsize=(20, 10))  # умножается на dpi
    plt.axis("off")
    plt.imshow(wc)
    plt.savefig(image_file_path, dpi=100, facecolor='k', bbox_inches='tight')
    ui.message.addItem(f"Облако слов сохранено в {image_file_path}")


def main():
    """
    Основная функция. Выполняет программу последовательно,
    если удалось получить текстовое содержимое из файла.
    PYQT не обновит интерфейс, пока не завершится функция main().
    Для изменения интерфейса в ходе выполнения функции main()
    используется прерывание на время с помощью QtTest.QTest.qWait(0)
    """
    global result_dict  # TODO: сделать локальным?
    start_time = time.time()
    word_type_list = get_word_type()
    interface_is_active(False)
    ui.message.clear()
    ui.result.clear()
    ui.message.addItem(f"Идет анализ текста. Пожалуйста, подождите!")
    QtTest.QTest.qWait(0)

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
        QtTest.QTest.qWait(0)

    if word_type_list:
        text_list = prepare_text(text_str)
        normal_list = morph_analyze_text(text_list, word_type_list)
        result_dict = count_words(normal_list)
        result_to_widget(result_dict)
        end_time = round(time.time() - start_time, 2)
        ui.message.addItem(f"Анализ завершен за {end_time} секунд")
        interface_is_active(True)
        # TODO: убрать в функцию интерфейса
        ui.save_result_to_file.setEnabled(True)
        ui.progress.setValue(0)

    else:
        ui.message.addItem(f"Части речи не выбраны, анализ невозможен!")
        ui.source_file_path.setEnabled(True)
        ui.show_source_select_dialog.setEnabled(True)
        ui.words_number.setEnabled(True)


# привязка сигналов к событиям элементов интерфейса
ui.show_source_select_dialog.clicked.connect(show_source_select_dialog)
ui.save_result_to_file.clicked.connect(save_result_to_file)
ui.source_file_path.textChanged.connect(check_source_file_path)
ui.analyze.clicked.connect(main)
ui.make_wordcloud.clicked.connect(make_wordcloud)

sys.exit(app.exec_())
