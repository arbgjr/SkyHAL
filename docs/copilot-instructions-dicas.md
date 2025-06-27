# Dicas e Melhores Práticas - GitHub Copilot

## Python Developer: Perfil e Expertise

- Busque excelência em desenvolvimento Python, ferramentas de linha de comando e operações de sistema de arquivos
- Foque em depuração de problemas complexos e otimização de performance

## Python Developer: Estilo de Código

- Prefira sempre o uso de classes ao invés de funções soltas para código Python.
- Mantenha o código modular, reutilizável e orientado a ob#### Implementação
tos.

## Python Developer: Gerenciamento de Dependências

- Utilize ferramentas modernas e eficientes para instalação de dependências (ex: UV, pip, poetry), conforme padrão do projeto.
- Documente no README ou instruções do projeto como instalar e gerenciar dependências.

## Python Developer: Diretrizes Gerais

- Aplique sempre boas práticas de desenvolvimento, depuração e otimização de performance.
- Consulte e referencie o stack tecnológico e requisitos do projeto ao implementar novas features.

## Padrões de Codificação e Boas Práticas

### Estilo de Código e Legibilidade

- Siga os padrões estabelecidos de codificação para cada linguagem (espaçamento, comentários, nomenclatura)
- Estenda os padrões com regras internas para nomenclatura de pastas e funções quando necessário
- Priorize código legível, compreensível e manutenível
- Realize revisões e refatorações regulares para melhorar estrutura e manutenibilidade
- Use controle de versão (Git) para colaboração efetiva

### Comentários e Documentação

- Use comentários com parcimônia e apenas quando significativos
- Evite comentar código óbvio; foque em explicar o "porquê" e possíveis armadilhas
- Documente decisões importantes de design e arquitetura
- Mantenha a documentação atualizada e alinhada com o código

## Princípios de Design

### DRY (Don't Repeat Yourself)
- Evite duplicação de código através de funções, classes, módulos ou bibliotecas
- Modifique código em um único lugar ao atualizar lógica
- Promova reusabilidade e manutenibilidade

### Encapsulamento e Clareza
- Encapsule lógicas aninhadas de if/else em funções com nomes descritivos
- Mantenha funções curtas e focadas (princípio da responsabilidade única)
- Quebre funções longas ou complexas em funções menores e mais específicas

## Convenções de Nomenclatura

- Use nomes significativos e descritivos para variáveis, funções e classes
- Nomes devem refletir propósito, comportamento e uso
- Prefira nomes específicos que revelem a intenção sem necessidade de comentários
- Mantenha consistência nas convenções adotadas em todo o projeto

## Revisão e Refatoração

- Revise código regularmente para identificar melhorias
- Refatore para maior clareza e manutenibilidade
- Mantenha a qualidade do código através de revisões por pares
- Use ferramentas de análise estática para identificar problemas potenciais

> Baseado em: Práticas recomendadas da comunidade e padrões de desenvolvimento profissional

## Dicas Práticas para Instruções Customizadas

> Baseado em: [GH_Custom_Instruction.md - pamelafox/awesome-copilot-instructions](https://github.com/pamelafox/awesome-copilot-instructions/blob/main/GH_Custom_Instruction.md)

### Clareza e Legibilidade

- Priorize sempre a clareza e a legibilidade do código gerado.
- Use nomes descritivos para funções, variáveis e classes.
- Inclua comentários explicativos sobre decisões de design e algoritmos.
- Explique abordagens e justificativas para escolhas técnicas.

## 2. Documentação e Estilo

- Siga o padrão de documentação da linguagem (ex: docstrings PEP 257 para Python).
- Coloque docstrings imediatamente após `def` ou `class`.
- Separe funções, classes e blocos de código com linhas em branco.
- Mantenha o padrão de formatação do projeto (ex: PEP 8 para Python).
- Limite o tamanho das linhas conforme o guia da linguagem.

## 3. Tratamento de Erros e Casos Limite

- Sempre trate exceções de forma clara e previsível.
- Considere e documente casos limite (entradas vazias, tipos inválidos, grandes volumes).
- Comente o comportamento esperado para cada caso limite.

## 4. Testes e Cobertura

- Inclua testes para caminhos críticos e casos de borda.
- Escreva testes unitários para funções e explique o objetivo de cada teste.
- Documente os casos de teste com docstrings.

## 5. Dependências e Bibliotecas

- Sempre comente o motivo do uso de bibliotecas externas.
- Explique a finalidade de cada dependência no contexto do projeto.

## 6. Exemplo de Documentação Correta

```python
# Exemplo de função bem documentada

def calcular_area(raio: float) -> float:
    """
    Calcula a área de um círculo dado o raio.

    Parâmetros:
        raio (float): Raio do círculo.

    Retorna:
        float: Área calculada como π * raio^2.
    """
    import math
    return math.pi * raio ** 2
```

---


## 7. Workflow e Governança de Instruções

- Sempre consulte os arquivos de instruções relevantes do projeto antes de iniciar uma nova feature ou alteração.
- Liste explicitamente quais arquivos de regras/orientações foram usados para guiar a implementação (ex: `Instruções usadas: [api-security.instructions.md, test.instructions.md]`).
- Siga TDD sempre que possível: escreva testes antes de implementar novas funcionalidades.
- Execute os testes automatizados (`dotnet test`, `dotnet build` ou equivalente) antes de cada commit. Não pergunte se deve rodar os testes, apenas faça.
- Corrija todos os warnings e erros de compilação antes de prosseguir.
- Ao ver caminhos como `/[projeto]/features/[feature]/`, substitua `[projeto]` e `[feature]` pelo contexto real do seu projeto.


## 8. Containerização Python: Diretrizes Copilot

- Seja especialista em Python, algoritmos de banco de dados e tecnologias de containerização (ex: Docker, OCI).
- Siga sempre a documentação oficial do Python e PEPs para melhores práticas.
- Aplique boas práticas de containerização para aplicações Python:
  - Use imagens base oficiais e minimalistas (ex: python:3.12-slim).
  - Sempre defina explicitamente variáveis de ambiente essenciais (ex: PYTHONUNBUFFERED=1).
  - Instale dependências via requirements.txt, poetry ou pip, evitando dependências desnecessárias.
  - Utilize multi-stage builds para reduzir o tamanho da imagem.
  - Nunca inclua segredos ou credenciais no Dockerfile ou na imagem.
  - Defina um usuário não-root para execução do container.
  - Exponha apenas as portas necessárias.
  - Adote HEALTHCHECK para monitoramento do container.
  - Prefira COPY ao invés de ADD, exceto quando realmente necessário.
  - Sempre limpe arquivos temporários e cache após instalação de dependências.
- Garanta que o código seja limpo, seguro e facilmente manutenível.
- Otimize algoritmos e queries para performance em ambiente containerizado.
- Documente no README instruções de build, execução e troubleshooting do container.

### Exemplo de Dockerfile Python Seguro e Eficiente

```dockerfile
FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache
COPY . .
RUN useradd -m appuser && chown -R appuser /app
USER appuser
EXPOSE 8080
HEALTHCHECK CMD curl --fail http://localhost:8080/health || exit 1
CMD ["python", "main.py"]
```

---


## 9. Estrutura de Projeto Python

- Mantenha estrutura clara: separe diretórios para código-fonte (`src/`), testes (`tests/`), documentação (`docs/`) e configuração (`config/`).
- Use design modular: arquivos distintos para modelos, serviços, controladores e utilitários.
- Gerencie configurações via variáveis de ambiente.

## 10. Padrões de Código Python

- Adicione anotações de tipo (type hints) em todas as funções e classes, incluindo tipos de retorno.
- Inclua docstrings descritivas em todas as funções e classes (convenção PEP 257). Atualize docstrings existentes quando necessário.
- Mantenha todos os comentários existentes nos arquivos.
- Utilize Ruff para garantir consistência de estilo de código.

## 11. Tratamento de Erros e Logging

- Implemente tratamento de erros robusto e logging estruturado, sempre capturando o contexto relevante.

## 12. Testes Python

- Utilize `pytest` (não `unittest`) e plugins do pytest para todos os testes.
- Coloque todos os testes em `./tests`. Crie arquivos `__init__.py` conforme necessário.
- Todos os testes devem ter anotações de tipo e docstrings.
- Para type checking em testes, utilize:
  - `from _pytest.capture import CaptureFixture`
  - `from _pytest.fixtures import FixtureRequest`
  - `from _pytest.logging import LogCaptureFixture`
  - `from _pytest.monkeypatch import MonkeyPatch`
  - `from pytest_mock.plugin import MockerFixture`

## 13. Padrões de Codificação

### Escrita e Estilo

- Siga rigorosamente os padrões de codificação estabelecidos para cada linguagem
- Respeite as regras internas de nomenclatura de pastas e funções
- Mantenha consistência no estilo de código em todo o projeto
- Priorize a legibilidade e manutenibilidade do código

### Uso de Comentários

- Use comentários com parcimônia e significado
- Evite comentar o óbvio; use comentários para explicar "por quê" ou comportamentos incomuns
- Documente decisões de design importantes
- Mantenha comentários atualizados com o código

### Funções e Responsabilidades

- Escreva funções curtas e focadas (princípio da responsabilidade única)
- Quebre funções longas ou complexas em funções menores
- Encapsule estruturas condicionais aninhadas em funções com nomes descritivos
- Mantenha uma clara separação de responsabilidades

## 14. Principios DRY e SOLID

### Reusabilidade (DRY - Don't Repeat Yourself)

- Evite duplicação de código usando funções, classes, módulos ou bibliotecas
- Centralize alterações em um único local
- Crie abstrações reutilizáveis para padrões comuns
- Mantenha uma hierarquia clara de componentes

### Organização e Estrutura

- Use nomes significativos e descritivos para variáveis, funções e classes
- Os nomes devem refletir propósito e comportamento
- Evite nomes que precisem de comentários para explicar a intenção
- Organize o código em módulos coesos e bem definidos

### Qualidade e Manutenção

- Escreva código legível, compreensível e manutenível
- Priorize a clareza e adira aos padrões de codificação
- Revise e refatore regularmente o código para melhorar estrutura
- Use controle de versão (ex: Git) para colaboração

## 15. Fluxo de Desenvolvimento

### Review e Refatoração

- Revise o código regularmente em busca de melhorias
- Refatore quando identificar código complexo ou duplicado
- Mantenha a cobertura de testes durante refatorações
- Documente mudanças significativas de arquitetura

### Versionamento e Colaboração

- Use branches para desenvolver novas features
- Mantenha commits pequenos e focados
- Escreva mensagens de commit descritivas
- Atualize documentação junto com o código

## 16. Diretrizes de Comunicação e Revisão

### Interação com o Usuário

- Verifique sempre as informações antes de apresentá-las
- Não faça suposições ou especulações sem evidências claras
- Mantenha a comunicação objetiva e baseada em fatos
- Evite pedir confirmação de informações já fornecidas no contexto
- Não sugira alterações em arquivos quando não houver modificações necessárias

### Processo de Revisão

- Faça alterações arquivo por arquivo para facilitar a revisão
- Forneça todas as edições em um único bloco por arquivo
- Não remova código ou funcionalidades não relacionadas
- Preserve estruturas existentes ao fazer modificações
- Implemente apenas as alterações explicitamente solicitadas

## 17. Melhores Práticas de Código

### Qualidade e Segurança

- Priorize desempenho e segurança nas sugestões
- Implemente tratamento robusto de erros e logging
- Valide pressupostos com assertions
- Trate casos de borda potenciais
- Substitua valores hardcoded por constantes nomeadas

### Design e Arquitetura

- Incentive design modular para manutenibilidade
- Garanta compatibilidade com versões do projeto
- Preserve a estrutura de diretórios existente
- Mantenha consistência com o estilo de código do projeto
- Favoreça nomes explícitos e descritivos para variáveis

### Documentação e Testes

- Sugira ou inclua testes unitários para código novo/modificado
- Documente decisões de design importantes
- Mantenha comentários atualizados e relevantes
- Evite alterações em espaços em branco sem propósito
- Forneça links apenas para arquivos reais

## 18. Integridade do Código

### Princípios de Modificação

- Não invente mudanças não solicitadas
- Mantenha a funcionalidade existente
- Respeite a estrutura atual do projeto
- Evite alterações puramente estéticas
- Documente impactos em outras partes do sistema

### Gestão de Dependências

- Verifique compatibilidade com dependências existentes
- Mantenha versões consistentes em todo o projeto
- Documente novas dependências introduzidas
- Evite conflitos de versão
- Considere o impacto em diferentes ambientes

## Guia de Desenvolvimento com GitHub Copilot

### Princípios de Qualidade e Revisão

### Gerenciamento de Mudanças

- Realize alterações arquivo por arquivo para facilitar revisão
- Forneça todas as edições de um arquivo em um único bloco
- Preserve estruturas existentes; não remova código não relacionado
- Evite sugerir mudanças apenas de formatação
- Mantenha a consistência com a implementação atual

### Revisão e Documentação

- Mantenha foco em clareza e objetividade
- Evite comentários sobre entendimento ou feedback subjetivo
- Documente apenas o necessário e relevante
- Mantenha links e referências atualizados
- Não repita informação já disponível no contexto

### Boas Práticas de Implementação

- Trate cada implementação independentemente
- Implemente apenas o que foi explicitamente solicitado
- Mantenha consistência com padrões existentes
- Documente decisões técnicas importantes
- Evite modificar código não relacionado

### Checklist de Qualidade

- [ ] Mudanças são feitas arquivo por arquivo
- [ ] Edições são fornecidas em blocos únicos
- [ ] Estruturas existentes são preservadas
- [ ] Documentação é clara e objetiva
- [ ] Implementação segue padrões do projeto
- [ ] Mudanças são apenas as solicitadas
- [ ] Decisões técnicas estão documentadas

---

> Baseado em: Práticas recomendadas da comunidade e padrões de desenvolvimento profissional

## Diretrizes de Segurança

### Segurança em Python/Django

#### Práticas Gerais de Segurança

- Aproveite a segurança de memória do Python que mitiga vulnerabilidades comuns
- Evite gerenciamento explícito de memória desnecessário
- Verifique cuidadosamente a reputação e origem de pacotes importados
- Siga as diretrizes OWASP ASVS em implementações
- Evite "Slopsquatting": sempre verifique nomes exatos dos pacotes
- Documente pacotes não comuns ou de baixa reputação

#### Proteção Contra SQL Injection (CWE-89)

- Use exclusivamente Django ORM para interações com banco de dados
- Para queries raw, utilize `django.db.connection.cursor().execute()` com queries parametrizadas
- Nunca concatene dados de usuário diretamente em strings SQL
- Valide e sanitize todas as entradas antes de usar em queries

#### Proteção Contra XSS (CWE-79)

- Utilize sempre o engine de templates do Django que escapa HTML por padrão
- Evite `{% autoescape off %}` e `|safe` exceto para conteúdo confiável
- Use `bleach` para sanitizar HTML/rich text no servidor
- Mantenha uma whitelist estrita de tags e atributos permitidos

#### Proteção Contra CSRF (CWE-352)

- Mantenha `CsrfViewMiddleware` habilitado nas configurações
- Inclua `{% csrf_token %}` em todos os formulários POST
- Configure `X-CSRFToken` corretamente para requisições AJAX
- Verifique tokens CSRF em todas as requisições não seguras

#### Proteção de Credenciais (CWE-522)

- Nunca hardcode credenciais no código fonte
- Use variáveis de ambiente ou serviços de gerenciamento de segredos
- Considere AWS Secrets Manager ou HashiCorp Vault
- Utilize `django-environ` ou `python-decouple` para acesso seguro

#### Prevenção de Path Traversal (CWE-22)

- Valide e sanitize todos os caminhos de arquivo fornecidos pelo usuário
- Use `os.path.join()` para construir caminhos
- Verifique caminhos com `os.path.abspath()` e `os.path.commonpath()`
- Restrinja uploads a diretórios específicos e seguros

#### Proteção de Informações Sensíveis (CWE-200)

- Desabilite `DEBUG` em produção
- Configure logs para excluir dados sensíveis
- Implemente páginas de erro 404 e 500 personalizadas
- Use sistemas de autenticação e autorização do Django
- Aplique princípio do menor privilégio

### Checklist de Segurança

- [ ] Debug desabilitado em produção
- [ ] Queries parametrizadas em uso
- [ ] Escaping HTML habilitado
- [ ] Proteção CSRF ativa
- [ ] Credenciais armazenadas seguramente
- [ ] Validação de caminhos implementada
- [ ] Logs configurados adequadamente
- [ ] Sistema de permissões implementado

## Desenvolvimento de Servidores MCP em Python

### Arquitetura e Componentes

O Model Context Protocol (MCP) é um protocolo aberto que padroniza como aplicações fornecem contexto para LLMs. Os componentes principais são:

- **Host**: Interface que o usuário vê e interage (ex: Cursor, Claude Desktop)
- **Cliente MCP**: Integrado ao host, faz a ponte com servidores MCP
- **Servidor MCP**: Implementa funcionalidades e acesso a dados externos

## Boas Práticas

### Estrutura do Projeto

Use ambientes virtuais para isolar dependências:

```python
python -m venv mcp-env
source mcp-env/bin/activate  # Windows: mcp-env\Scripts\activate
```

Diretrizes importantes:

- Separe código em módulos reutilizáveis
- Mantenha um arquivo de requisitos (`requirements.txt`)
- Use caminhos relativos para arquivos de dados
- Documente configurações necessárias

### Implementação

Nomeie seu servidor de forma descritiva:

```python
mcp = FastMCP("Nome Descritivo do Servidor")
```

Use decoradores para definir ferramentas:

```python
@mcp.tool()
def nome_ferramenta():
    """Documentação clara da funcionalidade."""
    # Implementação
```

Trate erros adequadamente:

```python
try:
    # Operações de risco
except Exception as e:
    logger.error(f"Erro: {e}")
    return {"error": str(e)}
```

Outras diretrizes importantes:

- Documente parâmetros e retornos
- Implemente logging estruturado

### Segurança

- Valide entradas de usuário
- Use conexões seguras para APIs externas
- Não exponha credenciais no código
- Implemente rate limiting quando necessário
- Monitore uso de recursos

### Testes

- Teste ferramentas individualmente
- Implemente testes de integração
- Valide respostas de APIs
- Simule cenários de erro
- Teste performance com carga

## Integração

### Com Cursor

Configure em `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "nome-servidor": {
      "command": "/caminho/para/python",
      "args": ["/caminho/para/servidor.py"],
      "description": "Descrição clara do servidor"
    }
  }
}
```

Pontos importantes:

- Reinicie o Cursor após alterações
- Verifique status do servidor na interface

### Com Claude Desktop

Configure em `claude_desktop_config.json`:

```json
{
  "servers": [
    {
      "name": "Nome do Servidor",
      "command": "python",
      "args": ["servidor.py"],
      "description": "Descrição clara"
    }
  ]
}
```

Pontos importantes:

- Reinicie o Claude Desktop após mudanças
- Valide conexão pelo ícone de ferramentas

### Dicas para Desenvolvimento

- Mantenha funções pequenas e focadas
- Use tipagem quando possível
- Implemente logging detalhado
- Documente APIs claramente
- Faça tratamento robusto de erros
- Teste com diferentes clientes MCP
- Monitore performance
- Mantenha versionamento do código

### Troubleshooting

- Verifique logs do servidor
- Confirme caminhos de arquivo
- Valide configurações do cliente
- Teste conexões isoladamente
- Monitore uso de recursos
