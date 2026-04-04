import os  # Library for file system operations

# Function to rename a file and append text to its contents
def rename_and_write_file(original_filename, new_filename, text_to_add):
    try:
        os.rename(original_filename, new_filename)  # Rename the file
        with open(new_filename, 'a', encoding='utf-8') as file:  # Open the renamed file in append mode
            file.write(text_to_add + '\n')  # Write the new text to the file
    except FileNotFoundError:
        print(f"Error: '{original_filename}' file not found.")  # Print error if file is not found
    except Exception as e:
        print(f"An error occurred: {e}")  # Print any other exceptions

# Define the variables for file names and text to add
original_filename = 'ornek.txt'  # The name of the file to be renamed
new_filename = 'yeni_dosya.txt'  # The new name for the file
text_to_add = 'This is a new line of text added to the file.'  # The text to be added to the file

# Call the function to rename the file and add new text
rename_and_write_file(original_filename, new_filename, text_to_add)
