import os

# Directories and files to explore
directories_to_explore = {
    "backend": ["main.py", "requirements.txt", "run_backtest"],
    "backend/strategies": [
        "__init__.py",
        "moving_average_crossover.py",
        "sma_strategy.py",
        "rsi_strategy.py"
    ],
    "backend/backtesting": [
        "__init__.py",
        "backtester.py",
        "performance.py"
    ],
    "backend/data": [
        "__init__.py",
        "data_loader.py"
    ],
    "backend/utils": [
        "__init__.py",
        "helpers.py"
    ],
    "backend/config": [
        "settings.py"
    ],
    "frontend/src": ["App.js", "index.js", "apiService.js"],
    "frontend/src/components": [
        "Chart.js",
        "Markets.js",
        "PriceTicker.js",
        "fetchMarkets.js",
        "Dashboard.js",
        "Header.js",
        "LiveData.js",
        "MarketList.js",
        "MarketSelector.js",
        "SettingsPanel.js"
    ]
}

# Function to read the content of files
def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# Function to explore directories and gather file contents
def explore_directories(base_dir, directories):
    file_contents = {}
    for directory, files in directories.items():
        full_dir_path = os.path.join(base_dir, directory)
        if os.path.exists(full_dir_path):
            for file_name in files:
                full_file_path = os.path.join(full_dir_path, file_name)
                if os.path.isfile(full_file_path):
                    content = read_file_content(full_file_path)
                    file_contents[full_file_path] = content
                else:
                    print(f"File {full_file_path} does not exist.")
        else:
            print(f"Directory {full_dir_path} does not exist.")
    return file_contents

# Function to save the gathered contents into a summary file
def save_summary(file_contents, output_file="filtered_code_summary.txt"):
    with open(output_file, 'w') as summary_file:
        for file_path, content in file_contents.items():
            summary_file.write(f"===== {file_path} =====\n")
            summary_file.writelines(content)
            summary_file.write("\n\n")

def main():
    base_dir = os.getcwd()  # Use the current directory as base
    file_contents = explore_directories(base_dir, directories_to_explore)
    save_summary(file_contents)

if __name__ == "__main__":
    main()
