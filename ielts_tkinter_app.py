import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import requests

API_URL = "http://localhost:8000/rate"

def submit_task():
    task_type = task_type_var.get()
    model_name = model_var.get()  # Get selected model
    question = question_text.get("1.0", tk.END).strip()
    response = response_text.get("1.0", tk.END).strip()
    
    if not question or not response:
        messagebox.showerror("Input Error", "Both question and response fields must be filled.")
        return
    
    data = {
        "task_type": task_type,
        "question": question,
        "response": response,
        "model": model_name  # Include selected model
    }
    
    try:
        response = requests.post(API_URL, json=data)
        response.raise_for_status()
        rating = response.json()["rating"]
        
        feedback_text.config(state=tk.NORMAL)
        feedback_text.delete("1.0", tk.END)
        feedback_text.insert(tk.END, f"Overall Score: {rating['overall_score']}\n\n", "title")
        feedback_text.insert(tk.END, f"Feedback: {rating['overall_feedback']}\n\n", "normal")
        
        for criterion, details in rating.items():
            if isinstance(details, dict):
                feedback_text.insert(tk.END, f"{criterion.replace('_', ' ').title()}:\n", "subtitle")
                feedback_text.insert(tk.END, f"- Score: {details['score']}\n", "bold")
                feedback_text.insert(tk.END, f"- Feedback: {details['feedback']}\n\n", "normal")
        
        feedback_text.config(state=tk.DISABLED)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("API Error", f"Failed to get feedback: {str(e)}")

# Tkinter GUI Setup
root = tk.Tk()
root.title("IELTS Writing Task Evaluator")
root.geometry("650x800")
root.configure(bg="#f4f4f4")

# Styling
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12), background="#f4f4f4")
style.configure("TCombobox", font=("Arial", 12))

# Title Label
title_label = ttk.Label(root, text="IELTS Writing Task Evaluator", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Frame for Model & Task Selection
selection_frame = ttk.Frame(root)
selection_frame.pack(pady=5)

# Model Selection
model_var = tk.StringVar(value="chatGPT")  # Default selection
ttm = ttk.Label(selection_frame, text="Select AI Model:")
ttm.grid(row=0, column=0, padx=5, pady=5, sticky="w")
model_options = ttk.Combobox(selection_frame, textvariable=model_var, values=["chatGPT", "llama3.2"], state="readonly")
model_options.grid(row=0, column=1, padx=5, pady=5)

# Task Type Selection
task_type_var = tk.StringVar(value="task1")
tttl = ttk.Label(selection_frame, text="Select Writing Task Type:")
tttl.grid(row=1, column=0, padx=5, pady=5, sticky="w")
task_options = ttk.Combobox(selection_frame, textvariable=task_type_var, values=["task1", "task2"], state="readonly")
task_options.grid(row=1, column=1, padx=5, pady=5)

# Question Input
ttq = ttk.Label(root, text="Enter Task Question:")
ttq.pack(pady=5)
question_text = scrolledtext.ScrolledText(root, width=75, height=5, font=("Arial", 12))
question_text.pack(pady=5)

# Response Input
ttr = ttk.Label(root, text="Enter Your Response:")
ttr.pack(pady=5)
response_text = scrolledtext.ScrolledText(root, width=75, height=10, font=("Arial", 12))
response_text.pack(pady=5)

# Submit Button
submit_btn = ttk.Button(root, text="Submit for Evaluation", command=submit_task)
submit_btn.pack(pady=10)

# Feedback Display
ttf = ttk.Label(root, text="Evaluation Feedback:")
ttf.pack(pady=5)
feedback_text = scrolledtext.ScrolledText(root, width=75, height=15, font=("Arial", 12), state=tk.DISABLED, bg="#ffffff", fg="#333333")
feedback_text.pack(pady=5)

# Text Styling
feedback_text.tag_configure("title", font=("Arial", 14, "bold"), foreground="#0078D7")
feedback_text.tag_configure("subtitle", font=("Arial", 12, "bold"), foreground="#2E8B57")
feedback_text.tag_configure("bold", font=("Arial", 12, "bold"))
feedback_text.tag_configure("normal", font=("Arial", 12))

# Run Tkinter Application
root.mainloop()
