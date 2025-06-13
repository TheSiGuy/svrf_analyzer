import os
from datetime import datetime
import pandas as pd


def generate_reports(summary_data, detailed_data, output_dir, report_type, report_name):
    """
    Generate enhanced HTML and Excel reports for the SVRF layout analysis results.

    Returns:
        tuple: (html_report_path, excel_report_path)
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if report_name=="None":
        html_report_path = os.path.join(output_dir, f"report_{timestamp}.html")
        excel_report_path = os.path.join(output_dir, f"report_{timestamp}.xlsx")
    else:
        html_report_path = os.path.join(output_dir, f"{report_name}.html")
        excel_report_path = os.path.join(output_dir, f"{report_name}.xlsx")


    # Generate HTML report
    if report_type=="html" or report_type=="both":
        with open(html_report_path, "w", encoding="utf-8") as f:
            f.write("<html><head><title>SVRF Analysis Report</title>\n")

            # CSS & JS
            f.write("""
            <link rel="stylesheet" href="https://cdn.datatables.net/1.13.6/css/jquery.dataTables.min.css">
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="https://cdn.datatables.net/1.13.6/js/jquery.dataTables.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.28/jspdf.plugin.autotable.min.js"></script>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 20px;
                    background-color: white;
                    color: black;
                }
                body.dark-mode {
                    background-color: #121212;
                    color: #e0e0e0;
                }
                .dark-mode table {
                    color: #e0e0e0;
                    border-color: #555;
                }
                .dark-mode th {
                    background-color: #333;
                }
                table {
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 30px;
                }
                th, td {
                    border: 1px solid #ccc;
                    padding: 8px;
                    text-align: left;
                }
                th {
                    background-color: #f2f2f2;
                }
                button, label {
                    margin: 10px 5px;
                    padding: 8px 12px;
                }
            </style>
            """)

            f.write("</head><body>\n")
            f.write("<h1>SVRF Layout Analysis Report</h1>\n")

            # Summary
            f.write("<h2>Summary Information</h2>\n")
            f.write("<table>\n")
            for key, value in summary_data.items():
                f.write(f"<tr><th>{key}</th><td>{value}</td></tr>\n")
            f.write("</table>\n")

            # Controls
            f.write("""
            <h2>Detailed Analysis Results</h2>
            <button id="exportBtn">Export Selected to PDF</button>
            <button id="csvBtn">Export Selected to CSV</button>
            <label><input type="checkbox" id="toggleDark"> Dark Mode</label>
            """)

            # Detailed table
            if detailed_data:
                f.write('<table id="resultsTable">\n<thead><tr>')
                headers = detailed_data[0].keys()
                for header in headers:
                    f.write(f"<th>{header}</th>")
                f.write("</tr></thead>\n<tbody>\n")
                for row in detailed_data:
                    f.write("<tr>")
                    for header in headers:
                        f.write(f"<td>{row.get(header, '')}</td>")
                    f.write("</tr>\n")
                f.write("</tbody></table>\n")
            else:
                f.write("<p>No detailed data available.</p>\n")

            # JavaScript for interactivity
            f.write("""
            <script>
            $(document).ready(function () {
                const table = $('#resultsTable').DataTable({
                    paging: true,
                    select: {
                        style: 'multi'
                    }
                });
        
                // Row selection
                $('#resultsTable tbody').on('click', 'tr', function () {
                    $(this).toggleClass('selected');
                });
        
                // PDF export
                $('#exportBtn').click(function () {
                    const { jsPDF } = window.jspdf;
                    const doc = new jsPDF();
                    const selectedRows = [];
        
                    $('#resultsTable tbody tr.selected').each(function () {
                        const rowData = [];
                        $(this).find('td').each(function () {
                            rowData.push($(this).text());
                        });
                        selectedRows.push(rowData);
                    });
        
                    if (selectedRows.length === 0) {
                        alert("No rows selected!");
                        return;
                    }
        
                    const headers = [];
                    $('#resultsTable thead th').each(function () {
                        headers.push($(this).text());
                    });
        
                    doc.autoTable({
                        head: [headers],
                        body: selectedRows
                    });
        
                    doc.save('Selected_Results.pdf');
                });
        
                // CSV export
                $('#csvBtn').click(function () {
                    const selectedRows = [];
                    $('#resultsTable tbody tr.selected').each(function () {
                        const rowData = [];
                        $(this).find('td').each(function () {
                            rowData.push('"' + $(this).text().replace(/"/g, '""') + '"');
                        });
                        selectedRows.push(rowData.join(','));
                    });
        
                    if (selectedRows.length === 0) {
                        alert("No rows selected!");
                        return;
                    }
        
                    const headers = [];
                    $('#resultsTable thead th').each(function () {
                        headers.push('"' + $(this).text() + '"');
                    });
        
                    const csvContent = [headers.join(',')].concat(selectedRows).join('\\n');
                    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                    const link = document.createElement("a");
                    link.href = URL.createObjectURL(blob);
                    link.download = "Selected_Results.csv";
                    link.click();
                });
        
                // Dark mode toggle
                $('#toggleDark').change(function () {
                    $('body').toggleClass('dark-mode', this.checked);
                });
        
                // Failed filter
                $('#filterFailed').change(function () {
                    if (this.checked) {
                        table.rows().every(function () {
                            const failedGood = parseInt($(this.node()).find('td:eq(5)').text() || 0);
                            const failedBad = parseInt($(this.node()).find('td:eq(7)').text() || 0);
                            if (failedGood === 0 && failedBad === 0) {
                                $(this.node()).hide();
                            } else {
                                $(this.node()).show();
                            }
                        });
                    } else {
                        table.rows().every(function () {
                            $(this.node()).show();
                        });
                    }
                });
            });
            </script>
            """)
            f.write("</body></html>\n")
    else:
        pass

        

    print(f"\nReports generated:\n")

    if report_type == "html" or report_type == "both":
        print(f"- HTML report: {html_report_path}\n")
    else:
        pass

    # Generate Excel report
    if report_type=="excel" or report_type=="both":
        with pd.ExcelWriter(excel_report_path) as writer:
            df_summary = pd.DataFrame(list(summary_data.items()), columns=["Metric", "Value"])
            df_summary.to_excel(writer, sheet_name="Summary", index=False)

            if detailed_data:
                df_details = pd.DataFrame(detailed_data)
                df_details.to_excel(writer, sheet_name="Detailed Results", index=False)

        print(f"- Excel report: {excel_report_path}\n")
    else:
        pass

    if report_type not in ("html", "excel", "both"):
        print("No reports generated")
        print("Report type should be 'html', 'excel', or 'both'.")
    else:
        pass


    return html_report_path, excel_report_path


# if __name__ == "__main__":
#     # Example usage
#     summary_example = {
#         "Host Name": "test-machine",
#         "Timestamp": "2025-06-07 12:34:56",
#         "Input Files": "rules.svrf, regression.gds",
#         "Overall Status": "Partial Pass"
#     }
#
#     detailed_example = [
#         {
#             "Rule Name": "SpacingRule",
#             "Good Patterns": 5,
#             "Bad Patterns": 3,
#             "Passed Good": 5,
#             "Failed Good": 0,
#             "Passed Bad": 0,
#             "Failed Bad": 3,
#             "Rule Comment": "Minimum spacing check",
#             "Fail Pattern Location": "regression.gds, Cell_1"
#         },
#         {
#             "Rule Name": "WidthRule",
#             "Good Patterns": 4,
#             "Bad Patterns": 2,
#             "Passed Good": 4,
#             "Failed Good": 0,
#             "Passed Bad": 0,
#             "Failed Bad": 2,
#             "Rule Comment": "Minimum width check",
#             "Fail Pattern Location": "regression_2.gds, Cell_2"
#         },
#         {
#             "Rule Name": "NoFailureRule",
#             "Good Patterns": 3,
#             "Bad Patterns": 0,
#             "Passed Good": 3,
#             "Failed Good": 0,
#             "Passed Bad": 0,
#             "Failed Bad": 0,
#             "Rule Comment": "No violations",
#             "Fail Pattern Location": ""
#         }
#     ]
#
#     generate_reports(summary_example, detailed_example, output_dir="output_reports")
