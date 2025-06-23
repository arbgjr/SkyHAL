---
applyTo: "**"
---

Summarized conversation historySegue o texto do arquivo api-security.instructions.md:

---

# 🛡️ Segurança da API - Diretrizes Específicas

## 🎯 Para GitHub Copilot: Implementação Automática

### Autenticação (Sempre Implementar)

```csharp
// Exemplo de estrutura esperada
[Authorize(Policy = "RequireValidJWT")]
[HttpGet]
public async Task<IActionResult> GetResource(
    [FromQuery] GetResourceRequest request)
{
    // Validação automática via ModelState
    if (!ModelState.IsValid)
        return BadRequest(ModelState);

    // Verificação de autorização específica
    var hasPermission = await _authService
        .HasPermissionAsync(User.Identity.Name, "resource:read");

    if (!hasPermission)
        return Forbid();

    // Implementação segura...
}
```

### Validação de Entrada (Padrão Obrigatório)

- **DTOs**: Sempre usar Data Transfer Objects
- **Annotations**: [Required], [StringLength], [Range] etc.
- **Custom Validators**: Para regras de negócio específicas
- **Sanitização**: Remover/escapar caracteres perigosos

### Implementação de Rate Limiting

```csharp
// Configuração padrão esperada
services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(
        httpContext => RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: httpContext.User.Identity?.Name ?? httpContext.Connection.RemoteIpAddress?.ToString(),
            factory: partition => new FixedWindowRateLimiterOptions
            {
                AutoReplenishment = true,
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));
});
```

### Headers de Segurança (Sempre Incluir)

```csharp
// Middleware de segurança obrigatório
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Add("Referrer-Policy", "strict-origin-when-cross-origin");
    context.Response.Headers.Add("Content-Security-Policy", "default-src 'self'");
    await next();
});
```

### Logging Seguro (Padrão de Implementação)

```csharp
// Estrutura de log segura
_logger.LogInformation("User {UserId} accessed resource {ResourceId} at {Timestamp}",
    user.Id,  // Nunca logar dados sensíveis
    resource.Id,
    DateTime.UtcNow);

// NUNCA fazer:
// _logger.LogInformation("User login: {Email} {Password}", email, password);
```

## 🔒 Checklist de Segurança por Feature

### APIs REST

- [ ] Autenticação JWT implementada
- [ ] Autorização baseada em roles/claims
- [ ] Validação de entrada rigorosa
- [ ] Rate limiting configurado
- [ ] Headers de segurança presentes
- [ ] HTTPS obrigatório
- [ ] Logs de auditoria implementados

### Acesso a Dados

- [ ] Queries parametrizadas (sem concatenação)
- [ ] Validação de permissões a nível de linha
- [ ] Auditoria de operações sensíveis
- [ ] Conexões seguras com banco
- [ ] Secrets em Azure Key Vault

### Tratamento de Erros

- [ ] Não exposição de stack traces
- [ ] Mensagens genéricas para usuário
- [ ] Logs detalhados para desenvolvimento
- [ ] Códigos de erro padronizados

## ⚠️ Vulnerabilidades Comuns a Evitar

### Injection Attacks

```csharp
// ❌ NUNCA fazer:
string sql = $"SELECT * FROM Users WHERE Id = {userId}";

// ✅ SEMPRE fazer:
var user = await context.Users
    .Where(u => u.Id == userId)
    .FirstOrDefaultAsync();
```

### XSS Prevention

```csharp
// ✅ Encoding automático
@Html.DisplayFor(model => model.UserInput)

// ✅ Validação de entrada
[RegularExpression(@"^[a-zA-Z0-9\s]*$", ErrorMessage = "Caracteres especiais não permitidos")]
public string UserInput { get; set; }
```

### CSRF Protection

```csharp
// ✅ Anti-forgery token
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> UpdateProfile(ProfileModel model)
{
    // Implementação segura
}
```

## 🎯 Instruções Específicas para Copilot

Quando gerar código de API:

1. **SEMPRE** incluir autenticação e autorização
2. **SEMPRE** validar entrada com DTOs
3. **SEMPRE** implementar logging estruturado
4. **SEMPRE** tratar erros adequadamente
5. **SEMPRE** considerar rate limiting
6. **NUNCA** incluir secrets hardcoded
7. **NUNCA** concatenar strings em queries SQL
8. **NUNCA** expor informações sensíveis em logs ou erros