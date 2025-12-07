import taipy.gui.builder as tgb

with tgb.Page() as insikter_page:
    tgb.navbar()

    # Header
    tgb.text("# Anordnare", mode="md", class_name="text-center")
    tgb.text("**Jämför anordnare och analysera prestanda**", mode="md", class_name="text-center")
    tgb.html("br")

    # FILTER SEKTION
    with tgb.part(class_name="card"):
        tgb.text("## Välj anordnare att analysera", mode="md")

        with tgb.layout(columns="1 1"):
            with tgb.part():
                tgb.text("**Välj anordnare:**", mode="md")
                tgb.selector(value="{selected_anordnare_insight}", lov="{anordnare}", dropdown=True, filter=True, on_change="update_anordnare_insights")

            with tgb.part():
                tgb.text("**Välj år:**", mode="md")
                tgb.selector(value="{selected_year_insight}", lov="{years}", dropdown=True, filter=True, on_change="update_anordnare_insights")

    tgb.html("br")

    # NYCKELTAL FÖR VALD ANORDNARE
    tgb.text("## Nyckeltal", mode="md")
    tgb.text("*{anordnare_summary_text}*", mode="md", class_name="text-muted")

    with tgb.layout(columns="1 1 1 1"):
        with tgb.part(class_name="card"):
            tgb.text("### Ansökningar", mode="md")
            tgb.text("# {anordnare_total_ansokningar}", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Beviljade", mode="md")
            tgb.text("# {anordnare_beviljade}", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Godkännandegrad", mode="md")
            tgb.text("# {anordnare_godkand_procent}%", mode="md", class_name="text-primary")

        with tgb.part(class_name="card"):
            tgb.text("### Totala platser", mode="md")
            tgb.text("# {anordnare_platser}", mode="md", class_name="text-primary")

    tgb.html("br")

    # JÄMFÖRELSE MED GENOMSNITTET
    tgb.text("## Jämförelse med genomsnittet", mode="md")

    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card"):
            tgb.text("### Godkännandegrad jämfört med genomsnittet", mode="md")
            tgb.chart(figure="{godkannande_comparison_chart}")

        with tgb.part(class_name="card"):
            tgb.text("### Position bland alla anordnare", mode="md")
            tgb.text("*{ranking_text}*", mode="md", class_name="text-muted")
            tgb.chart(figure="{ranking_chart}")

    tgb.html("br")

    # PRESTANDA PER OMRÅDE
    with tgb.part(class_name="card"):
        tgb.text("## Prestanda per utbildningsområde", mode="md")
        tgb.text("*Godkännandegrad per utbildningsområde för vald anordnare*", mode="md", class_name="text-muted")
        tgb.chart(figure="{styrkor_chart}")
