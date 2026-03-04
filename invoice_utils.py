import os
import uuid
from datetime import datetime, timedelta

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def generate_invoice(user, plan):
    """
    Generates a professional fake invoice PDF
    Returns: transaction_id, file_path
    """

    # Generate transaction ID
    transaction_id = str(uuid.uuid4())[:10]

    # Dates
    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    # Ensure folder exists
    folder = "media/invoices"
    os.makedirs(folder, exist_ok=True)

    file_path = f"{folder}/{transaction_id}.pdf"

    # Create document
    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    # Title
    elements.append(Paragraph("<b>Subscription Invoice</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    # Invoice Data Table
    data = [
        ["Customer Name:", f"{user.first_name} {user.last_name}"],
        ["Email:", user.email],
        ["Plan Name:", plan.name],
        ["Price:", f"₹ {plan.price}"],
        ["Start Date:", start_date.strftime("%Y-%m-%d")],
        ["End Date:", end_date.strftime("%Y-%m-%d")],
        ["Transaction ID:", transaction_id],
    ]

    table = Table(data, colWidths=[150, 300])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.whitesmoke),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 30))

    elements.append(Paragraph("Thank you for choosing our service!", styles["Normal"]))

    # Build PDF
    doc.build(elements)

    return transaction_id, file_path