import io
import pytz
from django.shortcuts import render
from django.http import HttpResponse
from history.models import History
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from datetime import timedelta, datetime

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
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ])
    table.setStyle(style)
    
    elements.append(table)
    doc.build(elements)
    
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