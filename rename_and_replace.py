import os

def rename_and_replace(directory, search_word, replace_word):
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            # Rename file if it contains the search word
            if search_word in file_name:
                new_file_name = file_name.replace(search_word, replace_word)
                os.rename(os.path.join(root, file_name), os.path.join(root, new_file_name))
                file_name = new_file_name

            # Replace content inside the file
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
            new_content = content.replace(search_word, replace_word)
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
                file.write(new_content)

# Usage
directory = 'path_to_your_directory'  # Replace with the path to your directory
search_word = 'test'
replace_word = 'now'
rename_and_replace(directory, search_word, replace_word)
