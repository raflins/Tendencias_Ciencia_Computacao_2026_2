# Programação Assistida e Automação com IA

## Identificação
**Nome:** Rafael Pereira de Oliveira[cite: 2]
**Turma:** Ciência da Computação / Tendências em CC[cite: 2]
**Data:** 10/09/2026[cite: 2]
**Ferramenta de IA utilizada:** Claude 3.5 Sonnet / Gemini[cite: 2]

## 1. Problema
**Opção E (Problema proposto):** Automatizar o cálculo de faturamento líquido diário como motorista de aplicativo, descontando a taxa da plataforma e o custo estimado de combustível ao final do dia[cite: 2].

## 2. Entrada
Uma lista de dicionários simulando um log de viagens diárias. Cada registro (dicionário) contém o valor recebido na corrida (`valor_bruto`) e a quilometragem rodada (`km_rodado`)[cite: 2].

## 3. Processamento
O script deve percorrer a lista de viagens, somar o faturamento bruto total, abater 25% de taxa do aplicativo e calcular o gasto com combustível com base no consumo do meu carro (um Ford Fiesta 2010 manual, com média de 10 km/L) a um preço médio da gasolina (R$ 5,80/L). Em seguida, subtrair as despesas para encontrar o lucro líquido diário[cite: 2].

## 4. Saída esperada
Exibição consolidada no terminal: Total Bruto, Total Retido pelo App, Gasto de Combustível e Lucro Líquido[cite: 2].

## 5. Prompt utilizado
> "Atue como um desenvolvedor Python. PROBLEMA: Preciso automatizar o cálculo dos meus ganhos diários como motorista de app. ENTRADA: Uma lista de dicionários com 'valor_bruto' e 'km_rodado'. SAÍDA ESPERADA: Um resumo impresso no terminal contendo o faturamento bruto, o custo do combustível, a taxa do aplicativo (25%) e o lucro líquido final. LINGUAGEM: Python (apenas libs padrão). RESTRIÇÕES: Considere o consumo do meu carro (manual) fixo em 10 km/L e o preço do combustível a R$ 5,80. Não crie classes complexas nesta primeira versão. CRITÉRIOS DE QUALIDADE: Código limpo, comentado e com variáveis em português."[cite: 2]

## 6. Código inicial
```python
def calcular_lucro_diario(corridas):
    total_bruto = 0
    total_km = 0
    
    for corrida in corridas:
        total_bruto += corrida["valor_bruto"]
        total_km += corrida["km_rodado"]
        
    taxa_app = total_bruto * 0.25
    custo_combustivel = (total_km / 10) * 5.80
    lucro_liquido = total_bruto - taxa_app - custo_combustivel
    
    print(f"Total Bruto: R$ {total_bruto:.2f}")
    print(f"Taxa do App: R$ {taxa_app:.2f}")
    print(f"Custo Combustível: R$ {custo_combustivel:.2f}")
    print(f"Lucro Líquido: R$ {lucro_liquido:.2f}")

# Log de teste
viagens = [
    {"valor_bruto": 25.00, "km_rodado": 12},
    {"valor_bruto": 15.50, "km_rodado": 6.5}
]
calcular_lucro_diario(viagens)
```

## 7. Análise crítica
O código funciona bem para uma primeira versão e atende à regra de negócio. Contudo, os valores operacionais (consumo do veículo de `10` km/L e preço da gasolina `5.80`) estão *hardcoded* (fixos direto no cálculo). Além disso, não há nenhum mecanismo de proteção caso a lista venha corrompida do aplicativo sem a chave `km_rodado`, o que causaria a interrupção da execução do script[cite: 2].

## 8. Casos de teste
### Teste 1 (Caso normal)
- **Entrada:** `[{"valor_bruto": 40.0, "km_rodado": 20}]`[cite: 2]
- **Resultado obtido:** Execução perfeita. Calculou R$ 40,00 bruto, R$ 10,00 de taxa, R$ 11,60 de combustível e R$ 18,40 líquidos[cite: 2].

### Teste 2 (Caso limite)
- **Entrada:** `[]` (Lista vazia no dia em que não rodei)[cite: 2]
- **Resultado obtido:** Funcionou, exibindo R$ 0,00 em todas as métricas[cite: 2].

### Teste 3 (Caso de erro)
- **Entrada:** `[{"valor_bruto": 18.0}]` (Falha no GPS, não salvou o KM)[cite: 2]
- **Resultado obtido:** O script travou imediatamente com um `KeyError: 'km_rodado'`[cite: 2].

## 9. Problemas encontrados
O script paralisou totalmente no Teste 3. A ausência de tratamento de erros em dicionários torna a automação muito frágil para dados do mundo real (que frequentemente apresentam falhas de registro)[cite: 2].

## 10. Prompt de refatoração
> "Revise o código abaixo. O programa já funciona para os casos normais. Agora analise e melhore a clareza e o tratamento de erros. Sugira melhorias sem alterar o comportamento esperado: extraia os valores de consumo e preço do combustível para parâmetros da função, e proteja o acesso ao dicionário (evitando o KeyError caso falte a chave do KM ou do valor bruto). Explique as alterações propostas."[cite: 2]

## 11. Código refatorado
```python
def calcular_lucro_diario_otimizado(corridas, consumo_km_l=10.0, preco_combustivel=5.80, taxa_plataforma=0.25):
    total_bruto = 0.0
    total_km = 0.0
    
    for corrida in corridas:
        # Tratamento de erro: uso do .get() com valor default 0.0
        # Evita KeyError e mantém o script rodando se faltar algum dado
        valor = corrida.get("valor_bruto", 0.0)
        km = corrida.get("km_rodado", 0.0)
        
        total_bruto += valor
        total_km += km
        
    total_taxa = total_bruto * taxa_plataforma
    
    # Tratamento para evitar divisão por zero, caso o consumo passado seja 0
    custo_combustivel = 0.0
    if consumo_km_l > 0:
        custo_combustivel = (total_km / consumo_km_l) * preco_combustivel
        
    lucro_liquido = total_bruto - total_taxa - custo_combustivel
    
    print("-" * 30)
    print("RELATÓRIO DIÁRIO DE CORRIDAS")
    print("-" * 30)
    print(f"Faturamento Bruto: R$ {total_bruto:.2f}")
    print(f"Taxa Retida (App): R$ {total_taxa:.2f}")
    print(f"Custo Combustível: R$ {custo_combustivel:.2f}")
    print(f"Lucro Líquido:     R$ {lucro_liquido:.2f}")
    print("-" * 30)

# Log de teste com erro injetado
viagens_reais = [
    {"valor_bruto": 25.00, "km_rodado": 12},
    {"valor_bruto": 15.50}, # Dado corrompido sem o KM
]
calcular_lucro_diario_otimizado(viagens_reais)
```

## 12. Comparação
| Critério | Inicial | Refatorado |
| :--- | :--- | :--- |
| Funcionamento | 3 | 5 |
| Clareza | 4 | 5 |
| Organização | 3 | 5 |
| Legibilidade | 4 | 5 |
| Tratamento de erros | 1 | 5 |

## 13. Reflexão
- **Onde a IA mais ajudou?** Na velocidade de construção da lógica aritmética inicial e na identificação rápida de que o método `.get(chave, valor_padrao)` era a forma mais pythônica de evitar a quebra do script[cite: 2].
- **Onde a IA errou?** A IA não se preocupou com a resiliência na primeira geração do código. Ela assumiu o melhor cenário possível, onde os logs de viagens são sempre perfeitos[cite: 2].
- **O que precisei modificar?** Precisei forçar a IA, via prompt, a desengessar as constantes operacionais (como a média do Fiesta e o preço atualizado da gasolina) e atuar em cima das vulnerabilidades de estrutura de dados que eu mesmo identifiquei nos testes de estresse[cite: 2].
- **Consigo explicar o código?** Sim, o código itera de forma segura sobre os relatórios extraindo chaves de forma defensiva, isola os fatores de desconto e renderiza as métricas finais formatadas no console[cite: 2].

## 14. Take Away
Programar com IA não significa delegar o desenvolvimento de forma cega. Significa atuar como um **Tech Lead**, onde eu planejo a estrutura, valido as condições de uso do mundo real, e oriento a IA a gerar uma solução robusta.

**Regras de uso responsável[cite: 2]:**
1. Nunca aceitar o "caminho feliz" (primeiro código) como código pronto para produção.
2. Planejar sempre os casos limites (entradas vazias ou corrompidas) antes de rodar o código.
3. Não colocar tokens bancários ou dados pessoais de passageiros nos prompts.
4. Manter variáveis de negócio parametrizáveis, nunca chumbadas no código da IA.
5. Só utilizar a sugestão da máquina caso consiga ler, explicar e depurar cada linha do processo.