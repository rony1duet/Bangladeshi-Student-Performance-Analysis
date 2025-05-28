#!/usr/bin/env python3
"""
Bangladeshi Student Performance Analysis - Demo Script
Group 16 | Academic Year 2024-2025

Quick demonstration of the analysis capabilities.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

def load_data():
    """Load and prepare the dataset."""
    print("📊 Loading Bangladeshi Student Performance Dataset...")
    df = pd.read_csv('data.csv')
    print(f"✅ Dataset loaded: {len(df):,} students, {len(df.columns)} variables")
    return df

def show_basic_stats(df):
    """Display basic dataset statistics."""
    print("\n📈 Dataset Overview:")
    print("-" * 40)
    print(f"Total Students: {len(df):,}")
    print(f"Age Range: {df['age'].min()} - {df['age'].max()} years")
    print(f"Locations: {', '.join(df['location'].unique())}")
    print(f"Student Groups: {', '.join(df['stu_group'].unique())}")
    print(f"Internet Access: {df['internet_access'].value_counts().to_dict()}")

def demo_visualization(df):
    """Create a sample visualization."""
    print("\n📊 Creating Sample Visualization...")
    
    # Internet access by location
    plt.figure(figsize=(10, 6))
    
    # Group data for visualization
    grouped_data = df.groupby(['location', 'internet_access']).size().unstack(fill_value=0)
    
    # Create bar plot
    ax = grouped_data.plot(kind='bar', 
                          figsize=(10, 6),
                          color=['#ff6b6b', '#4ecdc4'],
                          title='Internet Access Distribution by Location')
    
    plt.title('Internet Access Distribution by Location', fontsize=14, fontweight='bold')
    plt.xlabel('Location', fontsize=12)
    plt.ylabel('Number of Students', fontsize=12)
    plt.legend(title='Internet Access', loc='upper right')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Add value labels on bars
    for container in ax.containers:
        ax.bar_label(container, fmt='%d')
    
    plt.show()
    
    print("✅ Visualization generated successfully!")

def demo_analysis(df):
    """Perform sample analysis."""
    print("\n🔍 Sample Analysis: Academic Performance by Internet Access")
    print("-" * 60)
    
    # Define subjects
    subjects = ['english', 'math', 'science', 'social_science', 'ict', 'finance']
    
    # Calculate average scores by internet access
    internet_yes = df[df['internet_access'] == 'Yes'][subjects].mean()
    internet_no = df[df['internet_access'] == 'No'][subjects].mean()
    
    print("Average Scores by Internet Access:")
    print("\nWith Internet Access:")
    for subject, score in internet_yes.items():
        print(f"  {subject.replace('_', ' ').title()}: {score:.1f}")
    
    print("\nWithout Internet Access:")
    for subject, score in internet_no.items():
        print(f"  {subject.replace('_', ' ').title()}: {score:.1f}")
    
    # Calculate differences
    print("\nPerformance Difference (With - Without Internet):")
    for subject in subjects:
        diff = internet_yes[subject] - internet_no[subject]
        print(f"  {subject.replace('_', ' ').title()}: {diff:+.1f} points")

def main():
    """Main demo function."""
    print("🎓 Bangladeshi Student Performance Analysis - DEMO")
    print("=" * 55)
    
    try:
        # Load data
        df = load_data()
        
        # Show basic statistics
        show_basic_stats(df)
        
        # Demo analysis
        demo_analysis(df)
        
        # Demo visualization
        demo_visualization(df)
        
        # Next steps
        print("\n🚀 Next Steps:")
        print("- Run 'jupyter notebook main.ipynb' for interactive analysis")
        print("- Explore custom filtering and advanced visualizations")
        print("- Check the '/Report' folder for detailed findings")
        
    except FileNotFoundError:
        print("❌ Error: data.csv not found!")
        print("Please ensure you're in the project directory.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
