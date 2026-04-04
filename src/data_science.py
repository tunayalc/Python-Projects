import pandas as pd
import numpy as np
from scipy.stats import shapiro, kruskal, wilcoxon, sem, t
import statsmodels.api as sm
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Load the Excel file
file_path = '/mnt/data/tunahan veri.xlsx'
data = pd.read_excel(file_path)
data.head()

# Perform normality test for specified columns using Shapiro-Wilk test
columns_to_test = ['Toplam Alış Fiyatı', 'Toplam Satış Fiyatı', 'Kar', 'Gelir', 'Gider']
normality_results = {col: shapiro(data[col].dropna()) for col in columns_to_test}
normality_results

# Convert 'Tarih' column to datetime and sort the data
data['Tarih'] = pd.to_datetime(data['Tarih'], format='%d.%m.%Y')
data = data.sort_values('Tarih')
data.set_index('Tarih', inplace=True)
data[['Gelir', 'Gider', 'Toplam Satış Fiyatı']].describe()

# Calculate correlation matrix for numeric columns
numeric_data = data.select_dtypes(include=['float64', 'int64'])
correlation_matrix = numeric_data.corr()

# Perform Kruskal-Wallis test to check differences in 'Gelir' across months
monthly_income_data = [group["Gelir"].values for _, group in data.groupby("Ay")]
kruskal_test_stat, kruskal_p_value = kruskal(*monthly_income_data)
kruskal_test_stat, kruskal_p_value

# Perform linear regression to predict 'Gelir' using 'Toplam Alış Fiyatı' and 'Satış Fiyatı'
X = data[['Toplam Alış Fiyatı', 'Satış Fiyatı']]
y = data['Gelir']
X = sm.add_constant(X)
model = sm.OLS(y, X).fit()
model_summary = model.summary()
model_summary

# Wilcoxon test to check if May data differs from January to April data
ocak_nisan_gelirleri = data[data['Ay'].isin([1, 2, 3, 4])]['Gelir']
mayis_gelirleri = data[data['Ay'] == 5]['Gelir']
ocak_nisan_ortalama = ocak_nisan_gelirleri.mean()
mayis_verileri = mayis_gelirleri - ocak_nisan_ortalama
test_statistic, p_value = wilcoxon(mayis_verileri)
test_statistic, p_value

# Calculate overall profit margin
data['Tarih'] = pd.to_datetime(data['Tarih'], format='%d.%m.%Y')
total_revenue = data['Gelir'].sum()
total_expense = data['Gider'].sum()
overall_profit = total_revenue - total_expense
overall_profit_margin = (overall_profit / total_revenue) * 100

# Calculate monthly and group-based profit margins
monthly_data = data.groupby('Ay').agg({'Gelir': 'sum', 'Gider': 'sum'})
monthly_data['Profit'] = monthly_data['Gelir'] - monthly_data['Gider']
monthly_data['Profit_Margin (%)'] = (monthly_data['Profit'] / monthly_data['Gelir']) * 100

group_data = data.groupby('Grup').agg({'Gelir': 'sum', 'Gider': 'sum'})
group_data['Profit'] = group_data['Gelir'] - group_data['Gider']
group_data['Profit_Margin (%)'] = (group_data['Profit'] / group_data['Gelir']) * 100

overall_profit_margin, monthly_data, group_data

# Perform K-means clustering with 3 clusters
kmeans = KMeans(n_clusters=3, random_state=42)
data['Cluster'] = kmeans.fit_predict(data[['Gelir', 'Gider']])

# Visualize K-means clustering result
plt.figure(figsize=(8, 6))
scatter = plt.scatter(data['Gelir'], data['Gider'], c=data['Cluster'], cmap='viridis', s=50)
plt.colorbar(scatter, label='Cluster')
plt.title('K-means Clustering: Gelir vs Gider')
plt.xlabel('Gelir')
plt.ylabel('Gider')
plt.show()

# Perform ABC analysis to classify products into A, B, and C categories
data_sorted = data.sort_values(by='Toplam Satış Fiyatı', ascending=False).reset_index(drop=True)
data_sorted['Cumulative Sales'] = data_sorted['Toplam Satış Fiyatı'].cumsum()
total_sales = data_sorted['Toplam Satış Fiyatı'].sum()
data_sorted['Cumulative Percentage'] = data_sorted['Cumulative Sales'] / total_sales * 100

def categorize(row):
    if row['Cumulative Percentage'] <= 80:
        return 'A'
    elif row['Cumulative Percentage'] <= 95:
        return 'B'
    else:
        return 'C'

data_sorted['ABC Category'] = data_sorted.apply(categorize, axis=1)
data_sorted

# Calculate VIF for selected numeric columns to check multicollinearity
numeric_columns = ['Miktar', 'Alış Fiyatı', 'Satış Fiyatı', 'Kar', 'Gelir', 'Gider']
data_numeric = data[numeric_columns].dropna()

vif_data = pd.DataFrame({
    "Feature": data_numeric.columns,
    "VIF": [variance_inflation_factor(data_numeric.values, i) for i in range(data_numeric.shape[1])]
})
vif_data

# Train linear regression model to predict 'Gelir'
X_income = data[['Miktar', 'Alış Fiyatı', 'Satış Fiyatı', 'Toplam Alış Fiyatı']]
y_income = data['Gelir']
X_train_income, X_test_income, y_train_income, y_test_income = train_test_split(X_income, y_income, test_size=0.2, random_state=42)
model_income = LinearRegression()
model_income.fit(X_train_income, y_train_income)
y_pred_income = model_income.predict(X_test_income)

income_metrics = {
    "R²": r2_score(y_test_income, y_pred_income),
    "MAE": mean_absolute_error(y_test_income, y_pred_income),
    "RMSE": np.sqrt(mean_squared_error(y_test_income, y_pred_income))
}
income_metrics

# Train linear regression model to predict 'Gider'
X_expense = data[['Miktar', 'Alış Fiyatı', 'Satış Fiyatı', 'Toplam Alış Fiyatı']]
y_expense = data['Gider']
X_train_expense, X_test_expense, y_train_expense, y_test_expense = train_test_split(X_expense, y_expense, test_size=0.2, random_state=42)
model_expense = LinearRegression()
model_expense.fit(X_train_expense, y_train_expense)
y_pred_expense = model_expense.predict(X_test_expense)

expense_metrics = {
    "R²": r2_score(y_test_expense, y_pred_expense),
    "MAE": mean_absolute_error(y_test_expense, y_pred_expense),
    "RMSE": np.sqrt(mean_squared_error(y_test_expense, y_pred_expense))
}
expense_metrics

# Train linear regression model to predict 'Kar'
X_profit = data[['Miktar', 'Alış Fiyatı', 'Satış Fiyatı', 'Toplam Alış Fiyatı', 'Gelir', 'Gider']]
y_profit = data['Kar']
X_train_profit, X_test_profit, y_train_profit, y_test_profit = train_test_split(X_profit, y_profit, test_size=0.2, random_state=42)
model_profit = LinearRegression()
model_profit.fit(X_train_profit, y_train_profit)
y_pred_profit = model_profit.predict(X_test_profit)

profit_metrics = {
    "R²": r2_score(y_test_profit, y_pred_profit),
    "MAE": mean_absolute_error(y_test_profit, y_pred_profit),
    "RMSE": np.sqrt(mean_squared_error(y_test_profit, y_pred_profit))
}
profit_metrics

# Calculate confidence intervals for 'Gelir', 'Gider', and 'Kar'
def confidence_interval(data, confidence=0.95):
    mean = data.mean()
    std_error = sem(data)
    n = len(data)
    h = std_error * t.ppf((1 + confidence) / 2, n - 1)
    return mean - h, mean + h

confidence_intervals = {
    "Gelir": confidence_interval(data["Gelir"]),
    "Gider": confidence_interval(data["Gider"]),
    "Kar": confidence_interval(data["Kar"])
}
confidence_intervals

