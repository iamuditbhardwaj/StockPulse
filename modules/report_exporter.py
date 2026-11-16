
import csv
import io

from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


def generate_pdf_report(report):

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        textColor=colors.HexColor("#142337"),
        fontSize=20,
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#0F766E"),
        spaceBefore=14,
        spaceAfter=8
    )

    story = []

    symbol = escape(str(report.get("symbol", "N/A")))
    company = escape(str(report.get("company", "N/A")))
    report_date = escape(str(report.get("report_date", "N/A")))

    performance = report.get("performance", {})
    trend = report.get("trend_analysis", {})

    # Report title
    story.append(Paragraph("StockPulse", title_style))
    story.append(
        Paragraph("Stock Market Analysis Report", styles["Heading2"])
    )
    story.append(Spacer(1, 12))

    # Basic information
    story.append(Paragraph("Instrument Information", heading_style))

    basic_data = [
        ["Company", company],
        ["Symbol", symbol],
        ["Report Generated", report_date]
    ]

    basic_table = Table(basic_data, colWidths=[150, 330])

    basic_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F3F2")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#142337")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(basic_table)

    # Performance analysis
    story.append(Paragraph("Performance Analysis", heading_style))

    performance_data = [
        ["Metric", "Value"],
        ["Starting Price", str(performance.get("starting_price", "N/A"))],
        ["Ending Price", str(performance.get("ending_price", "N/A"))],
        ["Highest Price", str(performance.get("highest_price", "N/A"))],
        ["Lowest Price", str(performance.get("lowest_price", "N/A"))],
        ["Average Price", str(performance.get("average_price", "N/A"))],
        ["Price Change", str(performance.get("price_change", "N/A"))],
        [
            "Percentage Return",
            f'{performance.get("percentage_return", "N/A")}%'
        ]
    ]

    performance_table = Table(
        performance_data,
        colWidths=[240, 240]
    )

    performance_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#142337")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(performance_table)

    # Trend analysis
    story.append(Paragraph("Trend Analysis", heading_style))

    trend_data = [
        ["Metric", "Value"],
        ["Starting Price", str(trend.get("starting_price", "N/A"))],
        ["Ending Price", str(trend.get("ending_price", "N/A"))],
        ["Trend", str(trend.get("trend", "N/A"))],
        ["Highest Price", str(trend.get("highest_price", "N/A"))],
        ["Lowest Price", str(trend.get("lowest_price", "N/A"))],
        ["Price Range", str(trend.get("price_range", "N/A"))]
    ]

    trend_table = Table(trend_data, colWidths=[240, 240])

    trend_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#142337")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
    ]))

    story.append(trend_table)

    # Disclaimer
    story.append(Spacer(1, 20))
    story.append(
        Paragraph(
            "Disclaimer: StockPulse provides historical market data "
            "and educational analysis only. This report is not "
            "investment advice or a recommendation to buy or sell "
            "any financial instrument.",
            styles["Italic"]
        )
    )

    document.build(story)

    buffer.seek(0)

    return buffer


def generate_csv_report(report):

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["StockPulse Analysis Report"])
    writer.writerow(["Company", report.get("company", "N/A")])
    writer.writerow(["Symbol", report.get("symbol", "N/A")])
    writer.writerow(["Report Date", report.get("report_date", "N/A")])

    writer.writerow([])
    writer.writerow(["Performance Analysis"])
    writer.writerow(["Metric", "Value"])

    performance = report.get("performance", {})

    for key, value in performance.items():
        writer.writerow([key.replace("_", " ").title(), value])

    writer.writerow([])
    writer.writerow(["Trend Analysis"])
    writer.writerow(["Metric", "Value"])

    trend = report.get("trend_analysis", {})

    for key, value in trend.items():
        writer.writerow([key.replace("_", " ").title(), value])

    buffer = io.BytesIO(output.getvalue().encode("utf-8-sig"))

    return buffer
