# Python TK5 IEBCOPY Dataset Automation

Automacao em Python para demonstrar copia de membros PDS com `IEBCOPY` em um
fluxo que combina Linux local, Hercules/TK5 e terminal 3270.

O foco atual do projeto e ser honesto com o ambiente disponivel: TK5/MVS 3.8j
roda TSO, ISPF, JCL e utilitarios como `IEBCOPY`, mas nao roda Python moderno em
USS nem ZOAU. Por isso o Python fica fora do mainframe, gerando plano/JCL,
validando entradas, simulando datasets em pastas e mostrando exatamente qual
job seria levado para o emulador.

## O que o projeto entrega

- Gera control cards de `IEBCOPY` para copiar membros de um PDS.
- Gera JCL compativel com TK5/MVS para executar `IEBCOPY`.
- Roda um mock local onde pastas representam datasets e arquivos representam
  members.
- Trata erros comuns, como member ausente, com mensagem legivel.
- Mantem testes com `unittest`.
- Mantem uma ponte ZOAU opcional para um z/OS USS real, mas isso nao e requisito
  da demo TK5.

## Rodando local

```sh
PYTHONPATH=src python -m unittest discover -s tests
```

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

Depois disso, os members copiados aparecem em:

```text
examples/mock_zos/Z49216.OUTPUT/
```

## Planejando a copia

```sh
PYTHONPATH=src python -m mainframe_dataset_automation plan \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6
```

## Gerando JCL para TK5

```sh
PYTHONPATH=src python -m mainframe_dataset_automation jcl \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6 \
  --job-name CPYJ2P1
```

Saida esperada:

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

No TK5, esse JCL depende de datasets reais existindo no catalogo do emulador.
A demo do portfolio mostra a parte que cabe com seguranca no ambiente atual:
geracao do plano, geracao do JCL, copia mock, erro esperado e testes.

## Checando o ambiente

```sh
PYTHONPATH=src python -m mainframe_dataset_automation doctor
```

O resultado local esperado diz que a demo TK5 esta disponivel e que ZOAU e
opcional. Em um z/OS USS real com `zoautil_py`, a ponte ZOAU tambem pode ser
usada.

## Sobre o nome do repo

O nome original veio do estudo de ZOAU e do desafio J2P1 do IBM Z Xplore. A
versao atual foi ajustada para o que da para demonstrar com Hercules/TK5: JCL,
IEBCOPY, PDS members, validacao e automacao Python ao redor do mainframe.
