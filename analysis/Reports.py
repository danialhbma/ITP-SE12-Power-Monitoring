from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
import matplotlib.pyplot as plt

def generate_report():
    # Create a PDF canvas using ReportLab
    pdf_canvas = canvas.Canvas("report.pdf", pagesize=letter)

    # Create your matplotlib plot
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3, 4], [1, 4, 9, 16])
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Plot Title")

    # Save the matplotlib plot as a PNG image file
    image_path = "plot.png"
    plt.savefig(image_path, format="png", bbox_inches="tight")

    # Load the saved image file using ReportLab
    pdf_canvas.drawInlineImage(image_path, x=100, y=500)

    # Add some text to the PDF canvas
    pdf_canvas.drawString(100, 450, "This is a PDF report generated using ReportLab and matplotlib.")

    # Close the canvas to finalize the PDF document
    pdf_canvas.showPage()
    pdf_canvas.save()

if __name__ == "__main__":
    generate_report()
