import os
from tkinter import Tk, filedialog, Button, Label, messagebox, ttk, DoubleVar
from PIL import Image

# Supported formats for conversion
SUPPORTED_FORMATS = (".jpg", ".jpeg", ".bmp", ".webp")


def convert_images(input_folder, output_folder, progress_var, progress_bar):
    files = [
            f for f in os.listdir(input_folder)
            if f.lower().endswith(SUPPORTED_FORMATS)
            ]
    total_files = len(files)

    if total_files == 0:
        messagebox.showwarning(
                "No Images",
                "No supported image files found in the selected folder.")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, filename in enumerate(files, start=1):
        try:
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)
            clean_name = os.path.splitext(filename)[0]
            img.save(os.path.join(output_folder, f"{clean_name}.png"), "PNG")
        except Exception as e:
            print(f"Skipping {filename}: {e}")

        # Update progress
        progress_var.set((i / total_files) * 100)
        progress_bar.update()

    messagebox.showinfo("Done", "All conversions completed!")


def select_folder():
    return filedialog.askdirectory()


def start_conversion():
    input_folder = select_folder()
    if not input_folder:
        return
    output_folder = filedialog.askdirectory()
    if not output_folder:
        return
    convert_images(input_folder, output_folder, progress_var, progress_bar)


# GUI setup
root = Tk()
root.title("Image to PNG Converter")
root.geometry("400x200")

Label(root, text="JPEG/JPG/BMP/WebP to PNG Converter",
        font=("Arial", 14)).pack(pady=10)
Button(root,
        text="Select Folders & Convert",
        command=start_conversion,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 12)).pack(pady=10)

# Progress bar
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(root,
        variable=progress_var,
        maximum=100,
        length=300)
progress_bar.pack(pady=10)

root.mainloop()
