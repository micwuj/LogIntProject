import io
import os
import pytz
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from history.models import History
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (SimpleDocTemplate, Table, TableStyle)
from datetime import timedelta, datetime

def add_page_number(canvas, doc):
    page_num = canvas.getPageNumber()
    text = f"Page {page_num}"
    canvas.drawRightString(200 * inch, 20 * inch, text)

def header_footer(canvas, doc):
    width, height = A4
    canvas.saveState()
    
    canvas.setFont('Helvetica-Bold', 12)
    logo_path = 'static/img/BOEK_logo.png'
    if os.path.exists(logo_path):
        canvas.drawImage(logo_path, 0.5 * inch, height - 1.3 * inch, width=1.5 * inch, height=1.5 * inch, preserveAspectRatio=True, mask='auto')
    if canvas.getPageNumber() == 1:
        report_text = "Operations Report"
        text_width = canvas.stringWidth(report_text, 'Helvetica-Bold', 12)
        text_x = (width - text_width) / 2
        canvas.drawString(text_x, height - 0.6 * inch, report_text)
    
    canvas.setFont('Helvetica', 9)
    canvas.drawString(0.5 * inch, 0.75 * inch, f"Generated on: {timezone.now().astimezone(pytz.timezone('Europe/Warsaw')).strftime('%Y-%m-%d %H:%M:%S')}")
    canvas.drawRightString(width - 0.5 * inch, 0.75 * inch, f"Page {doc.page}")
    
    canvas.restoreState()

def generate_pdf(histories):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=0.5 * inch, rightMargin=0.5 * inch)
    elements = []
    
    data = [["Type", "Name", "Operation", "Operation Date"]]
    for history in histories:
        operation_date_warsaw = history.operation_date.astimezone(pytz.timezone('Europe/Warsaw'))
        data.append([
            history.type, 
            history.name, 
            history.operation, 
            operation_date_warsaw.strftime("%Y-%m-%d %H:%M:%S")
        ])
    
    page_width = A4[0] - (doc.leftMargin + doc.rightMargin)
    num_columns = len(data[0])
    col_width = page_width / num_columns
    
    table = Table(data, colWidths=[col_width] * num_columns)
    
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white])
    ])
    table.setStyle(style)
    
    elements.append(table)
    doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
    
    buffer.seek(0)
    return buffer

def generate_txt(histories):
    buffer = io.StringIO()
    buffer.write(f"{'Type':<15} {'Name':<25} {'Operation':<20} {'Operation Date':<20}\n")
    buffer.write("-" * 80 + "\n")
    for history in histories:
        operation_date_warsaw = history.operation_date.astimezone(pytz.timezone('Europe/Warsaw'))
        buffer.write(f"{history.type:<15} {history.name:<25} {history.operation:<20} {operation_date_warsaw.strftime('%Y-%m-%d %H:%M:%S'):<20}\n")
    
    buffer.seek(0)
    return buffer

def get_all_reports(request):
    if request.method == 'POST':
        histories = History.objects.all()
        buffer = generate_pdf(histories)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        
    return response

def reports(request):
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        type_value = request.POST.get('type')
        operation = request.POST.get('operation')
        if date_to:
            end_date = datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1)
        
        filter_kwargs = {}
        
        if type_value:
            filter_kwargs['type'] = type_value
        if operation:
            filter_kwargs['operation'] = operation
        if date_from and date_to:
            filter_kwargs['operation_date__range'] = (date_from, end_date)
        elif date_from and not date_to:
            filter_kwargs['operation_date__gte'] = date_from
        elif not date_from and date_to:
            filter_kwargs['operation_date__lt'] = end_date
        
        histories = History.objects.filter(**filter_kwargs)
        
        histories = histories.order_by('type', '-operation_date')
        
        buffer = generate_pdf(histories)
        
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="report.pdf"'
        return response
    
    return render(request, 'pages/reports.html')