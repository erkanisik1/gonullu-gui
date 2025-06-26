import os
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from config import API_URL, logo_path
import ttkbootstrap as tb

class MainWindow:
    def __init__(self, master):
        self.root = tb.Toplevel(master)
        self.logo_img = tk.PhotoImage(file=logo_path)  # root oluşturulduktan sonra!
        self.root.iconphoto(True, self.logo_img)
        self.root.title("Gönüllü - Ana Pencere")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Ana pencere arka plan rengini beyaz yap
        self.root.configure(bg="#ffffff")
        
        # Pencereyi ortala
        self.center_window()
        
        # Stil ayarları
        self.setup_styles()
        
        # Ana frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Grid ağırlıklarını ayarla
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Butonlar frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Otomatik Paket Al butonu
        self.auto_button = tk.Button(buttons_frame, text="Otomatik Paket Al", 
                                    command=self.on_auto_clicked, 
                                    bg="#2E86AB", fg="white",
                                    font=("Arial", 10, "bold"),
                                    relief="flat", borderwidth=0,
                                    activebackground="#2E86AB", activeforeground="white",
                                    width=20, height=2)
        self.auto_button.pack(side=tk.LEFT, padx=5)
        
        # Paket Seç butonu
        self.select_button = tk.Button(buttons_frame, text="Paket Seç", 
                                      command=self.on_select_clicked, 
                                      bg="#2E86AB", fg="white",
                                      font=("Arial", 10, "bold"),
                                      relief="flat", borderwidth=0,
                                      activebackground="#2E86AB", activeforeground="white",
                                      width=20, height=2)
        self.select_button.pack(side=tk.LEFT, padx=5)
        
        # Paket listesi frame
        list_frame = ttk.LabelFrame(main_frame, text="Paket Listesi", padding="10")
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Treeview (liste) oluştur
        columns = ('ID','Paket Adı', 'Repository', 'Branch', 'Durum')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=10)
        
        # Treeview seçim olayını dinle
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<ButtonRelease-1>', self.on_tree_select)  # Mouse tıklama
        self.tree.bind('<KeyRelease>', self.on_tree_select)  # Klavye seçimi
        
        # Sütun başlıkları
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Treeview ve scrollbar'ı yerleştir
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Seç butonu (başlangıçta gizli)
        self.select_pkg_button = tk.Button(main_frame, text="Seçilen Paketi Al", 
                                          command=self.on_package_select, 
                                          bg="#2E86AB", fg="white",
                                          font=("Arial", 10, "bold"),
                                          relief="flat", borderwidth=0,
                                          activebackground="#2E86AB", activeforeground="white",
                                          width=20, height=2)
        self.select_pkg_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
        self.select_pkg_button.config(state='disabled')  # Başlangıçta devre dışı
        
        # Durum etiketi
        self.status_label = ttk.Label(main_frame, text="", foreground="blue")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Paket verilerini sakla
        self.packages = []
        
        # Otomatik boyutlandırma
        self.root.update_idletasks()
        self.root.geometry("")
        
      
        
    def center_window(self):
        """Pencereyi ekranın ortasına yerleştir"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Özel stiller tanımla"""
        style = ttk.Style()
        
        # Ana pencere arka plan rengi
        style.configure("TFrame", background="#ffffff")
        style.configure("TLabelframe", background="#ffffff")
        style.configure("TLabelframe.Label", background="#ffffff", font=("Arial", 10, "bold"))
        style.configure("TLabel", background="#ffffff")
        style.configure("TButton", background="#ffffff")
        
        # Treeview stilleri
        style.configure("Treeview", background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", background="#ffffff")
        
        # Scrollbar stili
        style.configure("Vertical.TScrollbar", background="#ffffff")
    
    def on_auto_clicked(self):
        """Otomatik paket alma butonuna tıklandığında"""
        self.clear_package_list()
        messagebox.showinfo("Bilgi", "Otomatik paket alma başlatılacak!")
    
    def on_select_clicked(self):
        """Paket seç butonuna tıklandığında"""
        self.clear_package_list()
        self.status_label.config(text="Paketler yükleniyor...")
        
        # Butonları devre dışı bırak
        self.auto_button.config(state='disabled')
        self.select_button.config(state='disabled')
        
        # API çağrısını ayrı thread'de yap
        self.root.after(100, self.load_packages)
    
    def load_packages(self):
        """Paketleri API'den yükle"""
        try:
            response = requests.get(API_URL + 'selectpackage', timeout=10)
            if response.status_code == 200:
                data = response.json()
                packages = data.get('packages', [])
                if not packages:
                    self.status_label.config(text="Seçilebilecek paket bulunamadı.", foreground="orange")
                    self.auto_button.config(state='normal')
                    self.select_button.config(state='normal')
                    return
                
                self.show_package_list(packages)
                self.status_label.config(text=f"{len(packages)} paket yüklendi.", foreground="green")
            else:
                self.status_label.config(text=f"Paket listesi alınamadı: {response.text}", foreground="red")
                self.auto_button.config(state='normal')
                self.select_button.config(state='normal')
                
        except Exception as e:
            self.status_label.config(text=f"Hata: {e}", foreground="red")
            self.auto_button.config(state='normal')
            self.select_button.config(state='normal')
    
    def show_package_list(self, packages):
        """Paket listesini göster"""
        self.packages = packages
        
        # Treeview'ı temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Paketleri ekle
        for pkg in packages:
            self.tree.insert('', tk.END, values=(
                pkg.get('id',''),
                pkg.get('paket_adi', ''),
                pkg.get('repository', ''),
                pkg.get('branch', ''),
                pkg.get('durum', 'Beklemede')
            ))
        
        # Seç butonunu göster ve aktif et
        self.select_pkg_button.grid()
        self.select_pkg_button.config(state='normal')
        
        # Butonları tekrar aktif et
        self.auto_button.config(state='normal')
        self.select_button.config(state='normal')
    
    def on_package_select(self):
        """Seçilen paketi al"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Uyarı", "Lütfen bir paket seçin!")
            return
        
        # Seçilen satırın indeksini al
        item_index = self.tree.index(selected_item[0])
        if 0 <= item_index < len(self.packages):
            pkg = self.packages[item_index]
            messagebox.showinfo("Seçilen Paket", f"Seçilen paket: {pkg.get('paket_id', 'Bilinmiyor')}")
            self.clear_package_list()
        else:
            messagebox.showerror("Hata", "Seçilen paket bulunamadı!")
    
    def on_tree_select(self, event):
        """Treeview'da seçim yapıldığında"""
        print("Treeview seçim olayı tetiklendi!")
        selected_item = self.tree.selection()
        print(f"Seçilen öğe: {selected_item}")
        if selected_item:
            # Bir paket seçildi, butonu aktif et
            print("Paket seçildi, buton aktif ediliyor...")
            self.select_pkg_button.config(state='normal')
        else:
            # Hiçbir paket seçilmedi, butonu devre dışı bırak
            print("Paket seçilmedi, buton devre dışı bırakılıyor...")
            self.select_pkg_button.config(state='disabled')
    
    def clear_package_list(self):
        """Paket listesini temizle"""
        # Treeview'ı temizle
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Seç butonunu gizle
        self.select_pkg_button.grid_remove()
        
        # Paket verilerini temizle
        self.packages = []
        
        # Durum etiketini temizle
        self.status_label.config(text="")
    
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