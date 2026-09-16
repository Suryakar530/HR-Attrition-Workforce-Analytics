"""
HR Attrition Analysis - Pandas + Matplotlib only
Dataset: IBM HR Analytics Employee Attrition
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-interactive backend for saving files
import matplotlib.pyplot as plt

# -------------------------------------------------
# 1. Load Data
# -------------------------------------------------
df = pd.read_csv('hr_attrition.csv')
print("Shape:", df.shape)
print(df['Attrition'].value_counts())

# -------------------------------------------------
# 2. Overall Attrition Rate
# -------------------------------------------------
attrition_counts = df['Attrition'].value_counts()
attrition_pct = (attrition_counts / attrition_counts.sum() * 100).round(2)
print("\nAttrition %:\n", attrition_pct)

plt.figure(figsize=(5, 5))
colors = ["#178BDE", "#E27537"]
plt.pie(attrition_counts, labels=attrition_counts.index, autopct='%1.1f%%',
        colors=colors, startangle=90)
plt.title('Overall Attrition Rate')
plt.tight_layout()
plt.savefig('chart_1_overall_attrition.png')
plt.close()


# # -------------------------------------------------
# # 3. Attrition by Department
# # -------------------------------------------------
dept_attrition = pd.crosstab(df['Department'], df['Attrition'])
dept_rate = (dept_attrition['Yes'] / dept_attrition.sum(axis=1) * 100).round(2).sort_values(ascending=False)
print("\nAttrition rate by Department:\n", dept_rate)

plt.figure(figsize=(7, 5))
dept_rate.plot(kind='bar', color='#C44E52')
plt.title('Attrition Rate by Department (%)')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('charts_2_attrition_by_department.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 4. Attrition by OverTime
# # -------------------------------------------------
ot_attrition = pd.crosstab(df['OverTime'], df['Attrition'])
ot_rate = (ot_attrition['Yes'] / ot_attrition.sum(axis=1) * 100).round(2)
print("\nAttrition rate by OverTime:\n", ot_rate)

plt.figure(figsize=(5, 5))
ot_rate.plot(kind='bar', color='#55A868')
plt.title('Attrition Rate by OverTime (%)')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts_3_attrition_by_overtime.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 5. Monthly Income vs Attrition (Boxplot)
# # -------------------------------------------------
plt.figure(figsize=(6, 5))
data_to_plot = [df[df['Attrition'] == 'No']['MonthlyIncome'],
                df[df['Attrition'] == 'Yes']['MonthlyIncome']]
plt.boxplot(data_to_plot, tick_labels=['No', 'Yes'])
plt.title('Monthly Income by Attrition Status')
plt.ylabel('Monthly Income')
plt.xlabel('Attrition')
plt.tight_layout()
plt.savefig('charts_4_income_vs_attrition.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 6. Attrition by Age Group
# # -------------------------------------------------
bins = [17, 30, 40, 50, 61]
labels = ['<30', '30-40', '41-50', '50+']
df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels)
age_attrition = pd.crosstab(df['AgeGroup'], df['Attrition'])
age_rate = (age_attrition['Yes'] / age_attrition.sum(axis=1) * 100).round(2)
print("\nAttrition rate by Age Group:\n", age_rate)

plt.figure(figsize=(6, 5))
age_rate.plot(kind='bar', color='#8172B2')
plt.title('Attrition Rate by Age Group (%)')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts_5_attrition_by_agegroup.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 7. Attrition by Years at Company (Tenure Bands)
# # -------------------------------------------------
bins2 = [-1, 2, 5, 10, 100]
labels2 = ['0-2 yrs', '3-5 yrs', '6-10 yrs', '10+ yrs']
df['TenureBand'] = pd.cut(df['YearsAtCompany'], bins=bins2, labels=labels2)
tenure_attrition = pd.crosstab(df['TenureBand'], df['Attrition'])
tenure_rate = (tenure_attrition['Yes'] / tenure_attrition.sum(axis=1) * 100).round(2)
print("\nAttrition rate by Tenure Band:\n", tenure_rate)

plt.figure(figsize=(6, 5))
tenure_rate.plot(kind='bar', color='#CCB974')
plt.title('Attrition Rate by Tenure Band (%)')
plt.ylabel('Attrition Rate (%)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('charts_6_attrition_by_tenure.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 8. Attrition by Job Role (Top risk roles)
# # -------------------------------------------------
role_attrition = pd.crosstab(df['JobRole'], df['Attrition'])
role_rate = (role_attrition['Yes'] / role_attrition.sum(axis=1) * 100).round(2).sort_values(ascending=False)
print("\nAttrition rate by Job Role:\n", role_rate)

plt.figure(figsize=(9, 5))
role_rate.plot(kind='barh', color='#64B5CD')
plt.title('Attrition Rate by Job Role (%)')
plt.xlabel('Attrition Rate (%)')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('charts_7_attrition_by_jobrole.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 9. Correlation Heatmap (numeric columns only) - pure matplotlib
# # -------------------------------------------------
numeric_df = df.select_dtypes(include='number')
corr = numeric_df.corr()

plt.figure(figsize=(14, 12))
plt.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(label='Correlation')
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90, fontsize=7)
plt.yticks(range(len(corr.columns)), corr.columns, fontsize=7)
plt.title('Correlation Heatmap (Numeric Features)')
plt.tight_layout()
plt.savefig('charts_8_correlation_heatmap.png', dpi=150)
plt.close()

# # -------------------------------------------------
# # 10. Summary table export
# # -------------------------------------------------
summary = pd.DataFrame({
    'Metric': ['Overall Attrition Rate (%)', 'Highest Risk Department', 
               'Highest Risk Job Role', 'Overtime Attrition Rate (%)',
               'No-Overtime Attrition Rate (%)'],
    'Value': [attrition_pct.get('Yes', 0), dept_rate.idxmax(),
              role_rate.idxmax(), ot_rate.get('Yes', 0), ot_rate.get('No', 0)]
})
summary.to_csv('charts_summary_table.csv', index=False)
print("\n=== Summary ===")
print(summary)

print("\nAll charts saved to /home/claude/charts/")
