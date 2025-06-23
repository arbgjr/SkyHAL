# 📝 Padrões de Documentação - Implementação Prática

## 🎯 Para GitHub Copilot: Geração Automática

### Tipos de Documentação por Audiência

#### **Para Desenvolvedores (README.md)**

````markdown
# Nome do Projeto

> Breve descrição em uma linha do que o projeto faz

## 🚀 Quick Start

```bash
# Comandos essenciais para começar
git clone [repo]
cd [projeto]
dotnet restore
dotnet run
```
````

## 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐
│   Controllers   │───▶│    Services     │
└─────────────────┘    └─────────────────┘
         │                       │
         ▼                       ▼
┌─────────────────┐    ┌─────────────────┐
│   Validators    │    │  Repositories   │
└─────────────────┘    └─────────────────┘
```

## 🔧 Configuração

### Variáveis de Ambiente

```bash
DB_CONNECTION_STRING=Server=...
JWT_SECRET=sua-chave-secreta
REDIS_URL=redis://localhost:6379
```

### appsettings.json

```json
{
  "JwtSettings": {
    "Secret": "sua-chave-jwt",
    "ExpirationMinutes": 60
  }
}
```

## 📖 Guias

- [Setup Desenvolvimento](docs/setup-dev.md)
- [Deploy Production](docs/deploy.md)
- [Troubleshooting](docs/troubleshooting.md)

## 🤝 Contribuição

Veja [CONTRIBUTING.md](CONTRIBUTING.md)

````

#### **Para APIs (OpenAPI/Swagger)**
```yaml
# openapi.yml automático via attributes
[HttpPost("users")]
[ProducesResponseType(typeof(UserResponse), 201)]
[ProducesResponseType(typeof(ValidationErrorResponse), 400)]
[ProducesResponseType(401)]
public async Task<IActionResult> CreateUser(
    [FromBody] CreateUserRequest request)
{
    /// <summary>
    /// Cria um novo usuário no sistema
    /// </summary>
    /// <param name="request">Dados do usuário a ser criado</param>
    /// <returns>Usuário criado com ID gerado</returns>
    /// <response code="201">Usuário criado com sucesso</response>
    /// <response code="400">Dados de entrada inválidos</response>
    /// <response code="401">Token de autenticação necessário</response>
}
````

#### **Para Decisões Arquiteturais (ADRs)**

````markdown
# ADR-001: Escolha do Padrão Repository

## Status

✅ Aceito

## Contexto

Precisávamos de uma camada de abstração para acesso a dados que:

- Facilitasse testes unitários
- Permitisse troca de provedor de dados
- Mantivesse lógica de negócio separada

## Decisão

Implementar padrão Repository com Generic Repository base:

```csharp
public interface IRepository<T> where T : BaseEntity
{
    Task<T> GetByIdAsync(int id);
    Task<IEnumerable<T>> GetAllAsync();
    Task<T> CreateAsync(T entity);
    Task UpdateAsync(T entity);
    Task DeleteAsync(int id);
}
```
````

## Consequências

### Positivas

- ✅ Fácil mock para testes
- ✅ Código desacoplado do Entity Framework
- ✅ Reutilização de código comum

### Negativas

- ❌ Camada adicional de abstração
- ❌ Pode ocultar recursos específicos do EF

## Alternativas Consideradas

1. **DbContext direto**: Mais simples, mas acopla código ao EF
2. **CQRS puro**: Mais complexo para casos simples
3. **Mediator Pattern**: Considerado para futuras iterações

````

### Documentação de Código (XML Comments)

#### **Classes e Métodos Públicos:**
```csharp
/// <summary>
/// Serviço responsável por gerenciar operações de usuário
/// </summary>
/// <remarks>
/// Este serviço implementa regras de negócio relacionadas a:
/// - Criação e validação de usuários
/// - Autenticação e autorização
/// - Gerenciamento de perfis
///
/// Exemplo de uso:
/// <code>
/// var user = await userService.CreateAsync(new CreateUserRequest
/// {
///     Email = "user@example.com",
///     Name = "John Doe"
/// });
/// </code>
/// </remarks>
public class UserService : IUserService
{
    /// <summary>
    /// Cria um novo usuário no sistema
    /// </summary>
    /// <param name="request">Dados do usuário a ser criado</param>
    /// <returns>Usuário criado com ID gerado pelo sistema</returns>
    /// <exception cref="ValidationException">
    /// Lançada quando os dados de entrada são inválidos
    /// </exception>
    /// <exception cref="ConflictException">
    /// Lançada quando já existe usuário com o email informado
    /// </exception>
    /// <example>
    /// <code>
    /// var request = new CreateUserRequest
    /// {
    ///     Email = "john@example.com",
    ///     Name = "John Doe",
    ///     Role = UserRole.Standard
    /// };
    ///
    /// var user = await userService.CreateAsync(request);
    /// Console.WriteLine($"Usuário criado: {user.Id}");
    /// </code>
    /// </example>
    public async Task<User> CreateAsync(CreateUserRequest request)
    {
        // Implementação...
    }
}
````

### Templates de Documentação

#### **Feature Documentation Template:**

````markdown
# Feature: [Nome da Funcionalidade]

## Visão Geral

[Descrição de 1-2 parágrafos do que a feature faz]

## Casos de Uso

1. **[Ator]** quer **[objetivo]** para **[benefício]**
2. **[Ator]** precisa **[ação]** quando **[condição]**

## Fluxo Principal

1. Usuário acessa [endpoint/tela]
2. Sistema valida [critérios]
3. Sistema executa [ação]
4. Sistema retorna [resultado]

## Validações

- [ ] Campo X é obrigatório
- [ ] Email deve ter formato válido
- [ ] Senha deve ter mínimo 8 caracteres

## APIs Relacionadas

- `POST /api/users` - Criar usuário
- `GET /api/users/{id}` - Buscar usuário
- `PUT /api/users/{id}` - Atualizar usuário

## Testes

- [x] Testes unitários implementados
- [x] Testes de integração implementados
- [ ] Testes de performance pendentes

## Configuração

```json
{
  "UserSettings": {
    "MinPasswordLength": 8,
    "RequireEmailConfirmation": true
  }
}
```
````

## Monitoramento

- Métricas: Tempo de criação de usuário
- Logs: Tentativas de criação com dados inválidos
- Alertas: Taxa de erro > 5%

````

#### **Documentação para Usuários**

A documentação para usuários deve ser clara, objetiva e adaptada ao público-alvo.

##### **Guias de Usuário (Template):**

```markdown
# Guia: [Nome da Funcionalidade]

## Visão Geral
Breve descrição do recurso e seu propósito.

## Pré-requisitos
- Item 1 necessário antes de começar
- Item 2 necessário antes de começar

## Passo a Passo

### 1. [Primeiro Passo]
![Screenshot do primeiro passo](./images/passo1.png)
Descrição detalhada do que fazer.

### 2. [Segundo Passo]
![Screenshot do segundo passo](./images/passo2.png)
Descrição detalhada do que fazer.

### 3. [Terceiro Passo]
![Screenshot do terceiro passo](./images/passo3.png)
Descrição detalhada do que fazer.

## Cenários Comuns

### [Cenário 1]
Como realizar uma tarefa específica usando este recurso.

### [Cenário 2]
Como realizar outra tarefa específica usando este recurso.

## Dicas e Boas Práticas
- Dica 1
- Dica 2
- Dica 3
```

##### **FAQ (Template):**

```markdown
# Perguntas Frequentes: [Componente/Feature]

## Configuração

### Como configurar [recurso específico]?
Resposta detalhada com passos e exemplos.

### É possível personalizar [configuração]?
Sim, você pode personalizar através de [explicação].

## Uso Diário

### Como faço para [ação comum 1]?
Resposta detalhada com passos e exemplos.

### Como faço para [ação comum 2]?
Resposta detalhada com passos e exemplos.

## Solução de Problemas

### O que fazer quando [problema comum 1]?
Passos para diagnosticar e resolver.

### Como resolver [problema comum 2]?
Passos para diagnosticar e resolver.

## Integração

### É possível integrar com [sistema externo]?
Detalhes sobre a integração.

### Quais APIs estão disponíveis para [funcionalidade]?
Lista de APIs relevantes com exemplos básicos.
```

#### **Troubleshooting Guide Template:**
```markdown
# Troubleshooting: [Componente/Feature]

## Problemas Comuns

### ❌ Erro: "Connection timeout"
**Sintomas**: API retorna 500 após 30 segundos
**Causa**: Connection string incorreta ou banco indisponível
**Solução**:
1. Verificar connection string no appsettings.json
2. Testar conectividade: `telnet db-server 1433`
3. Verificar logs do banco de dados

### ❌ Erro: "JWT token invalid"
**Sintomas**: Retorna 401 mesmo com token válido
**Causa**: Configuração de JWT incorreta
**Solução**:
```csharp
// Verificar configuração no Startup.cs
services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidIssuer = "seu-issuer", // Deve coincidir com token
            ValidateAudience = true,
            ValidAudience = "sua-audience", // Deve coincidir com token
            ValidateLifetime = true,
            ClockSkew = TimeSpan.Zero
        };
    });
````

## Logs Úteis

```bash
# Verificar logs de autenticação
docker logs api-container | grep "Authentication"

# Verificar performance de banco
docker logs db-container | grep "slow query"

# Verificar uso de memória
docker stats api-container
```

## Ferramentas de Debug

- **Swagger UI**: `/swagger` para testar APIs
- **Health Checks**: `/health` para status dos serviços
- **Metrics**: `/metrics` para métricas Prometheus

````

### Automação de Documentação

#### **GitHub Actions para Docs:**
```yaml
# .github/workflows/docs.yml
name: Generate Documentation

on:
  push:
    branches: [main]
    paths: ['src/**/*.cs', 'docs/**/*.md']

jobs:
  generate-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Generate API Docs
        run: |
          dotnet tool install -g docfx
          docfx build docs/docfx.json

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs/_site
````

#### **Validação de Links:**

```yaml
- name: Check Links
  uses: lycheeverse/lychee-action@v1
  with:
    args: --verbose --no-progress './**/*.md'
```

## 📋 Checklist de Documentação

Para garantir a qualidade e completude da documentação, use os checklists abaixo:

### Para Documentação de Código

- [ ] Todos os métodos públicos possuem XMLDocs completos
- [ ] Comentários explicam o "por quê", não apenas o "o quê"
- [ ] Exemplos incluídos para APIs complexas
- [ ] Exceções documentadas com cenários que as lançam
- [ ] Casos de erro e validações documentados
- [ ] Dependências e pré-requisitos claramente listados

### Para Documentação de API

- [ ] Todos os endpoints têm descrição, parâmetros e respostas
- [ ] Códigos de erro e exceções documentados por endpoint
- [ ] Exemplos de request/response para cenários comuns
- [ ] Autenticação e autorização claramente explicadas
- [ ] Headers especiais e rate limits documentados
- [ ] Swagger/OpenAPI gerado e atualizado

### Para Documentação de Usuário

- [ ] Guias passo-a-passo para funcionalidades principais
- [ ] FAQ abrange questões comuns dos usuários
- [ ] Troubleshooting para problemas conhecidos
- [ ] Screenshots e exemplos visuais atualizados
- [ ] Linguagem apropriada para o público-alvo
- [ ] Testado com usuários reais ou representativos

## 🔄 Princípios Fundamentais

### 1. Proximidade ao Código

Documentação que se afasta do código tende a ficar desatualizada rapidamente. Sempre mantenha a documentação o mais próxima possível do código que ela descreve:

- Prefira documentação em XMLDocs dentro do código-fonte
- Use ferramentas como Swagger que extraem documentação do código
- Automatize a geração de documentação a partir de testes e exemplos
- Atualize a documentação no mesmo PR que altera o código

### 2. Atualização Constante

A documentação deve ser atualizada durante o desenvolvimento, não depois:

- Trate documentação como parte do Definition of Done
- Atualize documentação antes de fazer merge de PRs
- Revise documentação periodicamente como parte do processo de qualidade
- Implemente validação automática de documentação no pipeline CI/CD

### 3. Linguagem Clara

Use linguagem objetiva e acessível:

- Prefira frases curtas e diretas
- Evite jargões técnicos desnecessários
- Use voz ativa em vez de passiva
- Mantenha terminologia consistente em todo o projeto

### 4. Estrutura Consistente

Padronize a estrutura da documentação:

- Use templates para tipos comuns de documentação
- Mantenha hierarquia lógica e navegação clara
- Siga o mesmo padrão para documentos similares
- Use formatação consistente (Markdown, HTML, etc.)

### 5. Automação

Automatize a geração e validação de documentação:

- Configure geração automática a partir de comentários de código
- Implemente validadores de documentação no CI
- Use ferramentas de detecção de links quebrados
- Integre a documentação ao processo de build e deploy

## 🎯 Instruções para Copilot

Ao gerar documentação:

1. **SEMPRE** incluir exemplos práticos de código
2. **SEMPRE** documentar casos de erro e como resolvê-los
3. **SEMPRE** incluir diagramas quando ajudar na compreensão
4. **SEMPRE** manter linguagem clara e objetiva
5. **CONSIDERAR** diferentes audiências (dev, ops, usuário)
6. **INCLUIR** links para recursos relacionados
7. **FORNECER** templates reutilizáveis
8. **AUTOMATIZAR** geração quando possível
9. **EXPLICAR** o "por quê", não apenas o "o quê"
10. **MANTER** documentação próxima ao código
11. **ATUALIZAR** documentação durante o desenvolvimento, não depois
12. **USAR** estrutura consistente e padronizada
