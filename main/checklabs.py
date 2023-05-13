import os
import math
import docx
from docx.shared import Pt
import zipfile
from datetime import datetime


def check_on_properties(folder, font, alignment, interval, fontSize, indFirst, indLeft, indRight):
    paths = []
    count_of_files = 0
    fileName = ''
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('docx') and not file.startswith('~'):
                paths.append(os.path.join(root, file))
                count_of_files += 1
    for path in paths:
        doc = docx.Document(path)
        isTitlePage = True
        for paragraph in doc.paragraphs:
            countAlign = 0
            for run in paragraph.runs:
                if paragraph.style.font.name is not None and paragraph.style.font.size is not None and paragraph.style.paragraph_format.line_spacing is not None and paragraph.style.paragraph_format.first_line_indent is not None:
                    styleAlign = paragraph.style.paragraph_format.alignment
                    styleFontName = paragraph.style.font.name
                    styleFontSize = paragraph.style.font.size.pt
                    styleInterval = paragraph.style.paragraph_format.line_spacing
                    styleFInd = paragraph.style.paragraph_format.first_line_indent.cm
                    if paragraph.style.paragraph_format.left_indent is not None:
                        styleLInd = paragraph.style.paragraph_format.left_indent.cm
                    else:
                        continue
                    if paragraph.style.paragraph_format.right_indent is not None:
                        styleRInd = paragraph.style.paragraph_format.right_indent.cm
                    else:
                        continue
                else:
                    styleAlign = None
                    styleFontName = None
                    styleFontSize = None
                    styleInterval = None
                    styleFInd = None
                    styleLInd = None
                    styleRInd = None
                'Проверка на титульный лист'
                if 'w:lastRenderedPageBreak' in run._element.xml:
                    isTitlePage = False
                if isTitlePage != True:
                    if not paragraph.text.startswith('Лабораторная') and not paragraph.text.startswith(
                            'Таблица') and not paragraph.text.startswith('Рисунок') and not paragraph.text.startswith(
                        '«') and not 'w:drawing' in run._element.xml and not 'w:tbl' in run._element.xml:
                        'Проверка на соответствие заданному выравниванию'
                        if paragraph.alignment != alignment or styleAlign != alignment:

                            if countAlign == 0:
                                paragraph.add_comment(
                                    'Не соответствие выравниванию\nдолжно быть: ' + alignmentToStr(alignment),
                                    author='Check Labs', initials='ES')
                                countAlign += 1
                            else:
                                continue

                        'Проверка на соответствие заданному шрифту'
                        if run.font.name != font or styleFontName != font:
                            paragraph.add_comment('Не соответствие шрифту\nдолжно быть:' + font, author='Check Labs',
                                                  initials='ES')

                        'Проверка на соответствие заданному размеру шрифта'
                        if run.font.size != Pt(fontSize) or styleFontSize != fontSize:
                            paragraph.add_comment(
                                'Не соответствие размеру шрифта \nдолжно быть: ' + str(fontSize) + " пт",
                                author='Check Labs', initials='ES')

                        'Проверка на соответствие заданному интервалу'
                        if paragraph.paragraph_format.line_spacing != interval or styleInterval != interval:
                            paragraph.add_comment('Не соответствие интервалу\nдолжно быть: ' + str(interval),
                                                  author='Check Labs', initials='ES')

                        'Проверка на соответствие заданному отступу первой строки'
                        if paragraph.paragraph_format.first_line_indent is not None and math.isclose(
                                paragraph.paragraph_format.first_line_indent.cm,
                                indFirst) or styleFInd is not None and math.isclose(styleFInd, indFirst):
                            paragraph.add_comment(
                                'Не соответствие отступу первой строки\nдолжно быть: ' + str(indFirst) + " см",
                                author='Check Labs', initials='ES')

                        'Проверка на соответствие заданному отступу слева'
                        if paragraph.paragraph_format.left_indent is not None and paragraph.paragraph_format.left_indent.cm != indLeft or styleLInd is not None and math.isclose(
                                styleLInd, indLeft):
                            paragraph.add_comment('Не соответствие отступу слева\nдолжно быть: ' + str(indLeft) + " см",
                                                  author='Check Labs', initials='ES')

                        'Проверка на соответствие заданному отступу справа'
                        if paragraph.paragraph_format.right_indent is not None and paragraph.paragraph_format.right_indent.cm != indRight or styleRInd is not None and math.isclose(
                                styleRInd, indRight):
                            paragraph.add_comment(
                                'Не соответствие отступу справа\nдолжно быть: ' + str(indRight) + " см",
                                author='Check Labs', initials='ES')
                    else:
                        continue
        fileName = os.path.basename(path)
        doc.save(folder + "\\" + fileName)
        if os.path.isfile(folder + "\\" + fileName):
            print("Файл " + fileName + " сохранен!")
        else:
            print("Error {0}")
    is_zip = False
    if count_of_files > 1:
        is_zip = True
        zip_name = zipdocs(folder)
        return zip_name, is_zip
    else:
        is_zip = False
        return fileName, is_zip


def alignmentToStr(alignment):
    match (alignment):
        case 0:
            return 'Выравнивание по левому краю'
        case 1:
            return 'Выравнивание по центру'
        case 2:
            return 'Выравнивание по правому краю'
        case 3:
            return 'Выравнивание по ширине'


def zipdocs(folder):
    current_date = datetime.now().date()
    zip_name = folder + "/" + str(current_date) + ".zip"
    doczip = zipfile.ZipFile(zip_name, 'w')
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('docx') and not file.startswith('~'):
                doczip.write(os.path.join(root, file), file, compress_type=zipfile.ZIP_DEFLATED)
                if os.path.isfile(root + "/" + file):
                    os.remove(root + "/" + file)
    doczip.close()
    return zip_name
