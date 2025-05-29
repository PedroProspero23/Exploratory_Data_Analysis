# Bibliotecas
import pandas as pd

# Caminho do arquivo CSV exportado da UN Comtrade
arquivo = "C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Exploratory_Data_Analysis/TradeData_5_29_2025_9_6_47.csv"

# Leitura inicial do CSV
df = pd.read_csv(arquivo)

# Visualizar as primeiras linhas
print(df.head())

# Verificar nomes das colunas
print(df.columns)

# Verificar os tipos de dados de cada coluna 
print(df.dtypes)

# Selecionar colunas úteis para análise
colunas_uteis = [
    "refPeriodId",     # Ano de referência
    "reporterCode",    # Código do país exportador
    "partnerCode",     # Código do país importador
    "flowCode",        # Código do tipo de fluxo (provavelmente 2 = Exportação)
    "cmdCode",         # Código da commodity (ex: 1201 para soja)
    "qtyUnitAbbr",     # Unidade da quantidade
    "fobvalue",        # Valor FOB
    "cifvalue"         # Valor CIF
]

# Criar DataFrame reduzido
df_reduzido = df[colunas_uteis].copy()

# Renomear colunas para facilitar leitura
df_reduzido.rename(columns={
    "refPeriodId": "Year",
    "reporterCode": "Exporting Country",
    "partnerCode": "Importing Country",
    "flowCode": "Flow",
    "cmdCode": "Commodity Code",
    "qtyUnitAbbr": "Unity",
    "fobvalue": "value_fob_usd",
    "cifvalue": "value_cif_usd"
}, inplace=True)


# Verificar resultado
print(df_reduzido.head())

# Garantir que o ano esteja como inteiro (corrigido)
df_reduzido["Year"] = df_reduzido["Year"].astype(int)

# Verificar valores nulos por coluna
print(df_reduzido.isnull().sum())


# 📌 Diagnóstico detalhado de valores 0

# Total de registros com Unity == 0
total_zeros = (df_reduzido["Unity"] == 0).sum()
print(f"🔴 Total geral de registros com Unity = 0: {total_zeros}\n")

# Quebras por país exportador
print("📍 Quantidade de registros com Unity = 0 por país exportador:")
print(df_reduzido[df_reduzido["Unity"] == 0]["Exporting Country"].value_counts(), "\n")

# Quebras por ano
print("📍 Quantidade de registros com Unity = 0 por ano:")
print(df_reduzido[df_reduzido["Unity"] == 0]["Year"].value_counts(), "\n")

# Cruzamento por país e ano
print("📍 Cruzamento: país exportador x ano com Unity = 0")
print(df_reduzido[df_reduzido["Unity"] == 0].groupby(["Exporting Country", "Year"]).size())

# 📊 Verificar proporção de valores 0 em "Unity"
zeros_unity = (df_reduzido["Unity"] == 0).sum()
total = len(df_reduzido)
proporcao = (zeros_unity / total) * 100

print(f"\n🔎 Foram encontrados {zeros_unity} registros com 'Unity' igual a 0 ({proporcao:.2f}%).")

# ✅ Corrigir se < 20%
if proporcao < 20:
    print("✅ Corrigindo os valores de 'Unity' com base na média por país exportador...")

    # Criar cópia da coluna
    df_reduzido["Unity_adjusted"] = df_reduzido["Unity"]

    # Calcular médias por país, excluindo zeros
    medias_por_pais = df_reduzido[df_reduzido["Unity"] > 0].groupby("Exporting Country")["Unity"].mean()

    # Função para substituir
    def substituir_zero(row):
        if row["Unity_adjusted"] == 0:
            return medias_por_pais[row["Exporting Country"]]
        return row["Unity_adjusted"]

    # Aplicar substituição
    df_reduzido["Unity_adjusted"] = df_reduzido.apply(substituir_zero, axis=1)
    print("✅ Substituição concluída.")
else:
    print("⚠️ Proporção de zeros em 'Unity' acima do limite. Nenhuma substituição aplicada.")


# Verificar quantidade de linhas duplicadas (linhas idênticas)
duplicatas = df_reduzido.duplicated().sum()
print(f"🔍 Total de linhas duplicadas: {duplicatas}")

# Mostrar as duplicatas (para inspecionar antes de remover)
print(df_reduzido[df_reduzido.duplicated()])

# Remover duplicatas mantendo apenas a primeira ocorrência
df_corrigido = df_reduzido.drop_duplicates()
print("✅ Duplicatas removidas com sucesso!")

# Garantir que a versão final salva esteja corrigida e sem duplicatas
df_corrigido = df_reduzido.drop_duplicates().copy()

# Salvar CSV final
df_corrigido.to_csv("C:/Users/pedro/OneDrive/Área de Trabalho/Códigos/Exploratory_Data_Analysis/clean_data_soyUNComtrade.csv", index=False)
print("✅ Arquivo salvo com sucesso!")
