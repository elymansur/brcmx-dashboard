
import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def transformar_dados():
    arquivos = [f for f in os.listdir(DATA_DIR) if f.endswith(".csv")]
    dfs = []

    for arquivo in arquivos:
        path = os.path.join(DATA_DIR, arquivo)
        fluxo = "exportacao" if "EXP" in arquivo else "importacao"
        df = pd.read_csv(path, sep=';', encoding='latin1')
        df = df[['CO_ANO', 'CO_MES', 'CO_NCM', 'NO_NCM', 'SG_UF_NCM', 'CO_PAIS', 'NO_PAIS', 'KG_LIQUIDO', 'VL_FOB']]
        df.columns = ['ano', 'mes', 'ncm', 'descricao_ncm', 'uf', 'pais_id', 'pais', 'peso_liquido', 'valor_fob']
        df["tipo_fluxo"] = fluxo
        dfs.append(df)

    df_final = pd.concat(dfs, ignore_index=True)
    output_path = os.path.join(DATA_DIR, "comex_multianual_tratado.csv")
    df_final.to_csv(output_path, index=False)
    print(f"Dados tratados salvos em: {output_path}")

if __name__ == "__main__":
    transformar_dados()
