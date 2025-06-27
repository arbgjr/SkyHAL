---
applyTo: "**"
---
# 🐛 Bugs Encontrados - Registro e Rastreamento

## 🎯 Formato de Registro

### Estrutura Obrigatória
```markdown
## [ID do Bug] - [Status] - [Data]

### 🔍 Descrição
[Descrição clara e objetiva do bug]

### 🛠️ Passos para Reproduzir
1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

### 💥 Impacto
- [Severidade]
- [Usuários/sistemas afetados]
- [Dados comprometidos]

### 🩹 Correção
- **PR**: #[número-do-PR]
- **Commit**: [hash-do-commit]
- **Solução**: [descrição breve]
```

## Exemplos de Bugs Python/FastAPI

### BUG-001 - ABERTO - 2025-06-23

#### 🔍 Descrição
Race condition na execução de coroutines em operações assíncronas.

#### 🛠️ Passos para Reproduzir
1. Executar múltiplas requisições assíncronas simultâneas
2. Verificar logs de execução concorrente
3. Observar ordem de execução inconsistente

#### 💥 Impacto
- Severidade: Alta
- Afeta todas operações assíncronas
- Possível inconsistência de dados

#### 🩹 Correção
- **PR**: Pendente
- **Solução**: Implementar locks assíncronos

### BUG-000 - FECHADO - 2025-06-22

#### 🔍 Descrição
Memory leak em upload de arquivos grandes via FastAPI.

#### 🛠️ Passos para Reproduzir
```python
from fastapi import FastAPI, File, UploadFile

@app.post("/upload/")
async def upload_file(file: UploadFile):
    content = await file.read()  # Bug: Carrega arquivo inteiro na memória
    return {"filename": file.filename}
```

#### 💥 Impacto
- Severidade: Média
- Afeta uploads grandes
- Degradação de performance

#### 🩹 Correção
- **PR**: #123
- **Commit**: abc123def
- **Solução**: Implementado streaming
```python
@app.post("/upload/")
async def upload_file(file: UploadFile):
    async with aiofiles.open(dest_path, 'wb') as out_file:
        while content := await file.read(1024):  # Stream em chunks
            await out_file.write(content)
    return {"filename": file.filename}
```
