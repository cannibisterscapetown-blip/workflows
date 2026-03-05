import pandas as pd
import os
import sys

def process_leads(file_path):
    try:
        # Load the data
        print(f"📂 Loading {file_path}...")
        df = pd.read_excel(file_path)
        
        # Prepare clean columns
        print("🧼 Cleaning and filtering data...")
        clean_df = pd.DataFrame()
        clean_df['First Name'] = df['first_name']
        clean_df['Last Name'] = df['last_name']
        clean_df['Email Address'] = df['email']
        clean_df['Phone Number'] = df['phone_number'].fillna('').astype(str).str.replace('p:', '', regex=False).str.strip()
        clean_df['Address'] = df['city'].fillna('').astype(str).str.strip().str.title()
        clean_df['External ID'] = df['id']
        
        # Remove duplicates based on email
        count_before = len(clean_df)
        clean_df = clean_df.drop_duplicates(subset=['Email Address'])
        count_after = len(clean_df)
        print(f"✨ Removed {count_before - count_after} duplicate email entries.")
        
        # Create output directory for cities
        output_dir = "Organized_Leads_By_City"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        # Group and export
        print("📁 Exporting leads by city...")
        # Get unique cities, excluding empty strings
        cities = clean_df[clean_df['Address'] != '']['Address'].unique()
        
        for city in cities:
            city_df = clean_df[clean_df['Address'] == city]
            # Create safe filename
            safe_city = "".join([c if c.isalnum() else "_" for c in city])
            filename = f"{output_dir}/Leads_{safe_city}.csv"
            city_df.to_csv(filename, index=False)
            
        # Export master cleaned file
        master_file = "Cleaned_Leads_Master_March_2026.csv"
        clean_df.to_csv(master_file, index=False)
        
        print(f"\n✅ Successfully processed {len(clean_df)} leads.")
        print(f"🚀 Master file created: {master_file}")
        print(f"🏙️  Organized files created in: {output_dir}/")
        
    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    process_leads("Leads March 2026.xlsx")
