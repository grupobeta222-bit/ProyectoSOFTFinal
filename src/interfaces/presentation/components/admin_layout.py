from html import escape

from src.interfaces.presentation.context import (
    ui,
    add_css,
    admin_logueado,
    cerrar_sesion_admin,
    usuario_actual,
    es_gerente,
)


def _safe(value):
    return escape(str(value if value is not None else ""))


def _menu_link(active, key, icon, label, url):
    activo = active == key
    bg = "rgba(230,57,70,.14)" if activo else "transparent"
    border = "rgba(230,57,70,.55)" if activo else "rgba(255,255,255,0)"
    color = "#ffffff" if activo else "#bdbdbd"
    return f'''
    <a href="{url}" style="display:flex;align-items:center;gap:12px;color:{color};text-decoration:none;
       font-size:14px;font-weight:800;padding:13px 15px;margin:7px 0;border-radius:14px;
       border:1px solid {border};background:{bg};">
       <span style="width:20px;text-align:center;">{icon}</span><span>{label}</span>
    </a>'''


def admin_shell(active):
    add_css()
    if not admin_logueado():
        ui.navigate.to("/login")
        return None

    usuario = usuario_actual()
    rol = "Gerente" if usuario.get("rol") == "gerente" else "Asesor"
    nombre = usuario.get("nombre", "Usuario")

    menu_extra = ""
    if es_gerente():
        menu_extra = (
            _menu_link(active, 'vehiculos', '🚗', 'Vehículos', '/admin/vehiculos') +
            _menu_link(active, 'planes', '💳', 'Planes', '/admin/planes')
        )

    ui.html(f'''
    <div style="position:fixed;top:0;left:0;right:0;height:78px;z-index:300;background:#0b0b0b;
        border-bottom:1px solid rgba(255,255,255,.08);display:flex;align-items:center;justify-content:space-between;
        padding:0 clamp(26px,5vw,72px);box-shadow:0 18px 40px rgba(0,0,0,.28);">
      <a href="/" style="text-decoration:none;color:#fff;font-size:21px;font-weight:900;letter-spacing:-.5px;">
        Auto<span style="color:#e63946;">Ventas</span> Pro
      </a>
      <div style="color:#fff;font-size:13px;font-weight:800;border-bottom:2px solid #e63946;padding-bottom:9px;">
        {rol}: {_safe(nombre)}
      </div>
      <div style="display:flex;gap:10px;align-items:center;">
        <a href="/" style="text-decoration:none;background:#181818;color:#fff;border:1px solid #333;border-radius:13px;padding:12px 18px;font-weight:900;font-size:13px;">Sitio público</a>
        <a href="/login" style="text-decoration:none;background:#e63946;color:#fff;border-radius:13px;padding:12px 18px;font-weight:900;font-size:13px;">Cerrar sesión</a>
      </div>
    </div>

    <aside style="position:fixed;top:78px;left:0;bottom:0;width:260px;z-index:250;background:#101010;
        border-right:1px solid rgba(255,255,255,.08);padding:28px 18px;overflow-y:auto;">
      <div style="color:#666;font-size:11px;font-weight:900;letter-spacing:2px;text-transform:uppercase;padding:0 12px 18px;">Gestión</div>
      {_menu_link(active, 'dashboard', '🏠', 'Dashboard', '/admin')}
      {_menu_link(active, 'cotizaciones', '📄', 'Cotizaciones', '/admin/cotizaciones')}
      {_menu_link(active, 'clientes', '👥', 'Clientes', '/admin/clientes')}
      {menu_extra}
    </aside>
    ''')

    main = ui.element("main").style(
        "margin-left:260px;min-height:100vh;background:#0b0b0c;color:#fff;"
        "padding:122px clamp(34px,4vw,70px) 70px;display:block;"
    )
    return main


def logout_and_go_login():
    cerrar_sesion_admin()
    ui.navigate.to('/login')


def admin_title(title, subtitle=""):
    return f'''
    <section style="margin-bottom:26px;">
      <div style="font-size:12px;color:#e63946;font-weight:900;text-transform:uppercase;letter-spacing:2px;margin-bottom:8px;">Panel administrativo</div>
      <h1 style="font-size:clamp(30px,3vw,46px);font-weight:900;color:#fff;margin:0 0 8px;letter-spacing:-1px;">{_safe(title)}</h1>
      <p style="max-width:980px;color:#909090;font-size:14px;line-height:1.65;margin:0;">{_safe(subtitle)}</p>
    </section>
    '''


def card(title, body, icon=""):
    return f'''
    <div style="background:#141414;border:1px solid #242424;border-radius:20px;padding:24px;box-shadow:0 24px 70px rgba(0,0,0,.22);">
      <div style="font-size:26px;margin-bottom:10px;">{icon}</div>
      <div style="font-size:15px;color:#9a9a9a;font-weight:700;margin-bottom:7px;">{_safe(title)}</div>
      <div style="font-size:28px;color:#fff;font-weight:900;line-height:1.1;">{body}</div>
    </div>
    '''
