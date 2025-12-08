import taipy.gui.builder as tgb

with tgb.Page() as studerande_page:
    tgb.navbar()

    # Header
    tgb.text("# Studenttrender", mode="md", class_name="text-center")
    tgb.text("**Alla inskrivna studenter per utbildningsområde 2005-2024**", mode="md", class_name="text-center")
    tgb.html("br")

    # Filter: Välj utbildningsområde
    with tgb.part(class_name="card"):
        tgb.text("### Välj utbildningsområde", mode="md")
        tgb.selector(
            value="{selected_omrade}",
            lov="{omrade_list}",
            dropdown=True,
            filter=True,
            on_change="update_studerande"
        )

    tgb.html("br")

    # KPI: Examensgrad statistik
    with tgb.part(class_name="card"):
        tgb.text("### Examensgrad-statistik (2024)", mode="md")
        tgb.text("*Examensgrad = Antal examinerade / Antal aktiva studenter*", mode="md", class_name="text-muted")
        tgb.html("br")

        # Visa valt områdes examensgrad
        tgb.text("**{selected_omrade}:** {examensgrad_selected}%", mode="md", class_name="text-primary")

        tgb.html("br")

        # Visa top 5 områden med högst examensgrad
        tgb.text("**Top 5 områden med högst examensgrad:**", mode="md")
        tgb.table(
            data="{examensgrad_top5}",
            show_all=True
        )

    tgb.html("br")

    # Visualisering: Line chart
    with tgb.part(class_name="card"):
        tgb.text("### Trend: Totalt antal inskrivna studenter", mode="md")
        tgb.text("*Visar alla studenter som är inskrivna i utbildning vid mättillfället*", mode="md", class_name="text-muted")
        tgb.chart(figure="{studerande_chart}")

    tgb.html("br")

    # Visualisering: Examinerade studenter
    with tgb.part(class_name="card"):
        tgb.text("### Trend: Antal examinerade studenter", mode="md")
        tgb.text("*Visar studenter som slutfört sin utbildning och tagit examen*", mode="md", class_name="text-muted")
        tgb.chart(figure="{examinerade_chart}")

    tgb.html("br")

    # Visualisering: Jämförelse
    with tgb.part(class_name="card"):
        tgb.text("### Jämförelse: Inskrivna studenter vs Examinerade", mode="md")
        tgb.text("*Visar relationen mellan totalt antal inskrivna studenter och antal som examineras per år. Den gula linjen visar examensgrad (andel som tar examen).*", mode="md", class_name="text-muted")
        tgb.chart(figure="{comparison_chart}")
