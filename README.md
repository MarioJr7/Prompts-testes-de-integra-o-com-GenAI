# Prompts-testes-de-integra-o-com-GenAI

Repositório do fórum da pós. Cenário: API REST de cadastro de usuário
(`nome`, `cpf`, `dataNascimento`, `endereco`) integrando **front-end ↔ API ↔ banco**.

## Estrutura
- `docs/openapi.yaml` – contrato usado como entrada dos prompts
- `prompts/` – prompts v1 (inicial) e v2 (refinado) de cada tipo
- `casos-de-teste/cenarios-integracao.md` – cenários gerados (Tipo 1)
- `casos-de-teste/dados-teste.json` – dados válidos/inválidos e erros (Tipo 2)
- `tests/test_usuarios_api.py` – casos automatizados (pytest + requests)

## Tipos de prompt
1. **Geração de cenários de integração** a partir do contrato (OpenAPI).
2. **Geração de dados de teste e casos de erro** (CPF, datas, endereço, payloads).

## Como executar
```bash
pip install pytest requests
BASE_URL=http://localhost:8000 pytest -v
```
> Os testes assumem o contrato de `docs/openapi.yaml`. Sem API no ar, rode apenas
> `pytest --collect-only` para validar a estrutura.
