import os
import qrcode
from io import BytesIO
from PIL import Image

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_qr_code(text: str) -> BytesIO:
    """Generate a high-res QR code image buffer."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0f172a", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def generate_missing_person_pdf(case_details: dict) -> str:
    """
    Generate an official high-resolution MISSING PERSON ALERT PDF Poster with scannable QR Code.
    Returns: path to generated PDF file.
    """
    output_dir = "./resources/posters"
    os.makedirs(output_dir, exist_ok=True)
    
    case_id = case_details.get("id", "UNKNOWN")
    pdf_filename = f"MISSING_ALERT_{case_id[:8]}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Title & Header Style
    title_style = ParagraphStyle(
        'HeaderTitle',
        parent=styles['Heading1'],
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#dc2626'),
        alignment=1,  # Center
        fontName='Helvetica-Bold'
    )

    sub_title_style = ParagraphStyle(
        'HeaderSub',
        parent=styles['Normal'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e3a8a'),
        alignment=1,
        fontName='Helvetica-Bold'
    )

    story.append(Paragraph("🚨 OFFICIAL MISSING PERSON ALERT 🚨", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph(f"LAW ENFORCEMENT & PUBLIC BULLETIN • FIR ID: FIR-{case_id[:8].upper()}", sub_title_style))
    story.append(Spacer(1, 15))

    # Generate QR Code for tracking & instant smartphone scan
    portal_host = os.getenv("PORTAL_URL", "http://localhost:8501")
    tracking_payload = (
        f"🚨 POLICE MISSING PERSON ALERT 🚨\n"
        f"Case ID: {case_id}\n"
        f"Name: {case_details.get('name', 'N/A')}\n"
        f"Age: {case_details.get('age', 'N/A')}\n"
        f"Station: Avinashi Police Station, Tiruppur\n"
        f"Helpline: 112 / 100\n"
        f"Web Portal: {portal_host}/?case_id={case_id}"
    )
    qr_buffer = generate_qr_code(tracking_payload)
    qr_temp_path = os.path.join(output_dir, f"qr_{case_id[:8]}.png")
    with open(qr_temp_path, "wb") as f:
        f.write(qr_buffer.getbuffer())

    # Photo & Details Layout
    img_path = f"./resources/{case_id}.jpg"
    if not os.path.exists(img_path):
        # Fallback placeholder
        img_path = qr_temp_path

    person_img = RLImage(img_path, width=180, height=210)
    qr_img = RLImage(qr_temp_path, width=120, height=120)

    details_text = f"""
    <b>FULL NAME:</b> {case_details.get('name', 'N/A')}<br/><br/>
    <b>AGE:</b> {case_details.get('age', 'N/A')} &nbsp;&nbsp;|&nbsp;&nbsp; <b>CITY:</b> {case_details.get('city', 'N/A')}<br/><br/>
    <b>LAST SEEN LOCATION:</b> {case_details.get('last_seen', 'N/A')}<br/><br/>
    <b>DISTINGUISHING MARKS:</b> {case_details.get('birth_marks', 'None')}<br/><br/>
    <b>COMPLAINANT CONTACT:</b> {case_details.get('complainant_name', 'N/A')} ({case_details.get('complainant_mobile', 'N/A')})<br/><br/>
    <b>CASE ID:</b> <font color="#1d4ed8">{case_id}</font>
    """
    
    details_p = Paragraph(details_text, ParagraphStyle('Details', parent=styles['Normal'], fontSize=11, leading=16))

    # Grid Table
    data = [
        [person_img, details_p]
    ]

    t = Table(data, colWidths=[200, 340])
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('PADDING', (0, 0), (-1, -1), 12),
    ]))

    story.append(t)
    story.append(Spacer(1, 20))

    # QR Code Footer Table
    qr_notice = Paragraph(
        "<b>SCAN QR CODE TO TRACK LIVE STATUS</b><br/>"
        "<font size=9 color='#64748b'>Scan with smartphone camera to view live AI match updates, submit sighting evidence, or contact station officers directly.</font><br/><br/>"
        "<b>EMERGENCY POLICE HELPLINE: 112 / 100</b>",
        ParagraphStyle('QRNotice', parent=styles['Normal'], fontSize=10, leading=14)
    )

    qr_table = Table([[qr_img, qr_notice]], colWidths=[140, 400])
    qr_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1d4ed8')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#eff6ff')),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))

    story.append(qr_table)

    doc.build(story)
    
    # Cleanup temp QR image
    if os.path.exists(qr_temp_path):
        os.remove(qr_temp_path)

    return pdf_path
