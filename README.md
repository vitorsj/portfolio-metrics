# Napkin Radar - Astella (Hugging Face Spaces)

Aplicação Streamlit que gera um gráfico radar com o tema Astella, comparando métricas “Purple Metrics” com a faixa de benchmark Napkin (Low/High). O app permite ajustar as métricas e baixar o PNG do gráfico.

## Executar localmente

1. Crie/ative seu ambiente virtual.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Rode o app:
   ```bash
   streamlit run app.py
   ```

## Publicar no Hugging Face Spaces

1. Crie um Space novo:
   - SDK: Streamlit
   - Runtime: Python
2. Envie estes arquivos para o Space:
   - `app.py`
   - `napkin_plot.py`
   - `requirements.txt`
   - `README.md` (opcional, recomendado)
3. O build será feito automaticamente. Ao terminar, o link público ficará disponível.

## Estrutura

- `napkin_plot.py`: função `build_figure(...)` que monta e retorna a `matplotlib.figure.Figure` com o gráfico no tema Astella.
- `app.py`: interface Streamlit com inputs para métricas, renderização da figura e botão de download.
- `requirements.txt`: dependências fixadas para reprodutibilidade.

## Observações

- As fontes do Matplotlib usam fallback caso a fonte desejada não esteja disponível no ambiente do Space.


