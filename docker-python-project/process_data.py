import pandas as pd
import sys
import os

def process_csv_file(filepath='data.csv'):
    """
    Process CSV file and display various statistics
    """
    try:
        # Read the CSV file
        print(f"📊 Reading data from: {filepath}")
        df = pd.read_csv(filepath)
        
        print("\n" + "="*50)
        print("📈 DATA PROCESSING REPORT")
        print("="*50)
        
        # Display basic information
        print(f"\n📋 Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns")
        
        print("\n📄 First 5 rows:")
        print(df.head())
        
        print("\n🔍 Column Information:")
        print(df.info())
        
        # Basic statistics
        print("\n📊 Basic Statistics:")
        print(df.describe())
        
        # Additional analysis
        print("\n🎯 Additional Analysis:")
        print("-" * 30)
        
        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        for col in df.columns:
            if col in numeric_cols:
                print(f"\n📈 Column: {col}")
                print(f"   Mean: {df[col].mean():.2f}")
                print(f"   Median: {df[col].median():.2f}")
                print(f"   Min: {df[col].min():.2f}")
                print(f"   Max: {df[col].max():.2f}")
                print(f"   Std Dev: {df[col].std():.2f}")
            else:
                unique_values = df[col].nunique()
                print(f"\n📊 Column: {col}")
                print(f"   Type: Categorical")
                print(f"   Unique values: {unique_values}")
                print(f"   Top value: {df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A'}")
        
        # Group by analysis if 'department' exists
        if 'department' in df.columns and 'salary' in df.columns:
            print("\n👥 Department-wise Analysis:")
            print("-" * 30)
            dept_stats = df.groupby('department')['salary'].agg(['mean', 'median', 'count'])
            dept_stats.columns = ['Avg Salary', 'Median Salary', 'Employee Count']
            print(dept_stats)
        
        print("\n" + "="*50)
        print("✅ Processing Complete!")
        print("="*50)
        
    except FileNotFoundError:
        print(f"❌ Error: File '{filepath}' not found!")
        print(f"Current directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir('.')}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if a file argument was provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = 'data.csv'
    
    process_csv_file(filename)
