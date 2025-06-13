import argparse
import os
from tqdm import tqdm
import socket
import datetime

from src.svrf_parser import parse_svrf_rules
from src.gds_analyzer import load_gds_layout, extract_markers, associate_rules_to_patterns
from src.pattern_validator import validate_patterns
from src.report_generator import generate_reports

def main():
    parser = argparse.ArgumentParser(description="SVRF Layout Analysis Tool")
    parser.add_argument("--layout_dir", required=True, help="Directory containing GDS files")
    parser.add_argument("--svrf_file", required=True, help="SVRF rules file path")
    parser.add_argument("--output_dir", default="output_reports", help="Directory to save reports")
    parser.add_argument("--report_type", default="both", help="Output report type. Available values: html, excel, both. Default is both")
    parser.add_argument("--report_name", default="None", help="(optional) Name of the output reports")
    args = parser.parse_args()

    print("\n")
    print("\n[1/4] Parsing SVRF rule file...\n")
    rules = parse_svrf_rules(args.svrf_file)
    print(f"Parsed {len(rules)} rules.")
    print("\n")

    print("[2/4] Loading and analyzing layout files...")
    layouts = [f for f in os.listdir(args.layout_dir) if f.endswith(".gds")]

    all_results = {}

    for layout_file in tqdm(layouts, desc="\nAnalyzing layouts"):
        layout_path = os.path.join(args.layout_dir, layout_file)
        cells = load_gds_layout(layout_path)
        for cell in cells:

            # Extract result markers (layer 0.1)
            markers = extract_markers(cell).get((0, 1), [])

            # print("checking cell", cell.name)

            # Associate rule groups (polygons on layer 255.1) to rule names (texts on layer 22.22) and collect patterns (polygons on the pattern marking layer 255.0)
            rule_map = associate_rules_to_patterns(cell)

            # print("rule map of ", cell.name, "is", rule_map)

            for rule in rules:
                rule_name = rule['check name']
                if rule_name not in all_results:
                    all_results[rule_name] = {
                        'comment': rule['comment'],
                        'files': {}
                    }

                patterns_for_rule = rule_map.get(rule_name, [])
                validation_result = validate_patterns(rule_name, patterns_for_rule, markers)

                # Store result by gds_file and cell name
                all_results[rule_name]['files'].setdefault(layout_file, {})[cell.name] = validation_result

    print("\n")
    print("[3/4] Generating reports...")





    # Prepare detailed data
    good_patterns=[]
    bad_patterns=[]
    all_patterns=[]
    detailed_data = []
    for rule_name, rule_info in all_results.items():
        comment = rule_info['comment']
        for layout_file, cell_results in rule_info['files'].items():
            for cell_name, result in cell_results.items():
                detailed_data.append({
                    "Rule Name": rule_name,
                    "Good Patterns": result['good']['pass'] + result['good']['fail'],
                    "Bad Patterns": result['bad']['pass'] + result['bad']['fail'],
                    "Passed Good": result['good']['pass'],
                    "Failed Good": result['good']['fail'],
                    "Passed Bad": result['bad']['pass'],
                    "Failed Bad": result['bad']['fail'],
                    "Rule Comment": comment,
                    "Fail Pattern Location": f"{layout_file} / {cell_name}"
                })
                good_patterns.append(result['good']['pass'] + result['good']['fail'])
                bad_patterns.append(result['bad']['pass'] + result['bad']['fail'])
                all_patterns.append(result['good']['pass'] + result['good']['fail'] + result['bad']['pass'] + result['bad']['fail'])





    # Prepare summary data
    good_patterns_sum = sum(good_patterns)
    bad_patterns_sum = sum(bad_patterns)
    all_patterns_sum = sum(all_patterns)


    # overall_status = "Passed" if all(sts == 0 for sts in failed_good_bad) else "Failed"
    overall_status = f"{good_patterns_sum} Passed and {bad_patterns_sum} Failed out of {all_patterns_sum} patterns"

    summary_data = {
        "Host Name": socket.gethostname(),
        "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Input Files": f"{args.svrf_file}, {', '.join(layouts)}",
        "Overall Status": overall_status
    }

    generate_reports(summary_data, detailed_data, args.output_dir, args.report_type, args.report_name)

    print("\n")
    print("\n[4/4] Done\n")
    print("\n")

    # print("good patterns",good_patterns, " sum= ", good_patterns_sum, "\n")
    # print("bad patterns",bad_patterns, " sum ", bad_patterns_sum, "\n")
    # print("total patterns",all_patterns, " sum ", all_patterns_sum, "\n")

# GUI Mode Integration
if __name__ == "__main__":
    import sys
    if "--gui" in sys.argv:
        import tkinter as tk
        from src.gui.main_window import SVRFAnalyzerGUI

        root = tk.Tk()
        app = SVRFAnalyzerGUI(root)
        root.mainloop()
    else:
        main()
