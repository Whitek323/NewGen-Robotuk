import tkinter as tk
from tkinter import colorchooser, ttk

class SubtitleSettingsDialog:
    def __init__(self, parent, initial_settings):
        self.window = tk.Toplevel(parent)
        self.window.title("Subtitle Settings")
        self.window.geometry("400x350")
        self.window.protocol("WM_DELETE_WINDOW", self.cancel_settings)
        
        # Make window modal and always on top
        self.window.transient(parent)
        self.window.grab_set()
        self.window.lift()
        
        # Store original and current settings
        self.original_settings = initial_settings.copy()
        self.settings = initial_settings.copy()
        
        # Subtitle Enable/Disable
        self.enable_var = tk.BooleanVar(value=self.settings.get('enabled', True))
        tk.Checkbutton(self.window, text="Enable Subtitles", 
                       variable=self.enable_var).pack(pady=10)
        
        # Background Color
        self.bg_color_frame = tk.Frame(self.window)
        self.bg_color_frame.pack(pady=10)
        tk.Label(self.bg_color_frame, text="Background Color:").pack(side=tk.LEFT)
        self.bg_color_btn = tk.Button(self.bg_color_frame, 
                                      bg=self.settings.get('bg_color', 'black'), 
                                      width=5, 
                                      command=self.choose_bg_color)
        self.bg_color_btn.pack(side=tk.LEFT, padx=10)
        
        # Text Color
        self.text_color_frame = tk.Frame(self.window)
        self.text_color_frame.pack(pady=10)
        tk.Label(self.text_color_frame, text="Text Color:").pack(side=tk.LEFT)
        self.text_color_btn = tk.Button(self.text_color_frame, 
                                        bg=self.settings.get('text_color', 'white'), 
                                        width=5, 
                                        command=self.choose_text_color)
        self.text_color_btn.pack(side=tk.LEFT, padx=10)
        
        # Font Size
        self.font_size_frame = tk.Frame(self.window)
        self.font_size_frame.pack(pady=10)
        tk.Label(self.font_size_frame, text="Font Size:").pack(side=tk.LEFT)
        self.font_size_var = tk.IntVar(value=self.settings.get('font_size', 24))
        self.font_size_spinbox = tk.Spinbox(self.font_size_frame, 
                                            from_=10, to=50, 
                                            textvariable=self.font_size_var, 
                                            width=5)
        self.font_size_spinbox.pack(side=tk.LEFT, padx=10)
        
        # Button Frame
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=20)
        
        # Save and Cancel Buttons
        tk.Button(button_frame, text="Save", command=self.save_settings).pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Cancel", command=self.cancel_settings).pack(side=tk.LEFT, padx=10)
        
        self.on_save_callback = None
        
    def choose_bg_color(self):
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            self.bg_color_btn.configure(bg=color)
            
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Choose Text Color")[1]
        if color:
            self.text_color_btn.configure(bg=color)
            
    def save_settings(self):
        self.settings = {
            'enabled': self.enable_var.get(),
            'bg_color': self.bg_color_btn['bg'],
            'text_color': self.text_color_btn['bg'],
            'font_size': self.font_size_var.get()
        }
        if self.on_save_callback:
            self.on_save_callback(self.settings)
        self.window.destroy()
        
    def cancel_settings(self):
        # Restore original settings and close window
        if self.on_save_callback:
            self.on_save_callback(self.original_settings)
        self.window.destroy()
        
    def set_save_callback(self, callback):
        self.on_save_callback = callback