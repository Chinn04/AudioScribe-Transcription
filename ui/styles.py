"""
ui/styles.py
Central QSS stylesheet for the app. Keeping all styling in one string
here (instead of scattered inline styles) makes the "premium" look
consistent and easy to tweak.
"""

import config as cfg


def get_stylesheet() -> str:
    return f"""
    /* ---------- Global ---------- */
    QWidget {{
        background-color: {cfg.COLOR_BACKGROUND};
        color: {cfg.COLOR_TEXT};
        font-family: 'Segoe UI', 'Inter', sans-serif;
        font-size: 13px;
    }}

    QMainWindow {{
        background-color: {cfg.COLOR_BACKGROUND};
    }}

    QToolTip {{
        background-color: {cfg.COLOR_CARD_LIGHT};
        color: {cfg.COLOR_TEXT};
        border: 1px solid {cfg.COLOR_BORDER};
        padding: 6px;
        border-radius: 6px;
    }}

    /* ---------- Cards ---------- */
    #card {{
        background-color: {cfg.COLOR_CARD};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 16px;
    }}

    #cardLight {{
        background-color: {cfg.COLOR_CARD_LIGHT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 12px;
    }}

    /* ---------- Header ---------- */
    #appTitle {{
        font-size: 22px;
        font-weight: 700;
        color: {cfg.COLOR_TEXT};
    }}

    #appSubtitle {{
        font-size: 12px;
        color: {cfg.COLOR_TEXT_MUTED};
    }}

    /* ---------- Upload area ---------- */
    #uploadArea {{
        background-color: rgba(30, 41, 59, 0.55);
        border: 2px dashed {cfg.COLOR_BORDER};
        border-radius: 18px;
    }}

    #uploadArea[dragActive="true"] {{
        border: 2px dashed {cfg.COLOR_PRIMARY};
        background-color: rgba(59, 130, 246, 0.10);
    }}

    #uploadTitle {{
        font-size: 16px;
        font-weight: 600;
        color: {cfg.COLOR_TEXT};
    }}

    #uploadHint {{
        font-size: 11px;
        color: {cfg.COLOR_TEXT_MUTED};
    }}

    /* ---------- Buttons ---------- */
    QPushButton {{
        background-color: {cfg.COLOR_CARD_LIGHT};
        color: {cfg.COLOR_TEXT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 10px;
        padding: 9px 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background-color: #31435F;
        border: 1px solid {cfg.COLOR_PRIMARY};
    }}

    QPushButton:pressed {{
        background-color: #26364C;
    }}

    QPushButton:disabled {{
        color: {cfg.COLOR_TEXT_MUTED};
        background-color: {cfg.COLOR_CARD};
        border: 1px solid {cfg.COLOR_BORDER};
    }}

    #primaryButton {{
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {cfg.COLOR_PRIMARY}, stop:1 {cfg.COLOR_ACCENT}
        );
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 14px;
        font-weight: 700;
    }}

    #primaryButton:hover {{
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {cfg.COLOR_PRIMARY_DARK}, stop:1 {cfg.COLOR_ACCENT}
        );
    }}

    #primaryButton:disabled {{
        background-color: {cfg.COLOR_CARD_LIGHT};
        color: {cfg.COLOR_TEXT_MUTED};
    }}

    #dangerButton {{
        background-color: rgba(239, 68, 68, 0.12);
        border: 1px solid {cfg.COLOR_DANGER};
        color: {cfg.COLOR_DANGER};
    }}

    #dangerButton:hover {{
        background-color: rgba(239, 68, 68, 0.22);
    }}

    /* ---------- Text areas / inputs ---------- */
    QTextEdit, QPlainTextEdit {{
        background-color: {cfg.COLOR_BACKGROUND_ALT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 12px;
        padding: 12px;
        selection-background-color: {cfg.COLOR_PRIMARY};
    }}

    QLineEdit {{
        background-color: {cfg.COLOR_BACKGROUND_ALT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 8px;
        padding: 8px 10px;
    }}

    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {cfg.COLOR_PRIMARY};
    }}

    QComboBox {{
        background-color: {cfg.COLOR_BACKGROUND_ALT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 8px;
        padding: 7px 10px;
    }}

    QComboBox:hover {{
        border: 1px solid {cfg.COLOR_PRIMARY};
    }}

    QComboBox QAbstractItemView {{
        background-color: {cfg.COLOR_CARD_LIGHT};
        border: 1px solid {cfg.COLOR_BORDER};
        selection-background-color: {cfg.COLOR_PRIMARY};
        outline: none;
    }}

    /* ---------- Progress bar ---------- */
    QProgressBar {{
        background-color: {cfg.COLOR_BACKGROUND_ALT};
        border: 1px solid {cfg.COLOR_BORDER};
        border-radius: 10px;
        text-align: center;
        color: {cfg.COLOR_TEXT};
        height: 20px;
    }}

    QProgressBar::chunk {{
        border-radius: 9px;
        background-color: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 {cfg.COLOR_PRIMARY}, stop:1 {cfg.COLOR_ACCENT}
        );
    }}

    /* ---------- Labels ---------- */
    #statLabel {{
        color: {cfg.COLOR_TEXT_MUTED};
        font-size: 11px;
    }}

    #statValue {{
        color: {cfg.COLOR_TEXT};
        font-size: 15px;
        font-weight: 700;
    }}

    #stageLabel {{
        color: {cfg.COLOR_ACCENT};
        font-size: 12px;
        font-weight: 600;
    }}

    #errorLabel {{
        color: {cfg.COLOR_DANGER};
        font-size: 12px;
        font-weight: 600;
    }}

    /* ---------- Scrollbars ---------- */
    QScrollBar:vertical {{
        background: transparent;
        width: 10px;
        margin: 0px;
    }}

    QScrollBar::handle:vertical {{
        background: {cfg.COLOR_BORDER};
        border-radius: 5px;
        min-height: 24px;
    }}

    QScrollBar::handle:vertical:hover {{
        background: {cfg.COLOR_PRIMARY};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    /* ---------- Menus / dialogs ---------- */
    QMessageBox {{
        background-color: {cfg.COLOR_CARD};
    }}
    """
