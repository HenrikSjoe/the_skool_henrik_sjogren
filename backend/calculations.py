import pandas as pd

def calculate_kpis(data):
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

def filter_data(data, year_filter, type_filter, anordnare_filter):
    filtered = data.copy()

    if year_filter != "Alla":
        filtered = filtered[filtered['År'] == int(year_filter)]

    if type_filter != "Alla":
        filtered = filtered[filtered['Typ'] == type_filter]

    if anordnare_filter != "Alla":
        filtered = filtered[filtered['Anordnare namn'] == anordnare_filter]

    return filtered

def calculate_examensgrad_all():
    df_all = pd.read_csv("data/raw/studerande_utbildningsomrade_overtid.csv", encoding='ISO-8859-1')

    df_2024 = df_all[
        (df_all['år'] == 2024) &
        (df_all['kön'] == 'totalt') &
        (df_all['ålder'] == 'totalt')
    ].copy()

    aktiva = df_2024[df_2024['tabellinnehåll'] == 'Antal studerande'].set_index('utbildningens inriktning')
    examinerade = df_2024[df_2024['tabellinnehåll'] == 'Antal examinerade'].set_index('utbildningens inriktning')

    result = []
    for omrade in aktiva.index:
        if omrade == 'Totalt':
            continue

        if omrade in ['Pedagogik och lärarutbildning', 'Pedagogik och undervisning']:
            continue

        aktiva_val = aktiva.loc[omrade, 'Studerande och examinerade inom yrkeshögskolan']
        if isinstance(aktiva_val, pd.Series):
            aktiva_val = aktiva_val.iloc[0]

        if omrade in examinerade.index:
            exam_val = examinerade.loc[omrade, 'Studerande och examinerade inom yrkeshögskolan']
            if isinstance(exam_val, pd.Series):
                exam_val = exam_val.iloc[0]

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

def get_examensgrad_top5():
    df_all = calculate_examensgrad_all()

    if df_all.empty:
        return pd.DataFrame({'Meddelande': ['Ingen data tillgänglig']})

    return df_all.head(5)

def get_examensgrad_selected(omrade):
    df_all = calculate_examensgrad_all()

    if df_all.empty:
        return "N/A"

    row = df_all[df_all['Utbildningsområde'] == omrade]

    if row.empty:
        return "N/A"

    return f"{row['Examensgrad (%)'].values[0]}"
