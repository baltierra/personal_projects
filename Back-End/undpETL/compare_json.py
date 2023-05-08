import json

def compare_json_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)
        if json1 == json2:
            print("The two JSON files are identical.")
        else:
            print("The two JSON files are not identical.")

# Example usage
compare_json_files('AFGfinal.json', 'CountryDataCleanedWithStatus/AFG.json')