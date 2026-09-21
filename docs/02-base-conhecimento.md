# Base de Conhecimento

## Objetivo

A base do Senninha é orientada ao acompanhamento de contas recorrentes. Ela permite consultar valores, datas de fechamento e vencimento e o histórico de interações, sem usar dados bancários reais ou recomendar prioridades de pagamento.

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `contas.csv` | CSV | Fonte principal para datas de fechamento, vencimento, valor, status e recorrência das contas. |
| `historico_atendimento.csv` | CSV | Recuperar o contexto de atendimentos anteriores relacionados a contas e datas. |
| `transacoes.csv` | CSV | Apoiar a identificação de lançamentos demonstrativos associados às contas. |
| `perfil_investidor.json` | JSON | Mantido como dado de referência do desafio, mas não é usado para recomendações de investimento. |
| `produtos_financeiros.json` | JSON | Mantido como dado de referência do desafio, mas não é usado pelo Senninha. |

Todos os dados são fictícios e devem ser tratados apenas como material de demonstração.

---

## Adaptações nos Dados

Foi criado o arquivo `data/contas.csv`, que representa o domínio escolhido para o agente. Cada registro possui uma conta e seus ciclos de fechamento e vencimento. O campo `status` é informativo: o agente não classifica contas por prioridade nem orienta qual pagamento deve ser feito primeiro.

As datas foram mantidas como `YYYY-MM-DD` para facilitar o carregamento com `pandas` e a comparação com a data atual. Valores são armazenados em reais e formatados em reais somente na interface e nas respostas.

---

## Estratégia de Integração

### Como os dados são carregados?

`src/agente.py` carrega os arquivos CSV e JSON a partir da raiz do projeto, usando caminhos relativos ao próprio módulo. As contas são carregadas no início da sessão e podem ser recarregadas com o botão da interface. Não há conexão com banco externo.

### Como os dados são usados no prompt?

A pergunta é classificada primeiro por regras simples para identificar consultas de contas, fechamento, vencimento e contexto. Em seguida, o agente monta um contexto mínimo apenas com os registros relevantes e o envia ao Ollama no papel de contexto. O modelo recebe instruções para não criar datas, valores ou contas que não estejam no contexto.

Quando o Ollama não está disponível, o Senninha usa respostas determinísticas para as intenções suportadas. Assim, a aplicação continua demonstrável e não depende de uma resposta inventada pelo modelo.

---

## Exemplo de Contexto Montado

```text
Agente: Senninha
Objetivo: informar datas e valores de contas do cliente.
Regra: use somente os dados abaixo; se a informação não estiver presente, diga que não consta na base.

Contas relevantes:
- Cartão principal | fechamento: 2025-11-05 | vencimento: 2025-11-12 | valor: R$ 850,00 | status: aberta
- Conta de luz | fechamento: 2025-11-10 | vencimento: 2025-11-17 | valor: R$ 180,00 | status: aberta
```

O contexto não contém senhas, dados de autenticação ou informações sensíveis reais.
