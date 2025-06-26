import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import hashlib
import os
from config import API_URL, REMEMBER_FILE, logo_path
import ttkbootstrap as tb

class LoginWindow:
    def __init__(self, on_login_success):
        self.root = tb.Window(themename="flatly")
        self.logo_img = tk.PhotoImage(file=logo_path)  # root oluşturulduktan sonra!
        self.root.iconphoto(True, self.logo_img)
        self.root.title("Gönüllü - Giriş")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ana pencere arka plan rengini doğrudan ayarla
        self.root.configure(bg="#ffffff")
        
        # Pencereyi ortala
        self.center_window()
        
        # Stil ayarları
        self.setup_styles()
        
        self.on_login_success = on_login_success
        
        # Ana container
        main_container = tk.Frame(self.root, bg="#ffffff")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Form alanı
        form_frame = tk.Frame(main_container, bg="#ffffff", padx=20, pady=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Grid yapısı
        form_frame.columnconfigure(1, weight=1)
        
        # E-posta alanı
        tk.Label(form_frame, bg="#ffffff", text="E-posta:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5), padx=(0, 10))
        
        self.mail_entry = ttk.Entry(form_frame, width=40, font=("Arial", 12))
        self.mail_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        self.mail_entry.insert(0, "E-posta adresinizi girin")
        self.mail_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.mail_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        # Şifre alanı
        tk.Label(form_frame, bg="#ffffff", text="Şifre:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5), padx=(0, 10))
        
        self.pass_entry = ttk.Entry(form_frame, width=40, show="*", font=("Arial", 12))
        self.pass_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 15))
        self.pass_entry.insert(0, "Şifrenizi girin")
        self.pass_entry.bind('<FocusIn>', self.on_entry_focus_in)
        self.pass_entry.bind('<FocusOut>', self.on_entry_focus_out)
        
        # Beni Hatırla
        self.remember_var = tk.BooleanVar()
        self.remember_check = ttk.Checkbutton(form_frame, text="Beni Hatırla", 
                                             variable=self.remember_var, 
                                             style="Custom.TCheckbutton")
        self.remember_check.grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Buton alanı
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))
        
        # Giriş butonu
        self.login_button = tk.Button(button_frame, text="Giriş Yap", 
                                     command=self.on_login_clicked, 
                                     bg="#2E86AB", fg="white",
                                     font=("Arial", 10, "bold"),
                                     relief="flat", borderwidth=0,
                                     activebackground="#2E86AB", activeforeground="white",
                                     width=20, height=2)
        self.login_button.pack(side=tk.LEFT, padx=(0, 10))
        
        
        
        # Durum etiketi
        self.status_label = ttk.Label(form_frame, text="", 
                                     font=("Arial", 9), foreground="#666666")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))
        
        # Enter tuşu ile giriş
        self.root.bind('<Return>', lambda e: self.on_login_clicked())
        self.root.bind('<Escape>', lambda e: self.on_closing())
        
        # Hatırlanan bilgileri yükle
        self.load_remembered()
        
        # Placeholder'ları ayarla
        self.mail_placeholder = "E-posta adresinizi girin"
        self.pass_placeholder = "Şifrenizi girin"
        
        # Pencereye odaklan
        self.root.focus_force()
        
    def setup_styles(self):
        """Özel stiller tanımla"""
        style = ttk.Style()
        
        # Ana pencere arka plan rengi - Burayı değiştirerek pencere rengini ayarlayabilirsiniz
        # Örnek renkler: "#f0f0f0" (açık gri), "#e8f4fd" (açık mavi), "#f5f5f5" (gri)
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabelframe", background="#ffffff", borderwidth=0, relief="flat")
        style.configure("TLabelframe.Label", background="#ffffff", font=("Arial", 10, "bold"))
        
        # Buton stilleri - Hover durumunda renk değişimi olmasın
        style.configure("Accent.TButton", 
                       background="#2E86AB", 
                       foreground="white",
                       font=("Arial", 10, "bold"))
        
        # Hover durumunda da aynı renkleri koru
        style.map("Accent.TButton",
                 background=[('active', '#2E86AB'), ('pressed', '#2E86AB')],
                 foreground=[('active', 'white'), ('pressed', 'white')])
        
        # Checkbutton stili
        style.configure("Custom.TCheckbutton", 
                       background="#ffffff",
                       font=("Arial", 9))
        
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_entry_focus_in(self, event):
        """Entry'ye odaklanıldığında placeholder'ı temizle"""
        widget = event.widget
        if widget == self.mail_entry and widget.get() == self.mail_placeholder:
            widget.delete(0, tk.END)
            widget.config(foreground='black')
        elif widget == self.pass_entry and widget.get() == self.pass_placeholder:
            widget.delete(0, tk.END)
            widget.config(foreground='black')
            widget.config(show='*')
    
    def on_entry_focus_out(self, event):
        """Entry'den çıkıldığında boşsa placeholder ekle"""
        widget = event.widget
        if widget == self.mail_entry and not widget.get():
            widget.insert(0, self.mail_placeholder)
            widget.config(foreground='gray')
        elif widget == self.pass_entry and not widget.get():
            widget.insert(0, self.pass_placeholder)
            widget.config(foreground='gray')
            widget.config(show='')
    
    def load_remembered(self):
        """Hatırlanan bilgileri yükle"""
        if os.path.exists(REMEMBER_FILE):
            try:
                with open(REMEMBER_FILE, "r") as f:
                    data = json.load(f)
                    mail = data.get("mail", "")
                    password = data.get("password", "")
                    
                    if mail:
                        self.mail_entry.delete(0, tk.END)
                        self.mail_entry.insert(0, mail)
                        self.mail_entry.config(foreground='black')
                    
                    if password:
                        self.pass_entry.delete(0, tk.END)
                        self.pass_entry.insert(0, password)
                        self.pass_entry.config(foreground='black')
                        self.pass_entry.config(show='*')
                    
                    self.remember_var.set(True)
            except Exception:
                pass
    
    def save_remembered(self, mail, password):
        """Bilgileri kaydet"""
        data = {"mail": mail, "password": password}
        with open(REMEMBER_FILE, "w") as f:
            json.dump(data, f)
    
    def clear_remembered(self):
        """Hatırlanan bilgileri temizle"""
        if os.path.exists(REMEMBER_FILE):
            os.remove(REMEMBER_FILE)
    
    def on_login_clicked(self):
        """Giriş butonuna tıklandığında"""
        mail = self.mail_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        # Placeholder kontrolü
        if mail == self.mail_placeholder or password == self.pass_placeholder:
            self.status_label.config(text="Lütfen e-posta ve şifre girin.", foreground="red")
            return
        
        if not mail or not password:
            self.status_label.config(text="Lütfen e-posta ve şifre girin.", foreground="red")
            return
        
        self.status_label.config(text="Giriş yapılıyor...", foreground="blue")
        self.login_button.config(state='disabled')
        
        # Login işlemini ayrı thread'de yap
        self.root.after(100, lambda: self.login_request(mail, password))
    
    def login_request(self, mail, password):
        """Login isteği gönder"""
        try:
            md5_pass = hashlib.md5(password.encode('utf-8')).hexdigest()
            response = requests.post(API_URL + '/gonullu/login', json={
                "email": mail,
                "password": md5_pass
            }, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("exists") == True:
                    self.status_label.config(text="Giriş başarılı! Ana pencere açılıyor...", foreground="green")
                    
                    if self.remember_var.get():
                        self.save_remembered(mail, password)
                    else:
                        self.clear_remembered()
                    
                    # Ana pencereyi aç
                    self.root.after(1500, self.open_main_window)
                else:
                    self.status_label.config(text="Giriş başarısız: E-posta veya şifre hatalı!", foreground="red")
                    self.clear_remembered()
                    self.login_button.config(state='normal')
            else:
                self.status_label.config(text=f"Giriş başarısız: {response.text}", foreground="red")
                self.clear_remembered()
                self.login_button.config(state='normal')
                
        except requests.exceptions.ConnectionError:
            self.status_label.config(text="Sunucu kapalı veya erişilemiyor!", foreground="red")
            self.login_button.config(state='normal')
        except Exception as e:
            self.status_label.config(text=f"Hata: {e}", foreground="red")
            self.login_button.config(state='normal')
    
    def open_main_window(self):
        """Ana pencereyi aç"""
        self.root.withdraw()
        if self.on_login_success:
            self.on_login_success(self.root)
    
    def on_closing(self):
        """Pencere kapatıldığında"""
        try:
            if hasattr(self, 'after_id'):
                self.root.after_cancel(self.after_id)
            self.root.destroy()
        except Exception as e:
            print("Kapanışta hata:", e)
    
    def show(self):
        """Pencereyi göster"""
        self.root.mainloop()
