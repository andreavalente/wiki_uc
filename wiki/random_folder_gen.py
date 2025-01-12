import os
import random
import shutil

def create_table_header(columns):
    return f"""
        <thead>
            <tr>
                {" ".join([f"<th>{chr(65 + i)}</th>" for i in range(columns)])}
            </tr>
        </thead>
    """

def create_table_body(rows, columns):
    return f"""
        <tbody>
            {" ".join([f"{create_table_row(columns)}" for _ in range(rows)])}
        </tbody>
    """

def create_table_row(columns):
    return f"""
        <tr>
            {" ".join([f"<td>{random.randint(1, 100)}</td>" for _ in range(columns)])}
        </tr>
    """

def create_style():
    return """
        table {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid black;
            padding: 5px;
        }
        td {
            text-align: right;
        }
    """

def create_html_content(counter):
    columns = random.randint(5, 10)
    rows = random.randint(10, 20)

    return f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Use Case {counter}</title>
        </head>
        <style>
            {create_style()}
        </style>
        <body>
            <h1>Use Case {counter}</h1>
            <table width="100%">
            {create_table_header(columns)}
            {create_table_body(rows, columns)}
        </body>
        </html>
    """

def create_html_file(base_path):
    global counter
    html_file_path = os.path.join(base_path, f"use_case_{counter}.html")
    with open(html_file_path, "w") as html_file:
        html_file.write(create_html_content(counter))
        print(f"File HTML creato: {html_file_path}")
    counter += 1

def create_subfolders(base_path, level):
    if level > 3:
        create_html_file(base_path)
        return

    num_subfolders = random.randint(1, 5)
    for i in range(1, num_subfolders + 1):
        subfolder_name = f"{os.path.basename(base_path)}_{i}"
        subfolder_path = os.path.join(base_path, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)
        print(f"Sottocartella creata: {subfolder_path}")
        # Creazione di sottocartelle all'interno della sottocartella appena creata
        create_subfolders(subfolder_path, level + 1)
    return

# Funzione per cancellare tutte le cartelle e i file all'interno di una directory
def delete_all_subfolders(base_path):
    for root, dirs, _ in os.walk(base_path, topdown=False):
        for name in dirs:
            shutil.rmtree(os.path.join(root, name))

counter = 1
# Percorso della cartella in cui è posizionato lo script
current_directory = os.path.dirname(os.path.abspath(__file__))
# Cancellazione di tutte le cartelle e i file nella directory corrente
delete_all_subfolders(current_directory)
# Stampa delle cartelle trovate e creazione delle sottocartelle
create_subfolders(current_directory, 0)