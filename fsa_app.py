import tkinter as tk
from tkinter import ttk, messagebox
import re
import os
from PIL import Image, ImageTk  # Untuk menangani gambar

class FSA_MahasiswaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("APLIKASAUN FSA")
        self.root.geometry("900x650")
        self.root.configure(bg="#f5f7fa")
        self.root.minsize(800, 550)  # Ukuran minimum window
        
        # Inisialisasi variabel untuk logo
        self.logo_left_img = None
        self.logo_right_img = None
        
        # Daftar operator Timor-Leste berdasarkan prefix
        self.operators = {
            "73": "Telkomcel",
            "74": "Telkomcel",
            "75": "Telemor",
            "76": "Telemor",
            "77": "Timor Telecom",
            "78": "Timor Telecom"
        }
        
        # Pola-pola FSA untuk bahasa reguler
        self.pola_fsa = {
            "NRE Estudante": {
                "regex": r'^[0-9]{10}$',
                "contoh": "2023103701 (10 digit angka)",
                "deskripsi": "Numero Rejistu Estudante - 10 digit angka"
            },
            "Email Akademik": {
                "regex": r'^[a-z]+\.[a-z]+@student\.([a-z]+\.)*edu\.tl$',
                "contoh": "kitu.tci@student.edu.tl",
                "deskripsi": "Email ho domain student.edu.tl"
            },
            "Kode Materia": {
                "regex": r'^[A-Z]{2,3}[0-9]{3}$',
                "contoh": "IF101, CS201, MAT301",
                "deskripsi": "2-3 letra kapital tuir 3 numero"
            },
            "Numeru TL (Timor-Leste)": {
                "regex": r'^(\+670|670)?[7][3-8][0-9]{6}$',
                "contoh": "78123456, +67078123456, 67078123456",
                "deskripsi": "Format numeru Timor-Leste: +670/670 prefix 73-78"
            },
            "Data (DD/MM/AAAA)": {
                "regex": r'^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/(19|20)[0-9]{2}$',
                "contoh": "15/08/2004, 01/12/1999",
                "deskripsi": "Format data ho validasaun loron/fulan"
            },
            "IPK": {
                "regex": r'^([0-3]\.\d{2}|4\.00)$',
                "contoh": "3.75, 2.50, 4.00",
                "deskripsi": "Valor IPK 0.00 to'o 4.00"
            }
        }
        
        self.setup_gui()
        self.tampilkan_petunjuk()
        self.setup_responsive()
    
    def setup_responsive(self):
        """Setup untuk responsive design"""
        self.root.bind('<Configure>', self.on_window_resize)
        self.initial_width = 900
        self.initial_height = 650
        
    def on_window_resize(self, event):
        """Handle ketika window di-resize"""
        if event.widget == self.root:
            self.update_layout()
    
    def update_layout(self):
        """Update layout berdasarkan ukuran window saat ini"""
        current_width = self.root.winfo_width()
        if current_width < 850:
            font_scale = 0.9
        elif current_width < 1000:
            font_scale = 1.0
        else:
            font_scale = 1.1
        pass
    
    def setup_gui(self):
        # HEADER dengan logo
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=110)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        header_content = tk.Frame(header_frame, bg="#2c3e50")
        header_content.place(relx=0.5, rely=0.5, anchor="center")
        
        header_grid = tk.Frame(header_content, bg="#2c3e50")
        header_grid.pack()
        
        # LOGO KIRI
        logo_left_frame = tk.Frame(header_grid, bg="#2c3e50")
        logo_left_frame.grid(row=0, column=0, padx=(0, 20), sticky="ns")
        
        try:
            logo_paths = ["img/LOGO KITU.png", "img/logo_kiri.png", "img/logo1.png", 
                         "img/university.png", "img/logo.png", "img/left_logo.jpg",
                         "img/left_logo.png", "img/kitu_logo.png"]
            logo_found = False
            
            for path in logo_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((60, 60), Image.Resampling.LANCZOS)
                    self.logo_left_img = ImageTk.PhotoImage(img)
                    logo_found = True
                    break
            
            if logo_found:
                logo_label = tk.Label(logo_left_frame, image=self.logo_left_img, bg="#2c3e50")
                logo_label.pack()
                self.create_tooltip(logo_label, "LOGO KITU")
            else:
                placeholder = tk.Label(logo_left_frame, text="KITU", font=("Arial", 10, "bold"), 
                        bg="#3498db", fg="white", width=6, height=3, relief="raised")
                placeholder.pack()
                self.create_tooltip(placeholder, "Logo KITU (Universidade)")
                
        except Exception as e:
            print(f"Warning loading left logo: {e}")
            placeholder = tk.Label(logo_left_frame, text="KITU", font=("Arial", 10, "bold"), 
                    bg="#3498db", fg="white", width=6, height=3, relief="raised")
            placeholder.pack()
            self.create_tooltip(placeholder, "Logo KITU")
        
        # JUDUL TENGAH
        title_frame = tk.Frame(header_grid, bg="#2c3e50")
        title_frame.grid(row=0, column=1, padx=15)
        
        title_label = tk.Label(title_frame, 
                text="IDENTIFIKASAUN LIANGUAGEM REGULÁR", 
                font=("Arial", 18, "bold"), 
                bg="#2c3e50", 
                fg="white")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame, 
                text="Utiliza Finite State Automata (FSA) ba Dadus Estudante", 
                font=("Arial", 10), 
                bg="#2c3e50", 
                fg="#ecf0f1")
        subtitle_label.pack()
        
        # LOGO KANAN
        logo_right_frame = tk.Frame(header_grid, bg="#2c3e50")
        logo_right_frame.grid(row=0, column=2, padx=(20, 0), sticky="ns")
        
        try:
            logo_paths = ["img/TCI.png", "img/logo_kanan.png", "img/logo2.png",
                         "img/faculty.png", "img/logo2.jpg", "img/right_logo.jpg",
                         "img/right_logo.png", "img/tci_logo.png"]
            logo_found = False
            
            for path in logo_paths:
                if os.path.exists(path):
                    img = Image.open(path)
                    img = img.resize((60, 60), Image.Resampling.LANCZOS)
                    self.logo_right_img = ImageTk.PhotoImage(img)
                    logo_found = True
                    break
            
            if logo_found:
                logo_label = tk.Label(logo_right_frame, image=self.logo_right_img, bg="#2c3e50")
                logo_label.pack()
                self.create_tooltip(logo_label, "TCI - Teknika Komputador no Informatika")
            else:
                placeholder = tk.Label(logo_right_frame, text="TCI", font=("Arial", 10, "bold"), 
                        bg="#e74c3c", fg="white", width=6, height=3, relief="raised")
                placeholder.pack()
                self.create_tooltip(placeholder, "TCI - Teknika Komputador no Informatika")
                
        except Exception as e:
            print(f"Warning loading right logo: {e}")
            placeholder = tk.Label(logo_right_frame, text="TCI", font=("Arial", 10, "bold"), 
                    bg="#e74c3c", fg="white", width=6, height=3, relief="raised")
            placeholder.pack()
            self.create_tooltip(placeholder, "TCI")
        
        # MAIN CONTAINER
        main_container = tk.Frame(self.root, bg="#f5f7fa")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        main_container.grid_columnconfigure(0, weight=1, uniform="col")
        main_container.grid_columnconfigure(1, weight=1, uniform="col")
        main_container.grid_rowconfigure(0, weight=1)
        
        # LEFT PANEL - INPUT
        left_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", 
                             borderwidth=1)
        left_panel.grid(row=0, column=0, padx=(0, 10), sticky="nsew")
        
        input_label = tk.Label(left_panel, 
                text="INPUT TEKS", 
                font=("Arial", 13, "bold"), 
                bg="#ffffff", 
                fg="#2c3e50")
        input_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        text_container = tk.Frame(left_panel, bg="#ffffff")
        text_container.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        tk.Label(text_container, 
                text="Prense teks hodi identifika:", 
                font=("Arial", 10), 
                bg="#ffffff").pack(anchor="w")
        
        text_scrollbar = tk.Scrollbar(text_container)
        text_scrollbar.pack(side="right", fill="y")
        
        self.input_text = tk.Text(text_container, 
                                 height=10, 
                                 font=("Arial", 10), 
                                 wrap="word",
                                 relief="solid", 
                                 borderwidth=1,
                                 bg="#f8f9fa",
                                 yscrollcommand=text_scrollbar.set)
        self.input_text.pack(fill="both", expand=True, pady=(5, 0))
        
        text_scrollbar.config(command=self.input_text.yview)
        
        btn_frame = tk.Frame(left_panel, bg="#ffffff")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        btn_frame.grid_columnconfigure(2, weight=1)
        
        reset_btn = tk.Button(btn_frame, 
                 text="🧹 Reset", 
                 command=self.reset_input,
                 bg="#e74c3c", 
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=15,
                 pady=8,
                 cursor="hand2")
        reset_btn.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        ident_btn = tk.Button(btn_frame, 
                 text="🔍 Identifika", 
                 command=self.proses_identifikasi,
                 bg="#3498db", 
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=15,
                 pady=8,
                 cursor="hand2")
        ident_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        contoh_btn = tk.Button(btn_frame, 
                 text="📋 Ezemplu", 
                 command=self.isi_contoh,
                 bg="#2ecc71", 
                 fg="white",
                 font=("Arial", 10, "bold"),
                 padx=15,
                 pady=8,
                 cursor="hand2")
        contoh_btn.grid(row=0, column=2, padx=(5, 0), sticky="ew")
        
        # RIGHT PANEL - OUTPUT
        right_panel = tk.Frame(main_container, bg="#ffffff", relief="solid", 
                              borderwidth=1)
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        output_label = tk.Label(right_panel, 
                text="REZULTADU IDENTIFIKASAUN", 
                font=("Arial", 13, "bold"), 
                bg="#ffffff", 
                fg="#2c3e50")
        output_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        # Frame untuk operator info
        operator_frame = tk.Frame(right_panel, bg="#f8f9fa", relief="solid", borderwidth=1)
        operator_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        operator_info = """
        📱 OPERADOR TIMOR-LESTE:
        • 73, 74 = Telkomcel
        • 75, 76 = Telemor  
        • 77, 78 = Timor Telecom
        """
        
        tk.Label(operator_frame, text=operator_info, font=("Arial", 8), 
                bg="#f8f9fa", fg="#2c3e50", justify="left").pack(padx=5, pady=5)
        
        tree_frame = tk.Frame(right_panel, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        style = ttk.Style()
        style.configure("Treeview.Heading", 
                       font=("Arial", 9, "bold"),
                       background="#ecf0f1",
                       foreground="#2c3e50")
        style.configure("Treeview",
                       font=("Arial", 9),
                       rowheight=28,
                       fieldbackground="#ffffff")
        
        columns = ("No", "Teks Input", "Jenis Pola", "Status", "Keterangan")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
        
        self.tree.heading("No", text="No")
        self.tree.heading("Teks Input", text="Teks Input")
        self.tree.heading("Jenis Pola", text="Jenis Pola")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Keterangan", text="Keterangan")
        
        self.tree.column("No", width=50, anchor="center", minwidth=40)
        self.tree.column("Teks Input", width=150, minwidth=120)
        self.tree.column("Jenis Pola", width=120, minwidth=100)
        self.tree.column("Status", width=80, anchor="center", minwidth=70)
        self.tree.column("Keterangan", width=180, minwidth=150)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")
        
        # INFO PANEL
        info_frame = tk.Frame(self.root, bg="#34495e", relief="flat", height=70)
        info_frame.pack(fill="x", side="bottom", padx=20, pady=(0, 20))
        info_frame.pack_propagate(False)
        
        self.info_label = tk.Label(info_frame, 
                                  text="", 
                                  font=("Arial", 9), 
                                  bg="#34495e", 
                                  fg="white", 
                                  justify="left",
                                  wraplength=800)
        self.info_label.pack(expand=True, fill="both", padx=15, pady=10)
    
    def create_tooltip(self, widget, text):
        """Membuat tooltip untuk widget"""
        def enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(tooltip, text=text, background="#ffffe0", 
                           relief="solid", borderwidth=1, font=("Arial", 8))
            label.pack()
            
            widget.tooltip = tooltip
        
        def leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", enter)
        widget.bind("<Leave>", leave)
    
    def get_operator_name(self, phone_number):
        """Mendapatkan nama operator berdasarkan prefix nomor telepon"""
        # Bersihkan nomor dari +670 atau 670
        clean_number = re.sub(r'^(\+670|670)', '', phone_number)
        
        # Ambil 2 digit pertama (prefix)
        if len(clean_number) >= 2:
            prefix = clean_number[:2]
            if prefix in self.operators:
                return f"{self.operators[prefix]} ({prefix})"
        
        return "Numeru TL"
    
    def fsa_identifikasi(self, teks, pola_key):
        """Fungsi utama untuk identifikasi menggunakan FSA"""
        pola = self.pola_fsa[pola_key]["regex"]
        
        # Proses matching dengan regex (simulasi FSA)
        if re.match(pola, teks):
            # Khusus untuk nomor telepon, tambahkan info operator
            if pola_key == "Numeru TL (Timor-Leste)":
                operator = self.get_operator_name(teks)
                return True, f"✓ Kompativel - {operator}"
            else:
                return True, f"✓ Kompativel ho pola {pola_key}"
        else:
            return False, f"✗ La kompativel ho pola {pola_key}"
    
    def tampilkan_petunjuk(self):
        """Menampilkan petunjuk penggunaan"""
        petunjuk = """📖 INSTRUSAUN BA UZA:
1. Ketik ou paste teks iha area INPUT TEKS
2. Klik botão [Identifika] ba prosesu
3. Rezultadu sei mosu iha tabela REZULTADU IDENTIFIKASAUN
4. Uza botão [Ezemplu] ba ezemplu teks
5. Uza botão [Reset] ba repete foun"""
        
        self.info_label.config(text=petunjuk)
    
    def isi_contoh(self):
        """Mengisi contoh teks untuk testing"""
        contoh_teks = """📚 EZEMPLU DADUS ESTUDANTE TIMOR-LESTE:

✅ DADUS VALIDU:
2023103701
kitu.tci@student.edu.tl
IF101
78123456
15/08/2004
3.75

✅ NUMERU OPERADOR TIMOR-LESTE:
73123456    (Telkomcel - 73)
74123456    (Telkomcel - 74)
75123456    (Telemor - 75)
76123456    (Telemor - 76)
77123456    (Timor Telecom - 77)
78123456    (Timor Telecom - 78)

✅ FORMAT KÓDIGU PAÍS:
+67078123456
67077123456

❌ DADUS LA VALIDU:
12345
user@gmail.com
79123456    (prefix 79 la validu)
12345678    (prefix laos 7)
40/13/2020
4.50"""
        
        self.input_text.delete("1.0", tk.END)
        self.input_text.insert("1.0", contoh_teks)
    
    def reset_input(self):
        """Mengosongkan input dan hasil"""
        self.input_text.delete("1.0", tk.END)
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tampilkan_petunjuk()
    
    def proses_identifikasi(self):
        """Memproses identifikasi teks"""
        teks_input = self.input_text.get("1.0", tk.END).strip()
        
        if not teks_input:
            messagebox.showwarning("Input Mamuk", 
                                 "Favor prense teks antes!")
            self.input_text.focus_set()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.tree.tag_configure('valid', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('invalid', background='#f8d7da', foreground='#721c24')
        
        # Tag khusus untuk operator yang berbeda
        self.tree.tag_configure('telkomcel', background='#e3f2fd', foreground='#0d47a1')
        self.tree.tag_configure('telemor', background='#e8f5e9', foreground='#1b5e20')
        self.tree.tag_configure('timortelecom', background='#fff3e0', foreground='#e65100')
        
        baris_list = teks_input.split('\n')
        nomor = 1
        
        for baris in baris_list:
            baris = baris.strip()
            if not baris or baris.startswith("📚") or baris.startswith("✅") or baris.startswith("❌"):
                continue
            
            ditemukan = False
            for pola_key in self.pola_fsa:
                diterima, keterangan = self.fsa_identifikasi(baris, pola_key)
                
                if diterima:
                    status = "✅ VALIDU"
                    
                    # Tentukan tags berdasarkan pola
                    tags = ['valid']
                    
                    # Tambahkan tag operator khusus untuk nomor telepon
                    if pola_key == "Numeru TL (Timor-Leste)":
                        clean_number = re.sub(r'^(\+670|670)', '', baris)
                        if len(clean_number) >= 2:
                            prefix = clean_number[:2]
                            if prefix in ["73", "74"]:
                                tags.append('telkomcel')
                            elif prefix in ["75", "76"]:
                                tags.append('telemor')
                            elif prefix in ["77", "78"]:
                                tags.append('timortelecom')
                    
                    # Dapatkan nama pola yang sesuai
                    nama_pola = pola_key
                    if pola_key == "Numeru TL (Timor-Leste)":
                        nama_pola = self.get_operator_name(baris)
                    
                    self.tree.insert("", "end", 
                                   values=(nomor, baris, nama_pola, status, keterangan),
                                   tags=tuple(tags))
                    nomor += 1
                    ditemukan = True
                    break
            
            if not ditemukan and baris:
                status = "❌ INVALIDU"
                self.tree.insert("", "end", 
                               values=(nomor, baris, "La identifika", status, "La kompativel ho pola"),
                               tags=('invalid',))
                nomor += 1
        
        if not self.tree.get_children():
            self.tree.insert("", "end", 
                           values=("-", "Laiha pola kompativel", "-", "-", 
                                  "Koko uza botão [Ezemplu]"))
        
        total_ditemukan = len(self.tree.get_children())
        if total_ditemukan > 0:
            valid_count = len(self.tree.tag_has('valid'))
            invalid_count = len(self.tree.tag_has('invalid'))
            
            # Hitung jumlah per operator
            telkomcel_count = len(self.tree.tag_has('telkomcel'))
            telemor_count = len(self.tree.tag_has('telemor'))
            timortelecom_count = len(self.tree.tag_has('timortelecom'))
            
            info_text = f"📊 REZULTADU: Total {total_ditemukan} lina | ✅ Validu: {valid_count} | ❌ Invalidu: {invalid_count}"
            
            # Tambahkan info operator jika ada
            if telkomcel_count > 0 or telemor_count > 0 or timortelecom_count > 0:
                operator_info = " | 📱 Operator: "
                operator_details = []
                if telkomcel_count > 0:
                    operator_details.append(f"Telkomcel: {telkomcel_count}")
                if telemor_count > 0:
                    operator_details.append(f"Telemor: {telemor_count}")
                if timortelecom_count > 0:
                    operator_details.append(f"Timor Telecom: {timortelecom_count}")
                
                info_text += operator_info + ", ".join(operator_details)
            
            self.info_label.config(text=info_text)
    
    def run(self):
        self.root.mainloop()


# ==============================================
# FUNGSI UTAMA DAN PENJALANAN APLIKASI
# ==============================================

def main():
    """Fungsi utama untuk menjalankan aplikasi"""
    print("="*80)
    print("APLIKASAUN IDENTIFIKASAUN LIANGUAGEM REGULÁR UTILIZA FSA")
    print("="*80)
    print("\n📋 INFORMASAUN APLIKASAUN:")
    print("Aplikasaun ne'e bele identifika pola-pala tuir mai:")
    print("1. NRE Estudante (10 digit número)")
    print("2. Email Akademik (domain student.*.edu.tl)")
    print("3. Kode Materia (ezemplu: IF101)")
    print("4. Numeru TL (Timor-Leste): +670/670 prefix 73-78, 8 digit")
    print("5. Data formatu DD/MM/AAAA")
    print("6. IPK (0.00 to'o 4.00)")
    
    print("\n📱 OPERADOR TIMOR-LESTE:")
    print("• Prefix 73, 74 = Telkomcel")
    print("• Prefix 75, 76 = Telemor")
    print("• Prefix 77, 78 = Timor Telecom")
    
    print("\n🔄 HAKEREK PASTA LOGO...")
    if os.path.exists("img/"):
        files = os.listdir("img/")
        print(f"✅ Pasta 'img/' hetan ho {len(files)} file")
        if files:
            print(f"   File sira: {', '.join(files[:5])}")
    else:
        print("⚠️ Pasta 'img/' la hetan")
        print("💡 Kria pasta 'img/' no tau logo ho naran:")
        print("   - LOGO KITU.png ou logo_kiri.png")
        print("   - TCI.png ou logo_kanan.png")
    
    print("\n🖥️ Loke interface GUI...")
    print("="*80)
    
    root = tk.Tk()
    
    try:
        if os.path.exists("img/icon.ico"):
            root.iconbitmap("img/icon.ico")
        elif os.path.exists("img/icon.png"):
            icon_img = Image.open("img/icon.png")
            icon_photo = ImageTk.PhotoImage(icon_img)
            root.iconphoto(True, icon_photo)
    except:
        pass
    
    app = FSA_MahasiswaApp(root)
    
    print("\n👨‍🎓 INFORMASAUN DEZENVOLVEDOR:")
    print("Naran    : [Naran Kompletu Ita-Boot]")
    print("NRE      : [NRE Ita-Boot]")
    print("Klase    : [Klase Ita-Boot]")
    print("Materia  : Teoria Lianguagem Formal no Automata")
    print("="*80)
    
    app.run()


if __name__ == "__main__":
    try:
        from PIL import Image, ImageTk
        main()
    except ImportError:
        print("⚠️ ERRO: Biblioteca Pillow la hetan!")
        print("Instala ho komandu: pip install Pillow")
        input("Prens Enter atu sai...")