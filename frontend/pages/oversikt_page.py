import taipy.gui.builder as tgb
with tgb.Page() as oversikt_page:
    tgb.navbar()

    # Header
    tgb.text("# Översikt", mode="md", class_name="text-center")
    tgb.text("**YH-kollen Dashboard - Analys av ansökningar**", mode="md", class_name="text-center")
    tgb.text("*Utforska ansökningar till Yrkeshögskolan för kurser och program (2022-2024)*", mode="md", class_name="text-center text-muted")
    tgb.html("br")

    # FILTER SEKTION
    with tgb.part(class_name="card"):
        tgb.text("## Filter", mode="md")
        tgb.text("*Filtrera data efter år, utbildningstyp eller specifik anordnare*", mode="md", class_name="text-muted")

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

    tgb.html("br")

    # NYCKELTAL
    tgb.text("## Nyckeltal", mode="md")

    with tgb.layout(columns="1 1 1 1"):
        with tgb.part(class_name="card"):
            tgb.text("### Totalt ansökningar", mode="md")
            tgb.text("# {total_ansokningar}", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Beviljade", mode="md")
            tgb.text("# {antal_beviljade}", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Godkänd andel", mode="md")
            tgb.text("# {godkand_procent}%", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Totala platser", mode="md")
            tgb.text("# {total_platser}", mode="md", class_name="text-primary")

    tgb.html("br")

    # VISUALISERINGAR
    tgb.text("## Visualiseringar", mode="md")

    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card"):
            tgb.text("### Antal ansökningar per område", mode="md")
            tgb.text("*Visar fördelning av ansökningar över olika utbildningsområden*", mode="md", class_name="text-muted")
            tgb.chart(figure="{bar_chart}")

        with tgb.part(class_name="card"):
            tgb.text("### Godkännande", mode="md")
            tgb.text("*Andel beviljade vs avslagna ansökningar*", mode="md", class_name="text-muted")
            tgb.chart(figure="{pie_chart}")

    tgb.html("br")

    # FÖRDJUPAD ANALYS
    tgb.text("## Fördjupad analys", mode="md")

    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card"):
            tgb.text("### Kurser vs Program", mode="md")
            tgb.text("*Jämförelse mellan kortare kurser och längre program över tid*", mode="md", class_name="text-muted")
            tgb.chart(figure="{stacked_bar_chart}")

        with tgb.part(class_name="card"):
            tgb.text("### Beviljad vs Avslag", mode="md")
            tgb.text("*Trend för godkända och avslagna ansökningar per år*", mode="md", class_name="text-muted")
            tgb.chart(figure="{beslut_bar_chart}")
