# SVRF Layout Analyzer Tool

This is a Python-based tool for analyzing GDS layouts and SVRF rule files for DRC regression test validation. It:
- Parses SVRF rule files (extracts rule names and comments)
- Analyzes GDS layout files using [gdstk]
- Validates patterns (good/bad cases) against DRC results
- Generates detailed HTML and Excel reports
- Progress reporting via terminal with `tqdm`

Features:
- --gui option to launch a Tkinter-based graphical interface
- User-friendly interface for input selection and process execution
- Loading popup to prevent GUI from freezing during execution
- Real-time progress indicators and status updates
- Interactive result tables powered by JavaScript
  - Pagination support
  - Selectable individual results
  - PDF export for selected results
  - CSV export for selected results
  - Toggleable night mode via checkbox
- Feature-based Git repository with structured commits
- GitHub repository with Actions for automated unit testing (local runner supported)
- regression_runner shell script for easy system-wide execution



## Setup

```bash
pip install -r requirements.txt



## Project Structure

svrf_analyzer/
├── README.md
├── requirements.txt
├── setup.py
├── bin/
│   └── regression_runner.sh
├── src/
│   ├── svrf_parser.py
│   ├── gds_analyzer.py
│   ├── report_generator.py
│   ├── gui/
│   │   └── main_window.py
│   ├──utils/
│       └── create_gds.py
├── tests/
│   ├── test_pattern_validator.py
│   ├── test_svrf_parser.py
│   ├── test_gds_analyzer.py
│   └── test_report_generator.py
|
└── docs/
│       └── regression_runner.ppt
│
├── input_files/
│    ├── gds_testcases
│    │   ├── regression.gds
│    │   └── regression_2.gds
│    ├── svrf_files
│        └── rules.svrf  
│
├── out_reports/

*******************************************

Usage:

    Running the Script With Command Line
          To execute the script using CLI, use the following command:
              python setup.py --layout_dir ./input_files/gds_testcases --svrf_file ./input_files/svrf_files/rules.svrf --output_dir ./out_reports --report_type both
          
          Explanation of Arguments:
          
              --layout_dir
              Specifies the directory containing input GDS test cases or layout files. These are the designs to be analyzed.
          
              --SVRF_file
              Path to the SVRF-style rule file (rules.svrf) containing design validation rules and constraints.
          
              --output_dir
              Directory where the generated reports will be saved. This folder will be created if it doesn't exist.
          
              --report_type
              Specifies the format(s) of the output report. Available options include:
          
                  html: Generates an HTML report.
          
                  excel: Generates a Excel report.
          
                  both: Generates both HTML and Excel reports.
                  
                  Default value is both
                  
              --report_name 
	              (Optional) Allowing the user to specify a custom name for the 
	              output report (HTML and Excel formats). Otherwise, Name will be
	              determined by the script.
                  
                  
    Running the Script using GUI
        To execute the script using GUI, use the following command: 
              python setup.py --gui                                                                                               
                                                                                                                                                                   
        Explanation of Arguments:    
                  --gui: To load the GUI window  
                  
                  
    Running via Bash Script (regression_runner.sh)             
        Alternatively, you can use the provided bash script to run the program:
             regression_runner.sh --layout_dir ./input_files/gds_testcases --svrf_file ./input_files/svrf_files/rules.svrf --output_dir ./out_reports --report_type both  
             
             it take same arguments as setup.py                                                                                                              

        To run the script from anywhere in your terminal, add its directory to your system PATH. Here's how to do that:
              export PATH=$PATH:/path/to/regression_runner.sh_directory
        
        You can add this line to your shell profile file (e.g., .bashrc, .zshrc, or .bash_profile) to make it permanent:
                 echo 'export PATH=$PATH:/path/to/regression_runner.sh_directory' >> ~/.bashrc
                 source ~/.bashrc
                 
        Replace /path/to/regression_runner.sh_directory with the actual path to the folder containing regression_runner.sh
        
        



Output:
    Reports are generated in the specified --output_dir (default: ./out_reports/):
    report.html – summary of each rule, layout, and validation result
    report.xlsx – Excel with detailed breakdown
    if run from the gui, a log file will be generated in the output directory



Testing:
    Run unit tests using:
        python -m unittest discover tests






