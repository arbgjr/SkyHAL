---
applyTo: "**"
---

# 🧪 Estratégia de Testes - Implementação Prática

## 🎯 Para GitHub Copilot: Geração Automática de Testes

### Padrão AAA Obrigatório

```csharp
[Test]
public async Task UserService_CreateUser_DeveRetornarUsuarioCriado()
{
    // Arrange
    var userRequest = new CreateUserRequest
    {
        Email = "test@example.com",
        Name = "Test User"
    };
    var mockRepository = new Mock<IUserRepository>();
    var userService = new UserService(mockRepository.Object);

    // Act
    var result = await userService.CreateUserAsync(userRequest);

    // Assert
    Assert.That(result, Is.Not.Null);
    Assert.That(result.Email, Is.EqualTo(userRequest.Email));
    mockRepository.Verify(r => r.CreateAsync(It.IsAny<User>()), Times.Once);
}
```

### Nomenclatura Padrão

**Formato**: `<ClasseTeste>_<Método>_<Cenário>_<ResultadoEsperado>`

**Exemplos**:

```csharp
UserService_CreateUser_ComEmailValido_DeveRetornarUsuario()
UserService_CreateUser_ComEmailInvalido_DeveLancarValidationException()
UserService_CreateUser_QuandoEmailJaExiste_DeveLancarConflictException()
UserController_GetUser_ComIdValido_DeveRetornarOkResult()
UserController_GetUser_ComIdInexistente_DeveRetornar404()
```

### Testes por Camada

#### Controllers (Testes de Integração)

```csharp
[TestFixture]
public class UserControllerTests : IntegrationTestBase
{
    [Test]
    public async Task Post_User_ComDadosValidos_DeveRetornar201()
    {
        // Arrange
        var request = new CreateUserRequest { /* dados válidos */ };

        // Act
        var response = await Client.PostAsJsonAsync("/api/users", request);

        // Assert
        Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.Created));
        var user = await response.Content.ReadFromJsonAsync<UserResponse>();
        Assert.That(user.Email, Is.EqualTo(request.Email));
    }
}
```

#### Services (Testes Unitários)

```csharp
[TestFixture]
public class UserServiceTests
{
    private Mock<IUserRepository> _mockRepository;
    private Mock<ILogger<UserService>> _mockLogger;
    private UserService _userService;

    [SetUp]
    public void Setup()
    {
        _mockRepository = new Mock<IUserRepository>();
        _mockLogger = new Mock<ILogger<UserService>>();
        _userService = new UserService(_mockRepository.Object, _mockLogger.Object);
    }

    [Test]
    public async Task CreateUserAsync_ComEmailUnico_DeveRetornarUsuario()
    {
        // Implementação do teste...
    }
}
```

### Testes de API (Casos Obrigatórios)

#### Casos de Sucesso

- [ ] GET com dados válidos retorna 200
- [ ] POST com dados válidos retorna 201
- [ ] PUT com dados válidos retorna 200/204
- [ ] DELETE com ID válido retorna 204

#### Casos de Erro

- [ ] GET com ID inexistente retorna 404
- [ ] POST com dados inválidos retorna 400
- [ ] Operações sem autenticação retornam 401
- [ ] Operações sem autorização retornam 403

#### Validação de Entrada

```csharp
[Test]
[TestCase("", "Nome é obrigatório")]
[TestCase("a", "Nome deve ter pelo menos 2 caracteres")]
[TestCase(null, "Nome é obrigatório")]
public async Task CreateUser_ComNomeInvalido_DeveRetornarBadRequest(
    string nome, string mensagemEsperada)
{
    // Arrange
    var request = new CreateUserRequest { Name = nome };

    // Act
    var response = await Client.PostAsJsonAsync("/api/users", request);

    // Assert
    Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.BadRequest));
    var errors = await response.Content.ReadFromJsonAsync<ValidationErrorResponse>();
    Assert.That(errors.Errors.Any(e => e.Message.Contains(mensagemEsperada)), Is.True);
}
```

### Mocking Guidelines

#### Dependências Externas

```csharp
// ✅ Mock de serviços externos
var mockEmailService = new Mock<IEmailService>();
mockEmailService
    .Setup(s => s.SendAsync(It.IsAny<EmailMessage>()))
    .ReturnsAsync(true)
    .Verifiable();

// ✅ Verificação de chamadas
mockEmailService.Verify(
    s => s.SendAsync(It.Is<EmailMessage>(m => m.To == "test@example.com")),
    Times.Once);
```

#### Base de Dados

```csharp
// ✅ Usar banco em memória para testes de integração
services.AddDbContext<AppDbContext>(options =>
    options.UseInMemoryDatabase(databaseName: Guid.NewGuid().ToString()));

// ✅ Mock repository para testes unitários
var mockRepository = new Mock<IUserRepository>();
mockRepository
    .Setup(r => r.GetByIdAsync(It.IsAny<int>()))
    .ReturnsAsync((User)null);
```

### Performance Tests

```csharp
[Test]
public async Task GetUsers_ComMuitosRegistros_DeveRetornarEmMenosDe500ms()
{
    // Arrange
    var stopwatch = Stopwatch.StartNew();

    // Act
    var response = await Client.GetAsync("/api/users?pageSize=1000");
    stopwatch.Stop();

    // Assert
    Assert.That(response.StatusCode, Is.EqualTo(HttpStatusCode.OK));
    Assert.That(stopwatch.ElapsedMilliseconds, Is.LessThan(500));
}
```

### Dados de Teste (Builder Pattern)

```csharp
public class UserTestBuilder
{
    private User _user = new User();

    public UserTestBuilder WithEmail(string email)
    {
        _user.Email = email;
        return this;
    }

    public UserTestBuilder WithName(string name)
    {
        _user.Name = name;
        return this;
    }

    public User Build() => _user;
}

// Uso:
var user = new UserTestBuilder()
    .WithEmail("test@example.com")
    .WithName("Test User")
    .Build();
```

## 🎯 Instruções para Copilot

Ao gerar testes:

1. **SEMPRE** usar padrão AAA
2. **SEMPRE** seguir nomenclatura especificada
3. **SEMPRE** incluir casos de erro
4. **SEMPRE** mockar dependências externas
5. **SEMPRE** verificar assertions adequadas
6. **SEMPRE** incluir testes de validação
7. **CONSIDERAR** performance em testes de integração
8. **DOCUMENTAR** cenários complexos com comentários

```

```
