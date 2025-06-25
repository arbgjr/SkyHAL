---
applyTo: "**"
---
# 🧪 Testes de API REST

## 🎯 Objetivos
- Validar endpoints
- Verificar validação de entrada
- Testar serialização/desserialização
- Confirmar códigos HTTP corretos
- Testar integração entre camadas

## 🛠️ Ferramentas
- **CLI**: cURL, HTTPie
- **GUI**: Postman, Insomnia
- **Automação**: Newman, REST-assured, Karate

## 📝 Estrutura
- Agrupar por recurso/endpoint
- Nomear: `<Método>_<Endpoint>_<Cenário>_<Resultado>`

## ✅ O que Testar

### 1. Happy Path
- Requisições válidas (200, 201, 204)
- Verificar respostas e headers

### 2. Validação de Entrada
- Testar cada regra de validação
- Dados inválidos → 400 Bad Request

### 3. Cenários de Erro
- Verificar códigos apropriados (404, 409, 500)
- Validar formato das respostas de erro

### 4. Auth
- Sem token → 401 Unauthorized
- Token sem permissão → 403 Forbidden
- Expiração e renovação

### 5. Outros Cenários
- Negociação de conteúdo (Accept header)
- Idempotência (PUT, DELETE)

## 🔧 Exemplos Básicos

### GET
```bash
curl -X GET http://api.exemplo.com/usuarios/123 \
  -H "Authorization: Bearer TOKEN"
```

### POST
```bash
curl -X POST http://api.exemplo.com/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nome":"João","email":"joao@exemplo.com"}'
```

## 💡 Boas Práticas

- Teste em isolamento (mock dependências)
- Limpe recursos após testes
- Use ambiente dedicado
- Parametrize entradas
- Teste casos limite
- Valide headers relevantes
- Monitore tempos de resposta
- Automatize testes de regressão
- Gere relatórios de resultados
