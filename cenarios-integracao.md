# Cenários de integração gerados (prompt Tipo 1 v2)

| ID | Objetivo | Pré-condição | Passos | Resultado esperado | Tipo |
|----|----------|--------------|--------|--------------------|------|
| IT-01 | Criar usuário válido e persistir | Banco sem o CPF | POST /usuarios com payload válido | 201, corpo com `id` e dados enviados; registro existe no banco | Positivo |
| IT-02 | Persistência fiel | IT-01 executado | GET /usuarios/{id} | 200; todos os campos (incl. endereço) idênticos ao enviado | Positivo |
| IT-03 | Fluxo completo CRUD | Banco limpo | POST → GET → PUT (novo endereço) → GET → DELETE → GET | 201 → 200 → 200 → 200 (endereço novo) → 204 → 404 | Fluxo |
| IT-04 | CPF duplicado | Usuário A cadastrado | POST com mesmo CPF de A | 409; nenhum novo registro criado | Negativo |
| IT-05 | CPF com e sem máscara equivalem | Usuário A cadastrado sem máscara | POST com CPF de A com máscara | 409 (normalização antes da unicidade) | Borda |
| IT-06 | CPF inválido (DV errado) | — | POST com CPF 123.456.789-00 | 422 apontando `cpf`; nada persistido | Negativo |
| IT-07 | CPF com dígitos repetidos | — | POST com 111.111.111-11 | 422 | Negativo |
| IT-08 | Data de nascimento futura | — | POST com data > hoje | 422 apontando `dataNascimento` | Negativo |
| IT-09 | Menor de 18 anos | — | POST com 17 anos e 364 dias | 422 | Borda |
| IT-10 | Exatamente 18 anos hoje | — | POST com data = hoje − 18 anos | 201 | Borda |
| IT-11 | Campos obrigatórios ausentes | — | POST sem `endereco` | 422 listando campo ausente | Negativo |
| IT-12 | CEP e UF inválidos | — | POST com CEP de 7 dígitos / UF "AMZ" | 422 por campo | Negativo |
| IT-13 | JSON malformado | — | POST com corpo `{nome:` | 400 | Negativo |
| IT-14 | Buscar id inexistente | — | GET /usuarios/id-inexistente | 404 | Negativo |
| IT-15 | Atualizar CPF para um já existente | Usuários A e B | PUT em B com CPF de A | 409; B inalterado no banco | Negativo |
| IT-16 | Atualizar id inexistente | — | PUT /usuarios/id-inexistente | 404 | Negativo |
| IT-17 | Excluir duas vezes | Usuário A | DELETE; DELETE novamente | 204; depois 404 | Fluxo |
| IT-18 | Listagem consistente | 2 usuários criados | GET /usuarios | 200; contém os 2; não contém excluídos | Positivo |
| IT-19 | Entradas maliciosas no nome | — | POST com `'; DROP TABLE usuarios;--` | Sem erro 500; tabela íntegra; valor tratado/escapado ou 422 | Segurança |
| IT-20 | Acentos e caracteres especiais | — | POST com nome "José D'Ávila Çelso" | 201; GET devolve o nome idêntico (UTF-8 íntegro) | Borda |
