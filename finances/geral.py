import pandas as pd
import confidencial as conf

dataframe = pd.read_csv(conf.FONTE + conf.BRADESCO + '2024.csv')#, encoding='ISO-8859-1')


print(dataframe.dtypes)


