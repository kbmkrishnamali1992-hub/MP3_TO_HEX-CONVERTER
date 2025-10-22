import os
import sys
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ====== FFmpeg Portable Path ======
def get_portable_ffmpeg():
    """Return path to ffmpeg executable, portable or bundled."""
    if getattr(sys, 'frozen', False):  # Running from PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent

    portable_path = base_path / "ffmpeg" / "bin" / "ffmpeg.exe"
    if portable_path.exists():
        return str(portable_path)
    return None

# ====== Conversion Logic ======
def convert_mp3_to_raw(mp3_path, raw_path):
    ffmpeg_path = get_portable_ffmpeg()
    if not ffmpeg_path:
        messagebox.showerror("FFmpeg Not Found", "Portable FFmpeg not found in project directory!")
        return False
    try:
        subprocess.run([
            ffmpeg_path,
            "-i", mp3_path,
            "-f", "u8",
            "-ar", "8000",
            "-ac", "1",
            "-acodec", "pcm_u8",
            "-y",
            raw_path
        ], check=True)
        return True
    except Exception as e:
        messagebox.showerror("Conversion Failed", f"Error: {str(e)}")
        return False

def generate_header_file(raw_path, header_path):
    """Generate .h file with HEX array from RAW."""
    with open(raw_path, "rb") as f:
        data = f.read()
    with open(header_path, "w") as f:
        f.write("const uint8_t sound_audio[] PROGMEM = {\n")
        for i, b in enumerate(data):
            f.write(f"0x{b:02X},")
            if i % 16 == 15:
                f.write("\n")
        f.write("\n};\n")
        f.write(f"const unsigned int sound_audio_len = {len(data)};\n")

# ====== GUI Logic ======
root = tk.Tk()
root.title("🎵 MP3 → HEX Header Converter")
root.geometry("440x540")
root.resizable(False, False)
root.configure(bg="#f8f8f8")

FONT_TITLE = ("Segoe UI", 14, "bold")
FONT_TEXT = ("Segoe UI", 10)
BTN_WIDTH = 28
output_folder = None
selected_mp3 = None

# ====== Title ======
title_label = tk.Label(root, text="MP3 → HEX Converter", font=FONT_TITLE, bg="#f8f8f8", fg="#222")
title_label.pack(pady=(20, 0))

subtitle_label = tk.Label(root, text="with Header File Generator", font=("Segoe UI", 10, "italic"), bg="#f8f8f8", fg="#555")
subtitle_label.pack(pady=(0, 15))

# ====== Select MP3 ======
mp3_frame = tk.Frame(root, bg="#f8f8f8")
mp3_frame.pack(pady=10)
mp3_label = tk.Label(mp3_frame, text="🎵 Select MP3 File", font=FONT_TEXT, bg="#f8f8f8")
mp3_label.pack(pady=3)

def select_mp3():
    global selected_mp3
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3")])
    if file_path:
        selected_mp3 = Path(file_path)
        selected_file_label.config(text=selected_mp3.name)
        progress["value"] = 0
        open_btn.config(state="disabled")

select_mp3_btn = tk.Button(mp3_frame, text="Select MP3 File", font=FONT_TEXT, width=BTN_WIDTH, relief="raised", command=select_mp3)
select_mp3_btn.pack()
selected_file_label = tk.Label(mp3_frame, text="No file selected", font=("Segoe UI", 9), bg="#f8f8f8", fg="gray")
selected_file_label.pack(pady=3)

# ====== Destination Folder ======
dest_frame = tk.Frame(root, bg="#f8f8f8")
dest_frame.pack(pady=10)
dest_label = tk.Label(dest_frame, text="📁 Select Destination Folder (Optional)", font=FONT_TEXT, bg="#f8f8f8")
dest_label.pack(pady=3)

def select_folder():
    global output_folder
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder = folder_path
        selected_folder_label.config(text=output_folder)

select_folder_btn = tk.Button(dest_frame, text="Select Destination Folder", font=FONT_TEXT, width=BTN_WIDTH, relief="raised", command=select_folder)
select_folder_btn.pack()
selected_folder_label = tk.Label(dest_frame, text="Output Folder: Default (script folder)", font=("Segoe UI", 9), bg="#f8f8f8", fg="gray")
selected_folder_label.pack(pady=3)

# ====== Progress Bar ======
progress = ttk.Progressbar(root, orient="horizontal", length=350, mode="determinate")
progress.pack(pady=10)

# ====== Start Conversion ======
def start_conversion():
    if not selected_mp3:
        messagebox.showerror("Error", "Please select an MP3 file first!")
        return

    raw_path = selected_mp3.with_suffix(".raw")
    header_path = Path(output_folder) / "sound.h" if output_folder else selected_mp3.with_name("sound.h")

    progress["value"] = 10
    root.update_idletasks()

    if convert_mp3_to_raw(str(selected_mp3), str(raw_path)):
        progress["value"] = 70
        root.update_idletasks()
        generate_header_file(raw_path, header_path)
        progress["value"] = 100
        root.update_idletasks()

        messagebox.showinfo("Success", f"Conversion completed!\nSaved in:\n{header_path}")
        open_btn.config(state="normal")
    else:
        progress["value"] = 0

start_btn = tk.Button(root, text="▶ Start Conversion", font=("Segoe UI", 11, "bold"),
                      bg="#4CAF50", fg="white", width=BTN_WIDTH, relief="flat", command=start_conversion)
start_btn.pack(pady=15)

# ====== Open Folder Button ======
def open_folder():
    folder = output_folder if output_folder else os.getcwd()
    os.startfile(folder)

open_btn = tk.Button(root, text="📂 Open Destination Folder", font=("Segoe UI", 10),
                     bg="#2196F3", fg="white", width=BTN_WIDTH, relief="flat",
                     command=open_folder, state="disabled")
open_btn.pack(pady=(0, 15))

# ====== Close Button ======
close_btn = tk.Button(root, text="✖ Close", font=("Segoe UI", 10, "bold"),
                      bg="#E53935", fg="white", width=BTN_WIDTH, relief="flat",
                      command=root.destroy)
close_btn.pack(pady=5)

# ====== Footer ======
footer = tk.Label(root, text="Developed by KRISHNA B MALI",
                  font=("Segoe UI", 9, "italic"), bg="#eaeaea", fg="#555", pady=6)
footer.pack(side="bottom", fill="x")

root.mainloop()
