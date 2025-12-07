import taipy.gui.builder as tgb

with tgb.Page() as storytelling_page:
    tgb.navbar()

    # Header
    tgb.text("# Data Storytelling för The Skool", mode="md", class_name="text-center")
    tgb.text("**Strategiska insikter om Data/IT inom YH**", mode="md", class_name="text-center")
    tgb.html("br")

    # ===== ROW 1: VISUALIZATION 1 & 2 =====
    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card"):
            tgb.image("outputs/storytelling_1_approval_by_area.png", width="100%")

        with tgb.part(class_name="card"):
            tgb.image("outputs/storytelling_2_datait_trend.png", width="100%")

    tgb.html("br")

    # ===== ROW 2: VISUALIZATION 3 & 4 =====
    with tgb.layout(columns="1 1"):
        with tgb.part(class_name="card"):
            tgb.image("outputs/storytelling_3_geographic_opportunity.png", width="100%")

        with tgb.part(class_name="card"):
            tgb.image("outputs/storytelling_4_graduation_rate.png", width="100%")

    tgb.html("br")

    # Footer note
    tgb.text("*Visualiseringarna uppdateras genom att köra: `python storytelling.py`*",
             mode="md", class_name="text-muted")
