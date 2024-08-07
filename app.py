import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and clean the data
# Adjust the file path to where your Excel file is located
data = pd.read_excel('F:/my_dashboard/Student_expenses.xlsx', sheet_name='Data')
data.drop_duplicates(inplace=True)
data.ffill(inplace=True)  # Updated method to fill missing values

# Print the column names to verify
print(data.columns)

# layout of the app
app.layout = html.Div([
    html.H1("Student Expenses Dashboard"),
    dcc.Dropdown(
        id='some-input',
        options=[
            {'label': major, 'value': major} for major in data['major'].unique()
        ],
        value=data['major'].unique()[0],
        clearable=False
    ),
    dcc.Graph(id='expenses-by-category'),
    dcc.Graph(id='expense-distribution')
])

# Define callback to update the graphs
@app.callback(
    [Output('expenses-by-category', 'figure'),
     Output('expense-distribution', 'figure')],
    [Input('some-input', 'value')]
)
def update_graphs(selected_major):
   
    filtered_data = data[data['major'] == selected_major]

    # column names
    columns = ['tuition', 'housing', 'food', 'transportation', 'books_supplies', 'entertainment', 'technology', 'health_wellness', 'miscellaneous', 'personal_care', 'financial_aid']
    existing_columns = [col for col in columns if col in filtered_data.columns]

    # Total expenses by category
    expense_by_category = filtered_data[existing_columns].sum()
    bar_fig = px.bar(expense_by_category, x=expense_by_category.index, y=expense_by_category.values,
                     title='Total Expenses by Category')

    # Expense distribution by category
    pie_fig = px.pie(expense_by_category, values=expense_by_category.values, names=expense_by_category.index,
                     title='Expense Distribution by Category')

    return bar_fig, pie_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
