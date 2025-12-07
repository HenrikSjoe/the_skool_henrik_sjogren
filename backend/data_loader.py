import pandas as pd

def load_all_data():
    all_dfs = []

    for year in [2022, 2023, 2024]:
        try:
            df = pd.read_excel(
                f"data/raw/resultat-{year}-for-kurser-inom-yh.xlsx",
                sheet_name="Lista ansökningar"
            )
            df['Typ'] = 'Kurs'
            df['År'] = year
            all_dfs.append(df)
        except Exception as e:
            print(f"Fel vid laddning av kurser {year}: {e}")

    for year in [2022, 2023, 2024]:
        try:
            if year == 2022:
                df = pd.read_excel(
                    f"data/raw/resultat-ansokningsomgang-{year}-ny.xlsx",
                    sheet_name="Tabell 4"
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
            print(f"Fel vid laddning av program {year}: {e}")

    combined = pd.concat(all_dfs, ignore_index=True)
    return combined

def load_studerande_data():
    try:
        df_stud = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

        df_stud_filtered = df_stud[
            (df_stud['kön'] == 'totalt') &
            (df_stud['tabellinnehåll'] == 'Antal studerande') &
            (df_stud['ålder'] == 'totalt')
        ].copy()

        omrade_list = sorted([x for x in df_stud_filtered['utbildningens inriktning'].unique() if x != 'Totalt'])
        return df_stud_filtered, omrade_list
    except Exception as e:
        print(f"Kunde inte ladda studerande-data: {e}")
        return pd.DataFrame(), ["Data/It"]
