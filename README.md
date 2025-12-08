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
python main.py
```

Open your browser at `http://localhost:5005`

## Features

- **Overview**: Key metrics and distribution of applications by education area
- **Student Trends**: Historical data for enrolled and graduated students (2005-2024)
- **Map**: Geographic distribution of approved applications by county
- **Organizers**: Compare education organizers and analyze performance
- **Storytelling**: Visualizations of key insights

## Data structure

```
data/raw/
├── resultat-{year}-for-kurser-inom-yh.xlsx
├── resultat-ansokningsomgang-{year}.xlsx
└── studerande_utbildningsomrade_overtid.csv
```

## Tech stack

- Taipy GUI for frontend
- Plotly for visualizations
- Pandas for data handling
