import pandas as pd
import os
import numpy as np
pd.options.display.float_format = '{:.2f}'.format
pd.options.display.max_columns = None

def missing(x):
     return f"%{round(x.isnull().sum() / x.shape[0] * 100, 2)}"

def outlier_numbers(x):
    return np.where((abs(x - x.mean()) / x.std()) >= 3, 1, 0).sum()

def value_counts(x):
    value_dict = x.value_counts(normalize=True).sort_values(ascending=False).head(3).to_dict().items()
    return value_dict

def main(file_path):
    df = pd.read_excel(file_path)
    numeric = df.select_dtypes(include=['float','int'])
    categorical = df.select_dtypes(include='object')    
    try:
        categorical_agg = categorical.agg(['count', missing, value_counts])
        categorical_agg_exploded = categorical_agg.T.reset_index().rename(columns={'index': 'cols'}).explode('value_counts')
        categorical_agg_exploded['most_freq_frequencies'] = categorical_agg_exploded['value_counts'].str[1]
        categorical_agg_exploded['most_freq_values'] = categorical_agg_exploded['value_counts'].str[0]
        categorical_agg_exploded['order'] = 1
        categorical_agg_exploded['order'] = categorical_agg_exploded.groupby('cols').order.transform(np.cumsum)
        categorical_agg_exploded['order'] = categorical_agg_exploded['order'].replace({1: 'first_most_frequent_value', 2: 'second_most_frequent_value', 3: 'third_most_frequent_value'})
        categorical_agg_exploded['value_counts'] = categorical_agg_exploded['value_counts'].map(lambda x: f"%{round(x[1] * 100, 2)} {x[0]}")
        categorical_agg_pivoted = categorical_agg_exploded.pivot(index='cols', columns='order', values='value_counts').T
        categorical_agg_pivoted.index.name = None
        categorical_agg_pivoted.columns.name = None
        categorical_final = pd.concat([categorical_agg.drop(index='value_counts'), categorical_agg_pivoted])
    except:
        categorical_final = pd.DataFrame()
        
    
    try:
        numeric_final = numeric.agg(['mean', 'median', 'std', 'min', 'max', 'count', 'nunique', missing, outlier_numbers])
    except:
        numeric_final = pd.DataFrame()
        

    return df, categorical_final, numeric_final
    

if __name__ == '__main__':
    # Excel path'ini main fonksiyonunun içine yerleþtir.
    path = r'C:\Users\berkaygo\Desktop\Codes\notebooks\Lab\HistoricalEcommerce.xlsx'
    df, categoric, numeric = main(path)
    print(df)