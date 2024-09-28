import pandas as pd
import re

def preprocess_telegram_data(file_path):
    # Load your DataFrame
    df = pd.read_csv(file_path)
    
    # Check for NaN values in the 'Message' column
    print("Checking for NaN values in the 'Message' column:")
    nan_count = df['Message'].isnull().sum()
    print(f"Number of NaN values in 'Message' column: {nan_count}")
    
    # Drop NaN values from the 'Message' column
    df = df.dropna(subset=['Message'])
    
    # Function to remove emojis and special characters
    def clean_message(text):
        if pd.isnull(text):
            return text
        # Remove emojis and special characters, keeping only Amharic characters, numbers, and non-English text
        text = re.sub(r'[^\w\s፩-፺ጀ-ፀ0-9]', '', text)  # Updated character range to exclude special characters
        return text.strip()

    # Function to remove English words from a message
    def remove_english_words(text):
        if pd.isnull(text):
            return text
        # Remove all English words (a-z, A-Z) but keep other languages like Amharic and numbers
        return re.sub(r'[a-zA-Z]+', '', text).strip()

    # Clean the 'Message' column by removing special characters
    df['Cleaned_Message'] = df['Message'].apply(clean_message)

    # Remove English words from the 'Cleaned_Message' column
    df['Cleaned_Message'] = df['Cleaned_Message'].apply(remove_english_words)

    # Tokenize the cleaned message (split into words)
    df['Tokens'] = df['Cleaned_Message'].apply(lambda x: x.split() if pd.notnull(x) else [])

    # Selecting relevant columns and structuring the data for analysis
    structured_data = df[['Channel Title', 'Channel Username', 'ID', 'Date', 'Cleaned_Message', 'Tokens']]
    
    # Saving the cleaned data to a CSV file
    output_path = file_path.replace('.csv', '_cleaned.csv')  # Change output filename
    structured_data.to_csv(output_path, index=False)
    
    print(f"Cleaned data saved successfully to {output_path}")

    return structured_data



