"""
YH-kollen - Insikter för Anordnare

Denna sida visar personaliserade insikter och jämförelser för utbildningsanordnare.
"""

import taipy.gui.builder as tgb

with tgb.Page() as insikter_page:
    tgb.navbar()

    tgb.text("# 🔍 Insikter för Anordnare", mode="md")

    tgb.html("hr")

    # FILTER SEKTION
    tgb.text("## Välj anordnare att analysera", mode="md")

    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("**Välj anordnare:**", mode="md")
            tgb.selector(value="{selected_anordnare_insight}", lov="{anordnare}", dropdown=True, filter=True, on_change="update_anordnare_insights")

        with tgb.part():
            tgb.text("**Välj år:**", mode="md")
            tgb.selector(value="{selected_year_insight}", lov="{years}", dropdown=True, filter=True, on_change="update_anordnare_insights")

    tgb.html("hr")

    # NYCKELTAL FÖR VALD ANORDNARE
    tgb.text("## Nyckeltal", mode="md")
    tgb.text("*{anordnare_summary_text}*", mode="md")

    with tgb.layout(columns="1 1 1 1"):
        with tgb.part():
            tgb.text("### Ansökningar", mode="md")
            tgb.text("# {anordnare_total_ansokningar}", mode="md")

        with tgb.part():
            tgb.text("### Beviljade", mode="md")
            tgb.text("# {anordnare_beviljade}", mode="md")

        with tgb.part():
            tgb.text("### Godkännandegrad", mode="md")
            tgb.text("# {anordnare_godkand_procent}%", mode="md")

        with tgb.part():
            tgb.text("### Totala platser", mode="md")
            tgb.text("# {anordnare_platser}", mode="md")

    tgb.html("hr")

    # JÄMFÖRELSE MED GENOMSNITTET
    tgb.text("## Jämförelse med genomsnittet", mode="md")

    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("### Godkännandegrad: Du vs Alla", mode="md")
            tgb.text("&nbsp;", mode="md")
            tgb.chart(figure="{godkannande_comparison_chart}")

        with tgb.part():
            tgb.text("### Din position bland alla anordnare", mode="md")
            tgb.text("*{ranking_text}*", mode="md")
            tgb.chart(figure="{ranking_chart}")

    tgb.html("hr")

    # STYRKOR OCH SVAGHETER
    tgb.text("## Prestanda per utbildningsområde", mode="md")
    tgb.text("*Jämför din godkännandegrad med genomsnittet inom respektive område*", mode="md")

    tgb.chart(figure="{styrkor_chart}")
