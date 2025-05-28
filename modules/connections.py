import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from modules.utils import get_user_choice

def explore_connections(data):
    if data.empty:
        print("\nNo data available to explore connections.")
        return

    tutoring_choices = ["Yes", "No", "All"]
    tutoring_choice = get_user_choice("Select Tutoring (Yes/No):", tutoring_choices)
    if tutoring_choice != "All":
        data = data[data['tutoring'] == tutoring_choice]

    study_time_bins = ["<2 hours", "2-5 hours", "5-10 hours", ">10 hours"]
    data = data.copy()
    data['study_time_category'] = pd.cut(
        data['studytime'], bins=[0, 2, 5, 10, float('inf')], labels=study_time_bins
    )

    grouped_data = data.groupby(
        ['location', 'internet_access', 'study_time_category', 'tutoring']
    ).size().reset_index(name='count')

    grouped_data['percentage'] = grouped_data.groupby(['location'])['count'].transform(lambda x: (x / x.sum()) * 100)

    heatmap_data = grouped_data.pivot_table(
        values='percentage',
        index=['location', 'internet_access'],
        columns=['study_time_category', 'tutoring'],
        fill_value=0
    )

    plt.figure(figsize=(16, 10))
    sns.heatmap(
        heatmap_data,
        annot=True,
        fmt=".1f",
        cmap='coolwarm',
        linewidths=0.3,
        linecolor='black',
        cbar_kws={'label': 'Percentage (%)', 'shrink': 0.8, 'orientation': 'vertical'},
        annot_kws={'size': 10, 'weight': 'bold', 'color': 'black'}
    )

    plt.title(
        "Connections: Location, Internet Access, Study Time, and Tutoring",
        fontsize=18, fontweight='bold', color='black', pad=20
    )
    plt.xlabel(
        "Study Time & Tutoring",
        fontsize=14, fontweight='bold', color='black', labelpad=15
    )
    plt.ylabel(
        "Location & Internet Access",
        fontsize=14, fontweight='bold', color='black', labelpad=15
    )

    plt.xticks(fontsize=10, ha='right', weight='bold', color='black')
    plt.yticks(fontsize=10, weight='bold', color='black')

    plt.gca().patch.set_facecolor('white')
    plt.tight_layout(pad=2)
    plt.show()

    plt.figure(figsize=(14, 8))
    sns.barplot(
        data=grouped_data,
        x='study_time_category',
        y='count',
        hue='internet_access',
        ci=None,
        palette='viridis'
    )
    plt.title("Study Time and Internet Access by Location", fontsize=16, fontweight='bold')
    plt.xlabel("Study Time Category", fontsize=12)
    plt.ylabel("Student Count", fontsize=12)
    plt.legend(title="Internet Access")
    plt.tight_layout()
    plt.show()
