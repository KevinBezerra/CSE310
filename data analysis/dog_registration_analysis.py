import pandas as pd
import matplotlib.pyplot as plt

def load_all_files():
    """
    Loads the three yearly dog registration files and the breed mapping file.
    Returns them as four separate dataframes.
    """
    print("Loading files...")
    
    # Load the datasets using standard comma separation
    df_2015 = pd.read_csv("20151001hundehalter.csv")
    df_2016 = pd.read_csv("20160307hundehalter.csv")
    df_2017 = pd.read_csv("20170308hundehalter.csv")
    df_map = pd.read_csv("zuordnungstabellehunderassehundetyp.csv")
    
    # Add a year column to each dataframe before combining them
    df_2015["YEAR"] = 2015
    df_2016["YEAR"] = 2016
    df_2017["YEAR"] = 2017
    
    return df_2015, df_2016, df_2017, df_map

def clean_and_format_data(df_15, df_16, df_17, map_df):
    """
    Combines the yearly data, merges the breed map, translates German
    column names to English, and removes rows missing critical data.
    """
    print("Cleaning and formatting data...")
    
    # CONVERT/COMBINE: Stick all three years together into one big dataset
    all_years = pd.concat([df_15, df_16, df_17], ignore_index=True)
    
    # FILTER: Drop any rows where the breed is missing
    all_years = all_years.dropna(subset=["RASSE1"])
    
    # Clean up whitespace on the join keys just to be safe
    all_years["RASSE1"] = all_years["RASSE1"].str.strip()
    map_df["HUNDERASSE"] = map_df["HUNDERASSE"].str.strip()
    
    # CONVERT/MERGE: Attach the dog type (large, small, etc.) using the map file
    merged_data = all_years.merge(
        map_df[["HUNDERASSE", "HUNDERASSENTYP"]], 
        left_on="RASSE1", 
        right_on="HUNDERASSE", 
        how="left"
    )
    
    # CONVERT: Rename the German columns to English so it's easier to read
    merged_data = merged_data.rename(columns={
        "ALTER": "owner_age",
        "STADTKREIS": "district",
        "RASSE1": "breed",
        "HUNDERASSENTYP": "dog_size_type",
        "YEAR": "year"
    })
    
    return merged_data

def answer_question_one(df):
    """
    Question 1: How did the total number of registered dogs change 
    from 2015 to 2017?
    
    Demonstrates: Aggregation (groupby/size)
    """
    print("\n--- QUESTION 1 ---")
    print("Total registered dogs per year:")
    
    # AGGREGATE: Group by the year and count the total rows
    yearly_totals = df.groupby("year").size()
    print(yearly_totals)

def answer_question_two(df):
    """
    Question 2: What were the top 5 most popular dog breeds in 2017?
    
    Demonstrates: Filtering, Sorting, Aggregation (value_counts)
    """
    print("\n--- QUESTION 2 ---")
    print("Top 5 most popular dog breeds in 2017:")
    
    # FILTER: Only look at data from 2017
    data_2017 = df[df["year"] == 2017]
    
    # AGGREGATE & SORT: Count breeds and get the top 5
    top_breeds = data_2017["breed"].value_counts().head(5)
    print(top_breeds)
    
    return top_breeds

def create_visualization(top_breeds_data):
    """
    Additional Requirement: Draw a graph showing some of the results.
    This creates a simple bar chart of the top 5 breeds from Question 2.
    """
    print("\nCreating bar chart...")
    
    # Plot a simple bar chart
    top_breeds_data.plot(kind="bar", color="skyblue", figsize=(10, 6))
    
    # Add labels and a title
    plt.title("Top 5 Dog Breeds in 2017")
    plt.xlabel("Dog Breed")
    plt.ylabel("Number of Dogs")
    
    # Rotate the x-axis text so the breed names are readable
    plt.xticks(rotation=45, ha='right')
    
    # Save the chart as an image file
    plt.tight_layout()
    plt.savefig("simple_breed_chart.png")
    print("Chart saved as 'simple_breed_chart.png'")

def main():
    """
    The main function that runs the entire script in order.
    """
    # 1. Load the data
    df_15, df_16, df_17, map_df = load_all_files()
    
    # 2. Clean and format the data
    clean_data = clean_and_format_data(df_15, df_16, df_17, map_df)
    
    # 3. Answer the analytical questions
    answer_question_one(clean_data)
    top_5_2017 = answer_question_two(clean_data)
    
    # 4. Generate the graph
    create_visualization(top_5_2017)

if __name__ == "__main__":
    main()