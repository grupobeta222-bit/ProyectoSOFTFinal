import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

if __name__ == "__main__":
    import src.interfaces.presentation.app_ui
    from src.interfaces.presentation.context import ui

    puerto = int(os.environ.get("PORT", 8080))
    ui.run(
        host="0.0.0.0",
        port=puerto,
        title="AutoVentas Pro",
        reload=False,
        favicon="\U0001f697",
        storage_secret="autoventas-pro-admin",
    )
