import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2 BMI = weight / height^2 (m)
df['overweight'] = (df['weight'] / ((df['height'] / 100) ** 2) > 25).astype(int)

# 3 change 1 -> 0 (good), >1 -> 1 (bad)
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4 draw plot
def draw_cat_plot():
    # 5 convert data to long type
    df_cat = pd.melt(
        df,
        id_vars=['cardio'],
        value_vars=['cholesterol','gluc','smoke','alco','active','overweight'] 
    )

    # 6 count number by group
    df_cat = df_cat.groupby(['cardio','variable','value']).size().reset_index(name='total')
    

    # 7 

    # 8  
    fig = sns.catplot(
        data=df_cat,
        kind='bar',
        x='variable',
        y='total',
        hue='value',
        col='cardio'
    ).fig


    # 9 return figure
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11 clean invalid data
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    # 12 matrix correlation
    corr = df_heat.corr()

    # 13 create mask for triangle
    mask = np.triu(np.ones_like(corr,dtype=bool))

    # 14 create drawing frame
    fig, ax = plt.subplots(figsize=(12,10))

    # 15 drawing heatmap
    sns.heatmap(
        corr,mask=mask, annot=True,fmt='.1f',
        center=0,vmax=0.3,vmin=-0.1,square=True,
        linewidths=0.5,cbar={"shrink":0.5}
    )

    # 16
    fig.savefig('heatmap.png')
    return fig
