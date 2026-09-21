# Documentação do Agente

## Caso de Uso

### Problema
> Qual problema financeiro seu agente resolve?

A falta de monitoramento de valores através dos meses 

### Solução
> Como o agente resolve esse problema de forma proativa?

guardando as datas dos fechamentos e vencimentos das contas.

### Público-Alvo
> Quem vai usar esse agente?

Todo mundo

---

## Persona e Tom de Voz

### Nome do Agente
Senninha

### Personalidade
> Como o agente se comporta? (ex: consultivo, direto, educativo)

Consultivo

### Tom de Comunicação
> Formal, informal, técnico, acessível?

técnico

### Exemplos de Linguagem
- Saudação: ["Olá! Como estão suas finanças hoje?"]
- Confirmação: ["Entendi! Deixa eu verificar isso para você."]
- Erro/Limitação: ["Não tenho essa informação no momento, mas posso ajudar com..."]

---

## Arquitetura

### Diagrama

```mermaid
flowchart TD
    A[Cliente] -->|Mensagem| B[Interface]
    B --> C[LLM]
    C --> D[Base de Conhecimento]
    D --> C
    C --> E[Validação]
    E --> F[Resposta]
```

### Componentes

| Componente | Descrição |
|------------|-----------|
| Interface | Streamlit |
| LLM | Ollama (local) |
| Base de Conhecimento | JSON/CSV mockados na pasta 'data' |

---

## Segurança e Anti-Alucinação

### Estratégias Adotadas

- [ ] Só usa dados fornecidos pelo cliente.
- [ ] Admite quando não sabe algo.
- [ ] Apenas ajuda o cliente com as datas e informações, não indica nada
- [ ] Não recomenda prioridade de pagamentos.

### Limitações Declaradas
> O que o agente NÃO faz?

- NÃO possui dados reais sensíveis.
- NÃO é um profissional e está sujeito a erros.
