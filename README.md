# 📊 Sistema Inteligente de Consulta e Dashboard Automatizado de Vendas

Este projeto foi desenvolvido para solucionar um problema clássico de áreas de negócios: a dependência de planilhas locais lentas, poluídas e de difícil consulta. Unindo o poder de processamento do **Python** com técnicas de modelagem comuns ao **Power BI**, criei uma aplicação web intuitiva que automatiza o ETL (Extração, Tratamento e Carga) e entrega insights visuais interativos em tempo real.

---

## 👤 Desenvolvedor / Contato

* **Nome:** Nikolas Pinheiro
* **Função:** Assistente de Dados / Analista de BI
* **Telefone:** (14) 99186-8335
* **E-mail:** nikolas9pinheiro@gmail.com

---

## 🛠️ Tecnologias e Conceitos Utilizados

* **Linguagem:** Python 3.12
* **Tratamento de Dados (Engenharia):** `Pandas` (Equivalente ao Power Query / M)
* **Interface Web e UX:** `Streamlit` (Desenvolvimento ágil de aplicações de dados)
* **Motor de Leitura Excel:** `Openpyxl`
* **Visualização de Dados:** `Altair Graphics` (Gráficos interativos em JSON/Vega-Lite)

---

## 💡 Principais Funcionalidades do Sistema

1. **Camada de ETL Dinâmica:** O sistema lê arquivos `.xlsx` e automaticamente limpa strings eliminando espaços em branco nas bordas, corrige problemas de valores nulos e converte strings temporais em objetos de data reais.
2. **Sistema de Consulta Universal:** Embora venha configurado para ler a base de 1.000 registros, o sistema possui um componente de *File Upload* que permite ao usuário arrastar **qualquer nova planilha de vendas** para gerar o dashboard na hora.
3. **Métricas de Negócio em Tempo Real (KPIs):** Cálculo instantâneo de Volume de Transações, Faturamento Líquido e Ticket Médio guiados pelos filtros aplicados.
4. **Visão Segmentada em Abas (Tabs):** Separação clara entre a visão executiva (gráficos e KPIs) e a visão operacional (auditoria da tabela limpa).
5. **Cultura de Self-Service BI:** Botão integrado para download em Excel do resultado exato das consultas realizadas na tela.

---

## 🚀 Como Executar o Projeto Localmente

1. Certifique-se de ter o Python instalado.
2. Instale as dependências executando o comando:
   ```bash
   pip install pandas openpyxl streamlit altair