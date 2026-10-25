import tkinter as tk
from tkinter import ttk
import sys
from core.engine import validate_pattern, get_highlighted_segments
from core.cheatsheet import CHEATSHEET_DATA

F_LBL = ("", 10, "bold")
F_TXT = ("", 12, "bold")
F_SYM = ("Consolas", 10, "bold")
C_ERR, C_MATCH_BG, C_MATCH_FG, C_SYM = "#ffcccc", "#aaffaa", "#227722", "#e6e6e6"
C_FOCUS, C_SEL_BG, C_SEL_FG, C_PH = "#ffffe6", "#1a75ff", "white", "grey"

WIN_SHORTCUTS = {65: "select_all", 67: "copy", 86: "paste", 88: "cut", 90: "undo", 89: "redo"}
OTHER_SHORTCUTS = {"a": "select_all", "c": "copy", "v": "paste", "x": "cut", "z": "undo", "y": "redo"}

class RegexLabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RegexLab")
        self.root.geometry("850x600")
        self.root.minsize(600, 400)
        
        self.sidebar_visible = True
        self.default_width = 0
        self.re_error = False
        self.pattern_focused = False
        
        self.ph_pattern = "e.g. \\d+"
        self.ph_text = "Type your test text here..."
        self.context_widget = None

        self._build_layout()
        self._setup_menu()

        self._ph(self.pattern_entry, self.ph_pattern)
        self._ph(self.text_entry, self.ph_text)
        self.text_entry.bind("<FocusIn>", self._update, add="+")
        self.text_entry.bind("<FocusOut>", self._update, add="+")

        self.root.after(100, self._init_sash)

    def _build_layout(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned_window.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.sidebar_frame = ttk.Frame(self.paned_window, relief="solid", borderwidth=1)
        self._build_sidebar()
        
        self.editor_frame = ttk.Frame(self.paned_window, padding=(10, 5, 5, 5))
        self._build_editor()

        self.paned_window.add(self.sidebar_frame, weight=0)
        self.paned_window.add(self.editor_frame, weight=1)

    def _build_sidebar(self):
        self.sidebar_frame.rowconfigure(0, weight=1)
        self.sidebar_frame.columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self.sidebar_frame, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        right_col = ttk.Frame(self.sidebar_frame)
        right_col.grid(row=0, column=1, sticky="ns")

        self.btn_hide = ttk.Button(right_col, text="◀", width=2, command=self._toggle_sidebar)
        self.btn_hide.pack(side="top", pady=(2, 0))

        scrollbar = ttk.Scrollbar(right_col, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="top", fill="y", expand=True)

        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        for i, (category, items) in enumerate(CHEATSHEET_DATA.items()):
            tk.Label(self.scrollable_frame, text=category, font=F_LBL, fg="#222222").pack(anchor="w", pady=(2 if i == 0 else 15, 5), padx=10)
            for symbol, desc in items.items():
                row = ttk.Frame(self.scrollable_frame)
                row.pack(fill="x", padx=10, pady=2)
                tk.Label(row, text=symbol, font=F_SYM, bg=C_SYM, fg="#333", padx=6, pady=2).pack(side="left", anchor="n")
                ttk.Label(row, text=desc, justify="left").pack(side="left", padx=(10, 0), anchor="n")

        self._bind_wheel(self.scrollable_frame)

    def _build_editor(self):
        self.editor_frame.columnconfigure(0, weight=1)
        self.editor_frame.rowconfigure(4, weight=1)

        top_row = ttk.Frame(self.editor_frame)
        top_row.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        top_row.columnconfigure(1, weight=1)

        self.btn_show = ttk.Button(top_row, text="▶", width=2, command=self._toggle_sidebar)
        self.btn_show.grid(row=0, column=0, sticky="nw", padx=(0, 5))
        self.btn_show.grid_remove()

        regex_frame = ttk.Frame(top_row)
        regex_frame.grid(row=0, column=1, sticky="ew")
        regex_frame.columnconfigure(0, weight=1)

        ttk.Label(regex_frame, text="Regular Expression:", font=F_LBL, foreground="#000000").grid(row=0, column=0, sticky="w", pady=(0, 2))
        
        self.pattern_entry = tk.Text(regex_frame, height=1, font=F_TXT, bg="white", relief="sunken", bd=1, highlightthickness=0, selectbackground=C_SEL_BG, selectforeground=C_SEL_FG, undo=True, wrap="none")
        self.pattern_entry.grid(row=1, column=0, sticky="ew", ipady=3)
        
        self.pattern_entry.bind("<Return>", self._insert_newline)
        self.pattern_entry.bind("<KeyRelease>", self._update)
        self.pattern_entry.bind("<FocusIn>", lambda e: (setattr(self, 'pattern_focused', True), self._update()))
        self.pattern_entry.bind("<FocusOut>", lambda e: (setattr(self, 'pattern_focused', False), self._update()))
        self.pattern_entry.bind("<Button-3>", self._show_menu)
        self.pattern_entry.bind("<Key>", self._shortcuts)

        self.error_label = tk.Label(regex_frame, text="", fg="#ff6666", font=F_LBL)

        ttk.Label(self.editor_frame, text="Test String:", font=F_LBL, foreground="#000000").grid(row=1, column=0, sticky="w", pady=(0, 2))
        text_frame = ttk.Frame(self.editor_frame)
        text_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        
        self.text_entry = tk.Text(text_frame, height=6, font=F_TXT, undo=True, relief="sunken", bd=1, highlightthickness=0, selectbackground=C_SEL_BG, selectforeground=C_SEL_FG)
        self.text_entry.grid(row=0, column=0, sticky="ew")
        self.text_entry.bind("<KeyRelease>", self._update)
        self.text_entry.bind("<FocusIn>", lambda e: self.text_entry.config(bg=C_FOCUS), add="+")
        self.text_entry.bind("<FocusOut>", lambda e: self.text_entry.config(bg="white"), add="+")
        self.text_entry.bind("<Button-3>", self._show_menu)
        self.text_entry.bind("<Key>", self._shortcuts)
        
        txt_scroll = ttk.Scrollbar(text_frame, orient="vertical", command=self.text_entry.yview)
        txt_scroll.grid(row=0, column=1, sticky="ns")
        self.text_entry.config(yscrollcommand=txt_scroll.set)

        ttk.Label(self.editor_frame, text="Match Result:", font=F_LBL, foreground="#000000").grid(row=3, column=0, sticky="w", pady=(0, 2))
        result_frame = ttk.Frame(self.editor_frame)
        result_frame.grid(row=4, column=0, sticky="nsew")
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.result_entry = tk.Text(result_frame, font=F_TXT, state="disabled", bg="#cccccc", relief="sunken", bd=1, highlightthickness=0, selectbackground=C_SEL_BG, selectforeground=C_SEL_FG)
        self.result_entry.grid(row=0, column=0, sticky="nsew")
        res_scroll = ttk.Scrollbar(result_frame, orient="vertical", command=self.result_entry.yview)
        res_scroll.grid(row=0, column=1, sticky="ns")
        self.result_entry.config(yscrollcommand=res_scroll.set)

        self.result_entry.tag_config("match", background=C_MATCH_BG, foreground=C_MATCH_FG)

    def _insert_newline(self, event=None):
        try:
            self.pattern_entry.delete("sel.first", "sel.last")
        except tk.TclError:
            pass
        self.pattern_entry.insert(tk.INSERT, r"\n")
        self._update()
        return "break"

    def _ph(self, widget, text):
        def focus_in(event):
            if widget.get("1.0", "end-1c") == text:
                widget.config(undo=False, fg="black")
                widget.delete("1.0", tk.END)
                widget.config(undo=True)

        def focus_out(event):
            if not widget.get("1.0", "end-1c").strip():
                widget.config(undo=False, fg=C_PH)
                widget.insert("1.0", text)
                widget.config(undo=True)

        widget.config(undo=False, fg=C_PH)
        widget.insert("1.0", text)
        widget.config(undo=True)
        widget.bind("<FocusIn>", focus_in, add="+")
        widget.bind("<FocusOut>", focus_out, add="+")

    def _is_ph(self, widget):
        placeholder = {self.pattern_entry: self.ph_pattern, self.text_entry: self.ph_text}.get(widget)
        return placeholder is not None and widget.get("1.0", "end-1c") == placeholder

    def _shortcuts(self, event):
        modifier = 0x8 if sys.platform == "darwin" else 0x4
        if not event.state & modifier:
            return

        shortcuts = WIN_SHORTCUTS if sys.platform == "win32" else OTHER_SHORTCUTS
        key = event.keycode if sys.platform == "win32" else event.keysym.lower()
        action = shortcuts.get(key)
        if not action:
            return

        if action == "select_all":
            event.widget.tag_add("sel", "1.0", "end-1c")
        else:
            self._clip(action, event.widget)
        return "break"

    def _clip(self, action, widget):
        if widget not in (self.pattern_entry, self.text_entry) or self._is_ph(widget):
            return

        try:
            if action == "paste":
                text = self.root.clipboard_get()
                if widget == self.pattern_entry:
                    text = text.replace("\r\n", "\n").replace("\n", r"\n")
                else:
                    text = text.replace(r"\n", "\n")

                try:
                    widget.delete("sel.first", "sel.last")
                except tk.TclError:
                    pass
                widget.insert(tk.INSERT, text)

            elif action in ("copy", "cut"):
                selected = widget.get("sel.first", "sel.last")
                self.root.clipboard_clear()
                self.root.clipboard_append(selected)
                if action == "cut":
                    widget.delete("sel.first", "sel.last")

            elif action == "undo":
                widget.edit_undo()
            elif action == "redo":
                widget.edit_redo()
            else:
                return
        except tk.TclError:
            return

        if action != "copy":
            self._update()

    def _setup_menu(self):
        self.menu = tk.Menu(self.root, tearoff=0)
        for action in ("cut", "copy", "paste"):
            self.menu.add_command(label=action.capitalize(), command=lambda a=action: self._clip(a, self.context_widget))

    def _show_menu(self, event):
        self.context_widget = event.widget
        event.widget.focus_set()
        self.menu.post(event.x_root, event.y_root)

    def _init_sash(self):
        self.root.update_idletasks()
        self.default_width = self.scrollable_frame.winfo_reqwidth() + 40
        self.paned_window.sashpos(0, self.default_width)
        self.paned_window.bind("<ButtonRelease-1>", lambda e: self.paned_window.sashpos(0, max(self.default_width // 4, min(self.paned_window.sashpos(0), self.default_width))) if self.sidebar_visible else None)

    def _toggle_sidebar(self):
        self.sidebar_visible = not self.sidebar_visible
        if self.sidebar_visible:
            self.paned_window.insert(0, self.sidebar_frame, weight=0)
            self.btn_show.grid_remove()
            self.root.after(10, lambda: self.paned_window.sashpos(0, self.default_width))
        else:
            self.paned_window.forget(self.sidebar_frame)
            self.btn_show.grid()

    def _update(self, event=None):
        pattern = self.pattern_entry.get("1.0", "end-1c")
        text = self.text_entry.get("1.0", "end-1c")
        
        if pattern == self.ph_pattern: pattern = ""
        if text == self.ph_text: text = ""
        
        self.error_label.grid_remove()
        self.error_label.config(text="")

        error = validate_pattern(pattern)
        self.re_error = bool(error)
        
        if self.re_error:
            self.pattern_entry.config(bg=C_ERR)
            self.error_label.config(text=f"Invalid regular expression: {error}")
            self.error_label.grid(row=2, column=0, sticky="w", pady=(2, 0))
            self._render([(text, False)])
        else:
            self.pattern_entry.config(bg=C_FOCUS if self.pattern_focused else "white")
            segments = get_highlighted_segments(pattern, text) if pattern and text != "" else [(text, False)]
            self._render(segments)

    def _render(self, segments):
        self.result_entry.config(state="normal")
        self.result_entry.delete("1.0", tk.END)
        for part, is_match in segments:
            self.result_entry.insert(tk.END, part, "match" if is_match else "")
        self.result_entry.tag_raise("sel")
        self.result_entry.config(state="disabled")

    def _bind_wheel(self, widget):
        def on_mousewheel(e):
            self.canvas.yview_scroll(int(-1*(e.delta/120)), "units")
        def on_linux_scroll_up(e):
            self.canvas.yview_scroll(-1, "units")
        def on_linux_scroll_down(e):
            self.canvas.yview_scroll(1, "units")

        widget.bind("<MouseWheel>", on_mousewheel)
        widget.bind("<Button-4>", on_linux_scroll_up)
        widget.bind("<Button-5>", on_linux_scroll_down)
        
        for child in widget.winfo_children(): 
            self._bind_wheel(child)