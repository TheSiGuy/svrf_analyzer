import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, scrolledtext, ttk
import threading
import os
import sys
import io
import subprocess
from datetime import datetime
from setup import main as run_analysis


class RedirectText(io.TextIOBase):
    def __init__(self, text_widget, log_file_path=None):
        super().__init__()
        self.text_widget = text_widget
        self.log_file_path = log_file_path

    def write(self, s):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, s)
        self.text_widget.see(tk.END)
        self.text_widget.config(state=tk.DISABLED)
        if self.log_file_path:
            with open(self.log_file_path, 'a', encoding='utf-8') as f:
                f.write(s)

    def flush(self):
        pass


class SVRFAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SVRF Layout Analyzer")

        self.layout_dir = tk.StringVar()
        self.svrf_file = tk.StringVar()
        self.output_dir = tk.StringVar(value="output_reports")
        self.report_name = tk.StringVar(value="")
        self.options = ("html", "excel", "both")
        self.report_type = tk.StringVar(value="both")
        self.loading_popup = None
        self.progress_bar = None
        self.console = None
        self.log_file_path = None
        self.html_report_path = None
        self.excel_report_path = None

        self._build_gui()

    def update_type(self, selected_value):
        self.report_type.set(selected_value)
        self.report_type_label.config(text=f"Selected Report Type: {self.report_type.get()}")

    def _build_gui(self):
        tk.Label(self.root, text="GDS Layout Directory:").grid(row=0, column=0, sticky='e')
        tk.Entry(self.root, textvariable=self.layout_dir, width=50).grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_layout_dir).grid(row=0, column=2)

        tk.Label(self.root, text="SVRF File:").grid(row=1, column=0, sticky='e')
        tk.Entry(self.root, textvariable=self.svrf_file, width=50).grid(row=1, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_svrf_file).grid(row=1, column=2)

        tk.Label(self.root, text="Output Directory:").grid(row=2, column=0, sticky='e')
        tk.Entry(self.root, textvariable=self.output_dir, width=50).grid(row=2, column=1)
        tk.Button(self.root, text="Browse", command=self.browse_output_dir).grid(row=2, column=2)

        tk.Label(self.root, text="Report Name (Optional):").grid(row=3, column=0, sticky='e')
        tk.Entry(self.root, textvariable=self.report_name, width=50).grid(row=3, column=1)

        tk.Label(self.root, text="Report Type:").grid(row=4, column=0, padx=10, pady=20)
        dropdown = tk.OptionMenu(self.root, self.report_type, *self.options, command=self.update_type)
        dropdown.grid(row=4, column=2, padx=10, pady=20)
        self.report_type_label = tk.Label(self.root, text=f"Selected Report Type: {self.report_type.get()}")
        self.report_type_label.grid(row=4, column=1, padx=10, pady=20)

        tk.Button(self.root, text="Run Analysis", command=self.run).grid(row=5, column=1, pady=20)

        tk.Label(self.root, text="Console Output:").grid(row=6, column=0, columnspan=3)
        self.console = scrolledtext.ScrolledText(self.root, height=12, width=90, state='disabled', font=("Courier", 10))
        self.console.grid(row=7, column=0, columnspan=3, padx=10, pady=5)

        self.view_log_btn = tk.Button(self.root, text="View Log File", command=self.open_log_file, state=tk.DISABLED)
        self.view_log_btn.grid(row=8, column=0, pady=(5, 15))

        self.view_html_btn = tk.Button(self.root, text="View HTML Report", command=self.open_html_report, state=tk.DISABLED)
        self.view_html_btn.grid(row=8, column=1, pady=(5, 15))

        self.view_excel_btn = tk.Button(self.root, text="View Excel Report", command=self.open_excel_report, state=tk.DISABLED)
        self.view_excel_btn.grid(row=8, column=2, pady=(5, 15))

    def _redirect_stdout(self):
        sys.stdout = RedirectText(self.console, self.log_file_path)
        sys.stderr = RedirectText(self.console, self.log_file_path)

    def browse_layout_dir(self):
        selected = filedialog.askdirectory()
        if selected:
            self.layout_dir.set(selected)

    def browse_svrf_file(self):
        selected = filedialog.askopenfilename(filetypes=[("SVRF files", "*.svrf")])
        if selected:
            self.svrf_file.set(selected)

    def browse_output_dir(self):
        selected = filedialog.askdirectory()
        if selected:
            self.output_dir.set(selected)

    def run(self):
        if not self.layout_dir.get() or not self.svrf_file.get():
            messagebox.showerror("Missing Input", "Please select both layout directory and SVRF file.")
            return

        output_dir = self.output_dir.get()
        report_type = self.report_type.get()
        report_name = self.report_name.get()
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file_path = os.path.join(output_dir, f"log_{timestamp}.txt")
        # self.html_report_path = os.path.join(output_dir, f"report_{timestamp}.html")
        # self.excel_report_path = os.path.join(output_dir, f"report_{timestamp}.xlsx")

        if self.report_name.get() == "":
            self.html_report_path = os.path.join(output_dir, f"report_{timestamp}.html")
            self.excel_report_path = os.path.join(output_dir, f"report_{timestamp}.xlsx")
        else:
            self.html_report_path = os.path.join(output_dir, f"{self.report_name.get()}.html")
            self.excel_report_path = os.path.join(output_dir, f"{self.report_name.get()}.xlsx")

        self._redirect_stdout()

        self.view_log_btn.config(state=tk.DISABLED)
        self.view_html_btn.config(state=tk.DISABLED)
        self.view_excel_btn.config(state=tk.DISABLED)

        self._show_loading_popup()
        threading.Thread(target=self._run_analysis_thread, daemon=True).start()

    def _show_loading_popup(self):
        self.loading_popup = Toplevel(self.root)
        self.loading_popup.title("Running Analysis")
        self.loading_popup.geometry("300x120")
        self.loading_popup.resizable(False, False)
        self.loading_popup.grab_set()

        tk.Label(self.loading_popup, text="Please wait...\nRunning analysis...").pack(pady=(15, 10))

        self.progress_bar = ttk.Progressbar(self.loading_popup, mode="indeterminate", length=250)
        self.progress_bar.pack(pady=5)
        self.progress_bar.start(10)
        self.loading_popup.update()

    def _close_loading_popup(self):
        if self.progress_bar:
            self.progress_bar.stop()
        if self.loading_popup:
            self.loading_popup.destroy()
            self.loading_popup = None

    def _run_analysis_thread(self):
        rn=""
        if self.report_name.get() == "":
            rn="None"
        else:
            rn=self.report_name.get()

        try:
            sys.argv = [
                "setup.py",
                "--layout_dir", self.layout_dir.get(),
                "--svrf_file", self.svrf_file.get(),
                "--output_dir", self.output_dir.get(),
                "--report_type", self.report_type.get(),
                "--report_name", rn
            ]
            run_analysis()
            self._close_loading_popup()
            print("\nAnalysis completed successfully.")
            print(f"Log file saved to: {self.log_file_path}\n")
            self.view_log_btn.config(state=tk.NORMAL)

            if os.path.exists(self.html_report_path):
                self.view_html_btn.config(state=tk.NORMAL)
            else:
                print(f"HTML report not found: {self.html_report_path}")

            if os.path.exists(self.excel_report_path):
                self.view_excel_btn.config(state=tk.NORMAL)
            else:
                print(f"Excel report not found: {self.excel_report_path}")

            messagebox.showinfo("Done", f"Analysis complete.\nLog file saved to:\n{self.log_file_path}")
        except Exception as e:
            self._close_loading_popup()
            print(f"\nError occurred: {e}\n")
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def _open_file(self, path):
        if path and os.path.exists(path):
            try:
                if sys.platform.startswith('darwin'):
                    subprocess.call(['open', path])
                elif os.name == 'nt':
                    os.startfile(path)
                elif os.name == 'posix':
                    subprocess.call(['xdg-open', path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{e}")
        else:
            messagebox.showwarning("Not Found", f"File not found:\n{path}")

    def open_log_file(self):
        self._open_file(self.log_file_path)

    def open_html_report(self):
        self._open_file(self.html_report_path)

    def open_excel_report(self):
        self._open_file(self.excel_report_path)


def main():
    root = tk.Tk()
    app = SVRFAnalyzerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
