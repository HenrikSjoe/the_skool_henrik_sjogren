import taipy.gui.builder as tgb

with tgb.Page() as storytelling_page:
    tgb.navbar()

    # Header
    tgb.text("# Data Storytelling för The Skool", mode="md", class_name="text-center")
    tgb.text("**Strategiska insikter om Data/IT inom YH**", mode="md", class_name="text-center")
    tgb.html("br")

    # ===== VISUALIZATION 1 =====
    with tgb.part(class_name="card"):
        tgb.text("### 1. Varför är Data/IT så svårt?", mode="md")
        tgb.text("*Godkännandegrad per utbildningsområde - Data/IT har lägst godkännandegrad trots flest ansökningar*", mode="md", class_name="text-muted")
        tgb.image("outputs/storytelling_1_approval_by_area.png", width="100%")

    tgb.html("br")

    # ===== VISUALIZATION 2 =====
    with tgb.part(class_name="card"):
        tgb.text("### 2. Blir Data/IT bättre eller sämre över tid?", mode="md")
        tgb.text("*Trend för Data/IT ansökningar och godkännandegrad 2022-2024*", mode="md", class_name="text-muted")
        tgb.image("outputs/storytelling_2_datait_trend.png", width="100%")

    tgb.html("br")

    # ===== VISUALIZATION 3 =====
    with tgb.part(class_name="card"):
        tgb.text("### 3. Var finns de bästa möjligheterna geografiskt?", mode="md")
        tgb.text("*Godkännandegrad per län för Data/IT - stora regionala skillnader*", mode="md", class_name="text-muted")
        tgb.image("outputs/storytelling_3_geographic_opportunity.png", width="100%")

    tgb.html("br")

    # ===== VISUALIZATION 4 =====
    with tgb.part(class_name="card"):
        tgb.text("### 4. Hur ser examensgraden ut?", mode="md")
        tgb.text("*Examensgrad per utbildningsområde - andel studenter som slutför sina studier*", mode="md", class_name="text-muted")
        tgb.image("outputs/storytelling_4_graduation_rate.png", width="100%")

    tgb.html("br")
