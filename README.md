# Plataforma Comex (Exportações e Importações Brasil 2023)

Dashboard interativo de análise de dados de comércio exterior do Brasil (base ComexStat), com filtros por NCM, UF, país, mês, valor FOB, peso líquido e tipo de fluxo (importação/exportação).

### 🚀 Como usar (Streamlit Cloud)

1. Crie um repositório no GitHub e envie esses arquivos.
2. Acesse https://streamlit.io/cloud e conecte seu repositório.
3. Defina o caminho do arquivo principal como: `dashboard/app_streamlit.py`
4. O app será carregado automaticamente!

### 📂 Estrutura do projeto

- `etl/` — Scripts de extração, transformação e carga no banco
- `database/` — Script SQL + banco SQLite
- `dashboard/` — Dashboard Streamlit
- `data/` — Arquivos CSV baixados (ignorar no repositório)