import taipy.gui.builder as tgb

with tgb.Page() as karta_page:
    tgb.navbar()

    # Header
    tgb.text("# Geografisk fördelning", mode="md", class_name="text-center")
    tgb.text("**Översikt av beviljade ansökningar per län**", mode="md", class_name="text-center")
    tgb.html("br")

    # FILTER SEKTION
    with tgb.part(class_name="card"):
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

    tgb.html("br")

    # KARTA
    with tgb.part(class_name="card"):
        tgb.text("## Beviljade ansökningar per län", mode="md")
        tgb.chart(figure="{map_chart}")
