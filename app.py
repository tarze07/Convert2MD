import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from converter import convert_url_to_markdown
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Web to Markdown Converter")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Styl
        style = ttk.Style()
        style.theme_use('clam')
        
        # Ramka główna
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL
        ttk.Label(main_frame, text="Adres URL strony:").pack(anchor=tk.W, pady=(0, 5))
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=70)
        self.url_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Plik wyjściowy
        ttk.Label(main_frame, text="Zapisz jako (plik Markdown):").pack(anchor=tk.W, pady=(0, 5))
        
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_var = tk.StringVar(value=os.path.join(os.getcwd(), "output.md"))
        self.file_entry = ttk.Entry(file_frame, textvariable=self.file_var)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_btn = ttk.Button(file_frame, text="Przeglądaj...", command=self.browse_file)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Przycisk start
        self.start_btn = ttk.Button(main_frame, text="Rozpocznij konwersję", command=self.start_conversion)
        self.start_btn.pack(pady=10)
        
        # Logi
        ttk.Label(main_frame, text="Status:").pack(anchor=tk.W, pady=(10, 5))
        self.log_text = tk.Text(main_frame, height=8, state=tk.DISABLED, bg="#f0f0f0")
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
    def browse_file(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md"), ("All files", "*.*")],
            title="Wybierz miejsce zapisu"
        )
        if filename:
            self.file_var.set(filename)
            
    def update_log(self, message):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def log_from_thread(self, message):
        self.root.after(0, self.update_log, message)
        
    def conversion_thread(self, url, output_path):
        success, msg = convert_url_to_markdown(url, output_path, self.log_from_thread)
        self.root.after(0, self.conversion_finished, success, msg)
        
    def conversion_finished(self, success, msg):
        self.start_btn.config(state=tk.NORMAL)
        if success:
            messagebox.showinfo("Sukces", "Konwersja zakończona pomyślnie!")
        else:
            messagebox.showerror("Błąd", f"Wystąpił błąd:\n{msg}")

    def start_conversion(self):
        url = self.url_var.get().strip()
        output_path = self.file_var.get().strip()
        
        if not url:
            messagebox.showwarning("Brak URL", "Proszę podać adres URL.")
            return
            
        if not output_path:
            messagebox.showwarning("Brak pliku", "Proszę wybrać miejsce zapisu pliku.")
            return
            
        self.start_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Uruchamiamy w tle, żeby nie zablokować interfejsu (Tkinter)
        thread = threading.Thread(target=self.conversion_thread, args=(url, output_path))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
