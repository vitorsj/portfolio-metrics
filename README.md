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

### Opção 1: Criar Space conectado ao GitHub (Recomendado)

Esta opção permite atualizações automáticas quando você faz push no GitHub:

1. Acesse https://huggingface.co/spaces
2. Clique em **"Create new Space"**
3. Configure:
   - **Nome:** `portfolio-metrics` (ou outro de sua escolha)
   - **SDK:** Streamlit
   - **Hardware:** CPU Basic (gratuito)
   - **Visibility:** Public
4. **Importante:** Na seção **"Repository"**, escolha:
   - **"Import from GitHub"** ou **"GitHub"**
   - Selecione seu repositório: `vitorsj/portfolio-metrics`
   - Escolha o branch: `main`
5. Clique em **"Create Space"**
6. O Hugging Face irá:
   - Clonar o repositório automaticamente
   - Fazer o build inicial
   - Configurar sincronização automática com o GitHub

**Vantagens:**
- ✅ Atualizações automáticas ao fazer push no GitHub
- ✅ Histórico de commits preservado
- ✅ Fácil colaboração

### Opção 2: Conectar Space existente ao GitHub

Se você já criou o Space sem conectar ao GitHub:

1. Acesse seu Space no Hugging Face
2. Vá em **Settings** (ícone de engrenagem)
3. Na seção **"Repository"**, clique em **"Connect to GitHub"**
4. Autorize o Hugging Face a acessar seus repositórios
5. Selecione: `vitorsj/portfolio-metrics` e branch `main`
6. Salve as configurações

### Opção 3: Upload manual (sem GitHub)

Se preferir não conectar ao GitHub:

1. Crie um Space novo (SDK: Streamlit)
2. Faça upload manual destes arquivos:
   - `app.py`
   - `napkin_plot.py`
   - `requirements.txt`
   - `README.md` (opcional)
3. O build será feito automaticamente

**Nota:** Com esta opção, você precisará fazer upload manual a cada atualização.

## Estrutura

- `napkin_plot.py`: função `build_figure(...)` que monta e retorna a `matplotlib.figure.Figure` com o gráfico no tema Astella.
- `app.py`: interface Streamlit com inputs para métricas, renderização da figura e botão de download.
- `requirements.txt`: dependências fixadas para reprodutibilidade.

## Observações

- As fontes do Matplotlib usam fallback caso a fonte desejada não esteja disponível no ambiente do Space.


