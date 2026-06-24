import os
import json
import struct
import lzma
import time
import hashlib
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class TernosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ternos Secure Archiver")
        self.root.geometry("1050x700")
        self.root.configure(bg="#f5f6f5")
        self.root.minsize(900, 600)

        # Globals
        self.selected_files = [] # list of {"path": ..., "name": ..., "size": ..., "rel_path": ...}
        self.unpack_archive_path = None

        # Setup Styling
        self.setup_styles()
        
        # Create Menu
        self.create_menu()
        
        # Create Toolbar
        self.create_toolbar()
        
        # Main Layout
        self.create_main_layout()
        
        # Status Bar
        self.create_status_bar()

        self.log("Ядро Ternos Core (Tkinter GUI) инициализировано. Ожидание действий...", "info")

    def setup_styles(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Generic settings
        self.style.configure('.', font=("Segoe UI", 9))
        self.style.configure('TFrame', background='#f5f6f5')
        self.style.configure('TLabel', background='#f5f6f5', foreground='#212521')
        
        # Group Boxes (LabelFrame)
        self.style.configure('TLabelframe', background='#f5f6f5', bordercolor='#c2d1c5', lightcolor='#c2d1c5', darkcolor='#c2d1c5')
        self.style.configure('TLabelframe.Label', background='#f5f6f5', foreground='#2e7d32', font=("Segoe UI", 9, "bold"))

        # Notebook (Tabs)
        self.style.configure('TNotebook', background='#f5f6f5', bordercolor='#c2d1c5')
        self.style.configure('TNotebook.Tab', background='#e0e6e0', foreground='#5b635c', padding=[16, 6], font=("Segoe UI", 9, "bold"))
        self.style.map('TNotebook.Tab', background=[('selected', '#ffffff')], foreground=[('selected', '#2e7d32')])

        # Buttons (Solid Matte Green / White Theme)
        self.style.configure('TButton', background='#2e7d32', foreground='#ffffff', bordercolor='#1b5e20', font=("Segoe UI", 9, "bold"))
        self.style.map('TButton', background=[('active', '#1b5e20'), ('disabled', '#b2c2b4')], foreground=[('disabled', '#7a867c')])

        # Toolbar special buttons
        self.style.configure('Tool.TButton', background='#ffffff', foreground='#2e7d32', bordercolor='#2e7d32', font=("Segoe UI", 9))
        self.style.map('Tool.TButton', background=[('active', '#e0e6e0')])

        # Treeview (File grids)
        self.style.configure('Treeview', background='#ffffff', foreground='#212521', fieldbackground='#ffffff', bordercolor='#c2d1c5')
        self.style.configure('Treeview.Heading', background='#e0e6e0', foreground='#2e7d32', font=("Segoe UI", 9, "bold"), bordercolor='#c2d1c5')
        self.style.map('Treeview.Heading', background=[('active', '#c2d1c5')])

    def create_menu(self):
        self.menubar = tk.Menu(self.root)
        
        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label="Выход", command=self.root.quit)
        self.menubar.add_cascade(label="Файл", menu=self.file_menu)
        
        # Help Menu
        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label="О программе", command=self.show_about)
        self.menubar.add_cascade(label="Справка", menu=self.help_menu)
        
        self.root.config(menu=self.menubar)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg="#e0e6e0", bd=1, relief="raised", height=40)
        self.toolbar.pack(fill="x", side="top")

        self.btn_tb_add_files = ttk.Button(self.toolbar, text="Добавить файлы", style="Tool.TButton", command=self.select_files)
        self.btn_tb_add_files.pack(side="left", padx=4, pady=4)

        self.btn_tb_add_folder = ttk.Button(self.toolbar, text="Добавить папку", style="Tool.TButton", command=self.select_folder)
        self.btn_tb_add_folder.pack(side="left", padx=4, pady=4)

        self.btn_tb_clear = ttk.Button(self.toolbar, text="Очистить список", style="Tool.TButton", command=self.clear_file_list, state="disabled")
        self.btn_tb_clear.pack(side="left", padx=4, pady=4)

        self.separator = tk.Frame(self.toolbar, width=1, bd=1, relief="sunken", bg="#c2d1c5")
        self.separator.pack(side="left", fill="y", padx=8, pady=4)

        self.btn_tb_select_archive = ttk.Button(self.toolbar, text="Открыть архив (.ternos)", style="Tool.TButton", command=self.select_archive)
        self.btn_tb_select_archive.pack(side="left", padx=4, pady=4)

    def create_main_layout(self):
        self.main_frame = tk.Frame(self.root, bg="#f5f6f5")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left Column (Notebook with pack/unpack tabs)
        self.left_panel = tk.Frame(self.main_frame, bg="#f5f6f5")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.notebook = ttk.Notebook(self.left_panel)
        self.notebook.pack(fill="both", expand=True)

        self.create_pack_tab()
        self.create_unpack_tab()

        # Right Column (KDF stats and log console)
        self.right_panel = tk.Frame(self.main_frame, bg="#f5f6f5", width=350)
        self.right_panel.pack(side="right", fill="both", expand=False, padx=(6, 0))
        self.right_panel.pack_propagate(False)

        # 1. Crypto Analyzer Group
        self.analyzer_group = ttk.LabelFrame(self.right_panel, text="Крипто-анализатор архива")
        self.analyzer_group.pack(fill="x", pady=(0, 10))

        # Stats Table Layout
        self.stats_frame = tk.Frame(self.analyzer_group, bg="#f5f6f5")
        self.stats_frame.pack(fill="x", padx=6, pady=6)

        labels = [
            ("Алгоритм:", "val_algo", "AES-GCM-256 (AEAD)"),
            ("Ключ (KDF):", "val_kdf", "PBKDF2 SHA-256"),
            ("Итераций KDF:", "val_iter", "600 000"),
            ("Целостность:", "val_integrity", "—"),
            ("Соль (Salt):", "val_salt", "нет соли"),
            ("Вектор (IV):", "val_iv", "нет IV")
        ]

        self.stat_widgets = {}
        for idx, (label_text, key, default_val) in enumerate(labels):
            lbl = ttk.Label(self.stats_frame, text=label_text, font=("Segoe UI", 9, "bold"))
            lbl.grid(row=idx, column=0, sticky="w", pady=4, padx=(0, 10))
            
            val = ttk.Label(self.stats_frame, text=default_val, font=("Segoe UI", 9))
            val.grid(row=idx, column=1, sticky="w", pady=4)
            self.stat_widgets[key] = val

        # Adjust column weight
        self.stats_frame.columnconfigure(1, weight=1)

        # 2. Operations Log Group
        self.log_group = ttk.LabelFrame(self.right_panel, text="Протокол операций")
        self.log_group.pack(fill="both", expand=True)

        self.console_log = scrolledtext.ScrolledText(self.log_group, wrap="word", bg="#ffffff", fg="#000000", font=("Consolas", 9), bd=1, relief="solid")
        self.console_log.pack(fill="both", expand=True, padx=4, pady=4)
        
        # Tags for colored logs
        self.console_log.tag_config("info", foreground="#000000")
        self.console_log.tag_config("success", foreground="#2e7d32", font=("Consolas", 9, "bold"))
        self.console_log.tag_config("warning", foreground="#a56a00")
        self.console_log.tag_config("error", foreground="#c62828", font=("Consolas", 9, "bold"))
        self.console_log.tag_config("time", foreground="#777777")

    def create_pack_tab(self):
        self.pack_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pack_tab, text="Запаковать (Запись)")

        self.pack_page = tk.Frame(self.pack_tab, bg="#ffffff", bd=1, relief="solid")
        self.pack_page.pack(fill="both", expand=True, padx=4, pady=4)

        # Description bar
        self.desc_pack = tk.Label(self.pack_page, bg="#ffffe1", fg="#212521", font=("Segoe UI", 8), bd=1, relief="solid", justify="left", anchor="w", padx=10, pady=8,
                                  text="Для создания защищенного архива добавьте файлы или папку на панели управления,\nукажите пароль дешифрации архива и нажмите кнопку выполнения.")
        self.desc_pack.pack(fill="x", padx=10, pady=10)

        # File List Group
        self.group_files = ttk.LabelFrame(self.pack_page, text="Файлы для архивации")
        self.group_files.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Treeview Scrollbar
        self.tree_scroll = ttk.Scrollbar(self.group_files)
        self.tree_scroll.pack(side="right", fill="y")

        # Treeview Table
        self.pack_files_tree = ttk.Treeview(self.group_files, columns=("path", "size"), show="headings", yscrollcommand=self.tree_scroll.set)
        self.pack_files_tree.heading("path", text="Имя объекта / Относительный путь")
        self.pack_files_tree.heading("size", text="Размер")
        self.pack_files_tree.column("path", width=350, anchor="w")
        self.pack_files_tree.column("size", width=100, anchor="center")
        self.pack_files_tree.pack(fill="both", expand=True, padx=(4, 0), pady=4)
        
        self.tree_scroll.config(command=self.pack_files_tree.yview)

        # Password/Settings Group
        self.group_settings = ttk.LabelFrame(self.pack_page, text="Параметры безопасности и сжатия")
        self.group_settings.pack(fill="x", padx=10, pady=(0, 10))

        # Password field
        self.pwd_frame = tk.Frame(self.group_settings, bg="#f5f6f5")
        self.pwd_frame.pack(fill="x", padx=6, pady=4)
        
        ttk.Label(self.pwd_frame, text="Пароль архива:", font=("Segoe UI", 9, "bold"), width=12).pack(side="left", padx=(0, 6))
        self.pack_password_entry = ttk.Entry(self.pwd_frame, show="*")
        self.pack_password_entry.pack(side="left", fill="x", expand=True)
        self.pack_password_entry.bind("<KeyRelease>", self.on_pwd_type)
        
        self.btn_toggle_pack_pwd = ttk.Button(self.pwd_frame, text="Показать", style="Tool.TButton", width=10, command=lambda: self.toggle_password("pack"))
        self.btn_toggle_pack_pwd.pack(side="left", padx=(6, 0))

        # Password strength bar
        self.pwd_strength_frame = tk.Frame(self.group_settings, bg="#f5f6f5")
        self.pwd_strength_frame.pack(fill="x", padx=6, pady=(0, 6))
        
        # Spacer
        tk.Label(self.pwd_strength_frame, bg="#f5f6f5", width=12).pack(side="left", padx=(0, 6))
        
        self.pwd_bar = tk.Frame(self.pwd_strength_frame, height=4, bg="#e0e0e0", bd=1, relief="sunken")
        self.pwd_bar.pack(side="left", fill="x", expand=True)
        
        self.pwd_segments = []
        for _ in range(4):
            seg = tk.Frame(self.pwd_bar, bg="#e0e0e0", height=4)
            seg.pack(side="left", fill="both", expand=True, padx=1)
            self.pwd_segments.append(seg)

        # Compression selection
        self.comp_frame = tk.Frame(self.group_settings, bg="#f5f6f5")
        self.comp_frame.pack(fill="x", padx=6, pady=4)
        
        ttk.Label(self.comp_frame, text="Уровень сжатия:", font=("Segoe UI", 9, "bold"), width=12).pack(side="left", padx=(0, 6))
        self.pack_compression_combo = ttk.Combobox(self.comp_frame, values=["9 Экстремальный (LZMA)", "6 Стандартный (LZMA)", "0 Без сжатия (Быстро)"], state="readonly", width=30)
        self.pack_compression_combo.pack(side="left")
        self.pack_compression_combo.current(0)

        # Action Buttons
        self.action_frame = tk.Frame(self.pack_page, bg="#ffffff")
        self.action_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_pack_execute = ttk.Button(self.action_frame, text="Зашифровать и создать .ternos", command=self.perform_pack, state="disabled")
        self.btn_pack_execute.pack(fill="x", ipady=6)

        # Progress bar
        self.pack_progress = ttk.Progressbar(self.action_frame, mode="indeterminate")
        self.pack_progress.pack(fill="x", pady=(4, 0))

    def create_unpack_tab(self):
        self.unpack_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.unpack_tab, text="Распаковать (Чтение)")

        self.unpack_page = tk.Frame(self.unpack_tab, bg="#ffffff", bd=1, relief="solid")
        self.unpack_page.pack(fill="both", expand=True, padx=4, pady=4)

        # Description bar
        self.desc_unpack = tk.Label(self.unpack_page, bg="#ffffe1", fg="#212521", font=("Segoe UI", 8), bd=1, relief="solid", justify="left", anchor="w", padx=10, pady=8,
                                    text="Укажите зашифрованный файл архива .ternos на панели управления, введите правильный\nпароль дешифрации и укажите папку назначения для распаковки файлов.")
        self.desc_unpack.pack(fill="x", padx=10, pady=10)

        # Chosen Archive Info
        self.group_archive_info = ttk.LabelFrame(self.unpack_page, text="Информация о выбранном архиве")
        self.group_archive_info.pack(fill="x", padx=10, pady=(0, 10))

        self.arch_path_frame = tk.Frame(self.group_archive_info, bg="#f5f6f5")
        self.arch_path_frame.pack(fill="x", padx=6, pady=4)
        
        ttk.Label(self.arch_path_frame, text="Файл архива:", font=("Segoe UI", 9, "bold"), width=12).pack(side="left", padx=(0, 6))
        self.unpack_archive_entry = ttk.Entry(self.arch_path_frame, state="readonly")
        self.unpack_archive_entry.pack(side="left", fill="x", expand=True)
        
        self.btn_unpack_select_trigger = ttk.Button(self.arch_path_frame, text="Обзор...", style="Tool.TButton", width=10, command=self.select_archive)
        self.btn_unpack_select_trigger.pack(side="left", padx=(6, 0))

        self.arch_size_frame = tk.Frame(self.group_archive_info, bg="#f5f6f5")
        self.arch_size_frame.pack(fill="x", padx=6, pady=4)
        ttk.Label(self.arch_size_frame, text="Размер архива:", font=("Segoe UI", 9, "bold"), width=12).pack(side="left", padx=(0, 6))
        self.lbl_unpack_size = ttk.Label(self.arch_size_frame, text="Архив не выбран")
        self.lbl_unpack_size.pack(side="left")

        # Password Group
        self.group_unpack_security = ttk.LabelFrame(self.unpack_page, text="Параметры дешифрации")
        self.group_unpack_security.pack(fill="x", padx=10, pady=(0, 10))

        self.unpack_pwd_frame = tk.Frame(self.group_unpack_security, bg="#f5f6f5")
        self.unpack_pwd_frame.pack(fill="x", padx=6, pady=4)
        
        ttk.Label(self.unpack_pwd_frame, text="Пароль архива:", font=("Segoe UI", 9, "bold"), width=12).pack(side="left", padx=(0, 6))
        self.unpack_password_entry = ttk.Entry(self.unpack_pwd_frame, show="*")
        self.unpack_password_entry.pack(side="left", fill="x", expand=True)
        self.unpack_password_entry.bind("<KeyRelease>", lambda e: self.validate_unpack_form())
        
        self.btn_toggle_unpack_pwd = ttk.Button(self.unpack_pwd_frame, text="Показать", style="Tool.TButton", width=10, command=lambda: self.toggle_password("unpack"))
        self.btn_toggle_unpack_pwd.pack(side="left", padx=(6, 0))

        # Unpacking Actions
        self.unpack_action_frame = tk.Frame(self.unpack_page, bg="#ffffff")
        self.unpack_action_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.btn_unpack_execute = ttk.Button(self.unpack_action_frame, text="Выполнить распаковку архива", command=self.perform_unpack, state="disabled")
        self.btn_pack_execute_indicator = self.btn_unpack_execute
        self.btn_unpack_execute.pack(fill="x", ipady=6)

        self.unpack_progress = ttk.Progressbar(self.unpack_action_frame, mode="indeterminate")
        self.unpack_progress.pack(fill="x", pady=(4, 0))

        # Extracted Files Grid (Initially Hidden)
        self.unpack_frame_files = ttk.LabelFrame(self.unpack_page, text="Распакованные файлы")
        # will pack programmatically

        self.unpack_scroll = ttk.Scrollbar(self.unpack_frame_files)
        self.unpack_scroll.pack(side="right", fill="y")
        
        self.unpack_files_tree = ttk.Treeview(self.unpack_frame_files, columns=("name", "size"), show="headings", yscrollcommand=self.unpack_scroll.set)
        self.unpack_files_tree.heading("name", text="Имя файла / Относительный путь")
        self.unpack_files_tree.heading("size", text="Размер")
        self.unpack_files_tree.column("name", width=350, anchor="w")
        self.unpack_files_tree.column("size", width=100, anchor="center")
        self.unpack_files_tree.pack(fill="both", expand=True, padx=(4, 0), pady=4)
        self.unpack_scroll.config(command=self.unpack_files_tree.yview)

    def create_status_bar(self):
        self.statusbar = tk.Frame(self.root, bg="#e0e6e0", bd=1, relief="sunken", height=22)
        self.statusbar.pack(fill="x", side="bottom")

        self.status_left = tk.Label(self.statusbar, text="Готов к работе", bg="#e0e6e0", fg="#212521", font=("Segoe UI", 8), anchor="w")
        self.status_left.pack(side="left", padx=6)

        self.status_mid = tk.Label(self.statusbar, text="LZMA Engine", bg="#e0e6e0", fg="#212521", font=("Segoe UI", 8), anchor="center")
        self.status_mid.pack(side="left", padx=20)

        self.status_crypto = tk.Label(self.statusbar, text="AES-256-GCM Secure AEAD", bg="#e0e6e0", fg="#212521", font=("Segoe UI", 8), anchor="center")
        self.status_crypto.pack(side="left", padx=20)

        self.status_right = tk.Label(self.statusbar, text="Ternos v1.0 (Python Core)", bg="#e0e6e0", fg="#2e7d32", font=("Segoe UI", 8, "bold"), anchor="e")
        self.status_right.pack(side="right", padx=6)

    # ----------------------------------------------------
    # Helper & Logging Methods
    # ----------------------------------------------------
    def log(self, text, log_type="info"):
        time_str = f"[{time.strftime('%H:%M:%S')}]"
        self.console_log.config(state="normal")
        self.console_log.insert("end", time_str, "time")
        self.console_log.insert("end", " ")
        self.console_log.insert("end", text + "\n", log_type)
        self.console_log.config(state="disabled")
        self.console_log.see("end")

    def update_crypto_info(self, salt, iv, integrity):
        self.stat_widgets["val_salt"].config(text=salt[:24] + "..." if len(salt) > 24 else salt)
        self.stat_widgets["val_iv"].config(text=iv)
        self.stat_widgets["val_integrity"].config(text=integrity)
        
        if integrity in ["Верифицировано", "Аутентифицирован"]:
            self.stat_widgets["val_integrity"].config(foreground="#2e7d32")
        elif integrity in ["Ошибка", "Нарушена"]:
            self.stat_widgets["val_integrity"].config(foreground="#c62828")
        else:
            self.stat_widgets["val_integrity"].config(foreground="#212521")

    def format_bytes(self, bytes_num):
        if bytes_num == 0:
            return "0 Б"
        k = 1024
        sizes = ['Б', 'КБ', 'МБ', 'ГБ', 'ТБ']
        import math
        i = math.floor(math.log(bytes_num) / math.log(k))
        return f"{float(bytes_num / math.pow(k, i)):.2f} {sizes[i]}"

    def show_about(self):
        messagebox.showinfo("О программе", "Ternos Secure Archiver v1.0\n"
                                          "----------------------------\n"
                                          "Формат файла: .ternos\n"
                                          "Сжатие: LZMA (Preset 9/6)\n"
                                          "Шифрование: AES-256-GCM\n"
                                          "Режим: Аутентифицированный (AEAD)\n"
                                          "Защита от взлома/подмены: Есть\n\n"
                                          "Все вычисления производятся в локальной Python-среде.")

    def toggle_password(self, tab):
        if tab == "pack":
            entry = self.pack_password_entry
            btn = self.btn_toggle_pack_pwd
        else:
            entry = self.unpack_password_entry
            btn = self.btn_toggle_unpack_pwd

        if entry.cget("show") == "*":
            entry.config(show="")
            btn.config(text="Скрыть")
        else:
            entry.config(show="*")
            btn.config(text="Показать")

    # ----------------------------------------------------
    # Form Validation
    # ----------------------------------------------------
    def on_pwd_type(self, event=None):
        password = self.pack_password_entry.get()
        strength = self.check_password_strength(password)
        
        # Color segments
        for idx, seg in enumerate(self.pwd_segments):
            if idx < strength:
                if strength <= 1:
                    color = "#c62828" # Weak (Red)
                elif strength <= 3:
                    color = "#f59e0b" # Medium (Orange)
                else:
                    color = "#2e7d32" # Strong (Green)
                seg.config(bg=color)
            else:
                seg.config(bg="#e0e0e0")
                
        self.validate_pack_form()

    def check_password_strength(self, pwd):
        if not pwd:
            return 0
        score = 0
        if len(pwd) >= 8: score += 1
        if len(pwd) >= 12: score += 1
        if any(c.isupper() for c in pwd): score += 1
        if any(c.isdigit() for c in pwd): score += 1
        return min(score, 4)

    def validate_pack_form(self):
        has_pwd = len(self.pack_password_entry.get()) >= 8
        has_files = len(self.selected_files) > 0
        if has_pwd and has_files:
            self.btn_pack_execute.config(state="normal")
        else:
            self.btn_pack_execute.config(state="disabled")

    def validate_unpack_form(self):
        has_pwd = len(self.unpack_password_entry.get()) > 0
        has_file = self.unpack_archive_path is not None
        if has_pwd and has_file:
            self.btn_unpack_execute.config(state="normal")
        else:
            self.btn_unpack_execute.config(state="disabled")

    # ----------------------------------------------------
    # File Selection Methods
    # ----------------------------------------------------
    def select_files(self):
        paths = filedialog.askopenfilenames(title="Выберите файлы для добавления")
        if not paths:
            return
        
        added_count = 0
        for path in paths:
            if not any(f["path"] == path for f in self.selected_files):
                try:
                    stat = os.stat(path)
                    file_info = {
                        "name": os.path.basename(path),
                        "path": path,
                        "size": stat.st_size,
                        "rel_path": os.path.basename(path)
                    }
                    self.selected_files.append(file_info)
                    added_count += 1
                    self.log(f"Добавлен файл: {file_info['rel_path']} ({self.format_bytes(file_info['size'])})", "info")
                except Exception as e:
                    self.log(f"Ошибка при чтении {path}: {str(e)}", "error")

        if added_count > 0:
            self.update_pack_tree()
            self.validate_pack_form()

    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Выберите папку для добавления")
        if not folder_path:
            return

        self.log(f"Сканирование папки: {folder_path}...", "info")
        base_dir = os.path.dirname(folder_path)
        added_count = 0
        
        for root_dir, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root_dir, file)
                rel_path = os.path.relpath(full_path, base_dir).replace("\\", "/")
                
                if not any(f["path"] == full_path for f in self.selected_files):
                    try:
                        stat = os.stat(full_path)
                        file_info = {
                            "name": file,
                            "path": full_path,
                            "size": stat.st_size,
                            "rel_path": rel_path
                        }
                        self.selected_files.append(file_info)
                        added_count += 1
                        self.log(f"Добавлен объект: {file_info['rel_path']} ({self.format_bytes(file_info['size'])})", "info")
                    except Exception as e:
                        self.log(f"Ошибка сканирования {full_path}: {str(e)}", "error")

        self.log(f"Сканирование папки завершено. Добавлено объектов: {added_count}", "success")
        if added_count > 0:
            self.update_pack_tree()
            self.validate_pack_form()

    def clear_file_list(self):
        self.selected_files = []
        self.update_pack_tree()
        self.validate_pack_form()
        self.log("Список архивируемых файлов полностью очищен.", "info")

    def update_pack_tree(self):
        # Clear tree
        for item in self.pack_files_tree.get_children():
            self.pack_files_tree.delete(item)

        # Repopulate
        for file in self.selected_files:
            self.pack_files_tree.insert("", "end", values=(file["rel_path"], self.format_bytes(file["size"])))

        # Enable/Disable toolbar clear button
        if self.selected_files:
            self.btn_tb_clear.config(state="normal")
        else:
            self.btn_tb_clear.config(state="disabled")

    def select_archive(self):
        self.notebook.select(1) # Select Unpack tab
        path = filedialog.askopenfilename(title="Открыть архив .ternos", filetypes=[("Архивы Ternos (*.ternos)", "*.ternos")])
        if not path:
            return

        try:
            stat = os.stat(path)
            self.unpack_archive_path = path
            self.unpack_archive_entry.config(state="normal")
            self.unpack_archive_entry.delete(0, "end")
            self.unpack_archive_entry.insert(0, path)
            self.unpack_archive_entry.config(state="readonly")
            
            self.lbl_unpack_size.config(text=self.format_bytes(stat.st_size))
            self.log(f"Выбран архив для распаковки: {os.path.basename(path)} ({self.format_bytes(stat.st_size)})", "info")
            self.validate_unpack_form()
        except Exception as e:
            self.log(f"Ошибка чтения файла архива {path}: {str(e)}", "error")

    # ----------------------------------------------------
    # Crypto Core Execution
    # ----------------------------------------------------
    def perform_pack(self):
        password = self.pack_password_entry.get()
        if not password or len(password) < 8:
            messagebox.showerror("Ошибка", "Пароль должен состоять минимум из 8 символов!")
            return

        if not self.selected_files:
            messagebox.showerror("Ошибка", "Список файлов пуст!")
            return

        save_path = filedialog.asksaveasfilename(
            title="Сохранить зашифрованный архив",
            defaultextension=".ternos",
            filetypes=[("Архивы Ternos (*.ternos)", "*.ternos")]
        )
        if not save_path:
            self.log("Упаковка отменена пользователем.", "warning")
            return

        self.btn_pack_execute.config(state="disabled")
        self.pack_progress.start(10)
        self.root.update_idletasks()

        start_time = time.time()
        self.log(f"Запуск процесса архивации {len(self.selected_files)} объектов...", "info")

        try:
            # 1. Packing structure
            self.log("Шаг 1/4: Сборка структуры файлов...", "info")
            metadata = {
                "version": "1.0",
                "files": []
            }
            file_data_blocks = []
            total_size = 0
            
            for file_info in self.selected_files:
                path = file_info["path"]
                rel_path = file_info["rel_path"]
                with open(path, "rb") as f:
                    data = f.read()
                
                metadata["files"].append({
                    "path": rel_path,
                    "size": len(data)
                })
                file_data_blocks.append(data)
                total_size += len(data)

            meta_bytes = json.dumps(metadata, ensure_ascii=False).encode('utf-8')
            header = struct.pack(">I", len(meta_bytes))
            payload = header + meta_bytes + b"".join(file_data_blocks)

            # 2. Compression
            comp_level_str = self.pack_compression_combo.get()
            preset = int(comp_level_str.split()[0])
            
            if preset > 0:
                self.log(f"Шаг 2/4: Сжатие данных алгоритмом LZMA (уровень {preset})...", "info")
                compressed_payload = lzma.compress(payload, preset=preset)
                ratio = (len(compressed_payload) / len(payload)) * 100
                self.log(f"LZMA сжатие завершено: {self.format_bytes(total_size)} -> {self.format_bytes(len(compressed_payload))} ({ratio:.1f}%)", "success")
            else:
                self.log("Шаг 2/4: Сжатие отключено. Упаковка сырых байт...", "warning")
                compressed_payload = payload

            # 3. Encryption
            self.log("Шаг 3/4: Деривация ключа PBKDF2 (600,000 итераций) и шифрование AES-256-GCM...", "info")
            salt = os.urandom(16)
            iv = os.urandom(12)
            
            # Key derivation
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000, 32)
            
            # AES encryption
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(iv, compressed_payload, None)

            # 4. Save
            self.log("Шаг 4/4: Запись зашифрованного файла на диск...", "info")
            magic = b"TERNOS\x00"
            final_bytes = magic + salt + iv + ciphertext
            
            with open(save_path, "wb") as f:
                f.write(final_bytes)

            elapsed = time.time() - start_time
            self.log(f"Архив успешно создан и записан в: {save_path}", "success")
            self.log(f"Итоговый размер: {len(final_bytes)} байт. Время выполнения: {elapsed:.2f} сек.", "success")
            
            self.update_crypto_info(salt.hex(), iv.hex(), "Аутентифицирован")
            messagebox.showinfo("Успех", f"Архив успешно создан!\nПуть: {save_path}")

        except Exception as e:
            self.log(f"Критическая ошибка архивации: {str(e)}", "error")
            self.update_crypto_info("—", "—", "Ошибка")
            messagebox.showerror("Ошибка архивации", str(e))
            
        finally:
            self.pack_progress.stop()
            self.validate_pack_form()

    def perform_unpack(self):
        password = self.unpack_password_entry.get()
        if not password:
            messagebox.showerror("Ошибка", "Введите пароль для расшифровки!")
            return

        if not self.unpack_archive_path:
            messagebox.showerror("Ошибка", "Архив не выбран!")
            return

        output_folder = filedialog.askdirectory(title="Выберите папку для извлечения файлов")
        if not output_folder:
            self.log("Распаковка отменена пользователем.", "warning")
            return

        self.btn_unpack_execute.config(state="disabled")
        self.unpack_progress.start(10)
        self.root.update_idletasks()

        start_time = time.time()
        self.log(f"Запуск распаковки архива: {self.unpack_archive_path}...", "info")

        try:
            # 1. Read bytes
            with open(self.unpack_archive_path, "rb") as f:
                file_bytes = f.read()

            # 2. Parse Custom Format
            magic = file_bytes[:7]
            if magic != b"TERNOS\x00":
                raise ValueError("Некорректный формат. Файл не является архивом Ternos.")

            salt = file_bytes[7:23]
            iv = file_bytes[23:35]
            ciphertext = file_bytes[35:]

            self.update_crypto_info(salt.hex(), iv.hex(), "Проверка...")

            # 3. Decrypt
            self.log("Шаг 1/3: Вычисление PBKDF2 ключа и дешифрация AES-GCM-256...", "info")
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 600000, 32)
            aesgcm = AESGCM(key)
            
            try:
                decrypted_payload = aesgcm.decrypt(iv, ciphertext, None)
            except Exception:
                raise ValueError("Неверный пароль или архив был поврежден/модифицирован (нарушена целостность данных).")

            self.log("Целостность данных успешно верифицирована. Подпись верна.", "success")
            self.update_crypto_info(salt.hex(), iv.hex(), "Верифицировано")

            # 4. Decompress
            self.log("Шаг 2/3: Распаковка данных LZMA...", "info")
            try:
                uncompressed_payload = lzma.decompress(decrypted_payload)
            except Exception:
                uncompressed_payload = decrypted_payload

            # 5. Extract files
            self.log("Шаг 3/3: Восстановление файлов на диске...", "info")
            meta_len = struct.unpack(">I", uncompressed_payload[:4])[0]
            meta_bytes = uncompressed_payload[4:4+meta_len]
            metadata = json.loads(meta_bytes.decode('utf-8'))
            
            offset = 4 + meta_len
            extracted_files = []
            
            # Clear previous items from Treeview
            for item in self.unpack_files_tree.get_children():
                self.unpack_files_tree.delete(item)

            for file_info in metadata["files"]:
                rel_path = file_info["path"]
                size = file_info["size"]
                
                file_data = uncompressed_payload[offset:offset+size]
                offset += size
                
                dest_path = os.path.join(output_folder, rel_path)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                with open(dest_path, "wb") as f:
                    f.write(file_data)
                
                self.unpack_files_tree.insert("", "end", values=(rel_path, self.format_bytes(size)))
                extracted_files.append(rel_path)
                self.log(f"Извлечен файл: {rel_path} ({self.format_bytes(size)})", "info")

            self.unpack_frame_files.pack(fill="both", expand=True, pady=10) # Show tree
            
            elapsed = time.time() - start_time
            self.log(f"Успешно распаковано файлов: {len(extracted_files)} в папку {output_folder}", "success")
            self.log(f"Время выполнения: {elapsed:.2f} сек.", "success")
            messagebox.showinfo("Успех", f"Распаковка успешно завершена!\nИзвлечено файлов: {len(extracted_files)}\nПапка: {output_folder}")

        except Exception as e:
            self.log(f"Ошибка при распаковке: {str(e)}", "error")
            self.update_crypto_info("—", "—", "Нарушена")
            messagebox.showerror("Ошибка дешифрации", str(e))

        finally:
            self.unpack_progress.stop()
            self.validate_unpack_form()

def main():
    root = tk.Tk()
    app = TernosApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
