"""
cover_letter_pdf.py

Converts plain text cover letter content into a clean, well-formatted PDF.

Usage:
    from cover_letter_pdf import create_cover_letter_pdf

    result = create_cover_letter_pdf(
        content=my_cover_letter_text,
        output_filename="cover_letter.pdf",
        applicant_name="Jane Doe",
        contact_info="jane.doe@email.com | +94 71 234 5678 | Kandy, Sri Lanka",
        date="August 23, 2026",
    )
    print(result)
"""

import os
from datetime import date as _date

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

# Folder where generated PDFs are saved (relative to this file)
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


def create_cover_letter_pdf(
    content: str,
    output_filename: str = "cover_letter.pdf",
    applicant_name: str = None,
    contact_info: str = None,
    date: str = None,
    output_dir: str = OUTPUT_DIR,
) -> str:
    """
    Convert plain text cover letter content into a well-formatted PDF.

    Args:
        content: The full body text of the cover letter. Paragraphs should
                 be separated by a blank line (double newline) in the source
                 text -- this is how the function detects paragraph breaks.
        output_filename: Name of the PDF file to create (e.g. "cover_letter.pdf").
        applicant_name: Optional. Shown as a bold header at the top of the page.
        contact_info: Optional. Shown under the name (email, phone, location, etc).
        date: Optional. Shown below the contact info. Defaults to today's date
              if applicant_name or contact_info is provided but date is not.
        output_dir: Folder to save the PDF into. Defaults to the "output"
                    folder next to this script.

    Returns:
        The absolute path to the created PDF file.
    """
    if not content or not content.strip():
        raise ValueError("content must be a non-empty string")

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        topMargin=1 * inch,
        bottomMargin=1 * inch,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        title=output_filename.replace(".pdf", ""),
    )

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        "ApplicantName",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        spaceAfter=2,
        textColor="#1a1a1a",
    )

    contact_style = ParagraphStyle(
        "ContactInfo",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13,
        textColor="#555555",
        spaceAfter=2,
    )

    date_style = ParagraphStyle(
        "DateStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        spaceBefore=14,
        spaceAfter=18,
    )

    body_style = ParagraphStyle(
        "CoverLetterBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=12,
    )

    story = []

    # Optional header block: name, contact info, date
    if applicant_name:
        story.append(Paragraph(applicant_name, name_style))
    if contact_info:
        story.append(Paragraph(contact_info, contact_style))
    if applicant_name or contact_info:
        display_date = date or _date.today().strftime("%B %d, %Y")
        story.append(Paragraph(display_date, date_style))
    elif date:
        story.append(Paragraph(date, date_style))

    # Split content into paragraphs on blank lines, preserving order
    raw_paragraphs = [p.strip() for p in content.strip().split("\n\n")]
    for para in raw_paragraphs:
        if not para:
            continue
        # Collapse internal single newlines into spaces (soft line wraps)
        # but keep the paragraph as one flowing block.
        cleaned = " ".join(line.strip() for line in para.splitlines())
        story.append(Paragraph(cleaned, body_style))

    doc.build(story)

    return os.path.abspath(output_path)