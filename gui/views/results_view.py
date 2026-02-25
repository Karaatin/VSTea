import datetime
import importlib
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QTableWidget, QHeaderView,
                               QTableWidgetItem, QLineEdit, QFileDialog)
from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QColor, QDesktopServices

from exporters.html_generator import HTMLExporter
from exporters.json_generator import JSONExporter


class FormatTableItem(QTableWidgetItem):
    def __init__(self, sort_text):
        super().__init__("")
        self.sort_text = sort_text

    def __lt__(self, other):
        if isinstance(other, FormatTableItem):
            return self.sort_text < other.sort_text
        return super().__lt__(other)


class ResultsView(QWidget):
    def __init__(self, controller, on_back_callback):
        super().__init__()
        self.controller = controller
        self.on_back_callback = on_back_callback

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 20, 60, 50)
        layout.setSpacing(20)

        top = QHBoxLayout()
        top.setAlignment(Qt.AlignmentFlag.AlignBottom)

        title_box = QVBoxLayout()
        title_box.setSpacing(5)
        lbl = QLabel("Scan Results", objectName="H1")
        self.lbl_stats = QLabel("0 Plugins found", objectName="Sub")
        title_box.addWidget(lbl)
        title_box.addWidget(self.lbl_stats)

        btn_back = QPushButton("← Back")
        btn_back.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_back.clicked.connect(self.on_back_callback)

        btn_html = QPushButton("Export HTML Report")
        btn_html.setObjectName("ExportBtn")
        btn_html.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_html.clicked.connect(lambda: self.export_data("html"))

        btn_json = QPushButton("Export JSON")
        btn_json.setObjectName("ExportBtnSecondary")
        btn_json.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_json.clicked.connect(lambda: self.export_data("json"))

        top.addLayout(title_box)
        top.addStretch()
        top.addWidget(btn_back)
        top.addSpacing(10)

        top.addWidget(btn_json)
        top.addWidget(btn_html)

        layout.addLayout(top)

        self.search_bar = QLineEdit()
        self.search_bar.setObjectName("SearchBar")
        self.search_bar.setPlaceholderText("🔍 Search plugins by name or vendor...")
        self.search_bar.textChanged.connect(self.filter_table)
        layout.addWidget(self.search_bar)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["PLUGIN NAME", "VENDOR", "FORMATS", "DETECTED IN"])

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setStretchLastSection(False)

        self.table.verticalHeader().setVisible(False)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(50)

        layout.addWidget(self.table)

    def filter_table(self, text):
        query = text.lower()
        for row in range(self.table.rowCount()):
            match = False
            item_name = self.table.item(row, 0)
            item_vendor = self.table.item(row, 1)

            if item_name and query in item_name.text().lower(): match = True
            if item_vendor and query in item_vendor.text().lower(): match = True

            self.table.setRowHidden(row, not match)

    def update_results(self):
        library = self.controller.merger.get_sorted_library()
        self.table.setRowCount(len(library))
        self.table.setSortingEnabled(False)
        self.lbl_stats.setText(f"{len(library)} unique plugins discovered")

        theme_name = self.controller.config.get("theme", "matcha")
        try:
            theme_module = __import__(f"gui.themes.{theme_name}", fromlist=['COLORS'])
            COLORS = theme_module.COLORS
        except ImportError:
            from gui.themes.matcha import COLORS

        col_main = QColor(COLORS["TEXT_MAIN"])
        col_muted = QColor(COLORS["TEXT_MUTED"])

        for row, p in enumerate(library):
            fmts = [f for f in p.formats if f != "FL_NATIVE"]
            if not fmts: fmts = ["Internal"]

            item_name = QTableWidgetItem(p.name)
            item_name.setForeground(col_main)

            item_vendor = QTableWidgetItem(p.vendor)
            item_vendor.setForeground(col_muted)

            badge_container = QWidget()
            badge_layout = QHBoxLayout(badge_container)
            badge_layout.setContentsMargins(8, 0, 8, 0)
            badge_layout.setSpacing(6)
            badge_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            for f in sorted(fmts):
                lbl_badge = QLabel(f)
                lbl_badge.setObjectName("PluginBadge")
                badge_layout.addWidget(lbl_badge)

            item_src = QTableWidgetItem(", ".join(sorted(p.detected_by)))
            item_src.setForeground(col_muted)

            self.table.setItem(row, 0, item_name)
            self.table.setItem(row, 1, item_vendor)

            sort_string = "".join(sorted(fmts))
            format_item = FormatTableItem(sort_string)

            calc_size = badge_container.sizeHint()
            safe_width = calc_size.width() if calc_size.width() > 0 else (len(fmts) * 55 + 20)
            format_item.setSizeHint(QSize(safe_width + 10, 50))

            self.table.setItem(row, 2, format_item)
            self.table.setCellWidget(row, 2, badge_container)
            self.table.setItem(row, 3, item_src)

        self.table.setSortingEnabled(True)

    def export_data(self, fmt: str):
        data = self.controller.merger.get_sorted_library()
        if not data:
            return

        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        path, _ = QFileDialog.getSaveFileName(
            self,
            f"Export {fmt.upper()} Report",
            f"VSTea_Report_{date_str}.{fmt}",
            f"{fmt.upper()} Files (*.{fmt})"
        )

        if not path:
            return

        theme_name = self.controller.config.get("theme", "matcha")
        try:
            theme_colors = importlib.import_module(f"gui.themes.{theme_name}").COLORS
        except ImportError:
            from gui.themes.matcha import COLORS as theme_colors

        if fmt == "html" and HTMLExporter().generate(data, path, theme_colors):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

        elif fmt == "json" and JSONExporter().generate(data, path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))