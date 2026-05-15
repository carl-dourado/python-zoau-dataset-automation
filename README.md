# Mainframe Dataset Automation (Python + TK5)

Automação em Python focada no fluxo de trabalho com IBM Z Mainframes, simulando e gerando ativos para o ambiente MVS/TK5 (Hercules).

**Tech Stack:** Python, JCL, IBM Z, Hercules/TK5, Linux, Unittest, TN3270.

---

## Contexto do Projeto

Esta automação surgiu de desafios práticos realizados durante meus estudos sobre mainframes (IBM Z Xplore). O script demonstra o fluxo real de integração entre um Linux local, o emulador Hercules/TK5 e o terminal 3270.

Como o ambiente TK5 (MVS 3.8j) é uma versão clássica, ele não suporta Python moderno nativamente. Por isso, a solução utiliza o Python como uma ferramenta de suporte externa que prepara o terreno para o Mainframe, garantindo que os jobs sejam enviados sem erros de sintaxe ou de lógica.

## O Diferencial: Mock PDS System

O ponto central deste projeto é o sistema de Mock PDS (Partitioned Data Sets). Ele transforma pastas locais em "Datasets" e arquivos em "Members".

**Isso permite:**

1. Validar nomes e extensões antes de interagir com o mainframe.
2. Testar a lógica de cópia localmente.
3. Simular erros de sistema (como o código de retorno RC 12 de membro ausente) com mensagens legíveis para o usuário.

---

## O que o projeto entrega

- **Gerador de JCL:** Cria automaticamente jobs compatíveis com TK5/MVS para execução do utilitário IEBCOPY.
- **Control Cards:** Gera os cartões de controle (COPY OUTDD... SELECT MEMBER...) dinamicamente.
- **Mock Runner:** Executa uma simulação de cópia no Linux, espelhando o comportamento do mainframe.
- **Doctor Tool:** Ferramenta de diagnóstico para checar se o ambiente local e as dependências estão prontas.
- **Testes Automatizados:** Cobertura de lógica de erro e geração de strings usando unittest.

---

## Como Rodar

### 1. Testar a Lógica (Unittest)

```sh
PYTHONPATH=src python -m unittest discover -s tests
```

### 2. Simular uma Cópia (Mock)

```sh
PYTHONPATH=src python -m mainframe_dataset_automation \
  copy \
  --mock-root examples/mock_zos \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6 \
  --json
```

### 3. Gerar JCL para o TK5

```sh
PYTHONPATH=src python -m mainframe_dataset_automation jcl \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6 \
  --job-name CPYJ2P1
```

---

## Exemplo de Saída (JCL Gerado)

O script gera o código abaixo, pronto para ser submetido via leitor de cartões do Hercules:

```jcl
//CPYJ2P1  JOB (TK5),'IEBCOPY DEMO',CLASS=A,MSGCLASS=X,
//             MSGLEVEL=(1,1)
//COPY     EXEC PGM=IEBCOPY
//SYSPRINT DD SYSOUT=*
//INDS     DD DSN=ZXP.PUBLIC.J2PDATA,DISP=SHR
//OUTDS    DD DSN=Z49216.OUTPUT,DISP=OLD
//SYSIN    DD *
 COPY OUTDD=OUTDS,INDD=INDS
 SELECT MEMBER=(MEMBER1,MEMBER6)
/*
```

---

## Histórico e Aprendizado

O nome e a base do projeto vieram do estudo de ZOAU (Z Open Automation Utilities) e do desafio J2P1 do IBM Z Xplore que realizei em meados de 2024. Para tornar o projeto acessível a qualquer pessoa com um emulador Hercules, precisei adaptar a lógica para focar no que é essencial: JCL, IEBCOPY, PDS Members e Automação.
