import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def create_bar_chart(data):
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

    colors = []
    for beslut in beslut_counts['Beslut']:
        if beslut == 'Beviljad':
            colors.append('#10b981')
        else:
            colors.append('#ef4444')

    fig = go.Figure(data=[go.Pie(
        labels=beslut_counts['Beslut'],
        values=beslut_counts['Antal'],
        hole=0.3,
        marker=dict(colors=colors),
        textposition='inside',
        textinfo='percent+label'
    )])

    fig.update_layout(
        title="Fördelning: Beviljad vs Avslag",
        height=500,
        showlegend=True,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig

def create_stacked_bar_chart(data):
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

def create_godkannande_comparison_chart(data, anordnare_name):
    total_all = len(data)
    beviljade_all = len(data[data['Beslut'] == 'Beviljad'])
    avg_godkand = round((beviljade_all / total_all * 100), 1) if total_all > 0 else 0

    anordnare_data = data[data['Anordnare namn'] == anordnare_name]
    total_anordnare = len(anordnare_data)
    beviljade_anordnare = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
    anordnare_godkand = round((beviljade_anordnare / total_anordnare * 100), 1) if total_anordnare > 0 else 0

    comparison_df = pd.DataFrame({
        'Kategori': ['Genomsnitt alla anordnare', anordnare_name],
        'Godkännandegrad (%)': [avg_godkand, anordnare_godkand]
    })

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
        height=450,
        showlegend=False,
        margin=dict(l=50, r=50, t=20, b=100),
        xaxis=dict(tickangle=-15),
        yaxis=dict(range=[0, 100]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.3
    )

    return fig

def create_ranking_chart(data, anordnare_name):
    anordnare_stats = []

    for anordnare in data['Anordnare namn'].unique():
        if pd.isna(anordnare):
            continue

        anordnare_data = data[data['Anordnare namn'] == anordnare]
        total = len(anordnare_data)

        if total < 5:
            continue

        beviljade = len(anordnare_data[anordnare_data['Beslut'] == 'Beviljad'])
        godkand_procent = round((beviljade / total * 100), 1) if total > 0 else 0

        anordnare_stats.append({
            'Anordnare': anordnare,
            'Godkännandegrad (%)': godkand_procent,
            'Ansökningar': total
        })

    all_ranking_df = pd.DataFrame(anordnare_stats).sort_values('Godkännandegrad (%)', ascending=False)

    top_10 = all_ranking_df.head(10)

    if anordnare_name not in top_10['Anordnare'].values:
        selected_row = all_ranking_df[all_ranking_df['Anordnare'] == anordnare_name].copy()
        if len(selected_row) > 0:
            gap_row = pd.DataFrame({
                'Anordnare': ['...'],
                'Godkännandegrad (%)': [0],
                'Ansökningar': [0]
            })
            ranking_df = pd.concat([top_10.head(9), gap_row, selected_row]).reset_index(drop=True)
        else:
            ranking_df = top_10
    else:
        ranking_df = top_10

    colors = []
    for x in ranking_df['Anordnare']:
        if x == anordnare_name:
            colors.append('#3b82f6')
        elif x == '...':
            colors.append('#e5e7eb')
        else:
            colors.append('#94a3b8')

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

    fig.update_traces(textposition='outside', cliponaxis=False)

    fig.update_layout(
        height=450,
        showlegend=False,
        margin=dict(l=50, r=50, t=80, b=150),
        xaxis=dict(tickangle=-45),
        yaxis=dict(range=[0, 108]),
        plot_bgcolor='white',
        paper_bgcolor='white',
        bargap=0.15
    )

    return fig

def create_styrkor_svagheter_charts(data, anordnare_name):
    anordnare_data = data[data['Anordnare namn'] == anordnare_name]

    omrade_stats = []

    for omrade in anordnare_data['Utbildningsområde'].unique():
        if pd.isna(omrade):
            continue

        omrade_data = anordnare_data[anordnare_data['Utbildningsområde'] == omrade]
        total = len(omrade_data)

        beviljade = len(omrade_data[omrade_data['Beslut'] == 'Beviljad'])
        godkand_procent = round((beviljade / total * 100), 1) if total > 0 else 0

        omrade_stats.append({
            'Utbildningsområde': omrade,
            'Godkännandegrad (%)': godkand_procent,
            'Ansökningar': total,
            'Beviljade': beviljade
        })

    if len(omrade_stats) == 0:
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

    if len(omrade_df) == 1:
        row = omrade_df.iloc[0]
        omrade_namn = row['Utbildningsområde']
        anordnare_rate = row['Godkännandegrad (%)']

        omrade_all_data = data[data['Utbildningsområde'] == omrade_namn]
        total_omrade = len(omrade_all_data)
        beviljade_omrade = len(omrade_all_data[omrade_all_data['Beslut'] == 'Beviljad'])
        omrade_avg = round((beviljade_omrade / total_omrade * 100), 1) if total_omrade > 0 else 0

        if anordnare_rate >= 70:
            color = '#10b981'
        elif anordnare_rate >= 50:
            color = '#fbbf24'
        elif anordnare_rate >= 30:
            color = '#f97316'
        else:
            color = '#ef4444'

        fig = go.Figure()

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

        fig.add_trace(go.Bar(
            x=[anordnare_rate],
            y=[anordnare_name],
            orientation='h',
            text=[f"{anordnare_rate}%"],
            textposition='auto',
            marker=dict(color=color),
            name=f'{anordnare_name}',
            hovertemplate=f'<b>{anordnare_name}</b><br>Godkänd: {anordnare_rate}%<br>Ansökningar: {row["Ansökningar"]}<br>Beviljade: {row["Beviljade"]}<extra></extra>'
        ))

        fig.update_layout(
            title=f"{anordnare_name} vs genomsnitt inom {omrade_namn}",
            xaxis_title="Godkännandegrad (%)",
            yaxis_title="",
            height=250,
            margin=dict(l=250, r=50, t=60, b=50),
            xaxis=dict(range=[0, 100]),
            showlegend=False,
            barmode='group'
        )

        return fig, fig

    else:
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

        text_positions = []
        for val in omrade_df['Godkännandegrad (%)']:
            if val == 0:
                text_positions.append('outside')
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

        num_areas = len(omrade_df)
        if num_areas <= 3:
            height = 250
            font_size = 14
        else:
            height = 250 + (num_areas - 3) * 40
            font_size = 12

        fig.update_layout(
            title=f"{anordnare_name}s godkännandegrad per utbildningsområde",
            xaxis_title="Godkännandegrad (%)",
            yaxis_title="",
            height=height,
            margin=dict(l=250, r=50, t=60, b=50),
            xaxis=dict(range=[-5, 100]),
            yaxis=dict(
                tickfont=dict(size=font_size),
                automargin=True
            ),
            bargap=0.15,
            plot_bgcolor='white',
            paper_bgcolor='white'
        )

        return fig, fig

def create_studerande_chart(omrade, df_stud_filtered):
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

    # Remove ".." values and convert to numeric
    data_omrade = data_omrade[data_omrade['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_omrade['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_omrade['Studerande och examinerade inom yrkeshögskolan']
    )

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

def create_examinerade_chart(omrade):
    df_exam = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    data_exam = df_exam[
        (df_exam['kön'] == 'totalt') &
        (df_exam['utbildningens inriktning'] == omrade) &
        (df_exam['tabellinnehåll'] == 'Antal examinerade') &
        (df_exam['ålder'] == 'totalt')
    ].copy()

    data_exam['år'] = data_exam['år'].astype(int)
    data_exam = data_exam.sort_values('år')

    data_exam = data_exam[data_exam['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_exam['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_exam['Studerande och examinerade inom yrkeshögskolan']
    )

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

    fig.update_traces(line=dict(width=3, color='#28a745'), mode='lines+markers')
    fig.update_layout(
        height=500,
        hovermode='x unified',
        xaxis=dict(tickmode='linear', dtick=2)
    )

    return fig

def create_comparison_chart(omrade):
    df_all = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

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

    data_stud['år'] = data_stud['år'].astype(int)
    data_exam['år'] = data_exam['år'].astype(int)

    data_stud = data_stud[data_stud['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_stud['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_stud['Studerande och examinerade inom yrkeshögskolan']
    )

    data_exam = data_exam[data_exam['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_exam['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_exam['Studerande och examinerade inom yrkeshögskolan']
    )

    merged = pd.merge(
        data_stud[['år', 'Studerande och examinerade inom yrkeshögskolan']],
        data_exam[['år', 'Studerande och examinerade inom yrkeshögskolan']],
        on='år',
        suffixes=('_stud', '_exam')
    )

    merged['examensgrad'] = (merged['Studerande och examinerade inom yrkeshögskolan_exam'] /
                              merged['Studerande och examinerade inom yrkeshögskolan_stud'] * 100).round(1)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data_stud['år'],
        y=data_stud['Studerande och examinerade inom yrkeshögskolan'],
        mode='lines+markers',
        name='Aktiva studenter',
        line=dict(width=3, color='#4361ee'),
        yaxis='y',
        hovertemplate='<b>Aktiva studenter</b><br>År: %{x}<br>Antal: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=data_exam['år'],
        y=data_exam['Studerande och examinerade inom yrkeshögskolan'],
        mode='lines+markers',
        name='Examinerade',
        line=dict(width=3, color='#10b981'),
        yaxis='y',
        hovertemplate='<b>Examinerade</b><br>År: %{x}<br>Antal: %{y}<extra></extra>'
    ))

    fig.add_trace(go.Scatter(
        x=merged['år'],
        y=merged['examensgrad'],
        mode='lines+markers',
        name='Examensgrad (%)',
        line=dict(width=3, color='#f59e0b', dash='dash'),
        marker=dict(size=8),
        yaxis='y2',
        hovertemplate='<b>Examensgrad</b><br>År: %{x}<br>%{y}%<extra></extra>'
    ))

    fig.update_layout(
        title=f'Aktiva studenter, Examinerade och Examensgrad inom {omrade} (2007-2024)',
        xaxis_title='År',
        yaxis_title='Antal studenter',
        yaxis2=dict(
            title='Examensgrad (%)',
            overlaying='y',
            side='right',
            range=[0, 100]
        ),
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

def create_studerande_table(omrade, df_stud_filtered):
    if df_stud_filtered.empty:
        return pd.DataFrame({'Meddelande': ['Ingen data tillgänglig']})

    data_omrade = df_stud_filtered[df_stud_filtered['utbildningens inriktning'] == omrade].copy()

    # Remove ".." values and convert to numeric
    data_omrade = data_omrade[data_omrade['Studerande och examinerade inom yrkeshögskolan'] != '..']
    data_omrade['Studerande och examinerade inom yrkeshögskolan'] = pd.to_numeric(
        data_omrade['Studerande och examinerade inom yrkeshögskolan']
    )

    table_data = data_omrade[['år', 'Studerande och examinerade inom yrkeshögskolan']].copy()
    table_data.columns = ['År', 'Antal aktiva studenter']
    table_data = table_data.sort_values('År', ascending=False)

    return table_data
