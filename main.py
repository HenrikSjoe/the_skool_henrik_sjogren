"""
YH-kollen Dashboard
Multi-page dashboard för analys av YH-ansökningar
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from taipy.gui import Gui, notify
from map_page import create_map
from oversikt_page import oversikt_page
from karta_page_file import karta_page

# ===== DATA LOADING =====
def load_all_data():
    """Ladda kurser och program från alla tillgängliga år"""
    all_dfs = []

    for year in [2023, 2024]:
        try:
            df = pd.read_excel(
                f"data/raw/resultat-{year}-for-kurser-inom-yh.xlsx",
                sheet_name="Lista ansökningar"
            )
            df['Typ'] = 'Kurs'
            df['År'] = year
            all_dfs.append(df)
        except Exception as e:
            print(f"❌ Kurser {year}: {e}")

    for year in [2022, 2023, 2024]:
        try:
            if year == 2022:
                df = pd.read_excel(
                    f"data/raw/resultat-ansokningsomgang-{year}.xlsx",
                    sheet_name="Tabell 3"
                )
            else:
                df = pd.read_excel(
                    f"data/raw/resultat-ansokningsomgang-{year}.xlsx",
                    sheet_name="Tabell 3",
                    skiprows=5
                )

            if 'Utbildningsanordnare administrativ enhet' in df.columns:
                df['Anordnare namn'] = df['Utbildningsanordnare administrativ enhet']

            df['Typ'] = 'Program'
            df['År'] = year
            all_dfs.append(df)
        except Exception as e:
            print(f"❌ Program {year}: {e}")

    combined = pd.concat(all_dfs, ignore_index=True)
    return combined

def calculate_kpis(data):
    """Beräkna KPI-värden från data"""
    total_ansokningar = len(data)
    beviljade = data[data['Beslut'] == 'Beviljad']
    antal_beviljade = len(beviljade)
    godkand_procent = round((antal_beviljade / total_ansokningar * 100), 1) if total_ansokningar > 0 else 0

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

    return total_ansokningar, antal_beviljade, godkand_procent, total_platser

def create_bar_chart(data):
    """Skapa bar chart för top 10 utbildningsområden"""
    grouped = data.groupby('Utbildningsområde').size().reset_index(name='Antal')
    grouped = grouped.sort_values('Antal', ascending=False).head(10)

    if len(grouped) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Ingen data att visa med nuvarande filter",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=500)
        return fig

    fig = px.bar(
        grouped,
        x='Utbildningsområde',
        y='Antal',
        title="Top 10 Utbildningsområden (Antal ansökningar)",
        labels={'Utbildningsområde': 'Utbildningsområde', 'Antal': 'Antal ansökningar'},
        text='Antal',
        color_discrete_sequence=['#3b82f6']
    )

    max_value = grouped['Antal'].max()
    y_range_max = max_value * 1.15

    fig.update_traces(textposition='outside')
    fig.update_layout(
        height=500,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=100),
        xaxis=dict(tickangle=-45),
        yaxis=dict(range=[0, y_range_max])
    )

    return fig

def create_pie_chart(data):
    """Skapa pie chart för beslut (Beviljad vs Avslag)"""
    beslut_counts = data['Beslut'].value_counts().reset_index()
    beslut_counts.columns = ['Beslut', 'Antal']

    if len(beslut_counts) == 0:
        fig = go.Figure()
        fig.add_annotation(
            text="Ingen data att visa med nuvarande filter",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        fig.update_layout(height=500)
        return fig

    fig = px.pie(
        beslut_counts,
        values='Antal',
        names='Beslut',
        title="Fördelning: Beviljad vs Avslag",
        color_discrete_sequence=['#10b981', '#ef4444'],
        hole=0.3
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label'
    )

    fig.update_layout(
        height=500,
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def create_stacked_bar_chart(data):
    """Skapa stacked bar chart för Kurser vs Program per utbildningsområde"""
    grouped = data.groupby(['Utbildningsområde', 'Typ']).size().reset_index(name='Antal')
    top_areas = data.groupby('Utbildningsområde').size().sort_values(ascending=False).head(10).index
    grouped = grouped[grouped['Utbildningsområde'].isin(top_areas)]

    fig = px.bar(
        grouped,
        x='Utbildningsområde',
        y='Antal',
        color='Typ',
        title="Kurser vs Program per Utbildningsområde (Marknadsöversikt - Top 10)",
        labels={'Utbildningsområde': 'Utbildningsområde', 'Antal': 'Antal ansökningar'},
        color_discrete_map={'Kurs': '#8b5cf6', 'Program': '#06b6d4'},
        barmode='stack'
    )

    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>')

    fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        xaxis=dict(tickangle=-45),
        legend=dict(title="Typ", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

def create_beslut_bar_chart(data):
    """Skapa stacked bar chart för Beviljad vs Avslag per utbildningsområde"""
    grouped = data.groupby(['Utbildningsområde', 'Beslut']).size().reset_index(name='Antal')
    top_areas = data.groupby('Utbildningsområde').size().sort_values(ascending=False).head(10).index
    grouped = grouped[grouped['Utbildningsområde'].isin(top_areas)]

    fig = px.bar(
        grouped,
        x='Utbildningsområde',
        y='Antal',
        color='Beslut',
        title="Beviljad vs Avslag per Utbildningsområde (Marknadsöversikt - Top 10)",
        labels={'Utbildningsområde': 'Utbildningsområde', 'Antal': 'Antal ansökningar'},
        color_discrete_map={'Beviljad': '#10b981', 'Avslag': '#ef4444'},
        barmode='stack'
    )

    fig.update_traces(hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>')

    fig.update_layout(
        height=500,
        margin=dict(l=50, r=50, t=80, b=100),
        xaxis=dict(tickangle=-45),
        legend=dict(title="Beslut", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig

# ===== ANORDNARE INSIGHTS FUNCTIONS =====
def create_godkannande_comparison_chart(data, anordnare_name):
    """Skapa bar chart som jämför anordnarens godkännandegrad med genomsnittet"""

    # Beräkna genomsnittlig godkännandegrad för alla
    total_all = len(data)
    beviljade_all = len(data[data['Beslut'] == 'Beviljad'])
    avg_godkand = round((beviljade_all / total_all * 100), 1) if total_all > 0 else 0

    # Beräkna för vald anordnare
    anordnare_data = data[data['Anordnare namn'] == anordnare_name]
    total_anordnare = len(anordnare_data)
    beviljade_anordnare = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
    anordnare_godkand = round((beviljade_anordnare / total_anordnare * 100), 1) if total_anordnare > 0 else 0

    # Skapa jämförelse-data
    comparison_df = pd.DataFrame({
        'Kategori': ['Genomsnitt alla anordnare', anordnare_name],
        'Godkännandegrad (%)': [avg_godkand, anordnare_godkand]
    })

    # Välj färg baserat på om anordnaren är bättre eller sämre än genomsnittet
    colors = ['#94a3b8', '#10b981' if anordnare_godkand >= avg_godkand else '#ef4444']

    fig = px.bar(
        comparison_df,
        x='Kategori',
        y='Godkännandegrad (%)',
        text='Godkännandegrad (%)',
        color='Kategori',
        color_discrete_sequence=colors
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        height=450,  # Matchad höjd med ranking chart
        showlegend=False,
        margin=dict(l=50, r=50, t=20, b=100),
        xaxis=dict(tickangle=-15),
        yaxis=dict(range=[0, 100]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.3  # Mer gap mellan dessa två staplar för tydlighet
    )

    return fig

def create_ranking_chart(data, anordnare_name):
    """Skapa bar chart med top 10 anordnare efter godkännandegrad"""

    # Beräkna godkännandegrad för varje anordnare (minst 5 ansökningar för att kvalificera)
    anordnare_stats = []

    for anordnare in data['Anordnare namn'].unique():
        if pd.isna(anordnare):
            continue

        anordnare_data = data[data['Anordnare namn'] == anordnare]
        total = len(anordnare_data)

        # Kräv minst 5 ansökningar för att räknas
        if total < 5:
            continue

        beviljade = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
        godkand_procent = round((beviljade / total * 100), 1) if total > 0 else 0

        anordnare_stats.append({
            'Anordnare': anordnare,
            'Godkännandegrad (%)': godkand_procent,
            'Ansökningar': total
        })

    # Sortera alla anordnare
    all_ranking_df = pd.DataFrame(anordnare_stats).sort_values('Godkännandegrad (%)', ascending=False)

    # Ta top 10
    top_10 = all_ranking_df.head(10)

    # Om vald anordnare INTE är i top 10, lägg till den med separering
    if anordnare_name not in top_10['Anordnare'].values:
        # Hitta den valda anordnaren i hela listan
        selected_row = all_ranking_df[all_ranking_df['Anordnare'] == anordnare_name].copy()
        if len(selected_row) > 0:
            # Lägg till "..." som visuell separator
            gap_row = pd.DataFrame({
                'Anordnare': ['...'],
                'Godkännandegrad (%)': [0],
                'Ansökningar': [0]
            })
            # Ta top 9, lägg till gap, sedan valda anordnaren
            ranking_df = pd.concat([top_10.head(9), gap_row, selected_row]).reset_index(drop=True)
        else:
            ranking_df = top_10
    else:
        ranking_df = top_10

    # Highlighta vald anordnare
    colors = []
    for x in ranking_df['Anordnare']:
        if x == anordnare_name:
            colors.append('#3b82f6')
        elif x == '...':
            colors.append('#e5e7eb')  # Ljusgrå för gap
        else:
            colors.append('#94a3b8')

    # Skapa custom text - tom för "..." stapel
    text_labels = []
    for _, row in ranking_df.iterrows():
        if row['Anordnare'] == '...':
            text_labels.append('')
        else:
            text_labels.append(f"{row['Godkännandegrad (%)']}%")

    fig = px.bar(
        ranking_df,
        x='Anordnare',
        y='Godkännandegrad (%)',
        text=text_labels,
        color='Anordnare',
        color_discrete_sequence=colors,
        hover_data=['Ansökningar']
    )

    fig.update_traces(textposition='outside', cliponaxis=False)  # cliponaxis=False viktigt!

    fig.update_layout(
        height=450,  # Ökad höjd från 400 till 450
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=150),  # Ökad top margin till 80 för att ge plats åt text
        xaxis=dict(tickangle=-45),
        yaxis=dict(range=[0, 108]),  # Mindre range men med cliponaxis=False så syns texten ändå
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.15  # Mindre gap mellan staplar
    )

    return fig

def create_styrkor_svagheter_charts(data, anordnare_name):
    """
    Skapa smart horizontal bar chart för utbildningsområden
    - 1 område: Jämför med områdesspecifikt genomsnitt
    - 2+ områden: Visa alla områden i en horizontal bar
    """

    anordnare_data = data[data['Anordnare namn'] == anordnare_name]

    # Beräkna godkännandegrad per utbildningsområde
    omrade_stats = []

    for omrade in anordnare_data['Utbildningsområde'].unique():
        if pd.isna(omrade):
            continue

        omrade_data = anordnare_data[anordnare_data['Utbildningsområde'] == omrade]
        total = len(omrade_data)

        # Visa ALLA områden (även om det bara är 1-2 ansökningar)
        beviljade = len(omrade_data[omrade_data['Beslut'] == 'Beviljad'])
        godkand_procent = round((beviljade / total * 100), 1) if total > 0 else 0

        omrade_stats.append({
            'Utbildningsområde': omrade,
            'Godkännandegrad (%)': godkand_procent,
            'Ansökningar': total,
            'Beviljade': beviljade
        })

    if len(omrade_stats) == 0:
        # Ingen data - returnera tomma figurer
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text="Ingen tillräcklig data (minst 3 ansökningar per område krävs)",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14)
        )
        empty_fig.update_layout(height=400)
        return empty_fig, empty_fig

    omrade_df = pd.DataFrame(omrade_stats).sort_values('Godkännandegrad (%)', ascending=False)

    # SCENARIO 1: Endast 1 område - jämför med områdesspecifikt genomsnitt
    if len(omrade_df) == 1:
        row = omrade_df.iloc[0]
        omrade_namn = row['Utbildningsområde']
        anordnare_rate = row['Godkännandegrad (%)']

        # Beräkna genomsnitt för detta specifika område (alla anordnare)
        omrade_all_data = data[data['Utbildningsområde'] == omrade_namn]
        total_omrade = len(omrade_all_data)
        beviljade_omrade = len(omrade_all_data[omrade_all_data['Beslut'] == 'Beviljad'])
        omrade_avg = round((beviljade_omrade / total_omrade * 100), 1) if total_omrade > 0 else 0

        # Färgkoda baserat på prestanda
        if anordnare_rate >= 70:
            color = '#10b981'
        elif anordnare_rate >= 50:
            color = '#fbbf24'
        elif anordnare_rate >= 30:
            color = '#f97316'
        else:
            color = '#ef4444'

        fig = go.Figure()

        # Genomsnitt för området
        fig.add_trace(go.Bar(
            x=[omrade_avg],
            y=[f'Genomsnitt {omrade_namn}'],
            orientation='h',
            text=[f"{omrade_avg}%"],
            textposition='auto',
            marker=dict(color='#94a3b8'),
            name='Områdesgenomsnitt',
            hovertemplate=f'<b>Genomsnitt för {omrade_namn}</b><br>Godkänd: {omrade_avg}%<br>Baserat på {total_omrade} ansökningar<extra></extra>'
        ))

        # Din prestanda
        fig.add_trace(go.Bar(
            x=[anordnare_rate],
            y=[anordnare_name],
            orientation='h',
            text=[f"{anordnare_rate}%"],
            textposition='auto',
            marker=dict(color=color),
            name='Din prestanda',
            hovertemplate=f'<b>{anordnare_name}</b><br>Godkänd: {anordnare_rate}%<br>Ansökningar: {row["Ansökningar"]}<br>Beviljade: {row["Beviljade"]}<extra></extra>'
        ))

        fig.update_layout(
            title=f"Din prestanda vs genomsnitt inom {omrade_namn}",
            xaxis_title="Godkännandegrad (%)",
            yaxis_title="",
            height=250,
            margin=dict(l=250, r=50, t=60, b=50),
            xaxis=dict(range=[0, 100]),
            showlegend=False,
            barmode='group'
        )

        return fig, fig  # Returnera samma figur två gånger (används i två kolumner)

    # SCENARIO 2+: Flera områden - visa alla i horizontal bar
    else:
        # Färgkoda baserat på godkännandegrad
        colors = []
        for rate in omrade_df['Godkännandegrad (%)']:
            if rate >= 70:
                colors.append('#10b981')
            elif rate >= 50:
                colors.append('#fbbf24')
            elif rate >= 30:
                colors.append('#f97316')
            else:
                colors.append('#ef4444')

        # För att visa 0%-värden tydligt, sätt textposition baserat på värde
        text_positions = []
        for val in omrade_df['Godkännandegrad (%)']:
            if val == 0:
                text_positions.append('outside')  # Visa text utanför för 0%
            else:
                text_positions.append('auto')

        fig = go.Figure(go.Bar(
            x=omrade_df['Godkännandegrad (%)'],
            y=omrade_df['Utbildningsområde'],
            orientation='h',
            text=omrade_df['Godkännandegrad (%)'].apply(lambda x: f"{x}%"),
            textposition=text_positions,
            marker=dict(color=colors),
            hovertemplate='<b>%{y}</b><br>Godkänd: %{x}%<br>Ansökningar: %{customdata[0]}<br>Beviljade: %{customdata[1]}<extra></extra>',
            customdata=omrade_df[['Ansökningar', 'Beviljade']]
        ))

        # Justera höjd baserat på antal områden
        num_areas = len(omrade_df)
        if num_areas <= 3:
            height = 250
            font_size = 14
        else:
            height = 250 + (num_areas - 3) * 40
            font_size = 12

        fig.update_layout(
            title="Godkännandegrad per utbildningsområde",
            xaxis_title="Godkännandegrad (%)",
            yaxis_title="",
            height=height,
            margin=dict(l=250, r=50, t=60, b=50),
            xaxis=dict(range=[-5, 100]),  # Utöka range lite till vänster för 0%-text
            yaxis=dict(
                tickfont=dict(size=font_size),
                automargin=True  # Automatisk marginal
            ),
            bargap=0.15,  # Minska gap mellan staplar (default 0.2)
            plot_bgcolor='white',  # Vit bakgrund
            paper_bgcolor='white'  # Vit paper bakgrund
        )

        return fig, fig  # Returnera samma figur två gånger

# ===== FILTER LOGIC =====
def filter_data(data, year_filter, type_filter, anordnare_filter):
    """Filtrera data baserat på år, typ och anordnare"""
    filtered = data.copy()

    # Filtrera på år
    if year_filter != "Alla":
        filtered = filtered[filtered['År'] == int(year_filter)]

    # Filtrera på typ
    if type_filter != "Alla":
        filtered = filtered[filtered['Typ'] == type_filter]

    # Filtrera på anordnare
    if anordnare_filter != "Alla":
        filtered = filtered[filtered['Anordnare namn'] == anordnare_filter]

    return filtered

# ===== CALLBACK =====
def update_dashboard(state):
    """Uppdatera alla KPIs och visualiseringar när filter ändras"""

    # Filtrera data (alla filter)
    filtered_df = filter_data(state.df, state.selected_year, state.selected_type, state.selected_anordnare)

    # Filtrera data UTAN anordnare (för fördjupad analys)
    filtered_without_anordnare = filter_data(state.df, state.selected_year, state.selected_type, "Alla")

    # Beräkna KPIs (med alla filter)
    state.total_ansokningar, state.antal_beviljade, state.godkand_procent, state.total_platser = calculate_kpis(filtered_df)

    # Uppdatera visualiseringar (med alla filter)
    state.bar_chart = create_bar_chart(filtered_df)
    state.pie_chart = create_pie_chart(filtered_df)

    # Uppdatera "Fördjupad analys" grafer (UTAN anordnare-filter för bättre översikt)
    state.stacked_bar_chart = create_stacked_bar_chart(filtered_without_anordnare)
    state.beslut_bar_chart = create_beslut_bar_chart(filtered_without_anordnare)

    # Uppdatera karta med filtrerad data (med alla filter)
    state.map_chart = create_map(filtered_df)

    # Notifiera användaren
    notify(state, "success", f"Filtrerat: {state.total_ansokningar} ansökningar")

def update_anordnare_insights(state):
    """Uppdatera anordnare-insikter när filter ändras"""

    anordnare_name = state.selected_anordnare_insight
    year_filter = state.selected_year_insight

    # Om "Alla" är valt, välj första riktiga anordnaren istället
    if anordnare_name == "Alla":
        state.anordnare_summary_text = "Välj en anordnare för att se insikter"
        state.anordnare_total_ansokningar = 0
        state.anordnare_beviljade = 0
        state.anordnare_godkand_procent = 0
        state.anordnare_platser = 0
        state.ranking_text = ""

        # Skapa tomma figurer
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

    # Filtrera data baserat på år
    if year_filter == "Alla":
        filtered_data = state.df
    else:
        filtered_data = state.df[state.df['År'] == int(year_filter)]

    # Hämta data för vald anordnare
    anordnare_data = filtered_data[filtered_data['Anordnare namn'] == anordnare_name]

    # Beräkna KPIs för anordnaren
    state.anordnare_total_ansokningar = len(anordnare_data)
    state.anordnare_beviljade = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
    state.anordnare_godkand_procent = round((state.anordnare_beviljade / state.anordnare_total_ansokningar * 100), 1) if state.anordnare_total_ansokningar > 0 else 0

    # Beräkna totala platser
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

    # Skapa sammanfattningstext
    year_text = f"under {year_filter}" if year_filter != "Alla" else "totalt (alla år)"
    state.anordnare_summary_text = f"{anordnare_name} har {state.anordnare_total_ansokningar} ansökningar {year_text}, varav {state.anordnare_beviljade} beviljades ({state.anordnare_godkand_procent}%)"

    # Skapa ranking text
    # Beräkna position bland alla anordnare
    all_anordnare_stats = []
    for other_anordnare in filtered_data['Anordnare namn'].unique():
        if pd.isna(other_anordnare):
            continue
        other_data = filtered_data[filtered_data['Anordnare namn'] == other_anordnare]
        total = len(other_data)
        if total < 5:  # Minst 5 ansökningar för att räknas
            continue
        beviljade = len(other_data[other_data['Beslut'] == 'Beviljad'])
        godkand = round((beviljade / total * 100), 1) if total > 0 else 0
        all_anordnare_stats.append({'Anordnare': other_anordnare, 'Godkännandegrad': godkand})

    ranking_df = pd.DataFrame(all_anordnare_stats).sort_values('Godkännandegrad', ascending=False).reset_index(drop=True)

    if anordnare_name in ranking_df['Anordnare'].values:
        position = ranking_df[ranking_df['Anordnare'] == anordnare_name].index[0] + 1
        total_competitors = len(ranking_df)
        state.ranking_text = f"Du rankas #{position} av {total_competitors} anordnare (med minst 5 ansökningar)"
    else:
        state.ranking_text = "För få ansökningar för att rankas (minst 5 krävs)"

    # Uppdatera grafer
    state.godkannande_comparison_chart = create_godkannande_comparison_chart(filtered_data, anordnare_name)
    state.ranking_chart = create_ranking_chart(filtered_data, anordnare_name)
    state.styrkor_chart, state.svagheter_chart = create_styrkor_svagheter_charts(filtered_data, anordnare_name)

    notify(state, "success", f"Insikter uppdaterade för {anordnare_name}")

# ===== GLOBAL VARIABLES =====
df = load_all_data()

# Filter-alternativ
years = ["Alla", "2024", "2023", "2022"]
types = ["Alla", "Kurs", "Program"]
anordnare = ["Alla"] + sorted([x for x in df['Anordnare namn'].unique() if pd.notna(x)])

# Initiala filter-värden
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

try:
    df_stud = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    df_stud_filtered = df_stud[
        (df_stud['kön'] == 'totalt') &
        (df_stud['tabellinnehåll'] == 'Antal studerande') &
        (df_stud['ålder'] == 'totalt')
    ].copy()

    omrade_list = sorted([x for x in df_stud_filtered['utbildningens inriktning'].unique() if x != 'Totalt'])
    selected_omrade = "Data/It"

except Exception as e:
    print(f"❌ Kunde inte ladda studerande-data: {e}")
    omrade_list = ["Data/It"]
    selected_omrade = "Data/It"
    df_stud_filtered = pd.DataFrame()

def create_studerande_chart(omrade):
    """Skapa line chart för antal studerande över tid"""
    if df_stud_filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Ingen data tillgänglig",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    data_omrade = df_stud_filtered[df_stud_filtered['utbildningens inriktning'] == omrade].copy()
    data_omrade['år'] = data_omrade['år'].astype(int)
    data_omrade = data_omrade.sort_values('år')

    fig = px.line(
        data_omrade,
        x='år',
        y='Studerande och examinerade inom yrkeshögskolan',
        title=f'Totalt antal aktiva studenter inom {omrade} (2005-2024)',
        labels={
            'år': 'År',
            'Studerande och examinerade inom yrkeshögskolan': 'Antal aktiva studenter'
        }
    )

    fig.update_traces(line=dict(width=3, color='#4361ee'), mode='lines+markers')
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=2)
    )

    return fig

def create_studerande_table(omrade):
    """Skapa tabell med studerande-data"""

    if df_stud_filtered.empty:
        return pd.DataFrame({'Meddelande': ['Ingen data tillgänglig']})

    # Filtrera på valt område
    data_omrade = df_stud_filtered[df_stud_filtered['utbildningens inriktning'] == omrade].copy()

    # Välj relevanta kolumner och döp om
    table_data = data_omrade[['år', 'Studerande och examinerade inom yrkeshögskolan']].copy()
    table_data.columns = ['År', 'Antal aktiva studenter']
    table_data = table_data.sort_values('År', ascending=False)

    return table_data

# Funktion för att skapa examinerade-chart
def create_examinerade_chart(omrade):
    """Skapa line chart för antal examinerade studenter över tid"""

    if df_stud_filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Ingen data tillgänglig",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Läs hela datasetet igen för examinerade
    df_exam = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    # Filtrera på "Antal examinerade"
    data_exam = df_exam[
        (df_exam['kön'] == 'totalt') &
        (df_exam['utbildningens inriktning'] == omrade) &
        (df_exam['tabellinnehåll'] == 'Antal examinerade') &
        (df_exam['ålder'] == 'totalt')
    ].copy()

    # Konvertera år till int och sortera
    data_exam['år'] = data_exam['år'].astype(int)
    data_exam = data_exam.sort_values('år')

    # Filtrera bort rader med ".." (ingen data)
    data_exam = data_exam[data_exam['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_exam['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_exam['Studerande och examinerade inom yrkeshögskolan']
    )

    # Skapa line chart
    fig = px.line(
        data_exam,
        x='år',
        y='Studerande och examinerade inom yrkeshögskolan',
        title=f'Antal examinerade studenter inom {omrade} (2007-2024)',
        labels={
            'år': 'År',
            'Studerande och examinerade inom yrkeshögskolan': 'Antal examinerade'
        }
    )

    # Styling - grön färg för examinerade
    fig.update_traces(line=dict(width=3, color='#28a745'), mode='lines+markers')
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=2)
    )

    return fig

# Funktion för att skapa jämförelsechart
def create_comparison_chart(omrade):
    """Skapa jämförelsechart med både aktiva studenter och examinerade"""

    if df_stud_filtered.empty:
        fig = go.Figure()
        fig.add_annotation(
            text="Ingen data tillgänglig",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
        return fig

    # Läs hela datasetet
    df_all = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    # Filtrera på valt område
    data_stud = df_all[
        (df_all['kön'] == 'totalt') &
        (df_all['utbildningens inriktning'] == omrade) &
        (df_all['tabellinnehåll'] == 'Antal studerande') &
        (df_all['ålder'] == 'totalt')
    ].copy()

    data_exam = df_all[
        (df_all['kön'] == 'totalt') &
        (df_all['utbildningens inriktning'] == omrade) &
        (df_all['tabellinnehåll'] == 'Antal examinerade') &
        (df_all['ålder'] == 'totalt')
    ].copy()

    # Konvertera och rensa data
    data_stud['år'] = data_stud['år'].astype(int)
    data_exam['år'] = data_exam['år'].astype(int)

    data_exam = data_exam[data_exam['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_exam['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_exam['Studerande och examinerade inom yrkeshögskolan']
    )

    # Skapa figur med två linjer
    fig = go.Figure()

    # Lägg till linje för aktiva studenter
    fig.add_trace(go.Scatter(
        x=data_stud['år'],
        y=data_stud['Studerande och examinerade inom yrkeshögskolan'],
        mode='lines+markers',
        name='Aktiva studenter',
        line=dict(width=3, color='#4361ee'),
        hovertemplate='<b>Aktiva studenter</b><br>År: %{x}<br>Antal: %{y}<extra></extra>'
    ))

    # Lägg till linje för examinerade
    fig.add_trace(go.Scatter(
        x=data_exam['år'],
        y=data_exam['Studerande och examinerade inom yrkeshögskolan'],
        mode='lines+markers',
        name='Examinerade',
        line=dict(width=3, color='#28a745'),
        hovertemplate='<b>Examinerade</b><br>År: %{x}<br>Antal: %{y}<extra></extra>'
    ))

    # Layout
    fig.update_layout(
        title=f'Aktiva studenter vs Examinerade inom {omrade} (2005-2024)',
        xaxis_title='År',
        yaxis_title='Antal',
        height=500,
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=2),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    return fig

# Funktion för att beräkna examensgrad för alla områden
def calculate_examensgrad_all():
    """Beräkna examensgrad för alla utbildningsområden (2024)"""

    if df_stud_filtered.empty:
        return pd.DataFrame()

    # Läs hela datasetet
    df_all = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    # Filtrera på år 2024
    df_2024 = df_all[
        (df_all['år'] == 2024) &
        (df_all['kön'] == 'totalt') &
        (df_all['ålder'] == 'totalt')
    ].copy()

    # Separera aktiva studenter och examinerade
    aktiva = df_2024[df_2024['tabellinnehåll'] == 'Antal studerande'].set_index('utbildningens inriktning')
    examinerade = df_2024[df_2024['tabellinnehåll'] == 'Antal examinerade'].set_index('utbildningens inriktning')

    # Beräkna examensgrad
    result = []
    for omrade in aktiva.index:
        if omrade == 'Totalt':
            continue

        # Slå ihop de två pedagogik-kategorierna
        if omrade in ['Pedagogik och lärarutbildning', 'Pedagogik och undervisning']:
            # Skippa en av dem, vi hanterar dem tillsammans senare
            continue

        # Hämta värden och konvertera till skalär (första värdet om det är en Series)
        aktiva_val = aktiva.loc[omrade, 'Studerande och examinerade inom yrkeshögskolan']
        if isinstance(aktiva_val, pd.Series):
            aktiva_val = aktiva_val.iloc[0]

        if omrade in examinerade.index:
            exam_val = examinerade.loc[omrade, 'Studerande och examinerade inom yrkeshögskolan']
            if isinstance(exam_val, pd.Series):
                exam_val = exam_val.iloc[0]

            # Hantera ".." värden
            if exam_val != '..' and aktiva_val != '..':
                exam_antal = float(exam_val)
                aktiva_antal = float(aktiva_val)

                examensgrad = (exam_antal / aktiva_antal) * 100

                result.append({
                    'Utbildningsområde': omrade,
                    'Aktiva studenter': int(aktiva_antal),
                    'Examinerade': int(exam_antal),
                    'Examensgrad (%)': round(examensgrad, 1)
                })

    # Lägg till sammanslagna pedagogik-data
    if 'Pedagogik och lärarutbildning' in aktiva.index:
        ped_aktiva = aktiva.loc['Pedagogik och lärarutbildning', 'Studerande och examinerade inom yrkeshögskolan']
        if isinstance(ped_aktiva, pd.Series):
            ped_aktiva = ped_aktiva.iloc[0]

        if 'Pedagogik och lärarutbildning' in examinerade.index:
            ped_exam = examinerade.loc['Pedagogik och lärarutbildning', 'Studerande och examinerade inom yrkeshögskolan']
            if isinstance(ped_exam, pd.Series):
                ped_exam = ped_exam.iloc[0]

            if ped_exam != '..' and ped_aktiva != '..':
                ped_examensgrad = (float(ped_exam) / float(ped_aktiva)) * 100
                result.append({
                    'Utbildningsområde': 'Pedagogik',
                    'Aktiva studenter': int(float(ped_aktiva)),
                    'Examinerade': int(float(ped_exam)),
                    'Examensgrad (%)': round(ped_examensgrad, 1)
                })

    df_result = pd.DataFrame(result)
    df_result = df_result.sort_values('Examensgrad (%)', ascending=False)

    return df_result

# Funktion för att hämta top 5 examensgrad
def get_examensgrad_top5():
    """Hämta top 5 områden med högst examensgrad"""
    df_all = calculate_examensgrad_all()

    if df_all.empty:
        return pd.DataFrame({'Meddelande': ['Ingen data tillgänglig']})

    return df_all.head(5)

# Funktion för att hämta examensgrad för valt område
def get_examensgrad_selected(omrade):
    """Hämta examensgrad för valt område"""
    df_all = calculate_examensgrad_all()

    if df_all.empty:
        return "N/A"

    row = df_all[df_all['Utbildningsområde'] == omrade]

    if row.empty:
        return "N/A"

    return f"{row['Examensgrad (%)'].values[0]}"

# Callback för att uppdatera studerande-visualiseringar
def update_studerande(state):
    """Uppdatera alla studerande-charts och tabell när område ändras"""
    state.studerande_chart = create_studerande_chart(state.selected_omrade)
    state.examinerade_chart = create_examinerade_chart(state.selected_omrade)
    state.comparison_chart = create_comparison_chart(state.selected_omrade)
    state.studerande_table = create_studerande_table(state.selected_omrade)
    state.examensgrad_selected = get_examensgrad_selected(state.selected_omrade)
    # examensgrad_top5 ändras inte vid områdespval, så vi behöver inte uppdatera den

# Initialisera studerande-visualiseringar
studerande_chart = create_studerande_chart(selected_omrade)
examinerade_chart = create_examinerade_chart(selected_omrade)
comparison_chart = create_comparison_chart(selected_omrade)
studerande_table = create_studerande_table(selected_omrade)
examensgrad_top5 = get_examensgrad_top5()
examensgrad_selected = get_examensgrad_selected(selected_omrade)

from insikter_page import insikter_page
from storytelling_page import storytelling_page
from studerande_page import studerande_page

pages = {
    "home": oversikt_page,
    "Karta": karta_page,
    "Insikter": insikter_page,
    "Storytelling": storytelling_page,
    "Studerande": studerande_page
}

# ===== START APP =====
if __name__ == "__main__":
    Gui(pages=pages, css_file="assets/main.css").run(
        port=5005,
        debug=True,
        dark_mode=False,
        title="YH-kollen"
    )
