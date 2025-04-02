# Automation Test Report Generator

This project consists of a Python script and a Flask API for generating and serving HTML reports from automation testing results.

## Overview

The project automates the process of taking data from your automation testing process and converting it into a user-friendly HTML report.  It involves two main components:

1.  **Python Script (`generate_html_report.py`):** This script processes the raw test results.  It is designed to:
    * Scan a directory for test result files.
    * Parse the relevant data from these files.
    * Generate an HTML report.
    * Save the HTML report to a specified location.

2.  **Flask API (Conceptual):** While the provided code focuses on *generating* the report, a Flask API would be used to *serve* the generated HTML report.  This allows you to access the report through a web browser.

## Key Features

* **Automated Report Generation:** The Python script automates the creation of HTML reports, saving you the effort of manually creating them.
* **Customizable Report Structure:** The script provides a foundation for structuring your HTML report. You can customize the HTML template to match your specific needs.
* **Web Access to Reports (via Flask):** The Flask API (which you would need to add) enables you to view the generated reports from any device with a web browser.
* **Modular Design:** The Python script is separate from the (conceptual) Flask API, allowing for flexibility in how the reports are generated and served.

## How It Works (Detailed)

### 1. Python Script: `generate_html_report.py`

   A.  **Configuration:**
       * The script begins with configuration settings, including the path to the test results directory (`test_case_folder`) and the output HTML file name (`html_file_name`).  These should be set according to your environment.

   B.  **Data Processing:**
       * The script uses `os.walk` to traverse the directory specified by `test_case_folder`.  This allows it to find all relevant test result files within the directory structure.
       * For each test case folder found, the script extracts the folder name and description.
       * It then iterates through a set of predefined folders (likely representing different test runs or environments).
       * For each of these folders, it attempts to read a result from a file named after the folder.
       * The script handles potential file reading errors (`try...except` block).  If a file is not found, the result is recorded as "N/A".
       * The script also handles cases where the result might be a file path (which it attempts to read) or a direct value.
       * It appears the script is looking for specific files within each test case folder, such as  `'Test (25 Mar, 02:37 PM)'`,  `'Test (25 Mar, 02:01 PM)'`

   C.  **HTML Report Generation:**
       * The script uses an f-string to construct the HTML report.  This allows for dynamic insertion of the processed test data into the HTML structure.
       * The HTML structure includes:
           * A title ("Telemetry Data Dashboard") and basic styling.
           * A table to display the test case results, with columns for "ID", "Description", and the results from different folders.
           * JavaScript code to:
               * Dynamically update a chart based on the selected table row.
               * Handle table row selection.
               * Include placeholder chart data and labels.
       * The script writes the generated HTML content to the file specified by `html_file_name`.

### 2. Flask API (Conceptual)

   To make this report accessible via a web browser, you would typically use a framework like Flask.  Here's a conceptual outline:

   D.  **Flask Setup:**
       * Import the Flask library.
       * Create a Flask application instance.
   E. **Route for Serving the Report:**
       * Define a route (e.g., `/report`) that, when accessed:
           * Reads the generated HTML file.
           * Returns the HTML content as the response.
   F.  **Running the Flask App:**
        * Run the Flask application, which starts a web server.

## How to Use

### Prerequisites

* **Python 3.x:** Ensure you have Python 3 installed.
* **Chart.js:** The generated HTML report uses Chart.js.  The script assumes Chart.js is available.  You may need to ensure  Chart.js is installed or linked in your HTML.
* **Test Results Data:** You need to have your automation test results saved in a directory structure that the script can understand.  This structure is implied by the script's code.

### 1.  Prepare Your Test Results

   * Organize your test results in a directory structure that matches what the script expects.  Based on the script, it seems the structure is:
       ```
       test_case_folder/
           TestCaseName/
               Test (Date, Time)/result_file.txt  (or result_value)
       ```
       Where:
       * `test_case_folder` is the base directory you will provide to the script.
       * `TestCaseName` is the name of a specific test case.
       * `Test (Date, Time)`  are subfolders with the time of the test run.
       * `result_file.txt` contains the test result (or the result may be directly written as a value instead of a file).

### 2.  Configure the Script

   * Open the `generate_html_report.py` script.
   * Modify the `test_case_folder` variable to point to the directory where your test results are stored:
       ```python
       test_case_folder = "/path/to/your/test/results"  #  <-- CHANGE THIS
       ```
   * Modify the `folders` list to match the names of the folders you want to process.
       ```python
       folders = ["Test (25 Mar, 02:37 PM )", "Test (25 Mar, 02:01 PM )"] # <-- Change this
       ```
   * (Optional) Change the output HTML file name if needed:
       ```python
       html_file_name = "telemetry_report.html"
       ```

### 3.  Run the Script

   * Open a terminal or command prompt.
   * Navigate to the directory where you saved the `generate_html_report.py` script.
   * Execute the script:
       ```bash
       python generate_html_report.py
       ```
   * The script will generate the HTML report and save it to the specified `html_file_name`.

### 4.  Serve the Report (Conceptual - Requires Flask)

    * To serve the report over the web, you would create a Flask application.
    * Save the following code as `app.py` (or a similar name):
    ```python
    from flask import Flask, send_file

    app = Flask(__name__)

    @app.route("/report")
    def get_report():
        report_path = "telemetry_report.html"  #  Make sure this matches your output file name
        return send_file(report_path)

    if __name__ == "__main__":
        app.run(debug=True)  #  Use debug=False in production
    ```
    * Make sure you have Flask installed (`pip install Flask`)
    * Run the Flask application:
        ```bash
        python app.py
        ```
    * Open your web browser and go to `http://127.0.0.1:5000/report` (or the appropriate URL) to view the report.

## Customization

* **HTML Template:** You can customize the structure and styling of the generated HTML report by modifying the HTML string in the `generate_html_report.py` script.  You can add CSS, JavaScript, and any other HTML elements you need.
* **Data Processing:** You can modify the script to parse different test result formats or extract different data fields.  You'll need to adjust the file reading and data extraction logic within the script.
* **Flask API:** You can extend the Flask API to:
    * Store reports.
    * Implement user authentication.
    * Provide an interface to select and view different reports.

## Dependencies

* Python 3.x
* Flask (for serving the report - conceptual)
* Chart.js (for the chart in the HTML report)
