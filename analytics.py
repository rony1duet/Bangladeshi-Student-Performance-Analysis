import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

def text_format(str):
    cleaned = re.sub(r'[^A-Za-z0-9\s]', ' ', str)
    return cleaned.title()





def analyze_performance_by_demographics(data, subjects, plot=True, groupby=None, **filters):
    """
    Analyzes demographic data and optionally plots the results. 

    Parameters:
    -----------
    data : pandas.DataFrame
        The dataset containing demographic and performance information.
    subjects : list of str
        List of subject columns to analyze.
    plot : bool, optional
        If True, the function will generate plots based on the provided data. Default is True.
    groupby : str, optional
        Column to group by for analysis.
    **filters : dict
        Filters for demographic attributes.

    Returns:
    --------
    pandas.DataFrame
      A DataFrame with the calculated statistics (minimum, maximum, and average scores).
    """
    demographics_keys = ('age', 'gender', 'location', 'studytime', 'tutoring', 'stu_group')

    try:
        title = ''
        for k, v in filters.items():
            if k not in demographics_keys:
                raise ValueError(f"Invalid attribute '{k}' provided.")
            if isinstance(v, int):
                data = data[data[k] == v]
                title += f" {k.capitalize()}: {v},"
            else:
                data = data[data[k].str.lower() == str(v).lower()]
                title += f" {k.capitalize()}: {v.capitalize()},"
        
        if data.empty:
            raise ValueError("No data found for the specified filters.")
        
    except ValueError as ve:
        print(f"Error: {ve}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

    if groupby:
        if groupby not in demographics_keys:
            print(f"Groupby column '{groupby}' is not valid.")
            return None
        
        grouped_data = data.groupby(groupby)[subjects].mean()
        stats_df = pd.DataFrame({
            'Subject': subjects,
            'Minimum Score': grouped_data.min(),
            'Maximum Score': grouped_data.max(),
            'Average Score': grouped_data.mean()
        })

        if plot:
            overall_min = stats_df['Minimum Score'].min()
            overall_max = stats_df['Maximum Score'].max()
            overall_mean = stats_df['Average Score'].mean()

            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axhline(overall_min, color='red', linestyle='--', linewidth=1.5, label=f"Overall Min: {overall_min:.2f}")
            ax.axhline(overall_max, color='green', linestyle='--', linewidth=1.5, label=f"Overall Max: {overall_max:.2f}")
            ax.axhline(overall_mean, color='blue', linestyle='--', linewidth=1.5, label=f"Overall Avg: {overall_mean:.2f}")

            grouped_data.T.plot(kind='bar', colormap='coolwarm', alpha=0.7, ax=ax)
            if(len(filters) == 0):
                plt.title(f"Average Subject Scores by {groupby.capitalize()}", fontsize=14)
            else:
                plt.title(f"Average Subject Scores by {groupby.capitalize()} with Filters: {title.strip(',')}", fontsize=14)
            plt.xlabel('Subjects', fontsize=12)
            plt.ylabel('Mean Score', fontsize=12)
            plt.xticks(rotation=45)
            plt.legend(title=groupby.capitalize())
            plt.tight_layout()
            plt.show()
        else:
            return stats_df
    else:
        subject_scores = data[subjects]
        stats_df = pd.DataFrame({
            'Subject': subjects,
            'Minimum Score': subject_scores.min(),
            'Maximum Score': subject_scores.max(),
            'Average Score': subject_scores.mean()
        })

        if plot:
            overall_min = stats_df['Minimum Score'].min()
            overall_max = stats_df['Maximum Score'].max()
            overall_mean = stats_df['Average Score'].mean()

            fig, ax = plt.subplots(figsize=(12, 8))
            ax.axhline(overall_min, color='red', linestyle='--', linewidth=1.5, label=f"Overall Min: {overall_min:.2f}")
            ax.axhline(overall_max, color='green', linestyle='--', linewidth=1.5, label=f"Overall Max: {overall_max:.2f}")
            ax.axhline(overall_mean, color='blue', linestyle='--', linewidth=1.5, label=f"Overall Avg: {overall_mean:.2f}")

            sns.barplot(
                x='Subject',
                y='Average Score',
                data=stats_df,
                palette='coolwarm',
                ci=None,
                ax=ax
            )

            for i, row in stats_df.iterrows():
                plt.text(
                    i, row['Average Score'] + 0.5,
                    f"{row['Average Score']:.1f}",
                    ha='center',
                    fontsize=10
                )
            if(len(filters) == 0):
                plt.title(f"Average Subject Scores", fontsize=14)
            else:
                plt.title(f"Average Subject Scores with Filters: {title.strip(',')}", fontsize=14)
            plt.xlabel('Subjects', fontsize=14)
            plt.ylabel('Average Score', fontsize=14)
            plt.tight_layout()
            plt.xticks(rotation=45)
            plt.show()
        else:
            return stats_df



def analyze_studytime_by_demographics(data,column,plot=True,**Filters):
    """
    Analyzes the distribution of study time percentages across a specified demographic column.
    Optionally displays a plot or returns the grouped data.
    Parameters:
    ----------
    column : str
        - 'gender'
        - 'age'
        - 'location'
        - 'school_type'
        - 'stu_group'
    
    plot : bool, optional, default=True
        If True, displays a line graph showing the percentage distribution.
        If False, returns a DataFrame with grouped data.

    Returns:
    -------
    None or pandas.DataFrame
        - If plot=True: Displays the graph and returns None.
        - If plot=False: Returns a DataFrame containing the grouped data:
            - column: Unique values of the specified demographic column.
            - studytime: Study time groups (e.g., 1, 2, 3, 4).
            - count: The number of students in each group.
            - percentage: The percentage of students in each group.

    Raises:
    ------
    ValueError
        If the `column` is not one of the valid options.
    """
    title=''
    demographics_keys = ('age', 'gender', 'location', 'studytime', 'tutoring', 'stu_group')
    for k, v in Filters.items():
        if k not in demographics_keys:
            print(f"Invalid attribute '{k}' provided.")
        if isinstance(v, int):
            data = data[data[k] == v]
            title += f" {k.capitalize()}: {v},"
        else:
            data = data[data[k].str.lower() == str(v).lower()]
            title += f" {k.capitalize()}: {v.capitalize()},"
    if column not in ('gender', 'age', 'location', 'school_type', 'stu_group'):
        print("Enter a valid column from: 'gender', 'age', 'location', 'school_type', 'stu_group'")
        return None
    data = data.groupby([column, 'studytime']).size().reset_index(name='count')

    total_counts = data.groupby(column)['count'].transform('sum')
    data['percentage'] = (data['count'] / total_counts) * 100

    plt.figure(figsize=(10, 6))

    for location in data[column].unique():
        subset = data[data[column] == location]
        plt.plot(
            subset['studytime'],
            subset['percentage'],
            marker='o',
            label=location,
            linewidth=1
        )

    column = column.capitalize()
    if len(Filters) == 0:
        plt.title(f'Percentage of Study Time by {column}', fontsize=16)
    else:
        plt.title(f'Percentage of Study Time by {column} & filters: {title[:-1]}', fontsize=16)
    plt.xlabel('Study Time', fontsize=12)
    plt.ylabel('Percentage (%)', fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.legend(title=column, fontsize=12)
    plt.xticks(ticks=sorted(data['studytime'].unique()), labels=sorted(data['studytime'].unique()), fontsize=10)
    plt.tight_layout()
    if plot:
        plt.show()
        return
    return data



def analyze_extracurricular_influence(data,column,plot=True,**filters):
    """
    Analyzes the influence of extracurricular activities on students across different categories 
    (age, location, gender, student group) and shows the percentage of students who participate 
    in extracurricular activities (only 'Yes' participation) for the given column.

    Parameters:
    column : str
        The column name by which to group the data (e.g., 'age', 'location', 'gender', 'stu_group').
  
    plot : bool, optional, default=True
        If True, displays a bar plot. If False, returns the processed data without plotting
    
    """
    required_columns = ['age', 'location', 'gender', 'stu_group', 'extra_curricular_activities']
    title=''
    for k, v in filters.items():
            if k not in required_columns:
                print(f"Invalid attribute '{k}' provided.")
                return
            if isinstance(v, int):
                data = data[data[k] == v]
                title+=" {} : {},".format(k.capitalize(),v)
            else:
                data = data[data[k].str.lower() == str(v).lower()]
                title+=" {} : {},".format(k.capitalize(),v.capitalize())
        
    if data.empty:
        print("No data found for the specified filters.")
        return
    for col in required_columns:
        if col not in data.columns:
            print(f"The dataset must include the column: {col}")
            return

    data = data.groupby([column, 'extra_curricular_activities']).size().reset_index(name='count')

    total_counts = data.groupby(column)['count'].transform('sum')

    data['percentage'] = (data['count'] / total_counts) * 100

    yes_data = data[data['extra_curricular_activities'] == 'Yes']

    if not plot:
        return yes_data
    if(title != ''):
        title = f'Percentage of Students Participating in Extracurricular Activities by {column.capitalize()} & group by {title[:-1]}'
    else:
        title = f'Percentage of Students Participating in Extracurricular Activities by {column.capitalize()}'
    
    plt.figure(figsize=(12, 8))
    ax = sns.barplot(x=column, y='percentage', data=yes_data, palette='Blues', edgecolor='black')

    plt.title(title, fontsize=16)
    plt.xlabel(f'{column.capitalize()}', fontsize=12)
    plt.ylabel('Percentage of Students Participating', fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

    plt.tight_layout()
    plt.show()


def analyze_average_achievements(data,subjects,column, plot=True):
    """
    Analyze average achievements based on a demographic factor.

    Parameters:
        column (str): ('gender', 'age', 'location', 'school_type', 'stu_group').
        plot (bool): Whether to generate a bar plot for the analysis. Default is True.

    Returns:
        pd.DataFrame: A DataFrame summarizing average performance by the demographic factor.
    """
    if column not in ('gender', 'age', 'location', 'school_type', 'stu_group','tutoring'):
        print("Enter a valid column from: 'gender', 'age', 'location', 'school_type', 'stu_group'")
        return None


    performance_summary = data.groupby(column).agg(
        min_score=('total_score', 'min'),
        max_score=('total_score', 'max'),
        average_score=('total_score', 'mean')
    )

    subject_means = data.groupby(column)[subjects].mean()
    performance_summary = performance_summary.join(subject_means)

    if plot:
        sns.set_palette("pastel")
        fig, ax = plt.subplots(figsize=(10, 6))

        performance_summary['average_score'].plot(
            kind='bar', color='skyblue', edgecolor='black', ax=ax
        )

        overall_min = performance_summary['min_score'].min()
        overall_max = performance_summary['max_score'].max()
        overall_mean = performance_summary['average_score'].mean()

        ax.axhline(overall_min, color='red', linestyle='--', linewidth=1.5, label=f"Overall min Score: {overall_min}")
        ax.axhline(overall_max, color='green', linestyle='--', linewidth=1.5, label=f"Overall max Score: {overall_max}")
        ax.axhline(overall_mean, color='blue', linestyle='--', linewidth=1.5, label=f"Overall Average Score: {overall_mean:.2f}")

        plt.title(f"Average Academic Achievements by {column.capitalize()}")
        plt.ylabel("Average Score")
        plt.xlabel(column.capitalize())
        plt.xticks(rotation=45)
        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.show()
        return
    else:
        return performance_summary
















def analyze_location_schooltype(data,location):  
    """ Parameters:  location (str): The location to analyze. Valid options are {'Urban', 'Rural', 'City'}.
    Returns: None: Displays a pie chart of school type distribution for the given location.
    """
    try:
        data = data[data['location'] == location.capitalize()]
        if data.empty: 
            raise ValueError("No data found for the specified location.")
    except ValueError as ve:
        print(f"Error: {ve}")
        print("Please provide a valid location from the set: {'Urban', 'Rural', 'City'}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    else:
        plt.figure(figsize=(8, 6))
        data['school_type'].value_counts().plot(
            kind='pie', 
            autopct='%1.1f%%', 
            startangle=90, 
            colors=['skyblue', 'pink', '#D8765B']
        )
        plt.title(f"School Type Distribution in Location({location.capitalize()})") 
        plt.ylabel('')
        plt.show()



def analysis_attendance_vs_performance(data,  group_by='age',plot=True):
    """
    Analyze the relationship between attendance and performance, grouped by a specified category.

    Parameters:
    -----------
    data : pd.DataFrame
        The input DataFrame containing the data. It must include the following columns:
        - `attendance`: The attendance percentage or score.
        - `total_score`: The performance score to be analyzed.
        - The column specified in the `group_by` argument (default is 'age').

    plot : bool, optional
        If True (default), a line plot is generated showing the relationship between 
        attendance and performance, with each line representing a group defined by `group_by`.

    group_by : str, optional
        The column name in `data` to group by (default is 'age').
        Each unique value in this column will result in a separate line in the plot.

    """
    if(group_by == 'attendance'):
        print("cannot insert attendance, already exists")
        return
    data = data.groupby([group_by, 'attendance'])['total_score'].mean().reset_index()

    if plot:
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=data, x='attendance', y='total_score', hue=group_by, marker='o')
        plt.title('Attendance vs Performance by Age Group')
        plt.xlabel('Attendance')
        plt.ylabel('Performance')
        plt.legend(title=group_by)
        plt.grid(True)
        plt.show()
    else:
        return data


