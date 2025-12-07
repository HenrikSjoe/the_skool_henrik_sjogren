import taipy.gui.builder as tgb
with tgb.Page() as oversikt_page:
    tgb.navbar()

    tgb.text("# YH-kollen Dashboard", mode="md")

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

    tgb.text("## Nyckeltal", mode="md")

    # KPI kort (använd state-variabler för dynamisk uppdatering)
    with tgb.layout(columns="1 1 1 1"):
        with tgb.part():
            tgb.text("### Totalt ansökningar", mode="md")
            tgb.text("# {total_ansokningar}", mode="md")

        with tgb.part():
            tgb.text("### Beviljade", mode="md")
            tgb.text("# {antal_beviljade}", mode="md")

        with tgb.part():
            tgb.text("### Godkänd andel", mode="md")
            tgb.text("# {godkand_procent}%", mode="md")

        with tgb.part():
            tgb.text("### Totala platser", mode="md")
            tgb.text("# {total_platser}", mode="md")

    tgb.html("hr")

    tgb.text("## Visualiseringar", mode="md")

    # Layout med 2 kolumner: Bar chart och Pie chart
    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("### Antal ansökningar per område", mode="md")
            tgb.chart(figure="{bar_chart}")

        with tgb.part():
            tgb.text("### Godkännande", mode="md")
            tgb.chart(figure="{pie_chart}")

    tgb.html("hr")

    tgb.text("## Fördjupad analys", mode="md")

    # Två kolumner för stacked bar charts
    with tgb.layout(columns="1 1"):
        with tgb.part():
            tgb.text("### Kurser vs Program", mode="md")
            tgb.chart(figure="{stacked_bar_chart}")

        with tgb.part():
            tgb.text("### Beviljad vs Avslag", mode="md")
            tgb.chart(figure="{beslut_bar_chart}")
