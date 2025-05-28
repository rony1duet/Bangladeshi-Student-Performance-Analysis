import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns
import numpy as np
from modules.connections import explore_connections
from modules.utils import get_user_choice

def plot_grouped_averages(data):
    if data.empty:
        print("\nNo data available to process. Please check your filters.")
        return
    subject_mapping = {
        "Science": ["ict", "math", "science"],
        "Commerce": ["ict", "english", "finance"],
        "Humanities": ["ict", "english", "social_science"]
    }
    
    avg_scores = []

    for access in ["Yes", "No"]:
        filtered_data = data[data['internet_access'] == access]
        for group, subjects in subject_mapping.items():
            group_data = filtered_data[filtered_data['stu_group'] == group]
            if not group_data.empty:
                avg_subject_scores = group_data[subjects].mean().to_dict()
                avg_subject_scores["Internet Access"] = access
                avg_subject_scores["Group"] = group
                avg_scores.append(avg_subject_scores)


    if not avg_scores:
        print("\nNo data to visualize after filtering.")
        return
    

    avg_scores_df = pd.DataFrame(avg_scores)
    avg_scores_long = avg_scores_df.melt(id_vars=["Internet Access", "Group"], var_name="Subject", value_name="Average Score")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=avg_scores_long, x="Subject", y="Average Score", hue="Internet Access", palette="viridis",errorbar=None)
    plt.title("Average Scores by Internet Access and Subject", fontsize=14, fontweight="bold")
    plt.xlabel("Subjects", fontsize=12)
    plt.ylabel("Average Score", fontsize=12)
    plt.legend(title="Internet Access")
    plt.tight_layout()
    plt.show()
    print("\nSummary:")
    print("This bar plot shows the average scores of students based on their internet access and subject group.")

def plot_custom_analysis(data):
    if data.empty:
        print("\nNo data available for custom analysis.")
        return
    custom_analysis_choices = [
        "Internet Access vs Gender",
        "Internet Access vs Extra Curricular Activities",
        "Internet Access Distribution",
        "Explore Connections",
        "Go Back"
    ]

    custom_choice = get_user_choice("Choose a custom analysis:", custom_analysis_choices)


    if custom_choice == "Internet Access vs Gender":
        grouped_data = data.groupby(['internet_access', 'gender']).size().reset_index(name='count')
        grouped_data['label'] = grouped_data['internet_access'] + ' (' + grouped_data['gender'] + ')'
        sizes = grouped_data['count']
        labels = grouped_data['label']
        colors = cm.tab20c(np.arange(len(sizes)) / len(sizes))
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90, colors=colors, wedgeprops=dict(edgecolor='w'))
        plt.title('Percentage of Students with Internet Access by Gender', fontsize=14)
        plt.show()
        print("\nSummary:")
        print("This pie chart shows the percentage of students with internet access based on their gender.")



    elif custom_choice == "Internet Access vs Extra Curricular Activities":
        filtered_data = data.groupby(['internet_access', 'extra_curricular_activities']).size().reset_index(name='count')
        total_counts = filtered_data.groupby('internet_access')['count'].transform('sum')
        filtered_data['percentage'] = filtered_data['count'] / total_counts * 100
        plt.figure(figsize=(8, 6))
        sns.barplot(x='internet_access', y='percentage', hue='extra_curricular_activities', data=filtered_data, palette='viridis',errorbar=None)
        plt.title('Relationship between Internet Access and Extra Curricular Activities (Percentage)')
        ax = plt.gca()
        for p in ax.patches:
            if p.get_height() > 0:
                height = p.get_height()
                percentage = (height / grouped_data['count'].sum()) * 100
                ax.annotate(f'{height:.0f} ({percentage:.1f}%)', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
        plt.legend(title='Extra Curricular', fontsize='small', title_fontsize='10', loc='lower right')
        plt.ylabel('Percentage')
        plt.xlabel('Internet Access')
        plt.show()
        print("\nSummary:")
        print("This bar plot shows the relationship between internet access and extra curricular activities.")



    elif custom_choice == "Internet Access Distribution":
        grouped_data = data.groupby(['internet_access', 'location']).size().reset_index(name='count')
        total_counts = grouped_data.groupby('internet_access')['count'].transform('sum')
        grouped_data['percentage'] = grouped_data['count'] / total_counts * 100
        plt.figure(figsize=(10, 6))
        sns.set(style="whitegrid")
        sns.barplot(x='location', y='count', hue='internet_access', data=grouped_data, palette='viridis',errorbar=None)
        plt.title('Students with Internet Access by Location', fontsize=16, weight='bold', color='darkblue')
        plt.xlabel('Location', fontsize=12, weight='bold', color='darkslategray')
        plt.ylabel('Number of Students', fontsize=12, weight='bold', color='darkslategray')
        ax = plt.gca()
        for p in ax.patches:
            if p.get_height() > 0:
                height = p.get_height()
                percentage = (height / grouped_data['count'].sum()) * 100
                ax.annotate(f'{height:.0f} ({percentage:.1f}%)', (p.get_x() + p.get_width() / 2., height), ha='center', va='center', fontsize=10, color='black', xytext=(0, 5), textcoords='offset points')
        plt.xticks(ha='right', fontsize=10, weight='light', color='darkslategray')
        plt.yticks(fontsize=10, weight='light', color='darkslategray')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Internet Access', fontsize='small', title_fontsize='10', loc='lower right')
        plt.tight_layout()
        plt.show()
        print("\nSummary:")
        print("This bar plot shows the distribution of students with internet access by location.")


    elif custom_choice == "Explore Connections":
        explore_connections(data)
