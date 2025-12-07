"""
YH-kollen - Kartsida
Geografisk karta över beviljade ansökningar per län
"""

import pandas as pd
import plotly.graph_objects as go
import numpy as np
import json
from difflib import get_close_matches

# ===== LADDA GEOJSON =====
def load_geojson():
    """Ladda GeoJSON för svenska län"""
    with open("assets/swedish_regions.geojson", "r", encoding="utf-8") as file:
        return json.load(file)

# ===== SKAPA KARTA =====
def create_map(data):
    """Skapa choropleth map över beviljade ansökningar per län"""
    geojson = load_geojson()

    filtered = data[data['Län'].notna()].copy()
    filtered = filtered[filtered['Län'] != 'Se "Lista flera kommuner"']

    total_ansokningar = len(filtered)
    beviljade_total = len(filtered[filtered['Beslut'] == 'Beviljad'])

    properties = [feature["properties"] for feature in geojson["features"]]
    region_codes = {
        prop["name"]: prop["ref:se:länskod"] for prop in properties
    }

    all_lan = pd.DataFrame({
        'Län': list(region_codes.keys()),
        'Länskod': list(region_codes.values()),
        'Beviljade': 0
    })

    lan_counts = filtered[filtered['Beslut'] == 'Beviljad'].groupby('Län').size().reset_index(name='Beviljade')

    for _, row in lan_counts.iterrows():
        lan_name = row['Län']
        matches = get_close_matches(lan_name, region_codes.keys(), n=1, cutoff=0.6)
        if matches:
            matched_lan = matches[0]
            all_lan.loc[all_lan['Län'] == matched_lan, 'Beviljade'] = row['Beviljade']

    lan_data = all_lan
    log_beviljade = np.log1p(lan_data['Beviljade'])

    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson,
            locations=lan_data['Länskod'].tolist(),
            z=log_beviljade,
            featureidkey="properties.ref:se:länskod",
            colorscale="Blues",
            marker_opacity=0.9,
            marker_line_width=0.4,
            text=lan_data['Län'],
            customdata=lan_data['Beviljade'],
            hovertemplate="<b>%{text}</b><br>Beviljade: %{customdata}<extra></extra>",
            showscale=False,
        )
    )

    godkand_procent = round((beviljade_total / total_ansokningar * 100), 1) if total_ansokningar > 0 else 0

    fig.update_layout(
        title=dict(
            text=f"<br>Beviljade ansökningar per län<br>Ju mörkare färg, desto fler beviljade<br><b>{beviljade_total}</b> av <b>{total_ansokningar}</b> beviljade ({godkand_procent}%)",
            x=0.05,
            y=0.95,
            font=dict(size=13),
        ),
        mapbox=dict(
            style="white-bg",
            zoom=3.6,
            center=dict(lat=62.5, lon=15.5)
        ),
        margin=dict(r=0, t=80, l=0, b=0),
        height=600,
        autosize=True,
        dragmode=False
    )

    return fig
