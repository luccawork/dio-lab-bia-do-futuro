# Código da Aplicação

O Senninha é um protótipo Streamlit que consulta datas de fechamento e vencimento das contas fictícias em `data/contas.csv`.

## Estrutura

```text
src/
├── app.py            # Interface Streamlit
├── agente.py         # Carregamento, contexto e respostas seguras
└── requirements.txt  # Dependências
```

## Como Rodar

Na raiz do repositório:

```bash
pip install -r src/requirements.txt
streamlit run src/app.py
```

O modo padrão não exige API key nem serviço externo. Para respostas contextualizadas por LLM, instale e execute o [Ollama](https://ollama.ai/), baixe um modelo (por exemplo, `ollama run llama3.2`) e ative **Usar Ollama local** na barra lateral. Se o Ollama estiver indisponível, o app usa o fallback determinístico.

## Consultas para testar

- `Quais são os próximos vencimentos?`
- `Quando fecha o cartão principal?`
- `Qual o vencimento da conta XYZ?`
- `Qual conta devo pagar primeiro?`
- `Me passe uma senha cadastrada.`
