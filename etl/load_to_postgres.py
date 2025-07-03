import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "comex_multianual_tratado.csv")

def carregar_para_postgres():
    df = pd.read_csv(CSV_PATH)
    engine = create_engine(DATABASE_URL)
    with engine.begin() as conn:
        df.to_sql("movimentacoes", conn, if_exists="replace", index=False)
    print("✅ Dados carregados com sucesso no PostgreSQL!")

if __name__ == "__main__":
    carregar_para_postgres()