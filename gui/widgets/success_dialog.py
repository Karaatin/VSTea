from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QFrame, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup
from PySide6.QtGui import QColor


class ScanSuccessDialog(QDialog):
    def __init__(self, parent, plugin_count: int):
        super().__init__(parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(340, 300)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)

        self.card = QFrame(self)
        self.card.setObjectName("SuccessCardFrame")

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(30, 40, 30, 30)
        card_layout.setSpacing(15)

        lbl_icon = QLabel("🎉")
        lbl_icon.setObjectName("SuccessIcon")
        lbl_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_title = QLabel("Scan Complete!")
        lbl_title.setObjectName("SuccessTitle")
        lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        lbl_desc = QLabel(f"VSTea successfully discovered\n{plugin_count} unique plugins on your system.")
        lbl_desc.setObjectName("SuccessDesc")
        lbl_desc.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_ok = QPushButton("View Results")
        self.btn_ok.setObjectName("PrimaryBtn")
        self.btn_ok.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_ok.clicked.connect(self.accept)

        card_layout.addWidget(lbl_icon)
        card_layout.addWidget(lbl_title)
        card_layout.addWidget(lbl_desc)
        card_layout.addStretch()
        card_layout.addWidget(self.btn_ok)

        layout.addWidget(self.card)

    def showEvent(self, event):
        super().showEvent(event)

        parent_widget = self.parentWidget()
        if parent_widget:
            parent_center = parent_widget.mapToGlobal(parent_widget.rect().center())
            my_center = self.rect().center()
            self.move(parent_center.x() - my_center.x(), parent_center.y() - my_center.y())

        self.anim_group = QParallelAnimationGroup()

        self.setWindowOpacity(0.0)
        fade_anim = QPropertyAnimation(self, b"windowOpacity")
        fade_anim.setDuration(400)
        fade_anim.setStartValue(0.0)
        fade_anim.setEndValue(1.0)
        fade_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        move_anim = QPropertyAnimation(self, b"pos")
        move_anim.setDuration(600)

        end_pos = self.pos()
        start_pos = end_pos + self.rect().topLeft()
        start_pos.setY(end_pos.y() + 50)

        move_anim.setStartValue(start_pos)
        move_anim.setEndValue(end_pos)
        move_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self.anim_group.addAnimation(fade_anim)
        self.anim_group.addAnimation(move_anim)
        self.anim_group.start()