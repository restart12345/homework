import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from plotly.offline import plot
import plotly.express as px

app = dash.Dash(__name__)

incomedata = pd.read_excel(
    'income_per_person_gdppercapita_ppp_inflation_adjusted.xlsx')
lidata = incomedata.melt(
    id_vars='country',
    var_name='year',
    value_name='income'
)
lidata = lidata[(lidata['year'] >= 2005) & (lidata['year'] <= 2018)]
lidata['income'].replace('k', 'e3', regex=True)

ledata = pd.read_excel('life_expectancy_years.xlsx')
lifedata = ledata.melt(
    id_vars='country',
    var_name='year',
    value_name='lifeExp'
)
lifedata = lifedata[(lifedata['year'] >= 2005) & (lifedata['year'] <= 2018)]

pdata = pd.read_excel('population_total.xlsx')
pdata = pdata.melt(
    id_vars='country',
    var_name='year',
    value_name='pop'
)
pdata = pdata[(pdata['year'] >= 2005) & (pdata['year'] <= 2018)]

income_life = pd.merge(lidata, lifedata, left_on=['year', 'country'], right_on=[
                       'year', 'country'], how='inner')
income_life_pop = pd.merge(income_life, pdata, left_on=[
                           'year', 'country'], right_on=['year', 'country'], how='inner')

data = px.data.gapminder()
data = data[['country', 'continent']]
data = data.drop_duplicates(subset=['country', 'continent'], keep='first')
finishdata = pd.merge(income_life_pop, data,
                      left_on='country', right_on='country', how='left')
finishdata['income'].replace('k', 'e3', regex=True)

finishdata.to_excel('人均gdp和人均期望寿命2005-2018.xlsx')

finishdata = pd.read_excel('人均gdp和人均期望寿命2005-2018.xlsx')
finishdata = finishdata.dropna()
fig = px.scatter(finishdata, x="income", y="lifeExp", animation_frame="year",
                 animation_group="country", size="lifeExp", color="continent",
                 hover_name="country", log_x=True, size_max=35, range_x=[500, 200000], range_y=[25, 90],
                 labels=dict(income="人均收入(PPP购买力标准)", lifeExp="人均寿命"))
fig.update_layout(height=600)
app.layout = html.Div([
    html.H1(children="2005-2018人均gdp和人均期望寿命分析", style={"textAlign": "center"}),
    dcc.Graph(figure=fig)]
)

if __name__ == '__main__':
    app.run_server()
