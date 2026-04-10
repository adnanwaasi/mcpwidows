import tkinter as tk
from tkinter import scrolledtext, messagebox
import code_gen_with_groq as cg
import code_seperator as cs
import change_maker as cm
import postgres
from dotenv import load_dotenv

load_dotenv()


class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Generator")
        self.root.geometry("900x900")
        self.root.configure(bg="#1e1e1e")

        # Configure dark theme colors
        self.bg_color = "#1e1e1e"
        self.fg_color = "#d4d4d4"
        self.input_bg = "#2d2d2d"
        self.accent_color = "#007acc"
        self.error_color = "#f44747"
        self.success_color = "#4ec9b0"

        self.project_name = "."

        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="Code Generator",
            font=("Consolas", 18, "bold"),
            bg=self.bg_color,
            fg=self.accent_color,
        )
        title_label.pack(pady=10)

        # Prompt input label
        prompt_label = tk.Label(
            self.root,
            text="Enter your prompt:",
            font=("Consolas", 12),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        prompt_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Prompt input text area
        self.prompt_entry = tk.Text(
            self.root,
            height=5,
            font=("Consolas", 11),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.prompt_entry.pack(pady=(0, 10), padx=20, fill="x")

        # Generate button
        self.generate_btn = tk.Button(
            self.root,
            text="Generate Code",
            font=("Consolas", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.generate_code,
        )
        self.generate_btn.pack(pady=(0, 10), padx=20, fill="x")

        # Update prompt label
        update_label = tk.Label(
            self.root,
            text="Update prompt (for modifying generated code):",
            font=("Consolas", 12),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        update_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Update prompt text area
        self.update_entry = tk.Text(
            self.root,
            height=3,
            font=("Consolas", 11),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.update_entry.pack(pady=(0, 5), padx=20, fill="x")

        # Previous code label
        prev_label = tk.Label(
            self.root,
            text="Previous code (to update):",
            font=("Consolas", 12),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        prev_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Previous code text area
        self.prev_code_entry = tk.Text(
            self.root,
            height=5,
            font=("Consolas", 11),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.prev_code_entry.pack(pady=(0, 10), padx=20, fill="x")

        # Update button
        self.update_btn = tk.Button(
            self.root,
            text="Update Code",
            font=("Consolas", 12, "bold"),
            bg="#6a9955",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.update_code,
        )
        self.update_btn.pack(pady=(0, 10), padx=20, fill="x")

        # Output label
        output_label = tk.Label(
            self.root,
            text="Generated Code:",
            font=("Consolas", 12),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        output_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Output text area (read-only)
        self.output_text = scrolledtext.ScrolledText(
            self.root,
            height=12,
            font=("Consolas", 11),
            bg=self.input_bg,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief="flat",
            padx=10,
            pady=10,
        )
        self.output_text.pack(pady=(0, 10), padx=20, fill="both", expand=True)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Consolas", 10),
            bg=self.bg_color,
            fg=self.fg_color,
        )
        self.status_label.pack(pady=(0, 10), padx=20, anchor="w")

    def generate_code(self):
        prompt = self.prompt_entry.get("1.0", "end-1c").strip()

        if not prompt:
            self.set_status("Please enter a prompt!", "error")
            return

        self.set_status("Generating code...", "normal")
        self.root.update()

        try:
            generated_code = cg.generate_code_with_groq(prompt)
            self.project_name = cs.write_code_to_files(generated_code)
            postgres.push_data_to_postgres(1, prompt, generated_code)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", generated_code)
            self.set_status("Code generated successfully!", "success")

        except Exception as e:
            self.set_status(f"Error: {str(e)}", "error")
            messagebox.showerror("Error", str(e))

    def update_code(self):
        update_prompt = self.update_entry.get("1.0", "end-1c").strip()
        prev_code = self.prev_code_entry.get("1.0", "end-1c").strip()

        if not update_prompt:
            self.set_status("Please enter an update prompt!", "error")
            return

        if not prev_code:
            self.set_status("Please enter previous code to update!", "error")
            return

        self.set_status("Updating code...", "normal")
        self.root.update()

        try:
            updated_code = cm.update_context(update_prompt, prev_code)
            cs.write_code_to_files(updated_code, project_dir=self.project_name)
            postgres.push_data_to_postgres(1, update_prompt, updated_code)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", updated_code)
            self.set_status("Code updated successfully!", "success")

        except Exception as e:
            self.set_status(f"Error: {str(e)}", "error")
            messagebox.showerror("Error", str(e))

    def set_status(self, message, status_type):
        self.status_label.config(text=message)
        if status_type == "success":
            self.status_label.config(fg=self.success_color)
        elif status_type == "error":
            self.status_label.config(fg=self.error_color)
        else:
            self.status_label.config(fg=self.fg_color)


def main():
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
