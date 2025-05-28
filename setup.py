#!/usr/bin/env python3
"""
Bangladeshi Student Performance Analysis - Setup Script
Group 16 | Academic Year 2024-2025

This script sets up the analysis environment and validates the dataset.
"""

import os
import sys
import pandas as pd

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'seaborn', 'jupyter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    
    print("\n🎉 All dependencies are installed!")
    return True

def validate_dataset():
    """Validate the dataset file and structure."""
    dataset_path = 'data.csv'
    
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset file '{dataset_path}' not found!")
        return False
    
    try:
        df = pd.read_csv(dataset_path)
        print(f"✅ Dataset loaded successfully")
        print(f"📊 Records: {len(df):,}")
        print(f"📋 Columns: {len(df.columns)}")
        
        # Check key columns
        required_columns = [
            'age', 'gender', 'location', 'internet_access', 
            'english', 'math', 'science', 'stu_group'
        ]
        
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            print(f"⚠️  Missing columns: {missing_cols}")
            return False
        
        print("✅ All required columns present")
        return True
        
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return False

def main():
    """Main setup function."""
    print("🎓 Bangladeshi Student Performance Analysis - Setup")
    print("=" * 50)
    
    # Check dependencies
    print("\n1. Checking Dependencies...")
    deps_ok = check_dependencies()
    
    # Validate dataset
    print("\n2. Validating Dataset...")
    data_ok = validate_dataset()
    
    # Final status
    print("\n" + "=" * 50)
    if deps_ok and data_ok:
        print("🚀 Setup Complete! Ready to run analysis.")
        print("\nNext steps:")
        print("1. Open: jupyter notebook main.ipynb")
        print("2. Follow the interactive menu for analysis")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
