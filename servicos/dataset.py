import pandas as pd
import os

def atualizar_dataset(sintomas: dict, resultado: dict):
    dataset_path = "dataset.csv"
    columns = ['Febre', 'Diarreia', 'Vomito', 'DorUrinaria', 'Fadiga', 'Malaria', 'Tifoide', 'Colera', 'Meningite', 'InfeccaoUrinaria']
    
    if os.path.exists(dataset_path):
        df = pd.read_csv(dataset_path)
    else:
        df = pd.DataFrame(columns=columns)
    
    new_data = {**sintomas, **{k: 1 if v > 0.5 else 0 for k, v in resultado.items()}}
    df = df.append(new_data, ignore_index=True)
    df.to_csv(dataset_path, index=False)