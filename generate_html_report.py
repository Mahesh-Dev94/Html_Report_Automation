import os
import json
from datetime import datetime
import webbrowser

# ✅ TELEMETRY DATA path for local execution
TELEMETRY_DATA_PATH = os.path.join(os.getcwd(), "../", "telemetry_data")
# ✅ TELEMETRY DATA path for local execution in Windows systems
# TELEMETRY_DATA_PATH ="C:\\TTS_HOME\\bin\\invest\\src\\Results" 

def get_latest_folders(limit=5):
    """Get the latest 'limit' folders sorted by latest update time (only folders with results.json)."""
    folders = []

    if not os.path.exists(TELEMETRY_DATA_PATH):
        return []  # Return an empty list if directory doesn't exist

    for folder in os.listdir(TELEMETRY_DATA_PATH):
        folder_path = os.path.join(TELEMETRY_DATA_PATH, folder)
        results_file = os.path.join(folder_path, "results.json")

        if os.path.isdir(folder_path) and os.path.exists(results_file):  # ✅ Check if results.json exists
            creation_time = os.path.getctime(folder_path)  
            modification_time = os.path.getmtime(folder_path)  

            file_modification_time = os.path.getmtime(results_file)
            modification_time = max(modification_time, file_modification_time)

            latest_time = max(creation_time, modification_time)
            folders.append((folder, latest_time))

    latest_folders = sorted(folders, key=lambda x: x[1], reverse=True)[:limit]
    return [folder[0] for folder in latest_folders]


def get_telemetry_data():
    """Fetch telemetry data from latest valid folders (folders with results.json)."""
    result = {}
    latest_folders = get_latest_folders()

    for folder in latest_folders:
        file_path = os.path.join(TELEMETRY_DATA_PATH, folder, "results.json")

        if os.path.exists(file_path):  # ✅ Check again before reading
            with open(file_path, "r") as file:
                result[folder] = json.load(file)

    return {"folders": list(result.keys()), "data": result}  # ✅ Return only folders that have data


def is_number(value):
    """Check if the given value can be converted to a float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def generate_html_report():
    """Generate an HTML report with interactive Chart.js visualization."""
    telemetry_data = get_telemetry_data()
    folders = telemetry_data["folders"]
    data = telemetry_data["data"]

    # ✅ HTML Header and Table
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telemetry Data Dashboard</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>

        <style>
          /* Header Styling */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            background-color: #004b87;
            color: white;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        }

        .header h1 {
            font-size: 22px;
            margin: 0;
        }

        .logo {
            height: 40px;
        }
            body {
            font-family: 'Arial', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }
            .container {
            display: flex;
            flex-direction: row;
            padding: 10px;
        }
            .table-container {
            width: 65%;
            background: white;
            padding: 10px;
            border-radius: 8px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
			overflow-x: auto; /* ✅ Enables horizontal scrolling */
            max-height: 70vh; /* ✅ Set a max height*/
            max-width: 60%;
            overflow-y: auto; /* ✅ Enables vertical scrolling */
        }
            .chart-container {
            width: 35%;
            display: flex;
            justify-content: center;
            align-items: center;
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
            margin-left: 20px;
            max-height: 500px; /* ✅ Set a max height*/

        }
            table {
            width: 100%;
            border-collapse: collapse;
            min-width: 800px; /* ✅ Avoids breaking UI */
        }
            th, td {
            padding: 18px 10px;
            text-align: left; /* ✅ Aligns text left */
            border-bottom: 1px solid #ddd;
            white-space: nowrap; /* ✅ Prevents text wrapping */
        }
            th {
            background-color: #0071c5;
            color: white;
        }
            tr:hover {
            background-color: #eef7ff;
            cursor: pointer;
        }
            .selected-row {
            background-color: #d8eafd !important;
        }
        /* Footer */
        .footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 40px;
            background-color: #004b87;
            color: white;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        </style>
    </head>
    <body>
       <div class="header">
         <h1>Telemetry Data Dashboard</h1>
         <img src="data:image/png;base64,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" alt="Hotwire Communications" class="logo">
      </div>
        <div class="container">
            <div class="table-container">
                <table id="telemetryTable">
                    <tr>
                        <th>ID</th>
                        <th>Description</th>
    """

    test_cases = {}
    for folder, build_data in data.items():
        for test in build_data:
            test_id = test.get("ID", "Unknown")
            description = test.get("description", "No Description")
            duration = test.get("Duration", "N/A")

            if test_id not in test_cases:
                test_cases[test_id] = {"Description": description, "Results": {}}
            test_cases[test_id]["Results"][folder] = duration

    # Format folders for table headers and chart labels
    folder_labels = []
    for folder in folders:
        try:
            dt = datetime.strptime(folder, "%Y%m%d%H%M%S")  # Try parsing as timestamp
            formatted_folder = dt.strftime("%d %b, %I:%M %p")
        except ValueError:
            formatted_folder = folder  # Use original if format is incorrect
        folder_labels.append(f"Test ({formatted_folder})")
    
       # Format labels for chart (Test 1, Test 2, ...)
    chart_labels = []
    for i, _ in enumerate(folders):
        chart_labels.append(f"Test {i + 1}")

    # Add columns for each folder (build)
    for label in folder_labels:
        html_content += f"<th>{label}</th>"
    html_content += "</tr>"

    test_case_data = []
    for test_id, test_info in test_cases.items():
        case_data = {
            "id": test_id,
            "description": test_info["Description"],
            "results": test_info["Results"],
        }
        test_case_data.append(case_data)

    for case in test_case_data:
     html_content += f"<tr><td>{case['id']}</td><td>{case['description']}</td>"
     for folder in folders:
        result = case["results"].get(folder, "N/A")

        if result == "N/A":  # Show ✗ N/A in red
            html_content += f"<td style='color: red;'>✗ N/A</td>"
        elif result.startswith("$"):  # Show ✗ FAIL in red for values starting with $
            html_content += f"<td style='color: red;'>✗ FAIL</td>"
        else:  # Otherwise, show result in green with a checkmark
            html_content += f"<td style='color: green;'>✔ {result}</td>"

     html_content += "</tr>"


    html_content += """
                </table>
            </div>
            <div class="chart-container">
                <canvas id="telemetryChart" width="400" height="200"></canvas>
            </div>
        </div>
        <div class="footer"></div>
    """

    # ✅ JavaScript for Chart.js Visualization
    html_content += f"""
    <script>
         // Chart is likely available as just "Chart"
    // You need to CONFIRM the global variable name for the plugin. 
    // It MIGHT be ChartAnnotation, or something else. Check the plugin's documentation!
       if (window.ChartAnnotation) {{ 
            Chart.register(window.ChartAnnotation); 
    
        }} else {{
            console.error("Chart Annotation plugin not found!"); 
        }}
        const testCaseData = {json.dumps(test_case_data)};
        const folders = {json.dumps(folders)};
        const folderLabels = {json.dumps(folder_labels)};
        const chartLabels={json.dumps(chart_labels)};
        let chartInstance = null;
        let selectedRow = null;
        //--------------------------------------------
        
        function updateChart(testCase) {{
            const ctx = document.getElementById('telemetryChart').getContext('2d');
                let annotations = []; 
                let tempData = []; // Temporary array to store values before calculating min

                const data = folders.map((folder, index) => {{
                    const result = testCase.results[folder];
                    const parsedResult = isNaN(parseFloat(result)) ? 0 : parseFloat(result.split(" ")[0]);

                    tempData.push(parsedResult); // Store for min calculation

                    let annotationContent = '';

                    if (typeof result === 'string' && result.startsWith('$')) {{
                        annotationContent = 'FAIL';
                    }} else if (result === 'N/A' || result === null || result === undefined || result === "") {{
                        annotationContent = 'N/A';
                    }}

                    return parsedResult; // Store the processed data
                }});

                folders.forEach((folder, index) => {{
                    const result = testCase.results[folder];

                    let annotationContent = '';
                   // let val

                    if (typeof result === 'string' && result.startsWith('$')) {{
                        annotationContent = 'FAIL';
                    }} else if (result === 'N/A' || result === null || result === undefined || result === "") {{
                        annotationContent = 'N/A';
                    }}

                    if (annotationContent !== '') {{
                    const yOffset = 0.15;
                    const maxYValue = Math.max(...tempData);
                    // ✅ Use maxYValue as a placeholder for yValue
                    // const safeYValue = maxYValue <= 1 ? 0.05 : yOffset;
             
                    let safeYValue=0;
                    if( maxYValue <= 0.5){{
                      safeYValue= 0.02
                    }}else if (maxYValue <=1  && maxYValue >= 0.5){{
                    safeYValue= 0.05
                    }} else if(maxYValue <= 3 && maxYValue >= 1) {{
                     safeYValue= 0.07
                    }}
                    else if(maxYValue <= 5){{
                      safeYValue= 0.15
                    }}else{{
                      safeYValue= 0.25
                    }}

                       console.log('maxYValue---',maxYValue,'safeYValue--',safeYValue,'tempData---',JSON.stringify(tempData),)
                         annotations.push({{
                            clip: false,
                            type: 'label',
                            xValue: chartLabels[index], // Keep aligned with the column
                            yValue: safeYValue,  //  ✅  Set yValue (even though we override draw)
                            content: annotationContent,
                            borderRadius: 5,
                            color: (annotationContent === 'FAIL' || annotationContent === 'N/A') ? 'red' : 'green',
                            font: {{
                                size: 10
                            }},
                            textAlign: 'center',
                        }});
                     }}
                }});


            if (chartInstance) {{
                chartInstance.destroy();
            }}

            chartInstance = new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: chartLabels,
                    datasets: [{{
                        label: testCase.description,
                        data: data,
                        backgroundColor: ['#6CB8BF', '#97C7E8', '#C1E2E3', '#f59fa7'],
                        borderWidth: 1,
                        borderRadius: 10,
                        barThickness: 45,
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {{
                        duration: 1000,
                        easing: 'easeOutBounce'
                    }},
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: 'Duration (seconds)'
                            }}
                        }},
                        x: {{
                            title: {{
                                display: true,
                                text: 'Build Versions'
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            display: true,
                            position: 'bottom',
                            labels: {{
                                font: {{ size: 14 }},
                                usePointStyle: true,
                                pointStyle: 'rect',
                            }}
                        }},
                       annotation: {{
                           annotations:annotations
                      }},
                      
                    }}
                }}
            }});
        }}


   //-----------------------------------------------------------------------------
        // Show first row data by default
        const tableRows1 = document.querySelectorAll('#telemetryTable tbody tr');
        if (testCaseData.length > 0) {{
            updateChart(testCaseData[0]);
            if (tableRows1.length > 1) {{
                tableRows1[1].classList.add('selected-row');
                selectedRow = tableRows1[1];
            }}
        }}

        // Add click event listeners to table rows
         const tableRows = document.querySelectorAll('#telemetryTable tbody tr');
        tableRows.forEach((row, index) => {{
            row.addEventListener('click', () => {{
                if (selectedRow) {{
                    selectedRow.classList.remove('selected-row');
                }}
                row.classList.add('selected-row');
                selectedRow = row;
                updateChart(testCaseData[index-1]);
            }});
        }});
    </script>
    """

 
    html_content += "</body></html>"
    # Generate an incremental filename
    report_dir = "html_report"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)  # Create the directory if it doesn't exist

    i = 1
    while True:
        random_filename = os.path.join(report_dir, f"telemetry_report_{i}.html")
        if not os.path.exists(random_filename):
            break
        i += 1
    try:
        with open(random_filename, "w", encoding="utf-8") as report_file:
            report_file.write(html_content)
        print("✅ Telemetry report generated:" + random_filename)
        webbrowser.open("file://" + os.path.realpath(random_filename))  # Open the file in the default browser
    except OSError as e:
        print(f"❌ Error writing report: {e}")	  

def main():
    """Main function to generate telemetry report."""
    generate_html_report()

if __name__ == "__main__":
    main()