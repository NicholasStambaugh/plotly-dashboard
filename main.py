import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta
import dash
from dash import dcc, html
import dash_table
import plotly.express as px

# Seed for reproducibility
random.seed(42)

# Function to generate a random date within a given range
def random_date(start_date, end_date):
    return start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days)
    )

# Create a Faker instance
fake = Faker()

# Sample dataset with 5 employees
data = {
    'EmployeeID': [i for i in range(101, 106)],
    'Name': ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie White'],
    'Department': ['HR', 'Engineering', 'Marketing', 'Finance', 'Sales'],
    'Salary': [60000, 80000, 70000, 90000, 75000],
    'JoiningDate': [random_date(datetime(2020, 1, 1), datetime(2022, 1, 1)).strftime('%Y-%m-%d') for _ in range(5)]
}

# Add 30 more employees
for i in range(106, 200):
    data['EmployeeID'].append(i)
    data['Name'].append(fake.name())
    data['Department'].append(fake.random_element(elements=('HR', 'Engineering', 'Marketing', 'Finance', 'Sales')))
    data['Salary'].append(random.randint(50000, 100000))
    data['JoiningDate'].append(random_date(datetime(2020, 1, 1), datetime(2022, 1, 1)).strftime('%Y-%m-%d'))

dtframe = pd.DataFrame(data)
app = dash.Dash(__name__)
app.layout = html.Div(style={'background-color': '#f4f4f4', 'font-family': 'Helvetica, Arial, sans-serif', 'color': '#333333'}, children=[
    html.H1("Employee Analytics Dashboard", style={'color': '#009688', 'text-align': 'center', 'margin-top': '20px'}),
    html.H6("Made with ❤️ by Nick Stambaugh", style={'color': '#009688', 'text-align': 'center'}),
    html.P("Explore and analyze employee data using interactive visualizations.", style={'color': '#009688', 'text-align': 'center'}),

    # Table
    html.Div([
        dash_table.DataTable(
            id='employee-table',
            columns=[{'name': col, 'id': col} for col in dtframe.columns],
            data=dtframe.to_dict('records'),
            page_size=7,
            style_table={'height': '300px', 'overflowY': 'auto'},
            style_header={'backgroundColor': '#009688', 'color': '#ffffff'},
            style_cell={'backgroundColor': '#f9f9f9', 'color': '#333333', 'font-family': 'Helvetica, Arial, sans-serif'},
            style_data={'border-bottom': '1px solid #dddddd'},
        )
    ]),

    # Scatter plot
    html.Div([
        html.H2("Scatter Plot", style={'color': '#009688', 'text-align': 'center'}),
        dcc.Graph(
            id='salary-scatter-plot',
            figure=px.scatter(dtframe, x='Salary',
                              y='JoiningDate',
                              color='Department',
                              hover_data=['Name'])
        ),
    ], style={'width': '70%', 'display': 'inline-block', 'margin-right': '5%', 'text-align': 'center'}),

    # Bar chart
    html.Div([
        html.H2("Bar Chart", style={'color': '#009688', 'text-align': 'center'}),
        dcc.Graph(
            id='bar-chart',
            figure=px.bar(dtframe, x='Department', y='Salary', color='Department')
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'text-align': 'center'}),
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
