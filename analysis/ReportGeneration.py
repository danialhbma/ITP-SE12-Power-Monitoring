import os
import subprocess
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image

def execute_cost_efficiency_script():
    result = subprocess.run(['python3', 'cost_efficiency.py'], capture_output=True, text=True)
    return result.stdout

def convert_images_to_pdf(image_directory, output_pdf_name=None):
    # Get a list of image files from the specified directory
    image_files = [f for f in os.listdir(image_directory) if os.path.isfile(os.path.join(image_directory, f))]
    image_files.sort()

    # Get the current month and year for dynamic PDF file name
    current_month = datetime.now().strftime("%B")
    current_year = datetime.now().strftime("%y")

    script_directory = os.path.dirname(os.path.abspath(__file__))
    reports_directory = os.path.join(script_directory, "reports")

    # Create the "reports" folder if it doesn't exist
    if not os.path.exists(reports_directory):
        os.makedirs(reports_directory)

    # Save the PDF file with a dynamic name including the current month and year
    pdf_output_name = f"Analysis_{current_month}_{current_year}.pdf"
    pdf_output_path = os.path.join(reports_directory, pdf_output_name)

    c = canvas.Canvas(output_pdf_name or pdf_output_path, pagesize=A4)

    page_width, page_height = A4

    # Separate the predicted images from the historical images
    predicted_images = [image_file for image_file in image_files if image_file.startswith("Predicted")]
    historical_images = [image_file for image_file in image_files if image_file.startswith("Variable")]

    # Remove the predicted images from the historical_images list
    historical_images = [image_file for image_file in historical_images if image_file not in predicted_images]

    # Add remaining files to the "Prediction Analysis" section
    remaining_files = [image_file for image_file in image_files if image_file not in predicted_images and image_file not in historical_images]
    predicted_images += remaining_files

    # Section 1: Historical Analysis
    if historical_images:
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, page_height - 50, "Historical Analysis")

        for image_file in historical_images:
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

            c.showPage()

            # Print the name of the image that was included in the PDF - validation
            print(f"Included image in Historical Analysis: {image_file}")

        # Execute cost_efficiency.py and include the output in the PDF
        efficiency_output = execute_cost_efficiency_script()
        c.setFont("Helvetica", 12)
        c.drawString(50, page_height - 100, "Cost Efficiency Output:")
        y_offset = page_height - 120
        for line in efficiency_output.split('\n'):
            c.drawString(70, y_offset, line)
            y_offset -= 20

    # Section 2: Prediction Analysis
    if predicted_images:
        c.showPage()
        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, page_height - 50, "Prediction Analysis")

        for image_file in predicted_images:
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

            c.showPage()

            # Print the name of the image that was included in the PDF - validation
            print(f"Included image in Prediction Analysis: {image_file}")

    c.save()

    print(f"PDF file saved at: {pdf_output_path}")

if __name__ == "__main__":
    image_directory = "results"

    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Combine the script's directory with the image_directory to get the absolute path of the image directory
    image_directory_absolute = os.path.join(script_directory, image_directory)

    convert_images_to_pdf(image_directory_absolute)
