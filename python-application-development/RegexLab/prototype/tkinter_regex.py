import re, tkinter as tk

root = tk.Tk(); root.geometry('800x500'); root.title('Regular Expressions'); root.option_add('*selectBackground', '#1a75ff')
title_font, entry_font, span, RE_error = ('', 10, 'bold'), ('', 12, 'bold'), 0, False

def MR_update(event):
    global RE_error
    pattern, string = YRE_entry.get(), YTS_entry.get('1.0', tk.END)
    MR_entry.config(state = "normal")
    MR_entry.delete('1.0', tk.END)
    try:
        matches, last_index = re.finditer(pattern, string), 0
        IRE_title.place_forget()
        YRE_entry.config(bg = "#ffffe6" if root.focus_get() == YRE_entry else "white")
        for match in matches:
            start, end = match.span()
            MR_entry.insert(tk.END, string[last_index:start])
            MR_entry.insert(tk.END, string[start:end], "colored")
            last_index = end
        MR_entry.insert(tk.END, string[last_index:])
        MR_entry.tag_config("colored", background="#aaffaa", foreground="#227722", selectbackground="#1a75ff", selectforeground="white")
        RE_error = False
    except re.error:
        MR_entry.insert('1.0', string)
        IRE_title.place(x = root.winfo_width() - IRE_title.winfo_width() - span, y = span)
        YRE_entry.config(bg = '#ffcccc')
        RE_error = True
    MR_entry.config(state = "disabled")

MR_title = tk.Label(root, text = "Match result:", font = title_font)
YRE_title = tk.Label(root, text = "Your regular expression:", font = title_font)
YTS_title = tk.Label(root, text = "Your test string:", font = title_font)
IRE_title = tk.Label(root, fg = '#ff6666', font = title_font, text = "Invalid regular expression: unexpected end of regular expression")
YRE_entry = tk.Entry(root, font = entry_font, selectforeground = 'white'); YTS_entry = tk.Text(root, font = ('', 12, 'bold'), selectforeground = 'white')
YRE_entry.bind("<FocusIn>", lambda event: YRE_entry.config(bg = '#ffcccc' if RE_error else '#ffffe6'))
YRE_entry.bind("<FocusOut>", lambda event: YRE_entry.config(bg = '#ffcccc' if RE_error else 'white'))
YRE_entry.bind("<<Paste>>", lambda event: YRE_entry.delete(tk.SEL_FIRST, tk.SEL_LAST) if YRE_entry.get() else None)
YTS_entry.bind("<FocusIn>", lambda event: YTS_entry.config(bg = '#ffffe6'))
YTS_entry.bind("<FocusOut>", lambda event: YTS_entry.config(bg = 'white'))
YTS_entry.bind("<<Paste>>", lambda event: YTS_entry.delete(tk.SEL_FIRST, tk.SEL_LAST) if YTS_entry.get('1.0', tk.END).strip() else YTS_entry.insert(0, root.clipboard_get()))
YTS_entry.bind("<KeyRelease>", MR_update); YRE_entry.bind("<KeyRelease>", MR_update)
MR_entry = tk.Text(root, font = entry_font, bg = '#cccccc', state = 'disabled', selectforeground="white")

for obj in root.winfo_children():obj.place(y = 0, x = 0)

def place_objects():
    global span
    span = max(root.winfo_width() // 50, root.winfo_height() // 50)
    IRE_title.place_forget()
    YRE_title.place(x = span, y = span)
    YRE_entry.place(x = span, y = YRE_title.winfo_height() + span, width = root.winfo_width() - span*2)
    YTS_title.place(x = span, y = YRE_title.winfo_height() + YRE_entry.winfo_height() + span*2)
    YTS_entry.place(x = span, y = YRE_title.winfo_height() + YRE_entry.winfo_height() + YTS_title.winfo_height() + span*2,
    width = root.winfo_width() - span*2, height = root.winfo_height()//2 - YRE_title.winfo_height() - YRE_entry.winfo_height() - span*2); root.update()
    MR_title.place(x = span, y = YRE_title.winfo_height() + YRE_entry.winfo_height() + YTS_title.winfo_height() + YTS_entry.winfo_height() + span*3)
    MR_entry.place(x = span, y = YRE_title.winfo_height() + YRE_entry.winfo_height() + YTS_title.winfo_height() + YTS_entry.winfo_height() + MR_title.winfo_height() + span*3,
    width = root.winfo_width() - span*2, height = root.winfo_height()//2 - YRE_title.winfo_height() - YRE_entry.winfo_height() - span*2)

root.bind("<Button>", lambda event: root.focus_set() if isinstance(event.widget, tk.Tk) else None)
root.after(100, place_objects); root.mainloop()