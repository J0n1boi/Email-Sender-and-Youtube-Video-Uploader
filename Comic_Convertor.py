import subprocess
import os
from datetime import datetime

# Path to your HTML file
html_file = r'C:/Users/jonat/OneDrive/Desktop/Cool Scripts/Comic Getter/daily_comics.html'

# Path to Chrome executable (you need to specify the correct path for your system)
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'  # This is the default path

# Folder to save the PDF
save_folder = r'G:\My Drive\Comic Getter'

# Ensure the folder exists
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Get today's date in the format YYYY-MM-DD
today_date = datetime.now().strftime("%Y-%m-%d")

# Create the PDF filename using today's date
pdf_filename = os.path.join(save_folder, f"{today_date}.pdf")

# Check if Chrome exists at the specified path
if os.path.exists(chrome_path):
    # Build the command to run Chrome in headless mode and save as PDF
    command = [
        chrome_path,
        '--headless',  # Run Chrome in headless mode (no UI)
        '--disable-gpu',  # Disable GPU hardware acceleration
        '--no-sandbox',  # Ensure that it runs in sandbox mode
        '--print-to-pdf',  # Tell Chrome to save the page as PDF
        f'--print-to-pdf={pdf_filename}',  # Specify the output PDF file path
        f'file:///{os.path.abspath(html_file)}'  # Open the HTML file
    ]

    # Run the command
    subprocess.run(command)

    print(f"PDF saved to: {pdf_filename}")
else:
    print("Chrome not found. Please check the path to Chrome.")
