"""
YH-kollen - Kartsida

Denna sida visar en geografisk visualisering av beviljade YH-ansökningar
per län med interaktiva filter.
"""

import taipy.gui.builder as tgb

with tgb.Page() as karta_page:
    tgb.navbar()

    tgb.text("# 🗺️ Geografisk fördelning", mode="md")

    tgb.html("hr")

    # FILTER SEKTION
    tgb.text("## Filter", mode="md")

    with tgb.layout(columns="1 1 1"):
        with tgb.part():
            tgb.text("**Välj år:**", mode="md")
            tgb.selector(value="{selected_year}", lov="{years}", dropdown=True, filter=True, on_change="update_dashboard")

        with tgb.part():
            tgb.text("**Välj typ:**", mode="md")
            tgb.selector(value="{selected_type}", lov="{types}", dropdown=True, filter=True, on_change="update_dashboard")

        with tgb.part():
            tgb.text("**Välj anordnare:**", mode="md")
            tgb.selector(value="{selected_anordnare}", lov="{anordnare}", dropdown=True, filter=True, on_change="update_dashboard")

    tgb.html("hr")

    tgb.text("## Beviljade ansökningar per län", mode="md")

    # Karta
    tgb.chart(figure="{map_chart}")
