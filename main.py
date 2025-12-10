import pandas as pd
import plotly.graph_objects as go
from taipy.gui import Gui
from backend.data_loader import load_all_data, load_studerande_data
from backend.calculations import *
from backend.callbacks import *
from frontend.charts import *
from frontend.map_charts import create_map
from frontend.pages.oversikt_page import oversikt_page
from frontend.pages.karta_page import karta_page
from frontend.pages.anordnare_page import anordnare_page
from frontend.pages.storytelling_page import storytelling_page
from frontend.pages.studerande_page import studerande_page

df = load_all_data()
df_stud_filtered, omrade_list = load_studerande_data()

years = ["Alla", "2024", "2023", "2022"]
types = ["Alla", "Kurs", "Program"]
anordnare = ["Alla"] + sorted([x for x in df['Anordnare namn'].unique() if pd.notna(x)])

selected_year = "Alla"
selected_type = "Alla"
selected_anordnare = "Alla"

total_ansokningar, antal_beviljade, godkand_procent, total_platser = calculate_kpis(df)

bar_chart = create_bar_chart(df)
pie_chart = create_pie_chart(df)
stacked_bar_chart = create_stacked_bar_chart(df)
beslut_bar_chart = create_beslut_bar_chart(df)
map_chart = create_map(df)

distribution_table = df.groupby(['Typ', 'År']).size().reset_index(name='Antal')
table_description = "Visar hur ansökningarna är fördelade mellan kurser och program för varje år"

selected_anordnare_insight = "Alla"
selected_year_insight = "Alla"

anordnare_total_ansokningar = 0
anordnare_beviljade = 0
anordnare_godkand_procent = 0
anordnare_platser = 0
anordnare_summary_text = "Välj en anordnare för att se insikter"
ranking_text = ""

empty_fig = go.Figure()
empty_fig.add_annotation(
    text="Välj en anordnare för att se insikter",
    xref="paper", yref="paper",
    x=0.5, y=0.5, showarrow=False,
    font=dict(size=16)
)
empty_fig.update_layout(height=400)

godkannande_comparison_chart = empty_fig
ranking_chart = go.Figure(empty_fig)
styrkor_chart = go.Figure(empty_fig)
svagheter_chart = go.Figure(empty_fig)

selected_omrade = "Data/It"

studerande_chart = create_studerande_chart(selected_omrade, df_stud_filtered)
examinerade_chart = create_examinerade_chart(selected_omrade)
comparison_chart = create_comparison_chart(selected_omrade)
studerande_table = create_studerande_table(selected_omrade, df_stud_filtered)
examensgrad_top5 = get_examensgrad_top5()
examensgrad_selected = get_examensgrad_selected(selected_omrade)

pages = {
    "Översikt": oversikt_page,
    "Studenttrender": studerande_page,
    "Karta": karta_page,
    "Anordnare": anordnare_page,
    "Storytelling": storytelling_page
}

if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/main.css").run(
        port=5005,
        debug=True,
        dark_mode=False,
        title="YH-kollen"
    )
