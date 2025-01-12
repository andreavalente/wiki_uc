import PySimpleGUI as sg
import os
import webbrowser

folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

def populate_tree_data(tree, parent, path):
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            tree_data.Insert(parent, item_path, item, [], icon=folder_icon)
            populate_tree_data(tree, item_path, item_path)
        elif os.path.isfile(item_path):
            if item.endswith('.py'):
                continue
            tree_data.Insert(parent, item_path, item, [], icon=file_icon)

def calculate_folder_depth(path):
    max_depth = 0
    for root, dirs, files in os.walk(path):
        depth = root[len(path):].count(os.sep)
        if depth > max_depth:
            max_depth = depth
    return max_depth

# Definisci i dati dell'albero
tree_data = sg.TreeData()
current_directory = os.path.dirname(os.path.abspath(__file__))
depth = calculate_folder_depth(current_directory)
font = ('Helvetica', 12)
populate_tree_data(tree_data, "", current_directory)

# Definisci il layout della finestra con l'albero
layout = [
    [sg.Button('Collassa Tutto', key='-COLLAPSE-', font=font, visible=False)],
    [sg.Tree(data=tree_data, 
             headings=[], 
             auto_size_columns=True, 
             num_rows=20,
             col0_heading=os.path.basename(current_directory),
             col0_width=40, 
             key='-TREE-', 
             show_expanded=False,
             select_mode=sg.TABLE_SELECT_MODE_BROWSE,
             text_color='#353535',
             header_relief='flat',
             background_color='white',
             enable_events=True,
             click_toggles_select=False,
             font=font)],
    [sg.Button('Ok', font=font), sg.Button('Annulla', font=font)]
]

# Crea la finestra
window = sg.Window('Wiki', layout, font=font)

# Ciclo di eventi per gestire le interazioni con la finestra
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Annulla':
        break
    if event == '-TREE-' and len(values['-TREE-']) > 0:
        selected_item = values['-TREE-'][0]
        if not tree_data.tree_dict[selected_item].children:
            item_path = os.path.join(current_directory, selected_item)
            if os.path.isfile(item_path) and item_path.endswith('.html'):
                webbrowser.open(item_path)
    # if event == '-COLLAPSE-':
    #     window['-TREE-'].Widget.collapse_all()

# Chiudi la finestra
window.close()