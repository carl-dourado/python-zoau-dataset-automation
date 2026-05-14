# Python ZOAU Dataset Automation

Esse repo nasceu do desafio **J2P1 - JCL to Python** do IBM Z Xplore.

A ideia era pegar um job JCL simples com `IEBCOPY` e fazer a mesma coisa em
Python: copiar membros de um PDS de entrada para um PDS de saida.

Eu ainda nao deixei isso 100% validado no mainframe porque meu acesso z/OS
estava com senha expirada. Entao deixei duas partes:

- scripts para rodar no USS quando o acesso estiver ok
- modo mock local para testar a logica sem mainframe

## O que tem aqui

- `member_copy.py`: funcao principal que chama `IEBCOPY` via ZOAU
- `copy_members.py`: CLI no formato que o job `CHKJ2P1` espera
- `src/mainframe_dataset_automation`: versao mais organizada/testavel
- `examples/mock_zos`: simulacao local de datasets usando pastas
- `tests`: testes simples com `unittest`
- `docs/xplore-learning-map.md`: notas ligando o projeto aos labs do Xplore

## Por que fiz

Eu queria um projeto de IBM Z que mostrasse mais do que "fiz curso".

Esse aqui junta alguns pontos que apareceram nos PDFs/labs:

- JCL
- USS
- datasets e PDS members
- `IEBCOPY`
- Python
- ZOAU
- tratamento de erro
- validacao por job

## Rodando local

No Linux normal nao tem ZOAU nem datasets reais. Por isso existe o modo mock.

Ele trata uma pasta como se fosse um dataset e cada arquivo dentro dela como se
fosse um member.

```sh
python -m unittest discover -s tests
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

Depois disso, os members copiados aparecem aqui:

```text
examples/mock_zos/Z49216.OUTPUT/
```

## Planejando a copia

Esse comando nao copia nada. Ele so mostra como ficaria o plano do `IEBCOPY`.

```sh
PYTHONPATH=src python -m mainframe_dataset_automation plan \
  -i ZXP.PUBLIC.J2PDATA \
  -o Z49216.OUTPUT \
  -m MEMBER1 \
  -m MEMBER6
```

## Rodando no IBM Z Xplore

Quando o acesso ao z/OS estiver funcionando, a parte importante e copiar estes
dois arquivos para o home USS:

- `member_copy.py`
- `copy_members.py`

No USS:

```sh
chmod 755 member_copy.py copy_members.py
./copy_members.py -i ZXP.PUBLIC.J2PDATA -o "$USER.OUTPUT" -m MEMBER1 -m MEMBER6
```

Para validar pelo desafio:

```sh
submit "//'ZXP.PUBLIC.JCL(CHKJ2P1)'"
```

O job `CHKJ2P1` procura o `copy_members.py` no home USS e espera que ele use
`member_copy.py`.

## O que falta

- resetar/reativar minha senha z/OS
- copiar os scripts para USS
- rodar o `CHKJ2P1`
- salvar o output da validacao no repo, se fizer sentido

## Nota

Nao coloquei PDF da IBM aqui. O repo tem so minha implementacao, exemplos locais
e anotacoes.
