# Tipo 1 — Cenários de integração (v2, refinado)
```
Atue como engenheiro de QA sênior. Com base no contrato OpenAPI abaixo,
gere casos de TESTE DE INTEGRAÇÃO (API + banco de dados), não unitários.

Contexto: front-end envia JSON para a API REST, que persiste em banco relacional.
Regras de negócio: CPF único e válido (dígitos verificadores); data de nascimento
não futura e idade mínima 18 anos; CEP com 8 dígitos; UF com 2 letras.

Para cada caso retorne uma tabela com as colunas:
ID | Objetivo | Pré-condição | Passos (request) | Resultado esperado
(status HTTP + corpo + estado no banco) | Tipo (positivo/negativo/borda/fluxo)

Cubra obrigatoriamente: (1) fluxos encadeados (criar→buscar→atualizar→excluir→buscar),
(2) persistência (o que foi enviado é o que é retornado), (3) unicidade de CPF,
(4) validações por campo, (5) recursos inexistentes, (6) consistência da listagem.
Gere no mínimo 15 casos e NÃO repita cenários equivalentes.

[colar aqui o conteúdo de docs/openapi.yaml]
```
