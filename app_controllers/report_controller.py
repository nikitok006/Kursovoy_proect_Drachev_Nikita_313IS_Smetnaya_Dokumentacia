from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
import platform
import subprocess


class ReportController:
    pdfmetrics.registerFont(TTFont('DejaVu', 'fonts/DejaVuSans.ttf'))
    def __init__(self, model, session):
        self.model = model
        self.session = session

    def create_report_for_estimate(self, estimate):
        """
        Создает отчет для выбранной сметы, включая её материалы.
        """
        estimate_id = estimate["id"]  # Добавьте ID сметы в выбранный объект
        output_file = f"estimate_report_{estimate['estimate_number']}.pdf"

        # Получение материалов для сметы
        materials = self.model.get_materials_for_estimate(estimate_id)

        # Генерация PDF-отчета
        print(f"Создание отчета для сметы: {estimate}")
        self.generate_pdf_for_estimate(estimate, materials, output_file)

        # Открытие файла
        self.open_pdf(output_file)

    def generate_pdf_for_estimate(self, estimate, materials, output_file):
        """
        Генерирует PDF-отчет для одной сметы с материалами в табличной форме.
        """
        pdf = canvas.Canvas(output_file, pagesize=A4)
        pdf.setTitle(f"Отчет по смете № {estimate['estimate_number']}")

        x, y = 50, 800
        line_height = 20

        # Заголовок сметы
        pdf.setFont("DejaVu", 12)
        pdf.drawString(x, y, f"Смета № {estimate['estimate_number']}")
        y -= line_height
        pdf.setFont("DejaVu", 10)
        pdf.drawString(x, y, f"Общая стоимость: {estimate['total_cost']} руб.")
        y -= line_height
        pdf.drawString(x, y, f"Комментарий: {estimate['comment']}")
        y -= line_height * 2

        # Заголовок для материалов
        pdf.setFont("DejaVu", 11)
        pdf.drawString(x, y, "Материалы:")
        y -= line_height

        if not materials:
            pdf.drawString(x, y, "Нет связанных материалов.")
            y -= line_height
        else:
            # Данные для таблицы
            table_data = [["Наименование", "Количество", "Цена за единицу", "Общая стоимость"]]
            for material in materials:
                table_data.append([
                    material["material_name"],
                    f"{material['quantity']}",
                    f"{material['cost_per_unit']} руб.",
                    f"{material['total_cost']} руб."
                ])

            # Создаём таблицу
            table = Table(table_data, colWidths=[150, 100, 100, 100])
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),  # Фон для заголовка
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),  # Цвет текста заголовка
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),  # Выравнивание текста
                ("FONTNAME", (0, 0), (-1, 0), "DejaVu"),  # Шрифт заголовка
                ("FONTNAME", (0, 1), (-1, -1), "DejaVu"),  # Шрифт данных
                ("FONTSIZE", (0, 0), (-1, -1), 10),  # Размер шрифта
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),  # Отступы для заголовка
                ("GRID", (0, 0), (-1, -1), 1, colors.black),  # Границы таблицы
            ]))

            # Отображаем таблицу
            table.wrapOn(pdf, x, y)  # Устанавливаем положение
            table.drawOn(pdf, x, y - len(table_data) * line_height)

        pdf.save()
        print(f"Отчет сохранен в {output_file}")

    def open_pdf(self, file_path):
        """
        Открывает PDF-файл в системном приложении по умолчанию.
        """
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", file_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            print(f"Не удалось открыть файл {file_path}: {e}")

