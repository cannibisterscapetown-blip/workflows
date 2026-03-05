import pandas as pd
import sys

def filter_rejected_leads(master_file, skipped_file, output_file):
    try:
        print(f"📂 Loading Master List: {master_file}")
        master_df = pd.read_csv(master_file)
        
        print(f"📂 Loading Skipped List: {skipped_file}")
        skipped_df = pd.read_csv(skipped_file)
        
        # We use 'Email Address' as the primary key for removal
        # as it's the most reliable unique identifier across these lists
        rejected_emails = skipped_df['Email Address'].unique()
        
        print(f"🔍 Found {len(rejected_emails)} unique emails in skipped list.")
        
        # Filter master_df
        initial_count = len(master_df)
        purified_df = master_df[~master_df['Email Address'].isin(rejected_emails)]
        final_count = len(purified_df)
        
        removed_count = initial_count - final_count
        print(f"✨ Removed {removed_count} leads from the master list.")
        
        # Save final list
        purified_df.to_csv(output_file, index=False)
        print(f"🚀 Final purified list saved as: {output_file}")
        
        # Double check: Sample check
        if len(rejected_emails) > 0:
            sample_email = rejected_emails[0]
            if sample_email in purified_df['Email Address'].values:
                print(f"⚠️  Warning: Sample rejected email {sample_email} still found in purified list!")
            else:
                print(f"✅ Sample check: Rejected email {sample_email} successfully removed.")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    master = "Cleaned_Leads_Master_March_2026.csv"
    skipped = "XP9TPB_Cleaned_Leads_Master_March_2026_skipped_1772115854.csv"
    output = "Final_Purified_Leads_March_2026.csv"
    filter_rejected_leads(master, skipped, output)
