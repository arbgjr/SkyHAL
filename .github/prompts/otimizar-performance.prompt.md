---
mode: 'agent'
tools: ['performance']
description: 'Analisa e otimiza performance do código seguindo padrões'
---

# Otimizador de Performance

Analise o código fornecido e sugira otimizações de performance seguindo os padrões.

## Áreas de Análise

### Frontend Performance
- **Core Web Vitals**: LCP, FID, CLS
- **Bundle Size**: Code splitting, tree shaking
- **Rendering**: Virtual DOM, memoization
- **Loading**: Lazy loading, prefetching
- **Caching**: Service workers, HTTP caching

### Backend Performance
- **Database**: Query optimization, indexing
- **Caching**: Redis, in-memory cache
- **API**: Rate limiting, pagination
- **Concurrency**: Async operations, connection pooling
- **Resource Usage**: Memory leaks, CPU usage

### Algorithm Analysis
- **Time Complexity**: Big O analysis
- **Space Complexity**: Memory usage optimization
- **Data Structures**: Appropriate choice for use case
- **Algorithms**: More efficient alternatives

## Métricas de Performance
- Response time targets
- Throughput requirements
- Memory usage limits
- CPU utilization thresholds
- Network bandwidth considerations

## Ferramentas de Profiling
- **Browser**: DevTools, Lighthouse
- **Node.js**: Node clinic, 0x profiler
- **Database**: Query explain plans
- **APM**: New Relic, DataDog

## Output Esperado
1. **Performance Issues**: Gargalos identificados
2. **Optimizations**: Sugestões de melhorias
3. **Code Examples**: Implementações otimizadas
4. **Benchmarks**: Comparações before/after
5. **Monitoring**: Métricas para acompanhar
