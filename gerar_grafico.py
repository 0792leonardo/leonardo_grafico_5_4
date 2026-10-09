"""
Gráf﻿ico 5.4 – MP10 – Evolução das médias móveis – RMSP
================================================================================

Este script gera um gráfico interativo em HTML mostrando a evolução temporal
das médias móveis de MP₁₀ (material particulado) para estações
de monitoramento na região RM de São Paulo.

O gráfico exibe:
- Séries temporais para cada estação (2000-2025)
- Dados carregados de um arquivo CSV
- Layout otimizado para visualização e análise

Região de estudo: Região Metropolitana de São Paulo
Período de dados: 2005 a 2025 (exibição: 2000-2025)

Autor: Leonardo Rocha
Data: 2026-09-10
Versão: 1.0.0
"""
# =============================================================================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================

from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# ============================================================================
# 1. CARREGAMENTO E TRATAMENTO DOS DADOS
# ============================================================================

# Caminho do arquivo CSV usando pathlib (mais robusto que strings)
CSV = Path("Dd_grafico_5_4.csv")

# Lê o arquivo CSV com configurações específicas:
# - sep=None: detecta automaticamente o separador (vírgula, ponto-e-vírgula, etc.)
# - engine="python": usa o parser Python para maior flexibilidade
# - encoding="utf-8-sig": lida com arquivos UTF-8 com BOM (comum em Excel)
df = pd.read_csv(CSV, sep=None, engine="python", encoding="utf-8-sig")

# Converte colunas numéricas que possam estar em formato brasileiro (vírgula decimal)
# para formato padrão (ponto decimal) e tipo numérico
for c in ["med_int", "Per_90", "Per_10"]:
    df[c] = pd.to_numeric(
        df[c].astype(str).str.replace(",", ".", regex=False),  # Troca vírgula por ponto
        errors="coerce"  # Valores inválidos viram NaN
    )

# Remove linhas sem valor em "serie" (eixo X) e cria cópia independente
df = df.dropna(subset=["serie"]).copy()

# Garante que a coluna "serie" seja sempre string (evita problemas no eixo X)
df["serie"] = df["serie"].astype(str)

# =============================================================================
# CRIAÇÃO DO GRÁFICO
# =============================================================================

# Inicializa uma figura vazia
fig = go.Figure()


# -----------------------------------------------------------------------------
# TRAÇO 1: PERCENTIL 90 (BASE PARA PREENCHIMENTO)
# -----------------------------------------------------------------------------
# Este traço é adicionado primeiro para servir como base para o preenchimento
# da área entre os percentis. Ele não é visível (width=0) e não aparece na legenda.
fig.add_trace(go.Scatter(
    x=df["serie"],                            # Eixo X: séries/períodos
    y=df["Per_90"],                           # Eixo Y: valores do percentil 90
    mode="lines",                             # Modo: apenas linhas
    line=dict(
        color="rgba(255,255,255,0)",          # Cor transparente (invisível)
        width=0                               # Largura zero
    ),
    showlegend=False,                         # Não mostra na legenda
    hoverinfo="skip"
))


# -----------------------------------------------------------------------------
# TRAÇO 2: PERCENTIL 10 (ÁREA SOMBREADA)
# -----------------------------------------------------------------------------
# Este traço cria a área sombreada entre P10 e P90 usando fill="tonexty"
# O preenchimento é branco semitransparente para contraste com o fundo azul
fig.add_trace(go.Scatter(
    x=df["serie"],                            # Eixo X: séries/períodos
    y=df["Per_10"],                           # Eixo Y: valores do percentil 10
    mode="lines",                             # Modo: apenas linhas
    line=dict(
        color="rgba(255,255,255,0)",          # Cor transparente
        width=0                               # Largura zero
    ),
    fill="tonexty",                           # Preenche entre este traço e o anterior (Per_90)
    fillcolor="#dce6f2",       # Na cor Azul claro
    name="Percentis 10/90",                   # Nome na legenda
    
    # Dados customizados para o tooltip (valores do P90)
    # Permite exibir tanto P10 quanto P90 no mesmo tooltip
    customdata=df["Per_90"],
    
    # Template personalizado do tooltip
    # %{customdata} acessa os valores customizados (P90)
    hovertemplate=(
        "<b>Percentis 10/90</b><br>"          # Título em negrito
        "P10: %{y:.0f} µg/m³<br>"             # Valor do P10 com 1 decimal
        "P90: %{customdata:.0f} µg/m³<extra></extra>"  # Valor do P90
    )
))

# ----------------------------------------------------------------------------
# TRACE 3: Linha principal - Média Móvel de 3 anos
# ----------------------------------------------------------------------------
fig.add_trace(go.Scatter(
    x=df["serie"], y=df["med_int"],
    mode="lines+markers",
    name="Média Móvel (3 anos)",
    line=dict(color="#111111", width=3),         # Linha preta grossa
    marker=dict(
        color="#111111",          # Marcador preto
        size=9,
        symbol="circle",
        line=dict(color="#1D6FA5", width=2)  # Borda azul (destaque visual)
    ),
    # Template do tooltip com formatação numérica (sem casas decimais)
    hovertemplate=(
        "<b>Média Móvel (3 anos)</b><br>"
        "%{y:.0f} µg/m³<extra></extra>"
    )
))

# ============================================================================
# 3. CONFIGURAÇÃO DO LAYOUT
# ============================================================================

fig.update_layout(
    # Template base e dimensões
    template="plotly_white",
    height=760,
    margin=dict(l=105, r=35, t=25, b=155),  # Margens (inferior grande p/ legenda)
    
    paper_bgcolor="#FFFFFF",   # Fundo externo Branco
    plot_bgcolor="#FFFFFF",    # Fundo interno da área do gráfico Branco
    
    # Modo hover unificado (mostra todas as séries do mesmo X)
    hovermode="x unified",
    
    # Fonte global do gráfico
    font=dict(family="Arial, sans-serif", size=14, color="#555555"),
    
    # Configuração do eixo X
    xaxis=dict(
        tickangle=-45,               # Rótulos inclinados para melhor leitura
        showgrid=False,              # Sem grid vertical (visual limpo)
        showline=True,               # Linha do eixo visível
        linecolor="#B8B8B8",         # Cinza claro
        ticks="inside",               # Marcadores dentro do eixo
        range=[-0.0, len(df) - 0.0],          # COLA o primeiro ponto no eixo Y
        categoryorder="array",                # Mantém a ordem original dos dados
        categoryarray=df["serie"].tolist()    # Garante a ordem das categorias
    ),
    
    # Configuração do eixo Y
    yaxis=dict(
        title="MP₁₀ (µg/m³)",
        range=[0, 80],               # Limite fixo do eixo Y
        dtick=10,                    # Intervalos de 10 em 10
        showgrid=False,              # Sem grid horizontal
        zeroline=False,              # Sem linha no zero
        showline=True,
        linecolor="#B8B8B8",
        ticks="outside"               # Marcadores fora do eixo
    ),
    
    # Legenda horizontal centralizada abaixo do gráfico
    legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.16,
        xanchor="center",
        x=0.5,
        font=dict(size=13)
    )
)

# ============================================================================
# 4. EXPORTAÇÃO
# ============================================================================

fig.write_html(
    "index.html",
    include_plotlyjs=True,      # Plotly embutido (arquivo autônomo)
    full_html=True,             # Documento HTML completo
    config={
        "responsive": True,     # Adapta ao tamanho da tela
        "displaylogo": False,   # Remove logo da barra de ferramentas
        "scrollZoom": True      # Permite zoom com scroll
    }
)

