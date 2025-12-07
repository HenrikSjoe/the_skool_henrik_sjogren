"""
Data Storytelling för YH-kollen Presentation
=============================================
Strategiska visualiseringar för The Skool - fokus på Data/IT
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Konfigurera matplotlib för svenska tecken och professionell stil
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")

# ===== DATA LOADING =====
def load_all_data():
    """Ladda kurser och program från alla tillgängliga år"""
    all_dfs = []

    # KURSER 2023 och 2024
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
            print(f"⚠️ Kunde inte ladda Kurser {year}: {e}")

    # PROGRAM 2022, 2023, 2024
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
            print(f"⚠️ Kunde inte ladda Program {year}: {e}")

    combined = pd.concat(all_dfs, ignore_index=True)
    print(f"✅ Laddade {len(combined)} ansökningar totalt")
    return combined


# ===== STORYTELLING 1: GODKÄNNANDEGRAD PER OMRÅDE =====
def create_storytelling_approval_by_area(df, save_path="outputs/storytelling_1_approval_by_area.png"):
    """
    STORYTELLING 1: Varför är det så svårt att få beviljat inom Data/IT?
    Visa godkännandegrad per utbildningsområde
    """

    # Beräkna godkännandegrad per område
    approval_by_area = df.groupby('Utbildningsområde').apply(
        lambda x: pd.Series({
            'Totalt': len(x),
            'Godkännandegrad': (x['Beslut'] == 'Beviljad').sum() / len(x) * 100
        }),
        include_groups=False
    )

    # Filtrera bort områden med för få ansökningar (< 30)
    approval_by_area = approval_by_area[approval_by_area['Totalt'] >= 30]
    approval_by_area_sorted = approval_by_area.sort_values('Godkännandegrad', ascending=True)

    # Ta bottom 5 (inkl Data/IT) och top 5 för kontrast
    bottom_5 = approval_by_area_sorted.head(5)
    top_5 = approval_by_area_sorted.tail(5)
    approval_by_area = pd.concat([bottom_5, top_5])

    # Skapa figur
    fig, ax = plt.subplots(figsize=(14, 8))

    # Färgkodning: Röd för bottom 5 (svårast), grön för top 5 (lättast)
    colors = ['#dc3545'] * 5 + ['#28a745'] * 5

    bars = ax.barh(range(len(approval_by_area)), approval_by_area['Godkännandegrad'].values, color=colors)

    # Lägg till procentvärden på staplarna
    for i, (value, bar) in enumerate(zip(approval_by_area['Godkännandegrad'].values, bars)):
        ax.text(value + 1, i, f'{value:.1f}%',
                va='center', fontsize=11, fontweight='bold')

    # Formatera y-axel
    ax.set_yticks(range(len(approval_by_area)))
    ax.set_yticklabels(approval_by_area.index, fontsize=11)

    # Titlar och labels
    ax.set_xlabel('Godkännandegrad (%)', fontsize=12, fontweight='bold')
    ax.set_title('Varför är Data/IT så svårt?\nGodkännandegrad per utbildningsområde 2022-2024',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 65)

    # ANNOTATION - pekar på Data/IT
    datait_idx = list(approval_by_area.index).index('Data/IT')
    datait_value = approval_by_area.loc['Data/IT', 'Godkännandegrad']

    # Räkna totalt antal ansökningar för Data/IT
    datait_total = df[df['Utbildningsområde'] == 'Data/IT'].shape[0]

    annotation_text = f"Data/IT: Bara {datait_value:.0f}% godkänt\n#1 mest sökta: {datait_total} ansökningar!"

    ax.annotate(annotation_text,
                xy=(datait_value, datait_idx),
                xytext=(datait_value + 15, datait_idx + 1.5),
                fontsize=11,
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#ffe6e6', edgecolor='#dc3545', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#dc3545', lw=2.5, connectionstyle='arc3,rad=0.3'))

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()

    # Spara figur
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Sparad: {save_path}")
    plt.close()

    return fig


# ===== STORYTELLING 2: DATA/IT TREND ÖVER TID =====
def create_storytelling_datait_trend(df, save_path="outputs/storytelling_2_datait_trend.png"):
    """
    STORYTELLING 2: Blir det lättare eller svårare för Data/IT?
    Visa trend för Data/IT godkännandegrad över tid
    """

    # Filtrera Data/IT
    datait = df[df['Utbildningsområde'] == 'Data/IT']

    # Beräkna godkännandegrad per år
    datait_by_year = datait.groupby('År').apply(
        lambda x: pd.Series({
            'Ansökningar': len(x),
            'Beviljade': (x['Beslut'] == 'Beviljad').sum(),
            'Godkännandegrad': (x['Beslut'] == 'Beviljad').sum() / len(x) * 100
        }),
        include_groups=False
    ).reset_index()

    # Skapa figur
    fig, ax = plt.subplots(figsize=(14, 8))

    # Line chart med markers
    ax.plot(datait_by_year['År'], datait_by_year['Godkännandegrad'],
            marker='o', linewidth=3, markersize=14, color='#dc3545')

    # Lägg till värden på punkterna
    for x, y in zip(datait_by_year['År'], datait_by_year['Godkännandegrad']):
        ax.text(x, y - 3, f'{y:.1f}%', ha='center', fontsize=12, fontweight='bold')

    # Lägg till antal ansökningar under varje punkt
    for x, y, count in zip(datait_by_year['År'], datait_by_year['Godkännandegrad'], datait_by_year['Ansökningar']):
        ax.text(x, 5, f'{int(count)} ansökn.', ha='center', fontsize=10, style='italic', color='#666')

    ax.set_xlabel('År', fontsize=12, fontweight='bold')
    ax.set_ylabel('Godkännandegrad (%)', fontsize=12, fontweight='bold')
    ax.set_title('Data/IT: Blir det lättare att få beviljat?\nGodkännandegrad för Data/IT-ansökningar över tid',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 40)
    ax.set_xticks(datait_by_year['År'].unique())
    ax.grid(True, alpha=0.3, linestyle='--')

    # ANNOTATION - pekar på 2023 (toppen)
    best_year_idx = datait_by_year['Godkännandegrad'].idxmax()
    best_year = datait_by_year.loc[best_year_idx, 'År']
    best_value = datait_by_year.loc[best_year_idx, 'Godkännandegrad']

    annotation_text = f"2023: Bästa chansen!\n{best_value:.1f}% godkänt"

    ax.annotate(annotation_text,
                xy=(best_year, best_value),
                xytext=(best_year + 0.3, best_value + 5),
                fontsize=11,
                bbox=dict(boxstyle='round,pad=0.6', facecolor='#e6ffe6', edgecolor='#28a745', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#28a745', lw=2.5, connectionstyle='arc3,rad=0.2'))

    plt.tight_layout()

    # Spara figur
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Sparad: {save_path}")
    plt.close()

    return fig


# ===== STORYTELLING 3: GODKÄNNANDEGRAD PER LÄN =====
def create_storytelling_geographic_opportunity(df, save_path="outputs/storytelling_3_geographic_opportunity.png"):
    """
    STORYTELLING 3: Var är det lättast att få beviljat?
    Visa godkännandegrad per län (Beviljade/Totalt ansökningar)
    """

    # Filtrera bort 'Flera kommuner'
    df_clean = df[~df['Län'].str.contains('Flera|Lista', na=False, case=False)]

    # Beräkna godkännandegrad per län
    lan_stats = df_clean.groupby('Län').apply(
        lambda x: pd.Series({
            'Totalt': len(x),
            'Beviljade': (x['Beslut'] == 'Beviljad').sum(),
            'Godkännandegrad': (x['Beslut'] == 'Beviljad').sum() / len(x) * 100
        }),
        include_groups=False
    )

    # Filtrera på minst 30 ansökningar för statistisk relevans
    lan_stats = lan_stats[lan_stats['Totalt'] >= 30]
    lan_stats_sorted = lan_stats.sort_values('Godkännandegrad', ascending=True)

    # Ta bottom 5 (svårast) och top 5 (lättast)
    bottom_5 = lan_stats_sorted.head(5)
    top_5 = lan_stats_sorted.tail(5)
    combined = pd.concat([bottom_5, top_5])

    # Skapa figur
    fig, ax = plt.subplots(figsize=(14, 8))

    # Färgkodning: Röd för svårast (bottom 5), grön för lättast (top 5)
    colors = ['#dc3545'] * 5 + ['#28a745'] * 5

    bars = ax.barh(range(len(combined)), combined['Godkännandegrad'].values, color=colors)

    # Lägg till procentvärden på staplarna
    for i, (value, bar) in enumerate(zip(combined['Godkännandegrad'].values, bars)):
        ax.text(value + 1, i, f'{value:.1f}%',
                va='center', fontsize=11, fontweight='bold')

    # Formatera y-axel
    ax.set_yticks(range(len(combined)))
    ax.set_yticklabels(combined.index, fontsize=11)

    # Titlar och labels
    ax.set_xlabel('Godkännandegrad (%)', fontsize=12, fontweight='bold')
    ax.set_title('Var är det lättast att få beviljat?\nGodkännandegrad per län 2022-2024',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 65)

    # ANNOTATION 1 - pekar på Södermanland (lättast)
    best_lan_idx = list(combined.index).index(top_5.index[-1])
    best_lan = top_5.index[-1]
    best_value = top_5['Godkännandegrad'].values[-1]

    ax.annotate(f"{best_lan}: {best_value:.1f}% godkänt\nLättast att få beviljat!",
                xy=(best_value - 1, best_lan_idx - 0.4),  # Pilspets PERFEKT placerad
                xytext=(48, 6),  # Text högre upp i det vita området
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#e6ffe6', edgecolor='#28a745', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#28a745', lw=2.5, connectionstyle='arc3,rad=0.15'))

    # ANNOTATION 2 - pekar på Halland (svårast)
    worst_lan_idx = list(combined.index).index(bottom_5.index[0])
    worst_lan = bottom_5.index[0]
    worst_value = bottom_5['Godkännandegrad'].values[0]

    ax.annotate(f"{worst_lan}: {worst_value:.1f}% godkänt\nSvårast län",
                xy=(worst_value, worst_lan_idx - 0.3),  # Pilspets lite längre NER från 22.0%
                xytext=(worst_value + 15, worst_lan_idx + 0.6),  # Text NER (inte genom 22.0%)
                fontsize=10,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffe6e6', edgecolor='#dc3545', linewidth=2),
                arrowprops=dict(arrowstyle='->', color='#dc3545', lw=2.5, connectionstyle='arc3,rad=-0.2'))

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()

    # Spara figur
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Sparad: {save_path}")
    plt.close()

    return fig


# ===== STORYTELLING 4: EXAMENSGRAD PER UTBILDNINGSOMRÅDE =====
def create_storytelling_graduation_rate(save_path="outputs/storytelling_4_graduation_rate.png"):
    """
    STORYTELLING 4: Vilka områden har högst examensgrad?
    Visa examensgrad för olika utbildningsområden (2024 data från SCB)
    """

    # Läs SCB-data för studerande och examinerade
    df_scb = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    # Filtrera på år 2024
    df_2024 = df_scb[
        (df_scb['år'] == 2024) &
        (df_scb['kön'] == 'totalt') &
        (df_scb['ålder'] == 'totalt')
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

        # Hämta värden och konvertera till skalär
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
                    'Examensgrad': examensgrad
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
                    'Examensgrad': ped_examensgrad
                })

    df_exam = pd.DataFrame(result)
    df_exam_sorted = df_exam.sort_values('Examensgrad', ascending=True)

    # Beräkna medelvärde för alla områden
    medel_examensgrad = df_exam['Examensgrad'].mean()

    # Ta bottom 5 och top 5
    bottom_5 = df_exam_sorted.head(5)
    top_5 = df_exam_sorted.tail(5)
    combined = pd.concat([bottom_5, top_5])

    # Skapa figur
    fig, ax = plt.subplots(figsize=(14, 9))

    # Färgkodning: Röd för bottom 5 (lägst), grön för top 5 (högst)
    colors = ['#dc3545'] * 5 + ['#28a745'] * 5

    bars = ax.barh(range(len(combined)), combined['Examensgrad'].values, color=colors)

    # Lägg till procentvärden på staplarna
    for i, (value, bar) in enumerate(zip(combined['Examensgrad'].values, bars)):
        ax.text(value + 0.5, i, f'{value:.1f}%',
                va='center', fontsize=11, fontweight='bold')

    # Formatera y-axel
    ax.set_yticks(range(len(combined)))
    ax.set_yticklabels(combined['Utbildningsområde'].values, fontsize=11)

    # Titlar och labels
    ax.set_xlabel('Examensgrad (%)', fontsize=12, fontweight='bold')
    ax.set_title('Vilka utbildningsområden har högst examensgrad?\nTop 5 och Bottom 5 utbildningsområden efter examensgrad 2024',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlim(0, 50)

    # Lägg till vertikal linje för medelvärde
    ax.axvline(x=medel_examensgrad, color='#6c757d', linestyle='--', linewidth=2, alpha=0.7, label=f'Medel: {medel_examensgrad:.1f}%')

    # Legend för medelvärdeslinjen
    ax.legend(loc='lower right', fontsize=11)

    # ANNOTATION - Hitta Data/IT position
    if 'Data/It' in combined['Utbildningsområde'].values:
        datait_idx = list(combined['Utbildningsområde'].values).index('Data/It')
        datait_value = combined[combined['Utbildningsområde'] == 'Data/It']['Examensgrad'].values[0]

        ax.annotate(f"Data/IT: {datait_value:.1f}%\n(Medel: {medel_examensgrad:.1f}%)",
                    xy=(datait_value, datait_idx),
                    xytext=(datait_value + 10, datait_idx - 1.5),
                    fontsize=11,
                    bbox=dict(boxstyle='round,pad=0.6', facecolor='#fff3cd', edgecolor='#ffc107', linewidth=2),
                    arrowprops=dict(arrowstyle='->', color='#ffc107', lw=2.5, connectionstyle='arc3,rad=-0.3'))

    # Grid
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)

    # Använd subplots_adjust för att ge mer utrymme i botten
    plt.subplots_adjust(bottom=0.12)

    # Lägg till textförklaring för färger längst ner
    fig.text(0.12, 0.03, '🔴 Bottom 5: Lägst examensgrad', fontsize=10, color='#dc3545', fontweight='bold')
    fig.text(0.50, 0.03, '🟢 Top 5: Högst examensgrad', fontsize=10, color='#28a745', fontweight='bold')

    # Spara figur
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"✅ Sparad: {save_path}")
    plt.close()

    return fig


# ===== MAIN EXECUTION =====
if __name__ == "__main__":
    print("\n" + "="*60)
    print("📊 YH-KOLLEN STORYTELLING FÖR THE SKOOL")
    print("="*60 + "\n")

    # Ladda data
    print("📂 Laddar data...")
    df = load_all_data()

    print(f"\n✅ Data laddad: {len(df)} ansökningar")
    print(f"   • Beviljade: {len(df[df['Beslut'] == 'Beviljad'])}")
    print(f"   • Avslag: {len(df[df['Beslut'] == 'Avslag'])}")
    print(f"   • Godkännandegrad: {len(df[df['Beslut'] == 'Beviljad']) / len(df) * 100:.1f}%")

    # Data/IT stats
    datait = df[df['Utbildningsområde'] == 'Data/IT']
    print(f"\n📊 Data/IT specifikt:")
    print(f"   • Totalt: {len(datait)} ansökningar")
    print(f"   • Beviljade: {(datait['Beslut'] == 'Beviljad').sum()}")
    print(f"   • Godkännandegrad: {(datait['Beslut'] == 'Beviljad').sum() / len(datait) * 100:.1f}%")

    # Skapa visualiseringar
    print("\n📊 Skapar storytelling-visualiseringar...\n")

    print("1️⃣ Godkännandegrad per område (Data/IT challenge)...")
    fig1 = create_storytelling_approval_by_area(df)

    print("2️⃣ Data/IT trend över tid (Blir det bättre?)...")
    fig2 = create_storytelling_datait_trend(df)

    print("3️⃣ Geografiska möjligheter (Var finns chansen?)...")
    fig3 = create_storytelling_geographic_opportunity(df)

    print("4️⃣ Examensgrad per område (Vem slutför?)...")
    fig4 = create_storytelling_graduation_rate()

    print("\n" + "="*60)
    print("✅ KLART! Storytelling för The Skool klar!")
    print("="*60)
    print("\n📁 Filer:")
    print("   • storytelling_1_approval_by_area.png")
    print("   • storytelling_2_datait_trend.png")
    print("   • storytelling_3_geographic_opportunity.png")
    print("   • storytelling_4_graduation_rate.png")
    print("\n💡 Starta appen: python main.py")
    print("   Navigera till Storytelling-sidan!")
    print("\n")
