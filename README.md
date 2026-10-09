# Gráfico 5.4 — MP10 — Média Móvel de 3 anos

Gráfico interativo em Python + Plotly reproduzindo a estrutura da imagem de referência e utilizando diretamente os dados do CSV fornecido.

## Fonte

`Dd_grafico_5_4.csv`

### Campos

- `serie` — período da média móvel de três anos.
- `med_int` — Média Móvel (3 anos).
- `Per_90` — percentil 90.
- `Per_10` — percentil 10.

Os valores de percentis com vírgula decimal são convertidos automaticamente para números.

## Configuração

- Período: 2000-2002 até 2023-2025.
- Eixo Y: 0–80 µg/m³.
- Faixa branca: Percentis 10/90.
- Linha preta com círculos: Média Móvel (3 anos).
- Fundo: `#DDE9F4`.
- Rótulos do eixo X inclinados em 45°.
- HTML autocontido.
- Zoom e tooltip interativos.

## Arquivos

- `index.html`
- `Dd_grafico_5_4.csv`
- `gerar_grafico.py`
- `.github/workflows/pages.yml`
- `.nojekyll`
- `publicar_github.bat`
- `README.md`

## Instalação

```bash
pip install pandas plotly
```

## Gerar o gráfico

```bash
python gerar_grafico.py
```

## Publicar no GitHub Pages

```bash
git init
git add .
git commit -m "Adicionar grafico 5.4 MP10"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

No GitHub:

**Settings → Pages → Build and deployment → Source → GitHub Actions**

A página será publicada em:

```text
https://SEU_USUARIO.github.io/SEU_REPOSITORIO/
```

## Atualização

Substitua `Dd_grafico_5_4.csv`, execute:

```bash
python gerar_grafico.py
```

e depois:

```bash
git add .
git commit -m "Atualizar dados do grafico 5.4"
git push
```
