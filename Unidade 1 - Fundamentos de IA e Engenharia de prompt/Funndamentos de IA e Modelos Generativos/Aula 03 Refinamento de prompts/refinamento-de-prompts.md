# Atividade - Refinamento de Prompts

## Identificação
- **Nome:** Rafael Pereira de Oliveira
- **RGM:** 35959851
- **Curso:** Ciência da Computação
- **Disciplina:** Tendências em Ciência da Computação
- **Data:** 03/09/2026
- **Ferramenta de IA utilizada:** Claude (Anthropic)

---

## Problema Escolhido

- **Contexto:** Em sistemas concorrentes — servidores web multi-thread, aplicações mobile com múltiplas tarefas assíncronas ou sistemas embarcados — vários fluxos de execução acessam a mesma região de memória compartilhada ao mesmo tempo. Quando o acesso não é devidamente sincronizado, o resultado do programa passa a depender da ordem imprevisível em que as threads são escalonadas pelo sistema operacional, gerando falhas difíceis de reproduzir e depurar.
- **Problema:** O que é uma condição de corrida (*race condition*), por que ela surge mesmo em código aparentemente correto, e quais mecanismos de sincronização (locks, mutexes, semáforos, variáveis atômicas) existem para eliminá-la sem comprometer o desempenho?
- **Objetivo:** Investigar, por meio de refinamento iterativo de prompts, como a formulação do comando dado a uma IA generativa impacta diretamente a profundidade técnica, o rigor conceitual e o valor pedagógico da resposta obtida sobre esse tema de concorrência.

---

## Prompt 1 - Versão Inicial

- **Prompt:**
  ```
  Explique o que é condição de corrida.
  ```

- **Resultado:**
  > Condição de corrida é um problema que acontece em programação quando duas ou mais threads tentam acessar e modificar o mesmo dado ao mesmo tempo, e o resultado final depende da ordem em que isso acontece. Isso pode causar erros no programa, como valores incorretos ou comportamento inesperado. Para evitar isso, os programadores usam técnicas como locks para controlar o acesso aos dados compartilhados.

- **Análise:** A resposta é coerente e gramaticalmente correta, mas superficial: define o conceito em nível de senso comum, sem apresentar um exemplo de código, sem discutir a causa raiz (a não atomicidade de operações compostas como leitura-modificação-escrita), sem mencionar as ferramentas formais de sincronização e sem qualquer contextualização para o nível de um estudante de graduação em Ciência da Computação. Segundo a cartilha "IA no comando? Você no controle", esse é exatamente o risco descrito no capítulo "O que a IA não faz por você": um texto bem escrito, com aparência de segurança, mas que não substitui a leitura crítica nem entrega profundidade técnica real. Há coerência textual, mas ausência quase total de profundidade técnica — faltam formalização, exemplos e limites de aplicabilidade.

---

## Prompt 2 - Primeiro Refinamento

- **Alterações realizadas:** Aplicação dos 6 elementos essenciais de engenharia de prompt trabalhados na aula:
  1. **Perfil** — papel definido para a IA (professor de Sistemas Operacionais/Programação Concorrente).
  2. **Tarefa** — ação específica solicitada (explicar, exemplificar e comparar mecanismos).
  3. **Cenário/Contexto** — nível acadêmico e disciplina (graduação em Ciência da Computação, curso de Sistemas Operacionais ou Programação Concorrente).
  4. **Passo a passo** — estrutura lógica exigida para a resposta.
  5. **Exemplo/Público** — pedido explícito de um trecho de código ilustrativo.
  6. **Formato de saída/Restrições** — extensão, uso de tópicos e linguagem técnica esperada.

- **Prompt:**
  ```
  Atue como um professor universitário de Sistemas Operacionais e Programação 
  Concorrente. Preciso que você explique o conceito de condição de corrida 
  (race condition) para um estudante de graduação em Ciência da Computação 
  que já conhece os fundamentos de threads e processos, mas ainda não domina 
  mecanismos de sincronização.

  Siga esta estrutura:
  1. Defina formalmente o que é uma condição de corrida e por que ela ocorre 
     (relacione com o conceito de seção crítica e operações não atômicas).
  2. Apresente um pequeno exemplo de pseudocódigo (uma variável de saldo 
     bancário incrementada por duas threads) mostrando como o problema surge.
  3. Explique, em linhas gerais, dois mecanismos de sincronização usados para 
     resolvê-lo (mutex e semáforo), destacando a diferença conceitual entre eles.

  Formato de saída: use tópicos, linguagem técnica adequada ao nível de 
  graduação e no máximo 300 palavras.
  ```

- **Resultado:**
  > **1. Definição formal:** Uma condição de corrida ocorre quando o resultado de um trecho de código depende da ordem de execução de duas ou mais threads que acessam concorrentemente uma mesma região de memória compartilhada — a chamada seção crítica —, sem controle de exclusão mútua. A causa raiz está no fato de que operações que parecem uma única instrução em alto nível (como `saldo += 10`) na verdade se decompõem em múltiplos passos no nível de máquina (ler, somar, escrever), e o escalonador pode intercalar esses passos entre threads distintas.
  >
  > **2. Exemplo:**
  > ```
  > // saldo = 100 (compartilhado)
  > Thread A: ler saldo (100) -> somar 10 -> escrever (110)
  > Thread B: ler saldo (100) -> somar 20 -> escrever (120)
  > ```
  > Se A e B intercalarem a leitura antes de qualquer escrita, o resultado final pode ser 110 ou 120, e não 130 como o esperado, porque uma atualização sobrescreve a outra.
  >
  > **3. Mecanismos de sincronização:**
  > - **Mutex:** garante exclusão mútua — apenas uma thread por vez pode entrar na seção crítica, as demais ficam bloqueadas até a liberação do lock.
  > - **Semáforo:** generaliza o mutex ao permitir controlar o acesso de até *N* threads simultâneas por meio de um contador; é usado tanto para exclusão mútua (semáforo binário) quanto para sincronização de produtores/consumidores.

  Essa resposta já apresenta estrutura acadêmica, formalização e um exemplo prático, atendendo de forma mais consistente ao nível esperado de um curso de graduação.

---

## Comparação: Prompt 1 vs. Prompt 2

| Critério                  | Prompt 1 | Prompt 2 | Justificativa |
|----------------------------|:--------:|:--------:|----------------|
| Clareza                    | 3        | 5        | O Prompt 2 organiza a resposta em etapas numeradas, facilitando o acompanhamento do raciocínio. |
| Precisão                   | 2        | 4        | O Prompt 1 usa termos genéricos ("dado"); o Prompt 2 emprega vocabulário técnico correto (seção crítica, atomicidade). |
| Relevância                 | 3        | 5        | O Prompt 2 conecta a explicação diretamente ao conteúdo típico de uma disciplina de Sistemas Operacionais. |
| Organização                | 2        | 5        | A estrutura em tópicos do Prompt 2 reflete diretamente o passo a passo solicitado. |
| Adequação ao público       | 2        | 4        | O Prompt 2 calibra a explicação para quem já conhece threads/processos, evitando redundância básica. |
| Atendimento ao objetivo    | 2        | 4        | Ainda falta, no Prompt 2, uma etapa de verificação crítica ou contraexemplo — resolvido apenas no Prompt 3. |

---

## Prompt 3 - Segundo Refinamento

- **O que ainda precisava melhorar?** Mesmo estruturada, a resposta do Prompt 2 ainda apresenta risco de "ilusão de fluência": o estudante pode ler o texto, achá-lo convincente e assumir que compreendeu o assunto sem de fato testar seu próprio raciocínio. Faltam também: (i) grounding explícito em referências clássicas da área (ex.: Dijkstra, Silberschatz), (ii) casos em que os mecanismos apresentados falham ou têm custo de desempenho, (iii) limites de complexidade/overhead de cada solução, e (iv) um mecanismo ativo de verificação da aprendizagem, em vez de uma conclusão pronta.
- **Hipótese:** Se o prompt exigir explicitamente grounding em literatura consolidada, casos de falha e perguntas diagnósticas ao final — em vez de uma síntese fechada — o estudante é forçado a articular a própria resposta, o que caracteriza o método socrático descrito na cartilha (seção "IA como tutora"). Isso reduz a passividade cognitiva e aumenta a retenção, pois a IA deixa de "entregar a resposta pronta" e passa a estimular a checagem ativa do conhecimento.
- **Prompt:**
  ```
  Atue como um professor universitário de Sistemas Operacionais, especialista 
  em programação concorrente. Aprofunde a explicação sobre condição de corrida 
  para um estudante de graduação em Ciência da Computação, com as seguintes 
  exigências obrigatórias:

  1. Fundamente a explicação citando, por nome, ao menos um conceito ou autor 
     clássico da área de sistemas operacionais/concorrência (ex.: seção 
     crítica de Dijkstra, ou o modelo de exclusão mútua descrito em obras 
     consagradas de Sistemas Operacionais).
  2. Apresente um caso em que o uso de mutex NÃO é suficiente ou introduz um 
     novo problema (por exemplo, deadlock ou starvation), explicando por que 
     isso ocorre.
  3. Discuta o custo de desempenho (overhead) da sincronização e em que 
     situações mecanismos lock-free ou operações atômicas são preferíveis.
  4. NÃO conclua com um resumo fechado. Em vez disso, termine a resposta com 
     exatamente 2 perguntas diagnósticas que me obriguem a aplicar o conceito 
     e verificar minha própria compreensão.
  ```

- **Resultado:**
  > A condição de corrida está diretamente ligada ao conceito de seção crítica, formalizado por Edsger Dijkstra na década de 1960 ao propor o problema da exclusão mútua entre processos concorrentes. A ideia central é que apenas um processo/thread deve executar a seção crítica por vez, e qualquer solução deve garantir exclusão mútua, progresso e espera limitada.
  >
  > **Quando o mutex não é suficiente:** o uso de múltiplos locks pode gerar *deadlock* — por exemplo, quando a Thread A retém o Lock 1 e espera pelo Lock 2, enquanto a Thread B retém o Lock 2 e espera pelo Lock 1; nenhuma das duas consegue prosseguir. Esse cenário clássico (espera circular) mostra que resolver a condição de corrida não elimina automaticamente todos os riscos de concorrência — é possível também que uma thread sofra *starvation*, nunca conseguindo acesso ao recurso se o escalonador favorecer sistematicamente outras threads.
  >
  > **Custo de desempenho:** todo mecanismo de sincronização com bloqueio introduz overhead — contexto de troca de threads, possível serialização de operações que poderiam ser paralelas, e risco de contenção quando muitas threads disputam o mesmo lock. Em cenários de alta concorrência com operações simples (como incrementar um contador), operações atômicas (ex.: `compare-and-swap`) e estruturas *lock-free* costumam ter desempenho superior, pois evitam bloqueio de threads e delegam a consistência ao hardware.
  >
  > **Perguntas diagnósticas:**
  > 1. Se duas threads usam mutexes diferentes para proteger a mesma variável compartilhada por engano, a condição de corrida é eliminada? Justifique.
  > 2. Em que tipo de aplicação (baixa ou alta concorrência, operações simples ou complexas) você recomendaria usar uma operação atômica em vez de um mutex, e por quê?

---

## Comparação Final das Três Versões

| Critério                                | Prompt 1 | Prompt 2 | Prompt 3 |
|-------------------------------------------|:--------:|:--------:|:--------:|
| Clareza                                   | 3        | 5        | 5        |
| Precisão                                  | 2        | 4        | 5        |
| Relevância                                | 3        | 5        | 5        |
| Organização                               | 2        | 5        | 5        |
| Adequação ao público                      | 2        | 4        | 5        |
| Atendimento ao objetivo                   | 2        | 4        | 5        |
| Utilidade prática / aprendizado ativo     | 1        | 3        | 5        |
| **Total (de 35)**                         | **15**   | **30**   | **35**   |

---

## Validação Técnica

Para reduzir o risco de alucinação e de "ilusão de fluência" apontado na cartilha, adotei o seguinte procedimento de verificação crítica sobre as respostas geradas:

1. **Comparação com literatura padrão:** os conceitos de seção crítica, exclusão mútua, deadlock e starvation apresentados foram confrontados com definições consolidadas em bibliografia clássica de Sistemas Operacionais (ex.: Silberschatz, Galvin e Gagne, *Operating System Concepts*), confirmando que a terminologia empregada pela IA está alinhada ao consenso acadêmico da área.
2. **Verificação de terminologia:** termos técnicos específicos (mutex, semáforo, *compare-and-swap*, *lock-free*) foram checados individualmente quanto ao uso correto no contexto de programação concorrente, evitando o uso de jargão de forma imprecisa ou fora de contexto.
3. **Teste de explicação autoral:** após ler a resposta do Prompt 3, tentei reformular o conceito de deadlock e o exemplo de espera circular inteiramente com minhas próprias palavras, sem consultar novamente a resposta da IA, como forma de confirmar que a compreensão foi de fato internalizada e não apenas copiada.
4. **Resposta às perguntas diagnósticas:** respondi ativamente às duas perguntas finais do Prompt 3 antes de considerar o conteúdo validado, seguindo a lógica de tutoria socrática recomendada pela cartilha.

---

## Reflexão Individual

**1. Qual foi a principal diferença entre o prompt inicial e o refinado?**
O prompt inicial era genérico e não definia papel, público, estrutura ou formato, resultando em uma resposta correta mas rasa. O prompt refinado (Prompt 2) definiu claramente o perfil da IA, o público-alvo, uma estrutura em etapas e restrições de formato, o que elevou substancialmente a precisão técnica e a organização da resposta. O Prompt 3 foi além, adicionando exigências de fundamentação teórica, contraexemplos e verificação ativa.

**2. Quais elementos tiveram maior impacto no resultado?**
A definição do perfil/papel da IA e o passo a passo estrutural foram os elementos com maior impacto imediato, pois direcionaram o nível de profundidade e a organização da resposta. No Prompt 3, a exigência de citar referências clássicas e de apresentar um caso de falha do mecanismo (deadlock) foi o que mais elevou o rigor técnico, enquanto a exigência das perguntas diagnósticas foi o que mais aumentou o valor pedagógico.

**3. Um prompt mais longo necessariamente produz uma resposta melhor? Justifique.**
Não. Um prompt longo, porém vago ou redundante, pode gerar respostas dispersas ou repetitivas. O que determina a qualidade é a precisão das instruções — perfil, tarefa, contexto, estrutura, exemplo e restrições bem definidos — e não o número de palavras em si. O Prompt 3 é mais longo que o Prompt 1, mas sua superioridade vem da especificidade das exigências, não do comprimento em si.

**4. O que ocorre quando o objetivo não é claro?**
A IA tende a produzir uma resposta genérica, "segura" e superficial, tentando cobrir múltiplas interpretações possíveis do pedido. Isso é exatamente o que ocorreu no Prompt 1: sem um objetivo pedagógico claro, a resposta ficou correta em termos gerais, mas sem profundidade técnica nem direcionamento para o nível de um estudante de graduação.

**5. Quais informações são indispensáveis para formular um bom prompt?**
São indispensáveis: (i) o perfil/papel esperado da IA, (ii) a tarefa específica a ser realizada, (iii) o contexto ou cenário de aplicação, (iv) uma estrutura ou passo a passo desejado, (v) exemplos ou definição clara do público-alvo, e (vi) o formato de saída e eventuais restrições (extensão, tom, linguagem).

**6. Como essa habilidade se aplica na rotina profissional de Ciência da Computação?**
Engenharia de prompt é diretamente aplicável à documentação técnica, revisão de código assistida por IA, geração de testes, depuração guiada e até *design review* de arquiteturas de software. Um profissional que formula prompts precisos obtém respostas mais úteis e reduz o retrabalho de validar ou corrigir saídas genéricas — competência cada vez mais relevante em ambientes que integram IA generativa ao fluxo de desenvolvimento.

**7. Quais riscos existem ao confiar cegamente nas respostas da IA?**
Os principais riscos são: aceitar informações incorretas apresentadas com aparência de autoridade (alucinações), citar fontes inexistentes inventadas pela IA, desenvolver uma falsa sensação de domínio do conteúdo ("ilusão de fluência") sem capacidade real de explicá-lo, comprometer a integridade acadêmica ao entregar como próprio um raciocínio que não foi verificado nem compreendido, e expor dados sensíveis em ferramentas cuja política de privacidade e retenção de dados nem sempre é totalmente transparente.

---

## Take Away

*"Um bom prompt não é simplesmente um prompt longo. Ele precisa ser preciso, contextualizado e estruturado — definindo claramente quem a IA deve ser, o que deve fazer, para quem, com que profundidade e em que formato — além de exigir verificação ativa em vez de aceitação passiva da resposta."*

---

## Cinco Recomendações Práticas

1. **Defina sempre o perfil e o objetivo antes de perguntar.** Um prompt sem papel, público e objetivo claros tende a gerar respostas genéricas e de baixo valor acadêmico.
2. **Nunca entregue como seu algo que você não consegue explicar sem a IA.** Se não for capaz de reformular o conteúdo com as próprias palavras, o conhecimento ainda não foi internalizado.
3. **Confira toda citação, dado numérico ou referência gerada antes de usá-la.** IAs generativas podem produzir fontes plausíveis, porém inexistentes.
4. **Use a IA para gerar perguntas e testar seu raciocínio, não apenas para obter respostas prontas.** O método socrático potencializa o aprendizado ativo.
5. **Declare formalmente o uso de IA em trabalhos acadêmicos, sempre que a instituição ou a disciplina exigir.** Transparência sobre o apoio recebido preserva a integridade acadêmica.

---

## Modelo de Declaração de Uso da IA

> **Declaração de Uso de Inteligência Artificial**
>
> Eu, Rafael Pereira de Oliveira, RGM 35959851, declaro que utilizei a ferramenta de Inteligência Artificial Claude (Anthropic) como suporte ao processo de estudo e elaboração desta atividade da disciplina de Tendências em Ciência da Computação, referente ao tema "Condição de Corrida em Sistemas Concorrentes".
>
> A IA foi empregada para: (i) auxiliar na estruturação e no refinamento iterativo dos prompts apresentados; (ii) apoiar a explicação de conceitos técnicos previamente estudados; e (iii) sugerir exemplos e perguntas de verificação de aprendizagem.
>
> Toda a análise crítica, a validação técnica das informações apresentadas, a redação da reflexão individual e as conclusões desta atividade são de minha autoria e responsabilidade exclusiva. As informações geradas pela IA foram confrontadas com literatura acadêmica de referência antes de sua incorporação a este documento, em conformidade com os princípios de uso ético, crítico e responsável de IA estabelecidos na cartilha "IA no comando? Você no controle" (Grupo IA STHEM / SEMESP / MetaRed TIC).
>
> Assumo total responsabilidade pela veracidade, correção e originalidade do conteúdo aqui apresentado.
>
> São Paulo, 03 de setembro de 2026.
>
> ___________________________________
> Rafael Pereira de Oliveira
