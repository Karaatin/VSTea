def build_stylesheet(colors: dict) -> str:
    return f"""
/* =========================================
   GLOBAL & TYPOGRAPHY
========================================= */
QMainWindow, QDialog, QWidget#MainContainer {{  background-color: {colors['BG_APP']}; color: {colors['TEXT_MAIN']}; font-family: 'Segoe UI', 'Inter', sans-serif; }}
QLabel {{ color: {colors['TEXT_MAIN']}; border: none; }}
QLabel#TopBrand {{ font-size: 18px; font-weight: 900; color: {colors['ACCENT']}; letter-spacing: 1px; }}
QLabel#H1 {{ font-size: 32px; font-weight: 800; color: {colors['TEXT_MAIN']}; letter-spacing: -0.5px; }}
QLabel#H2 {{ font-size: 13px; font-weight: 700; color: {colors['TEXT_MUTED']}; text-transform: uppercase; letter-spacing: 1px; }}
QLabel#Sub {{ font-size: 15px; color: {colors['TEXT_MUTED']}; }}

/* =========================================
   SIDEBAR & NAVIGATION
========================================= */
QFrame#Sidebar {{ background-color: #050505; border-right: 1px solid {colors['BORDER']}; }}
QPushButton#NavBtn {{ background-color: transparent; color: {colors['TEXT_MUTED']}; border: none; text-align: left; padding: 12px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; }}
QPushButton#NavBtn:hover {{ background-color: {colors['BG_HOVER']}; color: {colors['TEXT_MAIN']}; }}
QPushButton#NavBtn:checked {{ background-color: {colors['BG_HOVER']}; color: {colors['ACCENT']}; font-weight: 800; }}

QPushButton#ToggleBtn {{ background: transparent; border: none; color: {colors['TEXT_MUTED']}; font-size: 20px; border-radius: 6px; padding: 4px 8px; }}
QPushButton#ToggleBtn:hover {{ background: {colors['BG_CARD']}; color: {colors['TEXT_MAIN']}; }}

/* =========================================
   DASHBOARD VIEW & DAW CARDS
========================================= */
QFrame#HeaderPill {{ background-color: {colors['BG_CARD']}; border: 1px solid {colors['BORDER']}; border-radius: 10px; }}
QLabel#HeaderStat {{ color: {colors['TEXT_MAIN']}; font-weight: 700; font-size: 13px; letter-spacing: 0.5px; }}

QScrollArea#TransparentScroll, 
QScrollArea#TransparentScroll QWidget {{ background-color: transparent; border: none; }}
QWidget#DimmerOverlay {{ background-color: rgba(0, 0, 0, 120); }}

QLabel#StatusDot {{ border-radius: 5px;  background-color: transparent; }}
QLabel#StatusDot[cardStatus="missing"] {{ background-color: {colors['BORDER_DIM']}; }}
QLabel#StatusDot[cardStatus="error"] {{ background-color: {colors['ERROR']}; }}
QLabel#StatusDot[cardStatus="ready"] {{ background-color: {colors.get('SUCCESS', '#10b981')}; }}
QLabel#StatusDot[cardStatus="loading"] {{ background-color: {colors['ACCENT']}; }}

QPushButton#CardIconBtn {{ background-color: {colors['BG_APP']}; border: 1px solid {colors['BORDER']}; color: {colors['TEXT_MUTED']}; border-radius: 6px; font-size: 13px; min-width: 26px; max-width: 26px; min-height: 26px; max-height: 26px; }}
QPushButton#CardIconBtn:hover {{ background-color: {colors['BG_HOVER']}; border: 1px solid {colors['ACCENT']}; color: {colors['ACCENT']}; }}
QPushButton#CardIconBtn:disabled {{ border: 1px solid transparent; color: {colors['BORDER_DIM']}; }}

QLabel#CardName {{ font-size: 16px; font-weight: 800; color: {colors['TEXT_MAIN']}; border: none; }}
QLabel#CardName[cardStatus="missing"] {{ color: {colors['TEXT_MUTED']}; }}
QLabel#CardInfo {{ color: {colors['TEXT_MUTED']}; font-size: 11px; font-family: monospace; border: none; }}

QProgressBar#CardLoader {{ background: {colors['BORDER']}; border: none; border-radius: 2px; }}
QProgressBar#CardLoader::chunk {{ background: {colors['ACCENT']}; border-radius: 2px; }}

QLabel#Badge {{ font-weight: 800; font-size: 11px; border: none; }}
QLabel#Badge[cardStatus="missing"] {{ color: {colors['TEXT_MUTED']}; }}
QLabel#Badge[cardStatus="error"] {{ color: {colors['ERROR']}; }}
QLabel#Badge[cardStatus="ready"], QLabel#Badge[cardStatus="loading"] {{ color: {colors['SUCCESS']}; }}

QFrame#DashboardFooter {{ background-color: transparent; border-top: 1px solid {colors['BORDER']}; border-radius: 0px; }}
QLabel#FooterInfo {{ color: {colors['TEXT_MUTED']}; font-size: 13px; font-weight: 600; }}

QPushButton#ScanBtn {{ background-color: {colors['ACCENT']}; border: none; color: #ffffff; font-size: 14px; padding: 10px 24px; border-radius: 8px; font-weight: 800; }}
QPushButton#ScanBtn:hover {{ background-color: {colors['ACCENT_HL']}; }}
QPushButton#ScanBtn:disabled {{ background-color: {colors['BG_CARD']}; color: {colors['TEXT_MUTED']}; border: 1px solid {colors['BORDER_DIM']}; }}

/* =========================================
   RESULTS TABLE & SEARCH
========================================= */
QLineEdit#SearchBar {{ background-color: {colors['BG_CARD']}; border: 1px solid {colors['BORDER']}; border-radius: 8px; padding: 12px 16px; color: {colors['TEXT_MAIN']}; font-size: 14px; }}
QLineEdit#SearchBar:focus {{ border: 1px solid {colors['ACCENT']}; background-color: {colors['BG_HOVER']}; }}

QTableWidget {{ background-color: {colors['BG_APP']}; alternate-background-color: {colors['BG_CARD']}; border: 1px solid {colors['BORDER']}; border-radius: 8px; gridline-color: transparent; outline: none; }}
QTableWidget::item {{ padding-left: 10px; border-bottom: 1px solid transparent; }}
QTableWidget::item:hover {{ background-color: {colors['BG_HOVER']}; }}
QTableWidget::item:selected {{ background-color: {colors['BG_HOVER']}; color: {colors['TEXT_MAIN']}; outline: none; border: none; }}

QHeaderView::section {{ background-color: {colors['BG_CARD']}; color: {colors['TEXT_MUTED']}; padding: 12px 8px; border: none; border-bottom: 1px solid {colors['BORDER']}; font-weight: 700; font-size: 11px; text-transform: uppercase; }}
QLabel#PluginBadge {{ background-color: transparent; color: {colors.get('SUCCESS', colors['ACCENT'])}; border: 1px solid {colors.get('SUCCESS', colors['ACCENT'])}; border-radius: 4px; padding: 2px 6px; font-size: 10px; font-weight: 800; }}

QScrollBar:vertical {{ background: transparent; width: 8px; margin: 0; }}
QScrollBar::handle:vertical {{ background: {colors['BORDER']}; border-radius: 4px; min-height: 20px; }}
QScrollBar::handle:vertical:hover {{ background: {colors['BORDER_DIM']}; }}
QScrollBar:horizontal {{ background: transparent; height: 8px; margin: 0; }}
QScrollBar::handle:horizontal {{ background: {colors['BORDER']}; border-radius: 4px; min-width: 20px; }}
QScrollBar::handle:horizontal:hover {{ background: {colors['BORDER_DIM']}; }}
QScrollBar::add-line, QScrollBar::sub-line {{ width: 0px; height: 0px; }}

/* =========================================
   GENERAL BUTTONS & FORMS
========================================= */
QPushButton#PrimaryBtn {{ background-color: {colors['ACCENT']}; border: none; color: #ffffff; font-size: 15px; padding: 14px 32px; border-radius: 8px; font-weight: 800; }}
QPushButton#PrimaryBtn:hover {{ background-color: {colors['ACCENT_HL']}; }}

QPushButton#ExportBtn {{ background-color: {colors['ACCENT']}; border: none; color: #ffffff; font-size: 13px; padding: 10px 24px; border-radius: 8px; font-weight: 800; }}
QPushButton#ExportBtn:hover {{ background-color: {colors['ACCENT_HL']}; }}
QPushButton#ExportBtnSecondary {{ background-color: transparent; border: 1px solid {colors['BORDER_DIM']}; color: {colors['TEXT_MUTED']}; font-size: 13px; padding: 10px 24px; border-radius: 8px; font-weight: 800; }}
QPushButton#ExportBtnSecondary:hover {{ background-color: {colors['BG_HOVER']}; color: {colors['TEXT_MAIN']}; border: 1px solid {colors['BORDER']}; }}

QComboBox {{ background: {colors['BG_CARD']}; border: 1px solid {colors['BORDER']}; border-radius: 6px; padding: 8px; color: {colors['TEXT_MAIN']}; font-size: 13px; }}
QComboBox::drop-down {{ border: none; }}

QCheckBox::indicator {{ width: 18px; height: 18px; border-radius: 4px; border: 1px solid {colors['BORDER_DIM']}; background: {colors['BG_CARD']}; }}
QCheckBox::indicator:checked {{ background: {colors['ACCENT']}; border-color: {colors['ACCENT']}; }}

/* =========================================
   DIALOGS & OTHERS (About / Splash)
========================================= */
QFrame#SuccessCardFrame {{ background-color: {colors['BG_CARD']}; border: 2px solid {colors.get('SUCCESS', colors['ACCENT'])}; border-radius: 16px; }}
QLabel#SuccessIcon {{ font-size: 64px; background: transparent; border: none; }}
QLabel#SuccessTitle {{ font-size: 22px; font-weight: 800; color: {colors['TEXT_MAIN']}; background: transparent; border: none; }}
QLabel#SuccessDesc {{ font-size: 13px; color: {colors['TEXT_MUTED']}; background: transparent; border: none; }}

QFrame#AboutCard {{ background-color: {colors['BG_CARD']}; border: 1px solid {colors['BORDER']}; border-radius: 12px; }}
QLabel#AboutKey {{ color: {colors['TEXT_MUTED']}; font-weight: 700; font-size: 13px; min-width: 100px; }}
QLabel#AboutVal {{ color: {colors['TEXT_MAIN']}; font-weight: 600; font-size: 13px; }}

QWidget#SplashContainer {{ background: transparent; }}
QProgressBar#SplashLoader {{ background-color: {colors['BORDER']}; border: none; border-radius: 3px; }}
QProgressBar#SplashLoader::chunk {{ background-color: {colors['ACCENT']}; border-radius: 3px; }}
QLabel#SplashStatus {{ color: {colors['ACCENT']}; font-family: monospace; font-size: 11px; font-weight: bold; }}
"""