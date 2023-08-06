from visualizations.radar import RadarChart
import pandas as pd

df = pd.read_excel('../df_cluster3.xlsx').set_index('k20')
radar = RadarChart(df, i_cols=3,font_size=30)
radar.create_chart()