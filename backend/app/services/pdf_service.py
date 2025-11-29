"""
PDF Generation Service for Checklist Reports
"""
from io import BytesIO
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from sqlalchemy.orm import Session
import base64
import requests
import os


class PDFService:
    """Service for generating PDF reports from checklist data."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=20,
            textColor=colors.HexColor('#10B981'),
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#1F2937'),
            borderPadding=5
        ))

        self.styles.add(ParagraphStyle(
            name='SubHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceBefore=10,
            spaceAfter=5,
            textColor=colors.HexColor('#374151')
        ))

        self.styles.add(ParagraphStyle(
            name='NormalText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.HexColor('#4B5563')
        ))

        self.styles.add(ParagraphStyle(
            name='MissedText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.HexColor('#DC2626'),
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='CompletedText',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=5,
            textColor=colors.HexColor('#059669')
        ))

        self.styles.add(ParagraphStyle(
            name='FooterText',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#9CA3AF'),
            alignment=TA_CENTER
        ))

    def generate_daily_checklist_report(
        self,
        db: Session,
        site_id: int,
        report_date: date,
        organization_name: str,
        site_name: str
    ) -> BytesIO:
        """
        Generate a PDF report for a single day's checklists at a site.

        Args:
            db: Database session
            site_id: ID of the site
            report_date: The date to generate the report for
            organization_name: Name of the organization
            site_name: Name of the site

        Returns:
            BytesIO buffer containing the PDF
        """
        from app.models.checklist import Checklist, ChecklistStatus
        from app.models.checklist_item import ChecklistItem
        from app.models.task_field_response import TaskFieldResponse
        from app.models.task_field import TaskField
        from app.models.category import Category

        # Create PDF buffer
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )

        # Build content
        elements = []

        # Title
        elements.append(Paragraph(
            f"Daily Checklist Report",
            self.styles['ReportTitle']
        ))

        # Report info
        elements.append(Paragraph(
            f"<b>Organization:</b> {organization_name}",
            self.styles['NormalText']
        ))
        elements.append(Paragraph(
            f"<b>Site:</b> {site_name}",
            self.styles['NormalText']
        ))
        elements.append(Paragraph(
            f"<b>Date:</b> {report_date.strftime('%A, %d %B %Y')}",
            self.styles['NormalText']
        ))
        elements.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            self.styles['NormalText']
        ))

        elements.append(Spacer(1, 15))
        elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
        elements.append(Spacer(1, 15))

        # Get checklists for this date and site
        checklists = db.query(Checklist).filter(
            Checklist.site_id == site_id,
            Checklist.checklist_date == report_date
        ).order_by(Checklist.category_id).all()

        if not checklists:
            elements.append(Paragraph(
                "No checklists found for this date.",
                self.styles['NormalText']
            ))
        else:
            # Summary section
            total_items = sum(c.total_items or 0 for c in checklists)
            completed_items = sum(c.completed_items or 0 for c in checklists)
            completion_rate = (completed_items / total_items * 100) if total_items > 0 else 0

            # Summary table
            summary_data = [
                ['Summary', ''],
                ['Total Categories', str(len(checklists))],
                ['Total Tasks', str(total_items)],
                ['Completed Tasks', str(completed_items)],
                ['Missed Tasks', str(total_items - completed_items)],
                ['Completion Rate', f"{completion_rate:.1f}%"]
            ]

            summary_table = Table(summary_data, colWidths=[100*mm, 60*mm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ]))
            elements.append(summary_table)
            elements.append(Spacer(1, 20))

            # Detailed sections for each category
            for checklist in checklists:
                category = db.query(Category).filter(Category.id == checklist.category_id).first()
                category_name = category.name if category else "Unknown Category"

                # Category header
                status_color = '#059669' if checklist.status == ChecklistStatus.COMPLETED else '#DC2626'
                status_text = checklist.status.value if checklist.status else 'UNKNOWN'

                elements.append(Paragraph(
                    f"<b>{category_name}</b> - <font color='{status_color}'>{status_text}</font>",
                    self.styles['SectionHeader']
                ))

                # Category stats
                cat_completion = (checklist.completed_items / checklist.total_items * 100) if checklist.total_items > 0 else 0
                elements.append(Paragraph(
                    f"Tasks: {checklist.completed_items}/{checklist.total_items} ({cat_completion:.1f}% complete)",
                    self.styles['NormalText']
                ))

                if checklist.completed_at:
                    elements.append(Paragraph(
                        f"Completed at: {checklist.completed_at.strftime('%H:%M')}",
                        self.styles['NormalText']
                    ))

                elements.append(Spacer(1, 10))

                # Get checklist items
                items = db.query(ChecklistItem).filter(
                    ChecklistItem.checklist_id == checklist.id
                ).order_by(ChecklistItem.id).all()

                for item in items:
                    # Item status icon and name
                    if item.is_completed:
                        icon = "✓"
                        style = self.styles['CompletedText']
                    else:
                        icon = "✗"
                        style = self.styles['MissedText']

                    item_name = item.item_name or "Unnamed Task"
                    elements.append(Paragraph(
                        f"{icon} {item_name}",
                        style
                    ))

                    # Get field responses for this item
                    responses = db.query(TaskFieldResponse).filter(
                        TaskFieldResponse.checklist_item_id == item.id
                    ).all()

                    if responses:
                        for response in responses:
                            field = db.query(TaskField).filter(
                                TaskField.id == response.task_field_id
                            ).first()
                            field_label = field.field_label if field else "Field"
                            value = response.get_value()

                            # Handle photo fields
                            if field and field.field_type == 'photo' and response.file_url:
                                elements.append(Paragraph(
                                    f"    <b>{field_label}:</b> [Photo attached]",
                                    self.styles['NormalText']
                                ))
                                # Try to embed the image
                                try:
                                    img = self._get_image_from_url(response.file_url)
                                    if img:
                                        elements.append(img)
                                        elements.append(Spacer(1, 5))
                                except Exception as e:
                                    print(f"Failed to embed image: {e}")
                            else:
                                # Format value for display
                                display_value = self._format_value(value, field)
                                elements.append(Paragraph(
                                    f"    <b>{field_label}:</b> {display_value}",
                                    self.styles['NormalText']
                                ))

                    # Item notes
                    if item.notes:
                        elements.append(Paragraph(
                            f"    <i>Notes: {item.notes}</i>",
                            self.styles['NormalText']
                        ))

                    # Item photo (legacy photo_url field)
                    if item.photo_url:
                        elements.append(Paragraph(
                            f"    Evidence photo attached",
                            self.styles['NormalText']
                        ))
                        try:
                            img = self._get_image_from_url(item.photo_url)
                            if img:
                                elements.append(img)
                                elements.append(Spacer(1, 5))
                        except Exception as e:
                            print(f"Failed to embed evidence photo: {e}")

                    elements.append(Spacer(1, 5))

                elements.append(Spacer(1, 10))
                elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#E5E7EB')))

        # Footer
        elements.append(Spacer(1, 20))
        elements.append(Paragraph(
            f"Generated by Zynthio Compliance Platform",
            self.styles['FooterText']
        ))

        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def _format_value(self, value: Any, field: Optional[Any] = None) -> str:
        """Format a field value for display in the PDF."""
        if value is None:
            return "N/A"

        if isinstance(value, bool):
            return "Yes" if value else "No"

        if isinstance(value, (int, float)):
            # Check if it's a temperature field
            if field and field.field_type == 'temperature':
                return f"{value}°C"
            return str(value)

        if isinstance(value, dict):
            # Handle JSON values
            return str(value)

        if isinstance(value, list):
            return ", ".join(str(v) for v in value)

        return str(value)

    def _get_image_from_url(self, url: str, max_width: float = 150*mm, max_height: float = 100*mm) -> Optional[Image]:
        """
        Fetch an image from URL and return a ReportLab Image object.

        Args:
            url: URL of the image
            max_width: Maximum width in points
            max_height: Maximum height in points

        Returns:
            ReportLab Image object or None if failed
        """
        try:
            # Handle relative URLs
            if url.startswith('/'):
                # This is a relative URL, need to construct full path
                # For local development, you might need to adjust this
                base_url = os.environ.get('API_BASE_URL', 'http://localhost:8000')
                url = f"{base_url}{url}"

            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                img_buffer = BytesIO(response.content)
                img = Image(img_buffer)

                # Scale image to fit within max dimensions
                img_width, img_height = img.drawWidth, img.drawHeight

                # Calculate scale factor
                scale_w = max_width / img_width if img_width > max_width else 1
                scale_h = max_height / img_height if img_height > max_height else 1
                scale = min(scale_w, scale_h)

                img.drawWidth = img_width * scale
                img.drawHeight = img_height * scale

                return img
        except Exception as e:
            print(f"Error fetching image from {url}: {e}")

        return None

    def generate_filename(
        self,
        organization_name: str,
        site_name: str,
        report_date: date,
        end_date: Optional[date] = None
    ) -> str:
        """
        Generate a standardized filename for the PDF report.

        Format: org-site-date.pdf or org-site-startdate-enddate.pdf
        """
        # Clean names for filename
        org_clean = self._clean_for_filename(organization_name)
        site_clean = self._clean_for_filename(site_name)

        if end_date and end_date != report_date:
            date_str = f"{report_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}"
        else:
            date_str = report_date.strftime('%Y%m%d')

        return f"{org_clean}-{site_clean}-{date_str}.pdf"

    def _clean_for_filename(self, name: str) -> str:
        """Clean a string for use in a filename."""
        import re
        # Remove special characters, replace spaces with underscores
        cleaned = re.sub(r'[^\w\s-]', '', name)
        cleaned = re.sub(r'[-\s]+', '_', cleaned)
        return cleaned.lower()[:30]  # Limit length


# Singleton instance
pdf_service = PDFService()
