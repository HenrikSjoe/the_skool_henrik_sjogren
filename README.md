# YH-kollen Dashboard

Dashboard for analyzing and visualizing application data for Swedish vocational higher education (Yrkeshögskolan).

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Running the application

```bash
# Generate storytelling images (required first time)
python -m backend.storytelling_charts

# Start the dashboard
python main.py
```

Open your browser at `http://localhost:5005`

## Features

- **Overview**: Key metrics and distribution of applications by education area
- **Student Trends**: Historical data for enrolled and graduated students (2005-2024)
- **Map**: Geographic distribution of approved applications by county
- **Organizers**: Compare education organizers and analyze performance
- **Storytelling**: Visualizations of key insights

## Key Performance Indicators (KPIs)

The dashboard tracks the following KPIs:

1. **Total Applications**: Total number of applications submitted (courses and programs)
2. **Approval Rate**: Percentage of approved applications vs total applications
3. **Total Approved Positions**: Number of student positions in approved applications
4. **Graduation Rate**: Percentage of students who complete their education (per education area)
5. **Organizer Ranking**: Performance ranking of education organizers based on approval rate
6. **Geographic Distribution**: Number of approved applications per county
7. **Trend Analysis**: Year-over-year changes in applications and approvals
8. **Area-specific Approval Rates**: Success rates for different education areas

## Data sources

- [Myndigheten för yrkeshögskolan (MYH)](https://www.myh.se) - Application results 2022-2024
- [Statistiska centralbyrån (SCB)](https://www.scb.se) - Student statistics 2005-2024

## Data structure

```
data/raw/
├── resultat-{year}-for-kurser-inom-yh.xlsx
├── resultat-ansokningsomgang-{year}.xlsx
└── studerande_utbildningsomrade_overtid.csv
```

## Tech stack

- Python
- Taipy GUI for frontend
- Plotly for interactive visualizations
- Matplotlib/Seaborn for storytelling charts
- Pandas for data handling
