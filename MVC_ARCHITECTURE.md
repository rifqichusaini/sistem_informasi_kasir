# Kasir GUI - Struktur MVC

## Folder Structure (Clean Architecture)

```
kasir-gui/
├── model/                    # 🔵 DATA LAYER - Database & Business Logic
│   ├── __init__.py
│   ├── login_model.py       # Authentication logic
│   ├── barang_model.py      # Product data management
│   └── transaksi_model.py   # Transaction logic
│
├── view/                     # 🟢 PRESENTATION LAYER - UI Components
│   ├── __init__.py
│   ├── login_view.py        # Login dialog UI
│   └── kasir_view.py        # Kasir window UI
│
├── controller/               # 🟡 LOGIC LAYER - Business Flow
│   ├── __init__.py
│   └── kasir_controller.py  # Kasir business logic & event handling
│
├── app/                      # 📋 UTILITIES & ENTRY POINT
│   ├── main_gui.py          # ⭐ APPLICATION ENTRY POINT
│   ├── login_gui.py         # (Legacy - use view.login_view instead)
│   ├── kasir_gui.py         # (Legacy - use view.kasir_view + controller instead)
│   ├── custom_dialog.py     # Dialog utilities
│   └── cli/                 # Command-line interface
│
├── style/                    # 🎨 STYLING
│   └── kasir_style.py       # PyQt5 stylesheets
│
├── assets/                   # 📁 RESOURCES
│   └── favicon.ico
│
├── data/                     # 📄 TRANSACTION RECEIPTS
│   └── struk-*.txt
│
├── .env                      # Supabase credentials (not in repo)
├── README.md                 # This file
└── requirements.txt          # Dependencies
```

## MVC Flow

### 1️⃣ Model Layer (`model/`)
- **Tanggung jawab:** Database operations & data business logic
- **Files:** `login_model.py`, `barang_model.py`, `transaksi_model.py`
- **Contoh:**
  ```python
  from model.login_model import LoginModel
  
  model = LoginModel()
  user = model.validate_user("kasir1", "123")
  ```

### 2️⃣ View Layer (`view/`)
- **Tanggung jawab:** UI components (PyQt5 widgets)
- **Files:** `login_view.py`, `kasir_view.py`
- **Sifat:** Passive (hanya display, NO business logic)
- **Contoh:**
  ```python
  from view.kasir_view import KasirView
  
  view = KasirView(cashier_name="Kasir 1")
  view.show()
  ```

### 3️⃣ Controller Layer (`controller/`)
- **Tanggung jawab:** Business logic & event handling
- **Files:** `kasir_controller.py`
- **Tugas:**
  - Handle user events (clicks, inputs)
  - Call model untuk data operations
  - Update view dengan hasil
  - Orchestrate application flow
- **Contoh:**
  ```python
  from controller.kasir_controller import KasirController
  
  controller = KasirController(view)
  # Controller akan connect signals & handle logic
  ```

## Entry Point

**Start aplikasi dari:**
```bash
python app/main_gui.py
```

**Flow:**
1. `main_gui.py` → Create LoginView
2. User login → Create KasirView + KasirController
3. Controller handle semua business logic
4. View hanya display data

## Dependencies (Supabase)

**Environment variables (.env):**
```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## Notes

- ✅ **Semua files lama di `/api/` sudah dihapus (redundant dengan `/model/`)**
- ✅ **Semua imports sudah diupdate ke `/model/`**
- ⚠️ Files legacy di `/app/` (login_gui.py, kasir_gui.py) tetap ada tapi DEPRECATED
  - Gunakan struktur MVC baru: `/view/` + `/controller/` + `/model/`

## Future Improvements

- [ ] Unit tests untuk model, view, controller
- [ ] Dependency injection untuk cleaner architecture
- [ ] Repository pattern untuk data access
- [ ] Service layer untuk complex business logic
