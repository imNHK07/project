from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from barcode import get_barcode_class
from barcode.writer import SVGWriter
from svglib.svglib import svg2rlg

def get_barcode_svg(barcode_string, options=None):
    """
    Generates an EAN13 barcode as an SVG and returns the SVG data as a string.
    """
    EAN13 = get_barcode_class('ean13')
    ean = EAN13(barcode_string[:12], writer=SVGWriter())
    svg_buffer = BytesIO()
    ean.write(svg_buffer, options)
    svg_buffer.seek(0)
    return svg_buffer.read().decode('utf-8')

def generate_barcode_pdf(queryset):
    """
    Generates a PDF with barcodes from a queryset of Master objects.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Setup a 4x11 grid layout
    cols = 4
    rows = 11
    x_margin = 25
    y_margin = 25
    col_width = (width - 2 * x_margin) / cols
    row_height = (height - 2 * y_margin) / rows
    
    barcode_count = 0
    
    for item in queryset:
        if barcode_count > 0 and barcode_count % (cols * rows) == 0:
            p.showPage()

        row = (barcode_count % (cols * rows)) // cols
        col = (barcode_count % (cols * rows)) % cols

        x = x_margin + col * col_width
        y = height - y_margin - (row + 1) * row_height

        # Generate barcode image
        if item.barcode:
            options = {'font_size': 8, 'text_distance': 3.0}
            svg_data = get_barcode_svg(item.barcode, options)
            drawing = svg2rlg(BytesIO(svg_data.encode('utf-8')))            
            # Scale drawing to fit the cell
            scale = (col_width - 10) / drawing.width
            drawing.width = drawing.width * scale
            drawing.height = drawing.height * scale
            
            drawing.drawOn(p, x, y + 10) # draw barcode

        barcode_count += 1

    p.save()
    buffer.seek(0)
    return buffer