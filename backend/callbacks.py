import pandas as pd
import plotly.graph_objects as go
from backend.calculations import calculate_kpis, filter_data, get_examensgrad_selected
from frontend.charts import *
from frontend.map_charts import create_map

def update_dashboard(state):
    filtered_df = filter_data(state.df, state.selected_year, state.selected_type, state.selected_anordnare)

    filtered_without_anordnare = filter_data(state.df, state.selected_year, state.selected_type, "Alla")

    state.total_ansokningar, state.antal_beviljade, state.godkand_procent, state.total_platser = calculate_kpis(filtered_df)

    state.bar_chart = create_bar_chart(filtered_df)
    state.pie_chart = create_pie_chart(filtered_df)

    state.stacked_bar_chart = create_stacked_bar_chart(filtered_without_anordnare)
    state.beslut_bar_chart = create_beslut_bar_chart(filtered_without_anordnare)

    state.map_chart = create_map(filtered_df)

def update_anordnare_insights(state):
    anordnare_name = state.selected_anordnare_insight
    year_filter = state.selected_year_insight

    if anordnare_name == "Alla":
        state.anordnare_summary_text = "Välj en anordnare för att se insikter"
        state.anordnare_total_ansokningar = 0
        state.anordnare_beviljade = 0
        state.anordnare_godkand_procent = 0
        state.anordnare_platser = 0
        state.ranking_text = ""

        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="Välj en anordnare för att se insikter",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        empty_fig.update_layout(height=400)

        state.godkannande_comparison_chart = empty_fig
        state.ranking_chart = empty_fig
        state.styrkor_chart = empty_fig
        state.svagheter_chart = empty_fig
        return

    if year_filter == "Alla":
        filtered_data = state.df
    else:
        filtered_data = state.df[state.df['År'] == int(year_filter)]

    anordnare_data = filtered_data[filtered_data['Anordnare namn'] == anordnare_name]

    state.anordnare_total_ansokningar = len(anordnare_data)
    state.anordnare_beviljade = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
    state.anordnare_godkand_procent = round((state.anordnare_beviljade / state.anordnare_total_ansokningar * 100), 1) if state.anordnare_total_ansokningar > 0 else 0

    beviljade = anordnare_data[anordnare_data['Beslut'] == 'Beviljad']
    total_platser = 0
    for _, row in beviljade.iterrows():
        if row['Typ'] == 'Kurs' and 'Totalt antal beviljade platser' in beviljade.columns:
            platser = row.get('Totalt antal beviljade platser', 0)
        elif row['Typ'] == 'Program' and 'Beviljade platser totalt' in beviljade.columns:
            platser = row.get('Beviljade platser totalt', 0)
        else:
            platser = 0

        if pd.notna(platser):
            total_platser += int(platser)

    state.anordnare_platser = total_platser

    year_text = f"under {year_filter}" if year_filter != "Alla" else "totalt (alla år)"
    state.anordnare_summary_text = f"{anordnare_name} har {state.anordnare_total_ansokningar} ansökningar {year_text}, varav {state.anordnare_beviljade} beviljades ({state.anordnare_godkand_procent}%)"

    all_anordnare_stats = []
    for other_anordnare in filtered_data['Anordnare namn'].unique():
        if pd.isna(other_anordnare):
            continue
        other_data = filtered_data[filtered_data['Anordnare namn'] == other_anordnare]
        total = len(other_data)
        if total < 5:
            continue
        beviljade = len(other_data[other_data['Beslut'] == 'Beviljad'])
        godkand = round((beviljade / total * 100), 1) if total > 0 else 0
        all_anordnare_stats.append({'Anordnare': other_anordnare, 'Godkännandegrad': godkand})

    ranking_df = pd.DataFrame(all_anordnare_stats).sort_values('Godkännandegrad', ascending=False).reset_index(drop=True)

    if anordnare_name in ranking_df['Anordnare'].values:
        position = ranking_df[ranking_df['Anordnare'] == anordnare_name].index[0] + 1
        total_competitors = len(ranking_df)
        state.ranking_text = f"{anordnare_name} rankas #{position} av {total_competitors} anordnare (med minst 5 ansökningar)"
    else:
        state.ranking_text = f"{anordnare_name} har för få ansökningar för att rankas (minst 5 krävs)"

    state.godkannande_comparison_chart = create_godkannande_comparison_chart(filtered_data, anordnare_name)
    state.ranking_chart = create_ranking_chart(filtered_data, anordnare_name)
    state.styrkor_chart, state.svagheter_chart = create_styrkor_svagheter_charts(filtered_data, anordnare_name)

def update_studerande(state):
    state.studerande_chart = create_studerande_chart(state.selected_omrade, state.df_stud_filtered)
    state.examinerade_chart = create_examinerade_chart(state.selected_omrade)
    state.comparison_chart = create_comparison_chart(state.selected_omrade)
    state.studerande_table = create_studerande_table(state.selected_omrade, state.df_stud_filtered)
    state.examensgrad_selected = get_examensgrad_selected(state.selected_omrade)
