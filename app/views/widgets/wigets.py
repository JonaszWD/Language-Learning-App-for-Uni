from PyQt6.QtWidgets import (
    QLabel, QLineEdit
)
from PyQt6.QtCore import Qt

def make_label(text, object_name, alignment=Qt.AlignmentFlag.AlignLeft):
    label = QLabel(text)
    label.setObjectName(object_name)
    label.setAlignment(alignment)
    return label


def make_input(placeholder, echo_mode=QLineEdit.EchoMode.Normal):
    field = QLineEdit()
    field.setPlaceholderText(placeholder)
    field.setEchoMode(echo_mode)
    field.setFixedHeight(38)
    return field