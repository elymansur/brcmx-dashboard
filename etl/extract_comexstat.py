
import os
import requests

BASE_URL = "https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/{fluxo}_{ano}_M{mes:02d}.csv"
SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
ANOS = [2023, 2024, 2025]
FLUXOS = ["EXP", "IMP"]

def download_comexstat():
    os.makedirs(SAVE_DIR, exist_ok=True)
    for ano in ANOS:
        for fluxo in FLUXOS:
            for mes in range(1, 13):
                url = BASE_URL.format(fluxo=fluxo, ano=ano, mes=mes)
                filename = f"{fluxo}_{ano}_M{mes:02d}.csv"
                filepath = os.path.join(SAVE_DIR, filename)

                print(f"Baixando {filename}...")
                response = requests.get(url)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    print(f"Salvo em: {filepath}")
                else:
                    print(f"Erro ao baixar {filename}: Status {response.status_code}")

if __name__ == "__main__":
    download_comexstat()
