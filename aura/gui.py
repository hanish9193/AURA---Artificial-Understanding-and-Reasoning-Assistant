"""
Tkinter-based interactive GUI for AURA data Q&A
Enhanced with premium dark glassmorphic design
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import threading
from PIL import Image, ImageTk
from io import BytesIO


class AuraGUI:
    """Tkinter GUI for interactive data Q&A with premium dark UI"""
    
    def __init__(self, aura_instance):
        self.aura = aura_instance
        self.window = None
        self.chat_display = None
        self.input_field = None
        self.send_button = None
        self.graphs_button = None
        self.typing_animation = False
        
    def launch(self):
        """Launch the enhanced Tkinter GUI"""
        self.window = tk.Tk()
        self.window.title("AURA - Data Insights Q&A")
        self.window.geometry("950x750")
        self.window.configure(bg="#000000")
        
        # Main container with subtle border
        main_container = tk.Frame(self.window, bg="#0a0a0a", highlightbackground="#1a1a1a", highlightthickness=1)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # ===== HEADER SECTION =====
        header = tk.Frame(main_container, bg="#0f0f0f", height=80)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        # Animated accent line
        accent_line = tk.Frame(header, bg="#ffffff", height=2)
        accent_line.pack(fill=tk.X)
        self._animate_line(accent_line)
        
        # Title with glow effect
        title_frame = tk.Frame(header, bg="#0f0f0f")
        title_frame.pack(expand=True)
        
        title = tk.Label(
            title_frame,
            text="✦ AURA",
            font=("Helvetica", 28, "bold"),
            bg="#0f0f0f",
            fg="#ffffff"
        )
        title.pack()
        
        subtitle = tk.Label(
            title_frame,
            text="Autonomous Understanding & Response Architecture",
            font=("Helvetica", 9),
            bg="#0f0f0f",
            fg="#666666"
        )
        subtitle.pack()
        
        # Dataset info bar with glassmorphic style
        info_bar = tk.Frame(main_container, bg="#0a0a0a", height=35)
        info_bar.pack(fill=tk.X, padx=0, pady=(10, 0))
        info_bar.pack_propagate(False)
        
        info_container = tk.Frame(info_bar, bg="#151515", highlightbackground="#252525", highlightthickness=1)
        info_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        dataset_info = tk.Label(
            info_container,
            text=f"  DATASET: {self.aura.data.shape[0]:,} rows × {self.aura.data.shape[1]} columns  •  MODEL: EfficientNetB7  •  GRAPHS: {len(self.aura.graphs)}  ",
            font=("Courier", 9),
            bg="#151515",
            fg="#888888"
        )
        dataset_info.pack(expand=True)
        
        # ===== CHAT DISPLAY AREA =====
        chat_container = tk.Frame(main_container, bg="#0a0a0a")
        chat_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=15)
        
        # Glassmorphic chat frame
        chat_glass_frame = tk.Frame(chat_container, bg="#0d0d0d", highlightbackground="#1f1f1f", highlightthickness=1)
        chat_glass_frame.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_glass_frame,
            wrap=tk.WORD,
            font=("Consolas", 10),
            bg="#080808",
            fg="#e8e8e8",
            insertbackground="#ffffff",
            selectbackground="#2a2a2a",
            selectforeground="#ffffff",
            height=20,
            borderwidth=0,
            highlightthickness=0,
            padx=15,
            pady=15
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.chat_display.config(state=tk.DISABLED)
        
        # Custom scrollbar styling
        self.chat_display.vbar.config(
            bg="#0d0d0d",
            troughcolor="#080808",
            activebackground="#ffffff",
            highlightthickness=0,
            width=8
        )
        
        # Initial welcome message with animation
        self._append_message("SYSTEM", "◆ AURA INITIALIZED ◆", is_assistant=True, is_system=True)
        self._append_message("AURA", 
            "Neural interface active. Ready to analyze your dataset.\n\n" +
            "▸ QUERY EXAMPLES:\n" +
            "  • Identify correlations and patterns\n" +
            "  • Detect data quality anomalies\n" +
            "  • Feature importance analysis\n" +
            "  • Outlier detection\n\n" +
            "Awaiting input...", 
            is_assistant=True)
        
        # ===== INPUT AREA =====
        input_container = tk.Frame(main_container, bg="#0a0a0a", height=60)
        input_container.pack(fill=tk.X, padx=0, pady=0)
        input_container.pack_propagate(False)
        
        # Glassmorphic input frame
        input_glass = tk.Frame(input_container, bg="#0f0f0f", highlightbackground="#252525", highlightthickness=1)
        input_glass.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
        
        input_inner = tk.Frame(input_glass, bg="#0f0f0f")
        input_inner.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input field with focus animation
        self.input_field = tk.Entry(
            input_inner,
            font=("Consolas", 11),
            bg="#080808",
            fg="#ffffff",
            insertbackground="#ffffff",
            borderwidth=0,
            highlightthickness=1,
            highlightbackground="#1a1a1a",
            highlightcolor="#ffffff",
            selectbackground="#2a2a2a",
            selectforeground="#ffffff"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.input_field.bind("<Return>", lambda e: self._send_message())
        self.input_field.bind("<FocusIn>", lambda e: self.input_field.config(highlightcolor="#ffffff", highlightbackground="#ffffff"))
        self.input_field.bind("<FocusOut>", lambda e: self.input_field.config(highlightcolor="#1a1a1a", highlightbackground="#1a1a1a"))
        
        # Buttons with hover effects
        button_container = tk.Frame(input_inner, bg="#0f0f0f")
        button_container.pack(side=tk.RIGHT)
        
        self.send_button = tk.Button(
            button_container,
            text="⚡ SEND",
            command=self._send_message,
            bg="#ffffff",
            fg="#000000",
            font=("Helvetica", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            activebackground="#e8e8e8",
            activeforeground="#000000"
        )
        self.send_button.pack(side=tk.LEFT, padx=(0, 8))
        self._add_button_hover(self.send_button, "#ffffff", "#d0d0d0")
        
        self.graphs_button = tk.Button(
            button_container,
            text="◈ GRAPHS",
            command=self._view_graphs,
            bg="#1a1a1a",
            fg="#ffffff",
            font=("Helvetica", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            borderwidth=0,
            activebackground="#252525",
            activeforeground="#ffffff"
        )
        self.graphs_button.pack(side=tk.LEFT)
        self._add_button_hover(self.graphs_button, "#1a1a1a", "#252525")
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(main_container, bg="#0a0a0a", height=25)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        footer = tk.Label(
            footer_frame,
            text="━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            font=("Courier", 7),
            bg="#0a0a0a",
            fg="#1a1a1a"
        )
        footer.pack()
        
        status = tk.Label(
            footer_frame,
            text="● ACTIVE",
            font=("Courier", 8),
            bg="#0a0a0a",
            fg="#666666"
        )
        status.pack()
        
        # Run GUI
        self.window.mainloop()
    
    def _animate_line(self, line):
        """Animate accent line with pulsing effect"""
        def pulse():
            colors = ["#ffffff", "#e8e8e8", "#d0d0d0", "#e8e8e8", "#ffffff"]
            for color in colors:
                if not self.window or not self.window.winfo_exists():
                    return
                line.config(bg=color)
                self.window.update()
                self.window.after(200)
            if self.window and self.window.winfo_exists():
                self.window.after(3000, pulse)
        
        self.window.after(1000, pulse)
    
    def _add_button_hover(self, button, normal_color, hover_color):
        """Add hover effect to button"""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=normal_color))
    
    def _send_message(self):
        """Send user message and get AI response"""
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        # Display user message
        self._append_message("USER", user_input, is_assistant=False)
        self.input_field.delete(0, tk.END)
        
        # Show typing indicator
        self._show_typing_indicator()
        
        # Process in background thread
        thread = threading.Thread(target=self._get_response, args=(user_input,))
        thread.daemon = True
        thread.start()
    
    def _show_typing_indicator(self):
        """Show typing animation"""
        self.typing_animation = True
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, "\n", "spacing")
        self.chat_display.insert(tk.END, "AURA:\n", "assistant_header")
        self.chat_display.tag_config("assistant_header", foreground="#ffffff", font=("Helvetica", 10, "bold"))
        
        typing_mark = self.chat_display.index(tk.END)
        self.chat_display.insert(tk.END, "▌Analyzing", "typing")
        self.chat_display.tag_config("typing", foreground="#666666", font=("Consolas", 10))
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        def animate_typing(dots=0):
            if not self.typing_animation:
                return
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete(typing_mark, tk.END)
            self.chat_display.insert(tk.END, "▌Analyzing" + "." * (dots % 4), "typing")
            self.chat_display.config(state=tk.DISABLED)
            if self.typing_animation:
                self.window.after(300, lambda: animate_typing(dots + 1))
        
        animate_typing()
    
    def _get_response(self, question):
        """Get AI response from Mistral"""
        try:
            response = self.aura.ask(question)
            self.typing_animation = False
            self.window.after(0, lambda: self._replace_typing_with_response(response))
        except Exception as e:
            self.typing_animation = False
            self.window.after(0, lambda: self._replace_typing_with_response(f"✖ ERROR: {str(e)}", is_error=True))
    
    def _replace_typing_with_response(self, response, is_error=False):
        """Replace typing indicator with actual response"""
        self.chat_display.config(state=tk.NORMAL)
        
        # Find and delete typing indicator
        content = self.chat_display.get("1.0", tk.END)
        lines = content.split("\n")
        for i in range(len(lines) - 1, -1, -1):
            if "Analyzing" in lines[i] or "▌" in lines[i]:
                line_start = f"{i + 1}.0"
                line_end = f"{i + 2}.0"
                self.chat_display.delete(line_start, line_end)
                break
        
        # Insert response
        if is_error:
            self.chat_display.insert(tk.END, f"{response}\n", "error")
            self.chat_display.tag_config("error", foreground="#ff4444")
        else:
            self.chat_display.insert(tk.END, f"{response}\n", "message")
            self.chat_display.tag_config("message", foreground="#e8e8e8")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _append_message(self, sender, message, is_assistant=False, is_system=False):
        """Append message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        
        self.chat_display.insert(tk.END, "\n", "spacing")
        
        if is_system:
            self.chat_display.insert(tk.END, f"{sender}\n", "system_header")
            self.chat_display.tag_config("system_header", foreground="#666666", font=("Courier", 9, "bold"), justify="center")
            self.chat_display.insert(tk.END, f"{message}\n", "system_message")
            self.chat_display.tag_config("system_message", foreground="#666666", font=("Courier", 9), justify="center")
        elif is_assistant:
            self.chat_display.insert(tk.END, f"{sender}:\n", "assistant_header")
            self.chat_display.tag_config("assistant_header", foreground="#ffffff", font=("Helvetica", 10, "bold"))
            self.chat_display.insert(tk.END, f"{message}\n", "message")
            self.chat_display.tag_config("message", foreground="#e8e8e8")
        else:
            self.chat_display.insert(tk.END, f"{sender}:\n", "user_header")
            self.chat_display.tag_config("user_header", foreground="#ffffff", font=("Helvetica", 10, "bold"))
            self.chat_display.insert(tk.END, f"{message}\n", "user_message")
            self.chat_display.tag_config("user_message", foreground="#cccccc")
        
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def _view_graphs(self):
        """Display generated graphs in premium dark window"""
        if not self.aura.graphs:
            self._show_custom_messagebox("NO GRAPHS DETECTED", "Generate insights first to view graphs.")
            return
        
        graph_window = tk.Toplevel(self.window)
        graph_window.title("AURA - Graph Viewer")
        graph_window.geometry("1050x850")
        graph_window.configure(bg="#000000")
        
        # Main container
        main = tk.Frame(graph_window, bg="#0a0a0a", highlightbackground="#1a1a1a", highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Header
        nav_frame = tk.Frame(main, bg="#0f0f0f", height=60)
        nav_frame.pack(fill=tk.X, padx=0, pady=0)
        nav_frame.pack_propagate(False)
        
        accent = tk.Frame(nav_frame, bg="#ffffff", height=2)
        accent.pack(fill=tk.X)
        
        title = tk.Label(
            nav_frame,
            text="◈ GRAPH VIEWER",
            font=("Helvetica", 18, "bold"),
            bg="#0f0f0f",
            fg="#ffffff"
        )
        title.pack(expand=True)
        
        # Canvas with scrollbar
        canvas_container = tk.Frame(main, bg="#0a0a0a")
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=15)
        
        canvas = tk.Canvas(canvas_container, bg="#080808", highlightthickness=0, borderwidth=0)
        scrollbar = tk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview, 
                                bg="#0d0d0d", troughcolor="#080808", activebackground="#ffffff", 
                                highlightthickness=0, width=8)
        scrollable_frame = tk.Frame(canvas, bg="#080808")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add graphs
        for idx, (graph_bytes, metadata) in enumerate(zip(self.aura.graphs, self.aura.graph_metadata)):
            try:
                img = Image.open(BytesIO(graph_bytes))
                img.thumbnail((950, 450))
                photo = ImageTk.PhotoImage(img)
                
                # Graph container
                graph_container = tk.Frame(scrollable_frame, bg="#0d0d0d", 
                                          highlightbackground="#1f1f1f", highlightthickness=1)
                graph_container.pack(fill=tk.BOTH, padx=10, pady=10)
                
                # Title bar
                title_bar = tk.Frame(graph_container, bg="#0f0f0f", height=40)
                title_bar.pack(fill=tk.X)
                title_bar.pack_propagate(False)
                
                graph_title = tk.Label(
                    title_bar,
                    text=f"▸ {metadata.get('name', 'VISUALIZATION')} #{idx + 1}",
                    font=("Helvetica", 11, "bold"),
                    bg="#0f0f0f",
                    fg="#ffffff"
                )
                graph_title.pack(side=tk.LEFT, padx=15, pady=10)
                
                # Image
                img_frame = tk.Frame(graph_container, bg="#080808")
                img_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
                
                img_label = tk.Label(img_frame, image=photo, bg="#080808")
                img_label.image = photo
                img_label.pack(pady=10)
                
            except Exception as e:
                error_frame = tk.Frame(scrollable_frame, bg="#0d0d0d")
                error_frame.pack(fill=tk.X, padx=10, pady=10)
                
                error_label = tk.Label(
                    error_frame,
                    text=f"✖ ERROR LOADING GRAPH {idx + 1}: {str(e)}",
                    font=("Courier", 9),
                    bg="#0d0d0d",
                    fg="#ff4444"
                )
                error_label.pack(pady=10)
        
        # Mousewheel binding
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def _show_custom_messagebox(self, title, message):
        """Custom dark-themed message box"""
        msg_window = tk.Toplevel(self.window)
        msg_window.title(title)
        msg_window.geometry("400x200")
        msg_window.configure(bg="#0a0a0a")
        msg_window.resizable(False, False)
        
        main = tk.Frame(msg_window, bg="#0f0f0f", highlightbackground="#252525", highlightthickness=1)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            main,
            text=title,
            font=("Helvetica", 12, "bold"),
            bg="#0f0f0f",
            fg="#ffffff"
        )
        title_label.pack(pady=20)
        
        msg_label = tk.Label(
            main,
            text=message,
            font=("Helvetica", 10),
            bg="#0f0f0f",
            fg="#cccccc",
            wraplength=350
        )
        msg_label.pack(pady=10)
        
        ok_button = tk.Button(
            main,
            text="OK",
            command=msg_window.destroy,
            bg="#ffffff",
            fg="#000000",
            font=("Helvetica", 9, "bold"),
            padx=30,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        ok_button.pack(pady=20)
        
        msg_window.transient(self.window)
        msg_window.grab_set()