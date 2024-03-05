import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import PyPDF3
import os
from tkinterdnd2 import DND_FILES, TkinterDnD # for the drag and drop function
import shutil

from reportlab.lib.pagesizes import letter  # for converting images to pdfs
from reportlab.pdfgen import canvas
from PIL import Image

#import tempfile     # to create temporary folders to store converted not yet  merged pdfs

import time 

def clean_path(raw):
    """
    cleans up the strings coming from the
    listbox gui element (which can contain
    multiple file paths), so it can be used
    with the open function
    """
    without_brackets = raw.replace("{", "")
    without_brackets = without_brackets.replace("}", "")    # if a filename had spaces, it was wrapped by curly brackets, so we have to delete them
    paths = []
    start_indices = []      # indices in the string where a filepath starts

    for i in range(len(without_brackets)):  # the letter before the : is always the start of a path
        if without_brackets[i] == ":":
            start_indices.append(i-1)

    for x in range(len(start_indices)):    # adding every single path to the list thats going to be returned
        if x == len(start_indices)-1:
            paths.append(without_brackets[(start_indices[x]):])
        else:
            paths.append(without_brackets[(start_indices[x]):(start_indices[x+1])-1])  # -1 because of the whitespace after a path

    return paths


def drop_inside_list_box(event):
    raw_paths = event.data
    cleaned_up_paths = clean_path(raw_paths)
    #file_names.extend(cleaned_up_paths)     # extend because there could be multiple files at once, if multiple files are highlighted and dropped # dont need that anymore, useing listbox.get() function
    for i in cleaned_up_paths:
            if i.endswith(("pdf", ".png",".jpg", "jpeg")):
                listb.insert("end", i)

def image_to_pdf(image_path, pdf_path, pdf_title):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Create a PDF file with a specific title
    pdf_width, pdf_height = letter
    pdf = canvas.Canvas(pdf_path, pagesize=(pdf_width, pdf_height))
    pdf.setTitle(pdf_title)

    # Calculate the aspect ratio of the image to fit into the PDF
    img_width, img_height = img.size
    aspect_ratio = img_width / img_height
    pdf_img_width = pdf_width
    pdf_img_height = pdf_width / aspect_ratio

    # Draw the image on the PDF
    pdf.drawInlineImage(img, 0, pdf_height - pdf_img_height, width=pdf_img_width, height=pdf_img_height)

    # Save the PDF file
    pdf.save()

def merge_pdfs(output_file, input_files): 
    pdf_merger = PyPDF3.PdfFileMerger()

    unique_folder = f"converted_{int(time.time() * 1000)}" # temp folder to store converted images
    os.makedirs(unique_folder)

    for file in input_files:
        if file[-4:] == ".pdf":
            with open(file, 'rb') as pdf:
                pdf_merger.append(pdf)
        else:   
            temp_out_name = name_from_path_wo_type(file) +".pdf"
            temp_out_path = unique_folder+"/"+temp_out_name
            image_to_pdf(file, temp_out_path , temp_out_name)
            with open(temp_out_path, 'rb') as pdf:
                pdf_merger.append(pdf)
             
    output_file =  os.path.join(os.path.dirname(__file__), output_file)

    with open(output_file, 'wb') as merged_pdf:
        pdf_merger.write(merged_pdf)

    pdf_merger.close()
    shutil.rmtree(os.path.join(os.getcwd(), unique_folder)) 

def merge():
    output_file = output_filename_entry.get()
    if len(listb.get(0, "end"))>0:              # if files are provided 
        if output_file == "":           # if output filename is empty
            merge_pdfs(generate_filename(listb.get(0, "end")), listb.get(0, "end"))   # use all names as filename
        else:
            merge_pdfs(output_file, listb.get(0, "end"))    # else use provided name
    else:
        return              # if  no files are provided do nothing

def generate_filename(names): 
    res = ""
    for i in names:
        res += name_from_path_wo_type(i) + ", "  # adding every filename to res without the .pdf ending
    res = res[:-2] + ".pdf"     # delete last comma and add .pdf
    return res

def name_from_path_wo_type(path):       # macht das sinn die endung beizubehalten?
    # Use os.path.basename to get the filename from the path
    filename = os.path.splitext(os.path.basename(path))[0]
    return filename

def move_up():
    selected_index = listb.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index > 0:
            item = listb.get(selected_index)
            listb.delete(selected_index)
            listb.insert(selected_index - 1, item)
            listb.selection_set(selected_index - 1)

def move_down():
    selected_index = listb.curselection()
    if selected_index:
        selected_index = selected_index[0]
        if selected_index < listb.size() - 1:
            item = listb.get(selected_index)
            listb.delete(selected_index)
            listb.insert(selected_index + 1, item)
            listb.selection_set(selected_index + 1)


def delete_selected():
    selected_index = listb.curselection()
    if selected_index:
        listb.delete(selected_index[0])

def delete_all():
    listb.delete(0, tk.END)


# custom class to use customtkinter with TkinterDnD2
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)


# Sytem Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")



# App Frame
window = Tk()
window.geometry("800x600")
window.title("PDF Merger")
window.resizable(False, False)
# window.iconbitmap('pdf_icon.ico')  

# UI
title = ctk.CTkLabel(master = window, text = "Drag the files here:", font=("Helvetica", 16))
title.pack(padx = 10, pady = 10)

file_names = [] # initialising list where the file paths are going to be stored 

listb = tk.Listbox(master = window, selectmode= tk.SINGLE, background="#ffffff")     # drag and drop window
listb.pack(fill=tk.X, padx=20)
listb.drop_target_register(DND_FILES)
listb.dnd_bind("<<Drop>>", drop_inside_list_box)


button_frame = ctk.CTkFrame(window)
button_frame.pack(pady=10)

move_up_button = ctk.CTkButton(button_frame, text="Move Up ↑", command=move_up)
move_up_button.pack(side=tk.LEFT, padx=5)

move_down_button = ctk.CTkButton(button_frame, text="Move Down ↓", command=move_down)
move_down_button.pack(side=tk.LEFT, padx=5)

delete_selected_button = ctk.CTkButton(button_frame, text="Delete Selected", command=delete_selected)
delete_selected_button.pack(side=tk.LEFT, padx=5)

delete_all_button = ctk.CTkButton(button_frame, text="Delete All", command=delete_all)
delete_all_button.pack(side=tk.LEFT, padx=5)

output_filename = ctk.CTkLabel(master = window, text = "Output-file name:")
output_filename.pack()

output_filename_entry = ctk.CTkEntry(master= window)
output_filename_entry.pack()

button = ctk.CTkButton(master = window, text="Merge", command = merge)      
button.pack(pady = 10)
# Run App
window.mainloop()
