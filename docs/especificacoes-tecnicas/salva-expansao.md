# Especificação Técnica: Auto-Expansão de Tools Python

## Objetivo

Permitir que o agente SkyHAL:

- Salve em disco, de forma automática, arquivos `.py` gerados dinamicamente pela IA (expansion).
- Disponibilize imediatamente a nova tool para uso no ciclo de vida do agente, sem reinicialização manual.

---

## 1. Fluxo Geral

1. O agente recebe um código Python gerado (string) e metadados (nome, tipo, dependências).
2. O agente determina o diretório correto conforme a arquitetura (ex: `src/utils/` para utilitários, `src/application/` para casos de uso).
3. O agente cria um novo arquivo `.py` com nome único e conteúdo fornecido.
4. O agente registra o novo arquivo/tool em um índice de tools disponíveis (ex: um registry Python ou arquivo de metadados).
5. O agente importa dinamicamente o novo módulo/tool usando `importlib` e o expõe para uso imediato.
6. O processo é logado de forma estruturada e erros são tratados.

---

## 2. Estrutura de Diretórios

- Utilitários: `src/utils/`
- Casos de uso: `src/application/`
- Infraestrutura: `src/infrastructure/`
- Outras tools: conforme padrão Clean Architecture

---

## 3. API Interna

### Função principal

```python
def expand_and_register_tool(code: str, tool_name: str, target_dir: str) -> Any:
    """
    Salva o código Python em disco, importa e registra a nova tool.

    Args:
        code (str): Código fonte Python gerado.
        tool_name (str): Nome da tool/módulo.
        target_dir (str): Caminho relativo do diretório de destino.

    Returns:
        Any: Referência à tool importada.
    Raises:
        Exception: Em caso de erro de escrita ou importação.
    """
```

### Passos detalhados

1. **Validação de entrada**: Verificar se `tool_name` é válido e não existe conflito.
2. **Salvar arquivo**: Escrever `code` em `{target_dir}/{tool_name}.py`.
3. **Atualizar índice**: Adicionar referência ao novo módulo/tool em um registry (ex: `src/utils/tool_registry.py`).
4. **Importação dinâmica**: Usar `importlib.util` para importar o novo módulo.
5. **Registro**: Adicionar a tool ao dicionário global de tools do agente.
6. **Logging**: Logar sucesso ou falha com `structlog`.
7. **Tratamento de erros**: Capturar exceções e retornar erro estruturado.

---

## 4. Exemplo de Implementação

Arquivo: `src/application/expansion_manager.py`

```python
import importlib.util
import os
import structlog

logger = structlog.get_logger()

def expand_and_register_tool(code: str, tool_name: str, target_dir: str) -> object:
    # 1. Validação
    if not tool_name.isidentifier():
        raise ValueError("Nome de tool inválido")
    file_path = os.path.join(target_dir, f"{tool_name}.py")
    if os.path.exists(file_path):
        raise FileExistsError(f"Tool {tool_name} já existe")

    # 2. Salvar arquivo
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    logger.info("tool_saved", tool_name=tool_name, file_path=file_path)

    # 3. Importação dinâmica
    spec = importlib.util.spec_from_file_location(tool_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # 4. Registro (exemplo: adicionar ao registry global)
    from src.utils.tool_registry import register_tool
    register_tool(tool_name, module)

    logger.info("tool_registered", tool_name=tool_name)
    return module
```

---

## 5. Registry de Tools

Arquivo: `src/utils/tool_registry.py`

```python
_tools = {}

def register_tool(name: str, module: object):
    _tools[name] = module

def get_tool(name: str) -> object:
    return _tools.get(name)
```

---

## 6. Testes

- Testar criação, importação e uso imediato da tool.
- Testar cenários de erro (nome inválido, conflito, erro de sintaxe).
- Testar logging e registro.

---

## 7. Observabilidade

- Logar todas as etapas (salvamento, importação, registro, erro).
- Incluir trace_id nos logs para rastreabilidade.

---

## 8. Segurança

- Validar entradas para evitar execução de código malicioso.
- Restringir diretórios de escrita.
- Auditar logs de expansão.

---

## 9. Documentação

- Atualizar README e docs/auto-extensao-mcp.md com exemplos de uso e fluxo.

---
