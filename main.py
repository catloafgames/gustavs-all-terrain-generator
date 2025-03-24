import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import terrain_generator

class FileProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gustav's All Terrain Generator")
        self.root.geometry("600x600")

        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # File Selection
        self.file_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Select Heightmap:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.file_path, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_file).grid(row=0, column=2, pady=5)

        # Save Output As
        self.save_path = tk.StringVar()
        ttk.Label(self.main_frame, text="Save Output As:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(self.main_frame, textvariable=self.save_path, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(self.main_frame, text="Browse", command=self.browse_save_location).grid(row=1, column=2, pady=5)

        # Image Size Selection
        ttk.Label(self.main_frame, text="Number Of Points To Generate:").grid(row=2, column=0, sticky=tk.W, pady=5)
        size_frame = ttk.Frame(self.main_frame)
        size_frame.grid(row=2, column=1, sticky=tk.W, pady=5)

        self.width = tk.StringVar(value="100")
        self.length = tk.StringVar(value="100")
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0)
        ttk.Entry(size_frame, textvariable=self.width, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(size_frame, text="Length:").grid(row=0, column=2, padx=5)
        ttk.Entry(size_frame, textvariable=self.length, width=10).grid(row=0, column=3)

        # Spacing Selection
        ttk.Label(self.main_frame, text="Spacing Between Points:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.spacing = tk.StringVar(value="10")
        ttk.Entry(self.main_frame, textvariable=self.spacing, width=10).grid(row=3, column=1, sticky=tk.W, pady=5)

        # Start Coordinates
        ttk.Label(self.main_frame, text="World Start Coordinates:").grid(row=4, column=0, sticky=tk.W, pady=5)
        coord_frame = ttk.Frame(self.main_frame)
        coord_frame.grid(row=4, column=1, sticky=tk.W, pady=5)

        self.start_x = tk.StringVar(value="10000")
        self.start_y = tk.StringVar(value="10000")
        ttk.Label(coord_frame, text="X:").grid(row=0, column=0)
        ttk.Entry(coord_frame, textvariable=self.start_x, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(coord_frame, text="Y:").grid(row=0, column=2, padx=5)
        ttk.Entry(coord_frame, textvariable=self.start_y, width=10).grid(row=0, column=3)

        ttk.Label(self.main_frame, text="Height:").grid(row=5, column=0, sticky=tk.W, pady=5)
        coord_frame = ttk.Frame(self.main_frame)
        coord_frame.grid(row=5, column=1, sticky=tk.W, pady=5)

        self.min_height = tk.StringVar(value="60")
        self.max_height = tk.StringVar(value="150")
        ttk.Label(coord_frame, text="Min Height:").grid(row=0, column=0)
        ttk.Entry(coord_frame, textvariable=self.min_height, width=10).grid(row=0, column=1, padx=5)
        ttk.Label(coord_frame, text="Max Height:").grid(row=0, column=2, padx=5)
        ttk.Entry(coord_frame, textvariable=self.max_height, width=10).grid(row=0, column=3)

        # Calculation Output Field
        ttk.Label(self.main_frame, text="Calculation Output:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.output_text = tk.Text(self.main_frame, height=4, width=50)
        self.output_text.grid(row=6, column=1, columnspan=2, pady=5)
        self.output_text.config(state='disabled')  # Make it read-only

        # Run Button
        ttk.Button(self.main_frame, text="Run Script", command=self.run_script).grid(row=7, column=0, columnspan=3,
                                                                                     pady=20)

        # Status Label
        self.status_var = tk.StringVar()
        ttk.Label(self.main_frame, textvariable=self.status_var).grid(row=8, column=0, columnspan=3)

    def browse_file(self):
        filename = filedialog.askopenfilename()
        self.file_path.set(filename)

    def browse_save_location(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        self.save_path.set(filename)

    def update_calculation_output(self, text):
        self.output_text.config(state='normal')
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')

    def save_output(self, calculation_result):
        save_path = self.save_path.get()
        if save_path:
            try:
                with open(save_path, 'w') as f:
                    for line in calculation_result:
                        f.write(line)
                self.status_var.set("Output saved successfully!")
            except Exception as e:
                self.status_var.set(f"Error saving output: {str(e)}")
        else:
            self.status_var.set("Please select a save location!")

    def run_script(self):
        # Collect all values
        try:
            params = {
                'file_path': self.file_path.get(),
                'width': int(self.width.get()),
                'length': int(self.length.get()),
                'min_height': int(self.min_height.get()),
                'max_height': int(self.max_height.get()),
                'spacing': int(self.spacing.get()),
                'start_x': int(self.start_x.get()),
                'start_y': int(self.start_y.get())
            }

            # Validate file path
            if not Path(params['file_path']).exists():
                self.status_var.set("Error: File does not exist!")
                return

            # Validate numeric values
            if any(v < 0 for v in [params['width'], params['length'], params['spacing']]):
                self.status_var.set("Error: Size and spacing must be positive numbers!")
                return

            sector_length = params['width'] * params["spacing"] / 320
            sector_height = params['length'] * params["spacing"] / 320
            total_area = params['width'] * params['length']
            total_space = params['spacing'] * params['spacing']
            calculation_result = f"Output will be \n"
            calculation_result += f"\t{sector_length} sectors long \n"
            calculation_result += f"\t{sector_length} sectors high \n"
            calculation_result += f"Starting at position: ({params['start_x']}, {params['start_y']}) \n"
            calculation_result += f"containing {total_area} location proxies \n"
            # Update the calculation output
            self.update_calculation_output(calculation_result)
            commandList = terrain_generator.process_image(params)
            # Save the output if a save path is specified
            self.save_output(commandList)

        except ValueError:
            self.status_var.set("Error: Please enter valid numbers for all numeric fields!")


def main():
    root = tk.Tk()
    app = FileProcessorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()