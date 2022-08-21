import pandas as pd
import random
df = pd.read_csv('Sales_Records.csv')
df = df.assign(rating=[random.uniform(1, 10) for i in range(len(df['Country']))])
df.columns = df.columns.str.replace(' ', '_')
sample_country = df["Country"].sample(n=3).unique()
sample_channel = df["Sales_Channel"].sample(n=1).unique()
sample_item = df["Item_Type"].sample(n=3).unique()