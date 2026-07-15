from src.interfaces.presentation.context import ui


def render_kpi_card(label, value, subtitle="", color=""):
    extra = f" {color}" if color else ""
    ui.html(
        '<div class="av-kpi">'
        f'<div class="av-kpi-label">{label}</div>'
        f'<div class="av-kpi-val{extra}">{value}</div>'
        f'<div class="av-kpi-sub">{subtitle}</div>'
        '</div>'
    )
