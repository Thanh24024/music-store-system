"""
Theme và Style cho GUI - Hệ thống bán nhạc cụ
"""

class Theme:
    # Colors
    PRIMARY = "#1e3a8a"        # Xanh dương đậm
    SECONDARY = "#3b82f6"      # Xanh dương nhạt
    SUCCESS = "#10b981"        # Xanh lá
    DANGER = "#ef4444"         # Đỏ
    WARNING = "#f59e0b"        # Cam
    INFO = "#06b6d4"           # Xanh ngọc
    
    BG_PRIMARY = "#ffffff"     # Trắng
    BG_SECONDARY = "#f3f4f6"   # Xám nhạt
    BG_DARK = "#1f2937"        # Xám đậm
    
    TEXT_PRIMARY = "#111827"   # Đen
    TEXT_SECONDARY = "#6b7280" # Xám
    TEXT_LIGHT = "#ffffff"     # Trắng
    
    BORDER = "#e5e7eb"         # Viền
    HOVER = "#dbeafe"          # Hover effect
    
    # Fonts
    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SMALL = 10
    FONT_SIZE_NORMAL = 12
    FONT_SIZE_LARGE = 14
    FONT_SIZE_XLARGE = 18
    FONT_SIZE_TITLE = 24
    
    # Dimensions
    PADDING = 10
    MARGIN = 15
    BORDER_RADIUS = 5
    BUTTON_HEIGHT = 35
    INPUT_HEIGHT = 35
    
    # Button Styles
    @staticmethod
    def get_button_style(button_type="primary"):
        styles = {
            "primary": {
                "bg": Theme.PRIMARY,
                "fg": Theme.TEXT_LIGHT,
                "activebackground": Theme.SECONDARY,
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8
            },
            "secondary": {
                "bg": Theme.BG_SECONDARY,
                "fg": Theme.TEXT_PRIMARY,
                "activebackground": Theme.HOVER,
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8
            },
            "success": {
                "bg": Theme.SUCCESS,
                "fg": Theme.TEXT_LIGHT,
                "activebackground": "#059669",
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8
            },
            "danger": {
                "bg": Theme.DANGER,
                "fg": Theme.TEXT_LIGHT,
                "activebackground": "#dc2626",
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL, "bold"),
                "relief": "flat",
                "cursor": "hand2",
                "padx": 20,
                "pady": 8
            }
        }
        return styles.get(button_type, styles["primary"])
    
    @staticmethod
    def get_entry_style():
        return {
            "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
            "relief": "solid",
            "borderwidth": 1,
            "highlightthickness": 0
        }
    
    @staticmethod
    def get_label_style(label_type="normal"):
        styles = {
            "normal": {
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_NORMAL),
                "fg": Theme.TEXT_PRIMARY,
                "bg": Theme.BG_PRIMARY
            },
            "title": {
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_TITLE, "bold"),
                "fg": Theme.PRIMARY,
                "bg": Theme.BG_PRIMARY
            },
            "subtitle": {
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_LARGE, "bold"),
                "fg": Theme.TEXT_PRIMARY,
                "bg": Theme.BG_PRIMARY
            },
            "secondary": {
                "font": (Theme.FONT_FAMILY, Theme.FONT_SIZE_SMALL),
                "fg": Theme.TEXT_SECONDARY,
                "bg": Theme.BG_PRIMARY
            }
        }
        return styles.get(label_type, styles["normal"])
    
    @staticmethod
    def get_frame_style():
        return {
            "bg": Theme.BG_PRIMARY,
            "relief": "flat"
        }