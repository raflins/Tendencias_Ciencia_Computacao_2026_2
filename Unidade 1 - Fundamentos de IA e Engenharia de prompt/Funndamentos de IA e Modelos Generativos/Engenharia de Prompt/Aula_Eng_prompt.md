# Aula 02 — Engenharia de Prompt

## 1. Identificação

Disciplina: Tendências em Ciências da Computação  
Turma: N1  
Grupo: Individual  
Data: 21/08/2026  
Integrante: Rafael Pereira de Oliveira  

---

## 2. Problema escolhido

### Contexto
No desenvolvimento de software, a modelagem de banco de dados relacional é uma etapa crítica para garantir consistência, integridade referencial e performance das aplicações. Estudantes e desenvolvedores iniciantes frequentemente enfrentam dificuldades para normalizar tabelas (1FN a 3FN), definir chaves primárias e estrangeiras apropriadas e prever restrições de integridade ao transformar regras de negócio em esquemas SQL estruturados.

### Problema
Como utilizar uma ferramenta de Inteligência Artificial Generativa para auxiliar na modelagem de um banco de dados relacional e na geração de scripts SQL DDL normalizados e consistentes a partir de requisitos de negócio?

---

## 3. Objetivo

Utilizar IA Generativa para converter regras de negócio de um sistema de controle de frotas e despesas operacionais em um esquema relacional normalizado (3FN) e script SQL correspondente, avaliando as limitações da resposta inicial e iterando para um prompt robusto com restrições técnicas precisas.

---

## 4. Prompt inicial

Crie o banco de dados para um sistema de controle de frotas e despesas de veículos.

5. Resultado inicial
CREATE TABLE veiculo (
    id INT PRIMARY KEY,
    modelo VARCHAR(50),
    placa VARCHAR(10)
);

CREATE TABLE despesa (
    id INT PRIMARY KEY,
    valor DECIMAL(10,2),
    descricao VARCHAR(100),
    veiculo_id INT
);


Embora o código seja funcional, a resposta ignora tipos de despesas específicos (combustível, manutenção), controle de quilometragem/odômetro, chaves estrangeiras explícitas (FOREIGN KEY), índices e integridade referencial.
6. Análise crítica
O que funcionou?
A IA identificou as duas entidades mais óbvias (veículos e despesas) e utilizou sintaxe SQL válida.
O que não funcionou?
 * Ausência de constraints essenciais (NOT NULL, UNIQUE, FOREIGN KEY com regras de deleção).
 * Não normalizou entidades fundamentais (ex: categorias de despesa).
 * Não utilizou tipos de dados seguros e modernos (ex: VARCHAR(7) para placas Mercosul, TIMESTAMP WITH TIME ZONE para auditoria).
O que faltou?
 * Definição do SGBD alvo (PostgreSQL).
 * Regras de negócio detalhadas (odômetro, data/hora, tipo de despesa).
 * Padrões de normalização explícitos (3FN).
 * Formato de saída estruturado com Dicionário de Dados e Script DDL.
O que precisa ser validado?
 * Compatibilidade e precisão dos tipos de dados com o PostgreSQL.
 * Eficiência dos tipos numéricos (NUMERIC(10,2)) e integridade referencial em cascata.
A IA fez alguma suposição inadequada?
Sim. A IA assumiu que toda despesa se resume a um texto livre genérico, desconsiderando a necessidade de análises financeiras e métricas de uso por quilometragem.
7. Prompt refinado
PAPEL:
Você é um Arquiteto de Dados e Engenheiro de Software Sênior especialista em PostgreSQL.

CONTEXTO:
Estamos projetando a camada de persistência para uma aplicação de gestão de frotas e despesas operacionais. A aplicação precisa registrar veículos, categorias de gastos (combustível, manutenção, seguro) e despesas detalhadas com odômetro e datas.

OBJETIVO:
Elaborar a modelagem conceitual das tabelas normalizadas (3FN) e gerar o script SQL DDL correspondente no padrão PostgreSQL.

TAREFA:
1. Identifique as entidades necessárias com base no contexto.
2. Defina os relacionamentos (1:N) e suas respectivas chaves primárias e estrangeiras.
3. Gere o script SQL DDL com constraints obrigatórias (NOT NULL, UNIQUE, CHECK, FOREIGN KEY).
4. Crie índices para colunas frequentemente utilizadas em consultas analíticas.
5. Aponte pontos de atenção e validações necessárias.

RESTRIÇÕES:
- Utilize o dialeto PostgreSQL (versão 15+).
- Aplique convenção snake_case para nomes de tabelas e colunas.
- Tipos de dados monetários devem usar NUMERIC(10,2).
- Campos de data/hora devem usar TIMESTAMP WITH TIME ZONE.
- Garanta que a placa do veículo siga padrão com constraint UNIQUE.

FORMATO:
Apresente a resposta contendo:
1. Dicionário de dados em tabela Markdown: | Tabela | Coluna | Tipo | Constraint | Descrição |
2. Bloco de código com o Script SQL DDL executável.
3. Seção "Pontos de Atenção e Validação".

CRITÉRIOS DE QUALIDADE:
O script deve estar sintaticamente correto, normalizado até a 3ª Forma Normal e pronto para execução sem dependências cíclicas.

8. Resultado refinado
Dicionário de Dados
| Tabela | Coluna | Tipo | Constraint | Descrição |
|---|---|---|---|---|
| veiculos | id | BIGSERIAL | PRIMARY KEY | Identificador único do veículo |
| veiculos | placa | VARCHAR(7) | NOT NULL, UNIQUE | Placa do veículo (padrão Mercosul/Nacional) |
| veiculos | modelo | VARCHAR(100) | NOT NULL | Modelo e versão do veículo |
| veiculos | ano_fabricacao | SMALLINT | NOT NULL | Ano de fabricação |
| veiculos | criado_em | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Data de cadastro |
| categorias_despesa | id | SERIAL | PRIMARY KEY | Identificador da categoria |
| categorias_despesa | nome | VARCHAR(50) | NOT NULL, UNIQUE | Nome da categoria (ex: Combustível, Óleo) |
| despesas | id | BIGSERIAL | PRIMARY KEY | Identificador da despesa |
| despesas | veiculo_id | BIGINT | NOT NULL, FK | Referência à tabela veiculos |
| despesas | categoria_id | INT | NOT NULL, FK | Referência à tabela categorias_despesa |
| despesas | valor_total | NUMERIC(10,2) | NOT NULL, CHECK (>0) | Valor total da despesa |
| despesas | odometro_km | INT | NOT NULL, CHECK (>=0) | Quilometragem do veículo no ato do registro |
| despesas | data_hora | TIMESTAMPTZ | NOT NULL, DEFAULT NOW() | Data e hora do registro |
Script SQL DDL
CREATE TABLE veiculos (
    id BIGSERIAL PRIMARY KEY,
    placa VARCHAR(7) NOT NULL UNIQUE,
    modelo VARCHAR(100) NOT NULL,
    ano_fabricacao SMALLINT NOT NULL,
    criado_em TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE categorias_despesa (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE despesas (
    id BIGSERIAL PRIMARY KEY,
    veiculo_id BIGINT NOT NULL,
    categoria_id INT NOT NULL,
    valor_total NUMERIC(10,2) NOT NULL CHECK (valor_total > 0),
    odometro_km INT NOT NULL CHECK (odometro_km >= 0),
    observacoes TEXT,
    data_hora TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_despesas_veiculo 
        FOREIGN KEY (veiculo_id) REFERENCES veiculos(id) ON DELETE RESTRICT,
    CONSTRAINT fk_despesas_categoria 
        FOREIGN KEY (categoria_id) REFERENCES categorias_despesa(id) ON DELETE RESTRICT
);

CREATE INDEX idx_despesas_veiculo_data ON despesas(veiculo_id, data_hora DESC);
CREATE INDEX idx_despesas_categoria ON despesas(categoria_id);

Pontos de Atenção e Validação
 * Regra ON DELETE RESTRICT: protege o histórico financeiro, impedindo a exclusão acidental de veículos com despesas vinculadas.
 * Validação de odômetro: implementar lógica na camada de aplicação ou gatilho (trigger) para impedir inserção de odômetro menor que o último registrado.
 * Indexação composta (veiculo_id, data_hora DESC): otimiza consultas analíticas periódicas.
9. Técnicas utilizadas
 * [x] Role Prompting
 * [ ] Few-Shot Prompting
 * [x] Contexto
 * [x] Restrições
 * [x] Formato de saída
 * [x] Prompt em etapas
 * [x] Refinamento iterativo
 * [ ] Outra
Justificativa
 * Role Prompting: Definição do papel de Arquiteto de Dados e Engenheiro Sênior especialista em PostgreSQL.
 * Contexto: Detalhamento do domínio da aplicação (frotas, abastecimentos e manutenções).
 * Restrições: Limitações de dialeto (PostgreSQL 15+), nomenclatura (snake_case) e tipos monetários (NUMERIC).
 * Formato de saída: Exigência de tabela estruturada com dicionário de dados e código SQL isolado em bloco Markdown.
 * Prompt em etapas: Divisão da tarefa entre modelagem, relacionamentos, constraints, índices e pontos de atenção.
 * Refinamento iterativo: Ajuste sistemático a partir das deficiências identificadas na resposta do prompt inicial.
10. Comparação
| Critério | Prompt Inicial | Prompt Refinado |
|---|---|---|
| Clareza | Baixa (instrução aberta e genérica) | Alta (especificações e requisitos explícitos) |
| Contexto | Quase inexistente | Rico em regras de negócio e objetivos do sistema |
| Relevância | Genérica | Altamente aderente às necessidades da aplicação |
| Organização | Bloco simples de código | Dicionário em tabela, script SQL e pontos de validação |
| Precisão | Baixa (sem constraints ou índices) | Alta (tipos de dados corretos e 3ª Forma Normal) |
| Utilidade | Apenas didática/introdutória | Código DDL pronto para execução em banco real |
Análise da comparação
O prompt refinado produziu um resultado tecnicamente superior porque substituiu suposições rasas por restrições operacionais concretas (dialeto, formas normais e constraints de integridade), transformando um exemplo didático básico em um artefato profissional de software.
11. Validação
A validação da resposta foi realizada por meio das seguintes etapas:
 * Execução em Sandbox: O script SQL DDL foi testado diretamente em uma instância local do PostgreSQL 15 para validar sintaxe, dependências de compilação e integridade de chaves estrangeiras.
 * Checagem de Formas Normais: Análise manual das tabelas para confirmar a eliminação de dependências parciais e transitivas (garantindo 3FN).
 * Casos de Borda de Negócio: Simulação de integridade referencial ao tentar deletar veículos com dependências vinculadas.
12. Ética e responsabilidade
O uso de IA Generativa para arquitetura de dados traz riscos substanciais se aceito sem auditoria:
 * Integridade e Consistência: A IA pode omitir restrições essenciais de unicidade ou chaves estrangeiras, gerando inconsistências que podem corromper bases de dados inteiras.
 * Segurança e Conformidade (LGPD): Modelagens geradas podem ignorar requisitos de privacidade de dados sensíveis ou expor credenciais sem o isolamento correto.
 * Responsabilidade Profissional: O desenvolvedor humano é o único responsável pela robustez do código e pela garantia de integridade do sistema. A IA atua como aceleradora de prototipação
