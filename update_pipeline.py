
import subprocess
import os

def rodar_etapas():
    base_dir = os.path.dirname(__file__)
    etl_dir = os.path.join(base_dir, "etl")
    db_dir = os.path.join(base_dir, "database")

    print("🔽 Baixando dados...")
    subprocess.run(["python", os.path.join(etl_dir, "extract_comexstat.py")])

    print("🧹 Transformando dados...")
    subprocess.run(["python", os.path.join(etl_dir, "transform_comexstat.py")])

    print("💾 Atualizando banco de dados...")
    subprocess.run(["sqlite3", os.path.join(db_dir, "comex.db"), f".read {os.path.join(db_dir, 'init_db.sql')}"])
    subprocess.run(["python", os.path.join(etl_dir, "load_to_sqlite.py")])

    print("✅ Atualização completa.")

if __name__ == "__main__":
    rodar_etapas()
