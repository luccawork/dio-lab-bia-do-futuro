# Pitch (3 minutos)

## Roteiro Sugerido

### 1. O Problema (30 seg)

Muitas pessoas perdem o controle das contas recorrentes porque não acompanham com clareza as datas de fechamento e vencimento ao longo dos meses. As informações ficam espalhadas, e uma dúvida simples exige consultar diferentes lugares.

### 2. A Solução (1 min)

O Senninha é um agente financeiro consultivo, com linguagem técnica e acessível, que centraliza os dados demonstrativos das contas. O usuário pergunta em linguagem natural e recebe datas de fechamento, vencimentos, valores e status informativo. A aplicação usa Streamlit, dados locais em CSV e Ollama como LLM local. Antes de gerar a resposta, o sistema filtra os dados relevantes; quando o modelo não está disponível, usa respostas determinísticas.

O agente foi desenhado com segurança: não acessa dados reais, não solicita senhas, não inventa informações e não recomenda qual conta deve ser paga primeiro.

### 3. Demonstração (1 min)

1. Abrir a aplicação e mostrar as contas cadastradas.
2. Perguntar: `Quais são os próximos vencimentos?`.
3. Perguntar: `Quando fecha o cartão principal?`.
4. Perguntar por uma conta inexistente e mostrar a admissão de ausência de dados.
5. Perguntar `Qual conta devo pagar primeiro?` e mostrar a recusa de recomendação.
6. Opcionalmente, ligar o Ollama e repetir uma consulta contextualizada.

### 4. Diferencial e Impacto (30 seg)

O diferencial é combinar uma interface simples com rastreabilidade: cada resposta vem da base de contas e tem um escopo explícito. Isso torna a IA mais segura para uma tarefa cotidiana, ajuda o usuário a se organizar e demonstra como linguagem natural, Python, dados e UX podem trabalhar juntos sem transformar o agente em consultor financeiro.

---

## Checklist do Pitch

- [ ] Duração máxima de 3 minutos
- [ ] Problema de acompanhamento de datas claramente definido
- [ ] Consulta de fechamento e vencimento demonstrada
- [ ] Tratamento de conta inexistente demonstrado
- [ ] Limitações e segurança explicadas
- [ ] Áudio e vídeo com boa qualidade

---

## Link do Vídeo

> Cole aqui o link do seu pitch (YouTube, Loom, Google Drive, etc.)

[Link do vídeo]
