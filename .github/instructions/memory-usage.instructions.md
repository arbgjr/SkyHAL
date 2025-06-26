---
description: "Instruções para uso efetivo do sistema de memória"
---

# Sistema de Memória Inteligente

## Protocolo de Memória

### 1. Identificação do Contexto
- Sempre identifique o usuário e projeto atual
- Use entidades específicas para diferentes contextos de trabalho

### 2. Recuperação de Memória
- **Sempre comece** dizendo "Lembrando..." e recupere informações relevantes
- Use `#memory_search` com termos específicos da tarefa
- Consulte knowledge graph como sua "memória"

### 3. Categorias de Informação para Armazenar
Durante conversas, seja atento a:

**a) Identidade Básica**:
- Papel/função, nível de experiência, localização
- Preferências técnicas, frameworks favoritos

**b) Comportamentos e Hábitos**:
- Padrões de trabalho, metodologias preferidas
- Frequência de certas tarefas

**c) Preferências**:
- Estilo de comunicação, linguagem preferida
- Ferramentas e bibliotecas favoritas

**d) Objetivos**:
- Metas de curto e longo prazo
- Projetos em andamento

**e) Relacionamentos**:
- Conexões com projetos, tecnologias, pessoas
- Dependências entre componentes

### 4. Atualização de Memória
Quando nova informação for coletada:

**a) Criar entidades** para:
- Organizações recorrentes
- Pessoas importantes
- Eventos significativos
- Projetos e tecnologias

**b) Conectar entidades** usando relações:
- "trabalha-em", "usa-tecnologia", "depende-de"
- "similar-a", "substitui", "melhoria-de"

**c) Armazenar fatos** como observações:
- Resultados de análises
- Lições aprendidas
- Problemas encontrados e soluções

## Exemplos Práticos

### Análise de Dados:
	```
	#memory_create_entities nome="Projeto_Vendas_Q4" tipo="projeto"
	#memory_create_observations entidade="Projeto_Vendas_Q4" observacao="Dataset tinha problemas em dezembro"
	#memory_create_relations origem="Projeto_Vendas_Q4" relacao="usa_tecnologia" destino="pandas"
	```

### Desenvolvimento:
	```
	#memory_create_entities nome="API_Usuarios" tipo="componente"
	#memory_create_relations origem="API_Usuarios" relacao="depende_de" destino="PostgreSQL"
	#memory_create_observations entidade="API_Usuarios" observacao="Autenticação JWT implementada com sucesso"
	```

### Reflexão e Aprendizado:
	```
	#memory_search "problemas performance banco dados"
	#memory_create_observations entidade="Otimizacao_DB" observacao="Indexes em colunas de join melhoram performance 300%"
	```

Use sempre o knowledge graph para construir uma base de conhecimento rica e consultável.
