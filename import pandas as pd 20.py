import pandas as pd 
import plotly.express as px
from dash import Dash, dcc, html

# ============================================================
# 1. LOAD EXCEL DATA
# ============================================================

file_path = "D:All 20 Coountry Data analysis.xlsx"

dataset = pd.read_excel(file_path)

# Remove accidental spaces from column names
dataset.columns = dataset.columns.str.strip()

# ============================================================
# 2. CHECK DATA
# ============================================================

print("\n========== DATASET INFORMATION ==========\n")
print(dataset.head())

print("\n========== COLUMNS ==========\n")
print(dataset.columns.tolist())

print("\n========== DATA TYPES ==========\n")
print(dataset.dtypes)

print("\n========== MISSING VALUES ==========\n")
print(dataset.isnull().sum())


# ============================================================
# 3. BASIC ANALYSIS
# ============================================================

total_countries = dataset["Country"].nunique()

total_population = dataset["Population Number"].sum()

total_gdp = dataset["GDP in Number"].sum()

average_literacy = dataset["Literacy Rate"].mean()

average_healthcare = dataset["Healthcare Score"].mean()

average_defense = dataset["Defense Score"].mean()

average_agriculture = dataset["Agriculture Score"].mean()

total_olympic_medals = dataset["Olympic Medals"].sum()


print("\n========== BASIC ANALYSIS ==========\n")

print("Total Countries:", total_countries)

print(
    "Total Population:",
    f"{total_population / 1e9:.2f} Billion"
)

print(
    "Total GDP:",
    f"${total_gdp / 1e12:.2f} Trillion"
)

print(
    "Average Literacy Rate:",
    f"{average_literacy:.2%}"
)

print(
    "Average Healthcare Score:",
    f"{average_healthcare:.2f}"
)

print(
    "Average Defense Score:",
    f"{average_defense:.2f}"
)

print(
    "Average Agriculture Score:",
    f"{average_agriculture:.2f}"
)

print(
    "Total Olympic Medals:",
    total_olympic_medals
)


# ============================================================
# 4. TOP COUNTRIES
# ============================================================

top_gdp = dataset.nlargest(5, "GDP in Number")

top_population = dataset.nlargest(5, "Population Number")

top_literacy = dataset.nlargest(5, "Literacy Rate")

top_healthcare = dataset.nlargest(5, "Healthcare Score")

top_defense = dataset.nlargest(5, "Defense Score")

top_agriculture = dataset.nlargest(5, "Agriculture Score")

top_olympics = dataset.nlargest(5, "Olympic Medals")


print("\n========== TOP 5 GDP ==========\n")
print(top_gdp[["Country", "GDP", "GDP in Number"]])

print("\n========== TOP 5 POPULATION ==========\n")
print(top_population[["Country", "Population", "Population Number"]])

print("\n========== TOP 5 LITERACY ==========\n")
print(top_literacy[["Country", "Literacy Rate"]])

print("\n========== TOP 5 HEALTHCARE ==========\n")
print(top_healthcare[["Country", "Healthcare Score"]])

print("\n========== TOP 5 DEFENSE ==========\n")
print(top_defense[["Country", "Defense Score"]])

print("\n========== TOP 5 AGRICULTURE ==========\n")
print(top_agriculture[["Country", "Agriculture Score"]])

print("\n========== TOP 5 OLYMPIC COUNTRIES ==========\n")
print(top_olympics[["Country", "Olympic Medals"]])


# ============================================================
# 5. CALCULATED COLUMNS
# ============================================================

# GDP per capita
dataset["GDP Per Capita"] = (
    dataset["GDP in Number"] /
    dataset["Population Number"]
)

# Overall development score
dataset["Overall Development Score"] = (
    dataset["Healthcare Score"]
    + dataset["Defense Score"]
    + dataset["Agriculture Score"]
) / 3

# Olympic medal rate per million population
dataset["Olympic Medals per Million"] = (
    dataset["Olympic Medals"] /
    (dataset["Population Number"] / 1e6)
)


# ============================================================
# 6. PRINT CALCULATED ANALYSIS
# ============================================================

print("\n========== GDP PER CAPITA ==========\n")

print(
    dataset[
        ["Country", "GDP Per Capita"]
    ].sort_values(
        "GDP Per Capita",
        ascending=False
    ).head(10)
)


print("\n========== OVERALL DEVELOPMENT ==========\n")

print(
    dataset[
        ["Country", "Overall Development Score"]
    ].sort_values(
        "Overall Development Score",
        ascending=False
    )
)


# ============================================================
# 7. DASH APPLICATION
# ============================================================

app = Dash(__name__)

app.title = "Global Country Analysis"


# ============================================================
# 8. CREATE CHARTS
# ============================================================

# GDP Chart
gdp_chart = px.bar(
    dataset.sort_values("GDP in Number", ascending=False),
    x="Country",
    y="GDP in Number",
    title="GDP by Country",
    text="GDP"
)

gdp_chart.update_layout(
    xaxis_tickangle=-45
)


# Population Chart
population_chart = px.bar(
    dataset.sort_values("Population Number", ascending=False),
    x="Country",
    y="Population Number",
    title="Population by Country"
)

population_chart.update_layout(
    xaxis_tickangle=-45
)


# Literacy Chart
literacy_chart = px.bar(
    dataset.sort_values("Literacy Rate", ascending=False),
    x="Country",
    y="Literacy Rate",
    title="Literacy Rate by Country",
    text="Literacy Rate"
)

literacy_chart.update_layout(
    xaxis_tickangle=-45,
    yaxis_tickformat=".0%"
)


# Healthcare Chart
healthcare_chart = px.bar(
    dataset.sort_values("Healthcare Score", ascending=False),
    x="Country",
    y="Healthcare Score",
    title="Healthcare Score by Country"
)

healthcare_chart.update_layout(
    xaxis_tickangle=-45
)


# Defense Chart
defense_chart = px.bar(
    dataset.sort_values("Defense Score", ascending=False),
    x="Country",
    y="Defense Score",
    title="Defense Score by Country"
)

defense_chart.update_layout(
    xaxis_tickangle=-45
)


# Agriculture Chart
agriculture_chart = px.bar(
    dataset.sort_values("Agriculture Score", ascending=False),
    x="Country",
    y="Agriculture Score",
    title="Agriculture Score by Country"
)

agriculture_chart.update_layout(
    xaxis_tickangle=-45
)


# Olympic Medal Chart
olympic_chart = px.bar(
    dataset.sort_values("Olympic Medals", ascending=False),
    x="Country",
    y="Olympic Medals",
    title="Olympic Medals by Country",
    text="Olympic Medals"
)

olympic_chart.update_layout(
    xaxis_tickangle=-45
)


# Olympic Medal Breakdown
olympic_breakdown = px.bar(
    dataset.sort_values("Olympic Medals", ascending=False),
    x="Country",
    y=[
        "Olympic Gold",
        "Olympic Silver",
        "Olympic Bronze"
    ],
    title="Olympic Medal Breakdown"
)

olympic_breakdown.update_layout(
    xaxis_tickangle=-45
)


# GDP vs Population
gdp_population_chart = px.scatter(
    dataset,
    x="Population Number",
    y="GDP in Number",
    size="Olympic Medals",
    color="Country",
    hover_data=[
        "GDP",
        "Population",
        "Literacy Rate",
        "Healthcare Score"
    ],
    title="GDP vs Population"
)


# GDP vs Literacy
gdp_literacy_chart = px.scatter(
    dataset,
    x="Literacy Rate",
    y="GDP in Number",
    size="Population Number",
    color="Country",
    hover_data=["GDP", "Population"],
    title="GDP vs Literacy Rate"
)


# Healthcare vs GDP
healthcare_gdp_chart = px.scatter(
    dataset,
    x="Healthcare Score",
    y="GDP in Number",
    size="Population Number",
    color="Country",
    title="Healthcare Score vs GDP"
)


# Defense vs GDP
defense_gdp_chart = px.scatter(
    dataset,
    x="Defense Score",
    y="GDP in Number",
    size="Population Number",
    color="Country",
    title="Defense Score vs GDP"
)


# Agriculture vs Population
agriculture_population_chart = px.scatter(
    dataset,
    x="Population Number",
    y="Agriculture Score",
    size="GDP in Number",
    color="Country",
    title="Agriculture Score vs Population"
)


# Space Mission Chart
space_chart = px.bar(
    dataset,
    x="Country",
    y="Success",
    color="Success",
    hover_data=["Space Mission"],
    title="Space Mission Success"
)

space_chart.update_layout(
    xaxis_tickangle=-45
)


# Overall Development
development_chart = px.bar(
    dataset.sort_values(
        "Overall Development Score",
        ascending=False
    ),
    x="Country",
    y="Overall Development Score",
    title="Overall Development Score"
)

development_chart.update_layout(
    xaxis_tickangle=-45
)


# ============================================================
# 9. DASHBOARD LAYOUT
# ============================================================

app.layout = html.Div(

    style={
        "fontFamily": "Arial",
        "padding": "20px"
    },

    children=[

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        html.H1(
            "🌍 Global Country Analysis Dashboard",
            style={
                "textAlign": "center",
                "marginBottom": "30px"
            }
        ),

        html.H3(
            "Economic • Population • Healthcare • Defense • Agriculture • Space • Olympics",
            style={
                "textAlign": "center"
            }
        ),


        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        html.Div(

            style={
                "display": "flex",
                "justifyContent": "space-around",
                "flexWrap": "wrap",
                "marginTop": "30px",
                "marginBottom": "30px"
            },

            children=[

                html.Div([
                    html.H4("Countries"),
                    html.H2(f"{total_countries}")
                ]),

                html.Div([
                    html.H4("Total GDP"),
                    html.H2(
                        f"${total_gdp / 1e12:.2f}T"
                    )
                ]),

                html.Div([
                    html.H4("Population"),
                    html.H2(
                        f"{total_population / 1e9:.2f}B"
                    )
                ]),

                html.Div([
                    html.H4("Avg Literacy"),
                    html.H2(
                        f"{average_literacy:.1%}"
                    )
                ]),

                html.Div([
                    html.H4("Olympic Medals"),
                    html.H2(
                        f"{total_olympic_medals:,}"
                    )
                ])

            ]
        ),


        # ----------------------------------------------------
        # ECONOMIC ANALYSIS
        # ----------------------------------------------------

        html.H2("💰 Economic Analysis"),

        dcc.Graph(
            figure=gdp_chart
        ),

        dcc.Graph(
            figure=gdp_population_chart
        ),

        dcc.Graph(
            figure=gdp_literacy_chart
        ),


        # ----------------------------------------------------
        # POPULATION
        # ----------------------------------------------------

        html.H2("👥 Population Analysis"),

        dcc.Graph(
            figure=population_chart
        ),


        # ----------------------------------------------------
        # LITERACY
        # ----------------------------------------------------

        html.H2("📚 Literacy Analysis"),

        dcc.Graph(
            figure=literacy_chart
        ),


        # ----------------------------------------------------
        # HEALTHCARE
        # ----------------------------------------------------

        html.H2("🏥 Healthcare Analysis"),

        dcc.Graph(
            figure=healthcare_chart
        ),

        dcc.Graph(
            figure=healthcare_gdp_chart
        ),


        # ----------------------------------------------------
        # DEFENSE
        # ----------------------------------------------------

        html.H2("🛡️ Defense Analysis"),

        dcc.Graph(
            figure=defense_chart
        ),

        dcc.Graph(
            figure=defense_gdp_chart
        ),


        # ----------------------------------------------------
        # AGRICULTURE
        # ----------------------------------------------------

        html.H2("🌾 Agriculture Analysis"),

        dcc.Graph(
            figure=agriculture_chart
        ),

        dcc.Graph(
            figure=agriculture_population_chart
        ),


        # ----------------------------------------------------
        # SPACE
        # ----------------------------------------------------

        html.H2("🚀 Space Mission Analysis"),

        dcc.Graph(
            figure=space_chart
        ),


        # ----------------------------------------------------
        # OLYMPICS
        # ----------------------------------------------------

        html.H2("🏅 Olympic Analysis"),

        dcc.Graph(
            figure=olympic_chart
        ),

        dcc.Graph(
            figure=olympic_breakdown
        ),


        # ----------------------------------------------------
        # OVERALL DEVELOPMENT
        # ----------------------------------------------------

        html.H2("📊 Overall Country Development"),

        dcc.Graph(
            figure=development_chart
        )

    ]
)


# ============================================================
# 10. RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    print("\n==========================================")
    print("   GLOBAL COUNTRY ANALYSIS DASHBOARD")
    print("==========================================")
    print("Dashboard running at:")
    print("http://127.0.0.1:8050/")
    print("==========================================\n")

    app.run(debug=True)

