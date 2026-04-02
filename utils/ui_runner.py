import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import code_gen_with_groq as cg
import code_seperator as cs
import change_maker as cm
import postgres
import os
from dotenv import load_dotenv

load_dotenv()


class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Generator")
        self.root.geometry("700x600")
        self.root.configure(bg="#1e1e1e")

        self.generated_code = ""

        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background="#1e1e1e")
        style.configure(
            "TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10)
        )
        style.configure(
            "TButton",
            background="#0e639c",
            foreground="#ffffff",
            font=("Segoe UI", 10),
            borderwidth=0,
        )
        style.map("TButton", background=[("active", "#1177bb")])
        style.configure(
            "TCheckbutton",
            background="#1e1e1e",
            foreground="#ffffff",
            font=("Segoe UI", 10),
        )

        style.configure(
            "Input.TFrame", background="#252526", borderwidth=1, bordercolor="#3c3c3c"
        )
        style.configure("Output.TFrame", background="#1e1e1e")

    def create_widgets(self):
        title_label = tk.Label(
            self.root,
            text="Code Generator",
            font=("Segoe UI", 18, "bold"),
            bg="#1e1e1e",
            fg="#569cd6",
        )
        title_label.pack(pady=(20, 10))

        input_frame = ttk.Frame(self.root, style="Input.TFrame", padding=15)
        input_frame.pack(fill="x", padx=20, pady=(0, 10))

        ttk.Label(input_frame, text="Enter your prompt:").pack(anchor="w", pady=(0, 5))

        self.prompt_text = tk.Text(
            input_frame,
            height=4,
            bg="#252526",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            font=("Consolas", 10),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#0e639c",
        )
        self.prompt_text.pack(fill="x")

        self.gen_btn = ttk.Button(
            input_frame, text="Generate Code", command=self.generate_code
        )
        self.gen_btn.pack(pady=15, fill="x")

        output_frame = ttk.Frame(self.root, style="Output.TFrame", padding=15)
        output_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        ttk.Label(output_frame, text="Generated Code:").pack(anchor="w", pady=(0, 5))

        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=12,
            bg="#1e1e1e",
            fg="#d4d4d4",
            insertbackground="#ffffff",
            font=("Consolas", 9),
            borderwidth=0,
            highlightthickness=1,
            highlightcolor="#0e639c",
        )
        self.output_text.pack(fill="both", expand=True)

        update_frame = ttk.Frame(self.root, style="TFrame", padding=15)
        update_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Label(update_frame, text="Update prompt:").pack(anchor="w", pady=(0, 5))

        self.update_entry = ttk.Entry(update_frame, font=("Segoe UI", 10))
        self.update_entry.pack(fill="x", pady=(0, 10))

        self.update_btn = ttk.Button(
            update_frame, text="Update Code", command=self.update_code, state="disabled"
        )
        self.update_btn.pack(fill="x")

        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#007acc",
            fg="#ffffff",
            font=("Segoe UI", 9),
            anchor="w",
            padx=10,
        )
        status_bar.pack(fill="x", side="bottom")

    def generate_code(self):
        prompt = self.prompt_text.get("1.0", "end").strip()
        if not prompt:
            messagebox.showwarning("Warning", "Please enter a prompt")
            return

        self.status_var.set("Generating code...")
        self.root.config(cursor="watch")
        self.root.update()

        try:
            self.generated_code = cg.generate_code_with_groq(prompt)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", self.generated_code)

            cs.write_code_to_files(self.generated_code)
            postgres.push_data_to_postgres(1, prompt, self.generated_code)

            self.update_btn.config(state="normal")
            self.status_var.set("Code generated successfully!")
            messagebox.showinfo("Success", "Files generated and saved to database!")

        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"Failed to generate code: {str(e)}")

        self.root.config(cursor="")

    def update_code(self):
        update_prompt = self.update_entry.get().strip()
        if not update_prompt:
            messagebox.showwarning("Warning", "Please enter an update prompt")
            return

        if not self.generated_code:
            messagebox.showwarning("Warning", "No generated code to update")
            return

        self.status_var.set("Updating code...")
        self.root.config(cursor="watch")
        self.root.update()

        try:
            updated_code = cm.update_context(update_prompt, self.generated_code)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", updated_code)

            cs.write_code_to_files(updated_code)
            postgres.push_data_to_postgres(1, update_prompt, updated_code)

            self.generated_code = updated_code
            self.update_entry.delete(0, "end")

            self.status_var.set("Code updated successfully!")
            messagebox.showinfo("Success", "Code updated and saved!")

        except Exception as e:
            self.status_var.set("Error")
            messagebox.showerror("Error", f"Failed to update code: {str(e)}")

        self.root.config(cursor="")


def main():
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
