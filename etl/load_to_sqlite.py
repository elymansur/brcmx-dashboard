
import os
import sqlite3
import pandas as pd

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "comex_multianual_tratado.csv")
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "comex.db")

def carregar_dados():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_csv(DATA_PATH)
    df.to_sql("movimentacoes", conn, if_exists="replace", index=False)
    conn.close()
    print("Dados carregados com sucesso no banco comex.db")

if __name__ == "__main__":
    carregar_dados()
