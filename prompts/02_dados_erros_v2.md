# Tipo 2 — Dados de teste e casos de erro (v2, refinado)
```
Gere dados de teste para o endpoint POST /usuarios (schema abaixo) em JSON
estrito, sem comentários, no formato:
{"validos":[{"descricao":"","payload":{}}],
 "invalidos":[{"descricao":"","payload":{},"status_esperado":422,"campo":""}]}

Requisitos:
- CPFs "válidos" DEVEM ter dígitos verificadores corretos (confira o cálculo);
  inclua CPF só com dígitos e com máscara.
- Inválidos: CPF com dígitos repetidos, DV errado, tamanho incorreto, letras;
  data futura, menor de 18 anos, formato inválido (31/02/2000); CEP com 7 dígitos
  e com letras; UF com 3 letras; campos ausentes e nulos; nome vazio, com 101
  caracteres e com acentos/emoji; tentativa de SQL injection e XSS no nome.
- Bordas: exatamente 18 anos hoje, 17 anos e 364 dias, nome com 3 e 100 caracteres.
- Para cada inválido, informe o campo e o status HTTP esperado (400 para JSON
  malformado, 422 para validação, 409 para CPF duplicado).

[colar schema UsuarioInput]
```
