from __future__ import annotations

import os

from gaphor.abc import ActionProvider, Service
from gaphor.core import action, gettext
from gaphor.diagram.export import save_pdf, save_png, save_svg
from gaphor.ui.filedialog import save_file_dialog


class DiagramExport(Service, ActionProvider):
    """Service for exporting diagrams as images (SVG, PNG, PDF)."""

    def __init__(self, diagrams=None, export_menu=None):

        self.diagrams = diagrams
        self.export_menu = export_menu
        if export_menu:
            export_menu.add_actions(self)
        self.dirname: str | None = None

    def shutdown(self):
        if self.export_menu:
            self.export_menu.remove_actions(self)

    def save_dialog(self, diagram, title, ext, mime_type, handler):
        dot_ext = f".{ext}"
        filename = (diagram.name or "export") + dot_ext

        def save_handler(filename):
            self.dirname = os.path.dirname(filename)
            handler(filename, diagram)

        save_file_dialog(
            title,
            save_handler,
            filename=filename,
            extension=dot_ext,
            dirname=self.dirname,
            filters=[
                (gettext("All {ext} Files").format(ext=ext.upper()), dot_ext, mime_type)
            ],
        )

    @action(
        name="file-export-svg",
        label=gettext("Export as SVG"),
        tooltip=gettext("Export diagram as SVG"),
    )
    def save_svg_action(self):
        diagram = self.diagrams.get_current_diagram()
        self.save_dialog(
            diagram, gettext("Export diagram as SVG"), "svg", "image/svg+xml", save_svg
        )

    @action(
        name="file-export-png",
        label=gettext("Export as PNG"),
        tooltip=gettext("Export diagram as PNG"),
    )
    def save_png_action(self):
        diagram = self.diagrams.get_current_diagram()
        self.save_dialog(
            diagram, gettext("Export diagram as PNG"), "png", "image/png", save_png
        )

    @action(
        name="file-export-pdf",
        label=gettext("Export as PDF"),
        tooltip=gettext("Export diagram as PDF"),
    )
    def save_pdf_action(self):
        diagram = self.diagrams.get_current_diagram()
        self.save_dialog(
            diagram,
            gettext("Export diagram as PDF"),
            "pdf",
            "application/pdf",
            save_pdf,
        )
