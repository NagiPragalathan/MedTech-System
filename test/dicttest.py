import ast
import re

# Example string
string = """ hello {'key1': "value1", 'key2': { }'value2'} """

# Find the dictionary part using regular expression
match = re.search(r"\{.*\}", string)

if match:
    # Extract the dictionary string
    dictionary_string = match.group()
    
    # Convert string to dictionary
    dictionary = ast.literal_eval(dictionary_string)

    print(dictionary)  # Output: {'key1': 'value1', 'key2': 'value2'}
else:
    print("No dictionary found in the string.")
