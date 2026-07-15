from src.interfaces.presentation.context import container, ui


def footer():
    contacto = container.contacto_service
    ui.html(f'''<div class="av-footer">
      © 2026 <span>AutoVentas Pro</span> · Guayaquil, Ecuador ·
      <a href="{contacto.enlace_whatsapp()}" target="_blank" rel="noopener noreferrer">WhatsApp</a> ·
      <a href="{contacto.enlace_correo()}">Correo</a>
    </div>''')
