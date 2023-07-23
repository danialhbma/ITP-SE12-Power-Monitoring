import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

def convert_images_to_pdf(image_directory, output_pdf_name=None):
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the script's directory with the "reports" folder to get the absolute path of the reports directory
    reports_directory = os.path.join(script_directory, "reports")

    # Create the "reports" folder if it doesn't exist - validation
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory)

    # Save the PDF file with a dynamic name including the current month and full year - can always change format 
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().strftime("%Y")
    pdf_output_name = f"Analysis_{current_month}_{current_year}.pdf"
    pdf_output_path = os.path.join(reports_directory, pdf_output_name)

    # Initialize the canvas for PDF generation with A4 size and the correct output file name - can always change format 
    c = canvas.Canvas(output_pdf_name or pdf_output_path, pagesize=A4)

    # Get a list of image files from the specified directory - will take all files in the directory
    image_files = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]

    image_files.sort()
    page_width, page_height = A4

    # Loop through the image files and add them to the PDF
    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        img = Image.open(image_path)
        img_width, img_height = img.size

        width_ratio = page_width / img_width
        height_ratio = page_height / img_height
        scaling_factor = min(width_ratio, height_ratio)

        scaled_width = img_width * scaling_factor
        scaled_height = img_height * scaling_factor

        x_offset = (page_width - scaled_width) / 2
        y_offset = (page_height - scaled_height) / 2

        c.drawInlineImage(img, x_offset, y_offset, width=scaled_width, height=scaled_height)

        # Add a new page for the next image
        c.showPage()

        # Print the name of the image that was included in the PDF - validation
        print(f"Included image: {image_file}")

    # Save the PDF file with a dynamic name including the current month
    current_month = datetime.now().strftime("%B")
    script_directory = os.path.dirname(os.path.abspath(__file__))
    pdf_output_path = os.path.join(script_directory, "reports", f"Analysis_{current_month}_{current_year}.pdf")
    c.save()

    print(f"PDF file saved at: {pdf_output_path}")

if __name__ == "__main__":
    image_directory = "results"

    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the script's directory with the image_directory to get the absolute path of the image directory
    image_directory_absolute = os.path.join(script_directory, image_directory)

    convert_images_to_pdf(image_directory_absolute)