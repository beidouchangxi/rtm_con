import tkinter as tk
from tkinter import ttk, messagebox, Menu
import binascii
import ast
import pprint
import sys
import datetime

from construct import Container

from rtm_con.utilities import con_to_pyobj

# ==========================================
# GUI Application
# ==========================================

class MessageAnalyzer(tk.Tk):
    '''Hex and object viewer for a constuct container, mostly for rtm msg'''
    def __init__(self, msg_map:dict[str, Container], *, tittle:str="Message analyzer"):
        super().__init__()
        self.msg_map = msg_map
        
        # Track selected protocol
        self.selected_proto_key = tk.StringVar(value=next(iter(self.msg_map)))

        self.title(tittle)
        self.geometry("1200x900")
        self.minsize(1000, 750)

        # Data State
        self.current_bytes = b""
        self.bytes_per_line = 10
        self.selection_range = (None, None) 
        
        # Layout State for Maximize/Restore
        self.is_text_maximized = False
        self.is_tree_maximized = False
        
        # Map tree item IDs to actual python objects for copy functionality
        self.tree_item_map = {} 

        # Style configuration
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6)
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("Treeview", font=("Arial", 10), rowheight=25)
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))
        self.style.configure("Bold.TLabel", font=("Arial", 10, "bold"))
        
        self.mono_font = ("Consolas", 10) if sys.platform == "win32" else ("Courier", 10)

        self.create_widgets()

    def create_widgets(self):
        # Main layout: Vertical Flow
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- Part 4: Bottom Buttons (Copy & Clear) ---
        # Pack first to reserve space at bottom
        self.frame_bottom_btns = ttk.Frame(self.main_frame, padding=10)
        self.frame_bottom_btns.pack(side=tk.BOTTOM, fill=tk.X)
        
        center_btn_frame = ttk.Frame(self.frame_bottom_btns)
        center_btn_frame.pack(anchor="center")

        # Copy Group
        ttk.Button(center_btn_frame, text="Copy Message", command=self.copy_full_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_btn_frame, text="Copy Data", command=self.copy_full_data).pack(side=tk.LEFT, padx=5)

        # Separator
        ttk.Separator(center_btn_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=15)

        # Clear Group
        ttk.Button(center_btn_frame, text="Clear Message", command=self.clear_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_btn_frame, text="Clear Data", command=self.clear_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(center_btn_frame, text="Clear All", command=self.clear_all).pack(side=tk.LEFT, padx=5)

        # We'll use a PanedWindow to separate Message Area and Data Area
        self.main_pane = ttk.PanedWindow(self.main_frame, orient=tk.VERTICAL)
        self.main_pane.pack(fill=tk.BOTH, expand=True)

        # --- Part 1: Message (Binary) ---
        self.frame_message = ttk.LabelFrame(self.main_pane, text="Message (Binary)", padding=10)
        self.main_pane.add(self.frame_message, weight=2)

        # Protocol Selection (Top of Message Area)
        proto_frame = ttk.Frame(self.frame_message)
        proto_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        ttk.Label(proto_frame, text="Protocol:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        for key in self.msg_map:
            rb = ttk.Radiobutton(proto_frame, text=key, variable=self.selected_proto_key, value=key)
            rb.pack(side=tk.LEFT, padx=10)

        # Message Input (Below Protocol Selection)
        input_frame = ttk.Frame(self.frame_message)
        input_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 10))
        ttk.Label(input_frame, text="Input Hex String:").pack(side=tk.LEFT)
        
        self.entry_hex = ttk.Entry(input_frame)
        self.entry_hex.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry_hex.bind("<Return>", self.on_hex_enter)
        self.entry_hex.bind("<<Paste>>", self.on_hex_paste)

        # Status Bar (Bottom of Message Frame)
        self.msg_status_frame = ttk.Frame(self.frame_message)
        self.msg_status_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(5, 0))
        
        self.lbl_total_len = ttk.Label(self.msg_status_frame, text="Total Length: 0 (0x0) bytes", style="Bold.TLabel")
        self.lbl_total_len.pack(side=tk.LEFT, padx=10)
        self.lbl_selection = ttk.Label(self.msg_status_frame, text="Selected: 0 (0x0) bytes")
        self.lbl_selection.pack(side=tk.LEFT, padx=10)
        self.lbl_byte_detail = ttk.Label(self.msg_status_frame, text="Byte Info: N/A")
        self.lbl_byte_detail.pack(side=tk.RIGHT, padx=10)

        # Hex Editor Display Area (Middle - Expands)
        display_container = ttk.Frame(self.frame_message)
        display_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        display_container.columnconfigure(1, weight=0) # Offset
        display_container.columnconfigure(2, weight=1) # Hex
        display_container.columnconfigure(3, weight=1) # Dec
        display_container.columnconfigure(4, weight=1) # ASCII
        display_container.columnconfigure(5, weight=0) # Scrollbar

        headers = ["Offset (Hex | Dec)", "Hex View", "Decimal View", "ASCII View"]
        for i, h in enumerate(headers, 1):
            lbl = ttk.Label(display_container, text=h, font=("Arial", 9, "bold"), anchor="center")
            lbl.grid(row=0, column=i, sticky="ew", padx=2)

        self.txt_offset = tk.Text(display_container, width=20, font=self.mono_font, bg="#e0e0e0", state="disabled", wrap="none")
        self.txt_hex = tk.Text(display_container, width=35, font=self.mono_font, wrap="none")
        self.txt_dec = tk.Text(display_container, width=45, font=self.mono_font, wrap="none")
        self.txt_ascii = tk.Text(display_container, width=15, font=self.mono_font, wrap="none")

        self.text_widgets = [self.txt_offset, self.txt_hex, self.txt_dec, self.txt_ascii]

        self.sb = ttk.Scrollbar(display_container, orient="vertical", command=self.sync_scroll)
        self.sb.grid(row=1, column=5, sticky="ns")

        for i, widget in enumerate(self.text_widgets):
            widget.grid(row=1, column=i+1, sticky="nsew", padx=1)
            widget["yscrollcommand"] = self.on_text_scroll
            widget.bind("<Button-1>", lambda e, w=widget: self.on_text_click(e, w))
            widget.bind("<B1-Motion>", lambda e, w=widget: self.on_text_drag(e, w))
            widget.bind("<ButtonRelease-1>", lambda e, w=widget: self.on_text_release(e, w))
            widget.bind("<MouseWheel>", self.on_mouse_wheel) 
            widget.bind("<Button-4>", self.on_mouse_wheel)
            widget.bind("<Button-5>", self.on_mouse_wheel)

        self.msg_context_menu = Menu(self, tearoff=0)
        self.msg_context_menu.add_command(label="Copy Hex String", command=self.copy_hex_selection)
        self.msg_context_menu.add_command(label="Copy ASCII String", command=self.copy_ascii_selection)
        for w in self.text_widgets[1:]: 
            w.bind("<Button-3>", self.show_msg_context_menu)


        # --- Part 2: Conversion Buttons Frame (Middle) ---
        self.frame_controls = ttk.Frame(self.main_pane, padding=10)
        self.main_pane.add(self.frame_controls, weight=0)
        
        btn_container = ttk.Frame(self.frame_controls)
        btn_container.pack(anchor="center")

        btn_msg_to_data = ttk.Button(btn_container, text="Message to Data  ⬇", command=self.msg_to_data)
        btn_msg_to_data.pack(side=tk.LEFT, padx=30)

        btn_data_to_msg = ttk.Button(btn_container, text="Data to Message  ⬆", command=self.data_to_msg)
        btn_data_to_msg.pack(side=tk.LEFT, padx=30)


        # --- Part 3: Data (Dict) - Split View ---
        self.frame_data = ttk.LabelFrame(self.main_pane, text="Data (Python Dictionary)", padding=10)
        self.main_pane.add(self.frame_data, weight=3)

        self.data_split = ttk.PanedWindow(self.frame_data, orient=tk.HORIZONTAL)
        self.data_split.pack(fill=tk.BOTH, expand=True)

        # -- Left: Text Editor Container --
        self.data_text_container = ttk.Frame(self.data_split)
        self.data_split.add(self.data_text_container, weight=1)
        
        # Header for Text
        text_header = ttk.Frame(self.data_text_container)
        text_header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(text_header, text="Input / Raw Text (Python Dict):").pack(side=tk.LEFT, anchor="center")
        self.btn_max_text = ttk.Button(text_header, text="⛶", width=3, command=self.toggle_max_text)
        self.btn_max_text.pack(side=tk.RIGHT)

        # Content for Text
        text_content_frame = ttk.Frame(self.data_text_container)
        text_content_frame.pack(fill=tk.BOTH, expand=True)
        
        self.txt_data = tk.Text(text_content_frame, font=self.mono_font, wrap="none")
        self.txt_data_scroll_y = ttk.Scrollbar(text_content_frame, orient="vertical", command=self.txt_data.yview)
        self.txt_data_scroll_x = ttk.Scrollbar(text_content_frame, orient="horizontal", command=self.txt_data.xview)
        self.txt_data.configure(yscrollcommand=self.txt_data_scroll_y.set, xscrollcommand=self.txt_data_scroll_x.set)
        
        self.txt_data_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_data_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.txt_data.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.txt_data.bind("<<Paste>>", self.on_data_paste)
        self.txt_data.bind("<Return>", self.on_data_return)

        # -- Right: Tree View Container --
        self.data_tree_container = ttk.Frame(self.data_split)
        self.data_split.add(self.data_tree_container, weight=2)
        
        # Header for Tree
        tree_header = ttk.Frame(self.data_tree_container)
        tree_header.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(tree_header, text="Tree Visualization (Private keys hidden):").pack(side=tk.LEFT, anchor="center")
        self.btn_max_tree = ttk.Button(tree_header, text="⛶", width=3, command=self.toggle_max_tree)
        self.btn_max_tree.pack(side=tk.RIGHT)

        # Content for Tree
        tree_content_frame = ttk.Frame(self.data_tree_container)
        tree_content_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_content_frame, columns=("Type", "Value"), selectmode="browse")
        self.tree.heading("#0", text="Key / Index")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Value", text="Value")
        
        self.tree.column("#0", width=200, anchor="w")
        self.tree.column("Type", width=100, anchor="w")
        self.tree.column("Value", width=300, anchor="w")

        tree_scroll_y = ttk.Scrollbar(tree_content_frame, orient="vertical", command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_content_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.tree_context_menu = Menu(self, tearoff=0)
        self.tree_context_menu.add_command(label="Copy Python Definition", command=self.copy_tree_item_def)
        self.tree.bind("<Button-3>", self.show_tree_context_menu)

    # ==========================================
    # Logic: Maximize / Restore
    # ==========================================
    def toggle_max_text(self):
        if self.is_text_maximized:
            # Restore View
            self.restore_layout()
            self.btn_max_text.config(text="⛶")
            self.is_text_maximized = False
        else:
            # Maximize Text
            # 1. Reset Tree max if active (mutually exclusive)
            if self.is_tree_maximized:
                self.toggle_max_tree() # This restores layout
            
            # 2. Hide other main components
            self.main_pane.forget(self.frame_message)
            self.main_pane.forget(self.frame_controls)
            self.frame_bottom_btns.pack_forget()
            
            # 3. Hide Tree Pane (Right side of data)
            self.data_split.forget(self.data_tree_container)
            
            self.btn_max_text.config(text="↙") # Restore icon
            self.is_text_maximized = True

    def toggle_max_tree(self):
        if self.is_tree_maximized:
            # Restore View
            self.restore_layout()
            self.btn_max_tree.config(text="⛶")
            self.is_tree_maximized = False
        else:
            # Maximize Tree
            # 1. Reset Text max if active
            if self.is_text_maximized:
                self.toggle_max_text()
            
            # 2. Hide other main components
            self.main_pane.forget(self.frame_message)
            self.main_pane.forget(self.frame_controls)
            self.frame_bottom_btns.pack_forget()
            
            # 3. Hide Text Pane (Left side of data)
            self.data_split.forget(self.data_text_container)
            
            self.btn_max_tree.config(text="↙")
            self.is_tree_maximized = True

    def restore_layout(self):
        
        if self.is_text_maximized or self.is_tree_maximized:
            # Re-insert Message at top
            self.main_pane.insert(0, self.frame_message)
            # Re-insert Controls at index 1
            self.main_pane.insert(1, self.frame_controls)
            
            # FIX: Force main pane to unpack so clear buttons can be packed 
            # to bottom FIRST, preserving layout order.
            self.main_pane.pack_forget()
            self.frame_bottom_btns.pack(side=tk.BOTTOM, fill=tk.X)
            self.main_pane.pack(fill=tk.BOTH, expand=True)
            
            # Restore Data Split
            if self.is_text_maximized:
                # Add Tree back to the right
                self.data_split.add(self.data_tree_container, weight=2)
            elif self.is_tree_maximized:
                # Add Text back to the left (insert before tree)
                self.data_split.insert(0, self.data_text_container, weight=1)


    # ==========================================
    # Logic: Synchronization & Scrolling (Message)
    # ==========================================
    def sync_scroll(self, *args):
        for widget in self.text_widgets:
            widget.yview(*args)

    def on_text_scroll(self, first, last):
        self.sb.set(first, last)
        for widget in self.text_widgets:
            # Check if sync is needed to avoid infinite loop or redundant updates
            if widget.yview()[0] != float(first):
                widget.yview_moveto(first)

    def on_mouse_wheel(self, event):
        if event.delta:
            for widget in self.text_widgets:
                widget.yview_scroll(int(-1*(event.delta/120)), "units")
        elif event.num == 4:
             for widget in self.text_widgets:
                widget.yview_scroll(-1, "units")
        elif event.num == 5:
             for widget in self.text_widgets:
                widget.yview_scroll(1, "units")
        return "break"

    # ==========================================
    # Logic: Message Input & Rendering
    # ==========================================
    def on_hex_enter(self, event):
        self.load_hex_string(self.entry_hex.get())

    def on_hex_paste(self, event):
        self.after(50, lambda: self.load_hex_string(self.entry_hex.get()))

    def load_hex_string(self, hex_str):
        cleaned = hex_str.replace(" ", "").replace("\n", "").replace("\r", "").replace("0x", "")
        try:
            data = binascii.unhexlify(cleaned)
            self.current_bytes = data
            self.refresh_hex_display()
        except binascii.Error:
            messagebox.showerror("Input Error", "Invalid Hex String provided.")
            return

    def refresh_hex_display(self):
        for w in self.text_widgets:
            w.config(state="normal")
            w.delete("1.0", tk.END)
        
        for w in self.text_widgets:
            w.tag_configure("highlight", background="#add8e6", foreground="black")
            w.tag_configure("current_byte", background="yellow", foreground="black")
            w.tag_configure("center", justify='center') # Configure center alignment

        data = self.current_bytes
        length = len(data)
        self.lbl_total_len.config(text=f"Total Length: {length} (0x{length:X}) bytes")
        self.selection_range = (None, None)
        self.lbl_selection.config(text="Selected: 0 (0x0) bytes")
        self.lbl_byte_detail.config(text="Byte Info: N/A")

        for i in range(0, length, self.bytes_per_line):
            chunk = data[i : i + self.bytes_per_line]
            offset_hex = f"{i:04X}"
            offset_dec = f"{i:04d}"
            # Apply "center" tag to all insertions
            self.txt_offset.insert(tk.END, f"0x{offset_hex} | {offset_dec}\n", "center")
            
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            self.txt_hex.insert(tk.END, f"{hex_part}\n", "center")
            
            dec_part = " ".join(f"{b:03d}" for b in chunk)
            self.txt_dec.insert(tk.END, f"{dec_part}\n", "center")
            
            ascii_part = ""
            for b in chunk:
                if 32 <= b <= 126:
                    ascii_part += chr(b) + " "
                else:
                    ascii_part += ". "
            self.txt_ascii.insert(tk.END, f"{ascii_part}\n", "center")

        self.txt_offset.config(state="disabled")
        for w in self.text_widgets[1:]:
             w.bind("<Key>", lambda e: "break")

    # ==========================================
    # Logic: Interaction (Click & Select)
    # ==========================================
    def get_byte_index_from_mouse(self, widget, event):
        try:
            row_str, col_str = widget.index(f"@{event.x},{event.y}").split('.')
            row = int(row_str) - 1
            if row < 0: return None
            
            col = int(col_str)
            byte_col = -1
            if widget == self.txt_hex: byte_col = col // 3
            elif widget == self.txt_dec: byte_col = col // 4
            elif widget == self.txt_ascii: byte_col = col // 2
                
            if byte_col >= self.bytes_per_line: byte_col = self.bytes_per_line - 1
            byte_index = row * self.bytes_per_line + byte_col
            if byte_index >= len(self.current_bytes): return None
            return byte_index
        except:
            return None

    def highlight_bytes(self, start_idx, end_idx):
        if start_idx is None or end_idx is None: return
        s = min(start_idx, end_idx)
        e = max(start_idx, end_idx)
        self.selection_range = (s, e)
        
        count = e - s + 1
        self.lbl_selection.config(text=f"Selected: {count} (0x{count:X}) bytes")
        try:
            val = self.current_bytes[end_idx]
            
            # Uint16 logic
            u16_be = "N/A"
            u16_le = "N/A"
            if end_idx + 1 < len(self.current_bytes):
                b_slice = self.current_bytes[end_idx:end_idx+2]
                u16_be = int.from_bytes(b_slice, 'big')
                u16_le = int.from_bytes(b_slice, 'little')
            
            ascii_char = repr(chr(val)) if 32 <= val <= 126 else '.'
            
            detail_text = (f"Offset: {end_idx} (0x{end_idx:X}) | "
                           f"Hex: {val:02X} | "
                           f"Dec(Uint8): {val} | "
                           f"Dec(Uint16BE): {u16_be} | "
                           f"Dec(Uint16LE): {u16_le} | "
                           f"ASCII: {ascii_char}")
            
            self.lbl_byte_detail.config(text=detail_text)
        except IndexError:
            pass

        for w in self.text_widgets:
            w.tag_remove("highlight", "1.0", tk.END)
            w.tag_remove("current_byte", "1.0", tk.END)

        for i in range(s, e + 1):
            row = (i // self.bytes_per_line) + 1
            col_idx = i % self.bytes_per_line
            
            self.txt_offset.tag_add("highlight", f"{row}.0", f"{row}.end")
            h_start = col_idx * 3
            self.txt_hex.tag_add("highlight", f"{row}.{h_start}", f"{row}.{h_start+2}")
            if i == end_idx: self.txt_hex.tag_add("current_byte", f"{row}.{h_start}", f"{row}.{h_start+2}")

            d_start = col_idx * 4
            self.txt_dec.tag_add("highlight", f"{row}.{d_start}", f"{row}.{d_start+3}")
            if i == end_idx: self.txt_dec.tag_add("current_byte", f"{row}.{d_start}", f"{row}.{d_start+3}")

            a_start = col_idx * 2
            self.txt_ascii.tag_add("highlight", f"{row}.{a_start}", f"{row}.{a_start+1}")
            if i == end_idx: self.txt_ascii.tag_add("current_byte", f"{row}.{a_start}", f"{row}.{a_start+1}")

    def on_text_click(self, event, widget):
        idx = self.get_byte_index_from_mouse(widget, event)
        if idx is not None:
            self._drag_start_idx = idx
            self.highlight_bytes(idx, idx)
        else:
            self._drag_start_idx = None

    def on_text_drag(self, event, widget):
        if self._drag_start_idx is None: return
        idx = self.get_byte_index_from_mouse(widget, event)
        if idx is not None:
            self.highlight_bytes(self._drag_start_idx, idx)

    def on_text_release(self, event, widget):
        self._drag_start_idx = None

    def show_msg_context_menu(self, event):
        if self.selection_range[0] is not None:
            self.msg_context_menu.post(event.x_root, event.y_root)

    def copy_hex_selection(self):
        s, e = self.selection_range
        if s is None: return
        data = self.current_bytes[s : e+1]
        self.clipboard_clear()
        self.clipboard_append(data.hex().upper())

    def copy_ascii_selection(self):
        s, e = self.selection_range
        if s is None: return
        data = self.current_bytes[s : e+1]
        txt = "".join([chr(b) if 32<=b<=126 else "." for b in data])
        self.clipboard_clear()
        self.clipboard_append(txt)

    # ==========================================
    # Logic: Data Tree Visualization & Interaction
    # ==========================================
    def populate_tree(self, data):
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Reset object map
        self.tree_item_map = {}
        
        self.tree_insert_node("", data)

    def tree_insert_node(self, parent_id, value, key_label=None):
        # Determine label and values
        text_label = str(key_label) if key_label is not None else "Root"
        val_type = type(value).__name__
        val_display = ""
        
        node_id = None

        if isinstance(value, (dict, list, tuple)):
            # Complex types
            if isinstance(value, (list, tuple)):
                val_display = f"Array [{len(value)} items]"
            elif isinstance(value, dict):
                # Filter out hidden keys for display count
                visible_count = len([k for k in value.keys() if not str(k).startswith('_')])
                val_display = f"Object {{{visible_count} keys}}"
            
            node_id = self.tree.insert(parent_id, "end", text=text_label, values=(val_type, val_display), open=False)
            
            # Register object for copy functionality
            self.tree_item_map[node_id] = value

            # Recurse
            if isinstance(value, dict):
                for k, v in value.items():
                    # FILTER: Ignore keys starting with _
                    if str(k).startswith('_'):
                        continue
                    self.tree_insert_node(node_id, v, key_label=k)
            elif isinstance(value, (list, tuple)):
                for i, v in enumerate(value):
                    self.tree_insert_node(node_id, v, key_label=f"[{i}]")
            
            # If it's the root, expand it
            if parent_id == "":
                self.tree.item(node_id, open=True)
                
        else:
            # Primitive types
            val_display = str(value)
            node_id = self.tree.insert(parent_id, "end", text=text_label, values=(val_type, val_display))
            # Register object for copy functionality
            self.tree_item_map[node_id] = value

    def show_tree_context_menu(self, event):
        item_id = self.tree.identify_row(event.y)
        if item_id:
            self.tree.selection_set(item_id)
            self.tree_context_menu.post(event.x_root, event.y_root)

    def copy_tree_item_def(self):
        selection = self.tree.selection()
        if not selection: return
        item_id = selection[0]
        
        # Retrieve actual object
        obj = self.tree_item_map.get(item_id)
        
        try:
            # Format as python definition
            txt = pprint.pformat(obj, indent=4)
            self.clipboard_clear()
            self.clipboard_append(txt)
        except Exception as e:
            messagebox.showerror("Copy Error", f"Failed to format object: {e}")

    # ==========================================
    # Logic: Data Input (Validation & Formatting)
    # ==========================================
    def on_data_paste(self, event):
        try:
            content = self.clipboard_get()
            self.validate_and_format_data_input(content)
            return "break" # Stop default paste
        except tk.TclError:
            pass 
    
    def on_data_return(self, event):
        content = self.txt_data.get("1.0", tk.END)
        self.validate_and_format_data_input(content)
        return "break"

    def validate_and_format_data_input(self, text_content):
        # 1. Parse
        data_dict = self.parse_text_to_dict(text_content)
        
        if data_dict is not None:
            if not isinstance(data_dict, dict):
                 messagebox.showerror("Invalid Data", "Input must be a valid Python Dictionary definition.")
                 return

            # 2. Format (Prettify)
            pretty_str = pprint.pformat(data_dict, indent=4)
            
            # 3. Update Text Widget
            self.txt_data.delete("1.0", tk.END)
            self.txt_data.insert("1.0", pretty_str)
            
            # 4. Trigger Tree Update (Using clean dict from text)
            self.populate_tree(data_dict)
        else:
            messagebox.showerror("Invalid Data", "Input is not a valid Python definition.\nPlease check syntax.")

    def parse_text_to_dict(self, text):
        text = text.strip()
        if not text: return None
        try:
            # Try AST safe eval first
            return ast.literal_eval(text)
        except:
            try:
                # Fallback for datetime etc
                safe_locals = {
                    "datetime": datetime,
                    "True": True, "False": False, "None": None
                }
                return eval(text, {"__builtins__": {}}, safe_locals)
            except:
                return None

    def get_data_dict_from_text(self):
        content = self.txt_data.get("1.0", tk.END)
        return self.parse_text_to_dict(content)

    # ==========================================
    # Logic: Main Conversion Buttons
    # ==========================================
    def msg_to_data(self):
        if not self.current_bytes:
            messagebox.showwarning("Warning", "Message is empty.")
            return

        try:
            # 1. Parse raw bytes -> internal structure
            # Req: bytes 转 dict (用于展示部分)：msg.parse(binary_data)
            # Use selected protocol
            selected_proto = self.selected_proto_key.get()
            current_msg = self.msg_map[selected_proto]
            
            internal_obj = current_msg.parse(self.current_bytes)
            
            # 2. Path A: For Text Box
            # Req: bytes 转 dict (用于文本框)：con_to_pyobj(msg.parse(binary_data))
            data_dict_text = con_to_pyobj(internal_obj)
            pretty = pprint.pformat(data_dict_text, indent=4, sort_dicts=False)
            self.txt_data.delete("1.0", tk.END)
            self.txt_data.insert("1.0", pretty)
            
            # 3. Path B: For Tree View (Raw object with potential private keys)
            self.populate_tree(internal_obj)
            
        except Exception as e:
            messagebox.showerror("Conversion Failed", f"Failed to convert Message to Data:\n{str(e)}")

    def data_to_msg(self):
        # Use the data from the Text Box for conversion
        data_dict = self.get_data_dict_from_text()
        
        if data_dict is None:
            messagebox.showerror("Error", "Invalid Data in Text Box")
            return

        try:
            # Req: dict 转 bytes：msg.build(data_dict)
            selected_proto = self.selected_proto_key.get()
            current_msg = self.msg_map[selected_proto]
            
            binary_data = current_msg.build(data_dict)
            if not isinstance(binary_data, bytes):
                raise TypeError(f"Build returned {type(binary_data)}, expected bytes")

            self.current_bytes = binary_data
            self.refresh_hex_display()
            self.entry_hex.delete(0, tk.END)
            self.entry_hex.insert(0, binary_data.hex().upper())
            
            # Optional: Refresh tree 
            self.populate_tree(data_dict)
            
        except Exception as e:
            messagebox.showerror("Conversion Failed", f"Failed to convert Data to Message:\n{str(e)}")

    # ==========================================
    # Logic: Copy & Clear Buttons
    # ==========================================
    def copy_full_message(self):
        if not self.current_bytes:
            return
        self.clipboard_clear()
        self.clipboard_append(self.current_bytes.hex().upper())
        messagebox.showinfo("Copied", "Full Message Hex string copied to clipboard.")

    def copy_full_data(self):
        content = self.txt_data.get("1.0", tk.END).strip()
        if not content:
            return
        self.clipboard_clear()
        self.clipboard_append(content)
        messagebox.showinfo("Copied", "Data text content copied to clipboard.")

    def clear_message(self):
        self.entry_hex.delete(0, tk.END)
        self.current_bytes = b""
        self.refresh_hex_display()

    def clear_data(self):
        self.txt_data.delete("1.0", tk.END)
        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tree_item_map = {}

    def clear_all(self):
        self.clear_message()
        self.clear_data()

if __name__ == "__main__":
    from rtm_con.msg_format import msg, data_2016, data_2025
    app = MessageAnalyzer({
        "RTM message": msg,
        "Payload 2016": data_2016,
        "Payload 2025": data_2025,
    })
    app.mainloop()