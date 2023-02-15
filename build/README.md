# Gerar executável _"portable"_ para Windows

É a melhor forma de tentar garantir o correto funcionamento do programa BMA na máquina do usuário que está sendo assistido, **especialmente se você tem alterado código-fonte,** e principalmente no que se refere ao Python.

A construção exemplificada a seguir gera binários em `build/[plataforma]`, um diretório que **em tese** contém tudo o que é necessário para o programa executar _"standalone (portable)"._ Basta copiá-lo.

## Exemplo de sucesso no _building_

```console
c:\[project]> python setup.py build

 Removing package PyNeuro

 Installing package PyNeuro
  [info] new ZIP created (.egg moved)

 Beginning extraction to -egg dir
  [info] extraction terminated
  [info] the new ZIP file was erased too

 Starting building...
 (it can take a long time)

  [info] calling the setup()'s configurator
  [info] call ended

Stopwatch result: 51 seconds
```

Se erros acontecerem, analise os arquivos `build/*.log`

O diretório `build/issues-backup` apenas guarda anotações mais relevantes, de problemas de programação que foram estudados desde o início do desenvolvimento do projeto.

## O quanto isso é importante?

Nos primórdios do BMA, para a finalização do primeiro protótipo, com seu pai agonizando sem comunicação, o desenvolvedor ainda destinou uma porção substancial — pode-se dizer: [bizarra!](issues-backup/error-freeze_ValueError.log) — de tempo para a viabilização técnica de um `setup.py` que seja razoável.

**Binários executando sem transtornos em qualquer máquina** que atenda aos requisitos de software e hardware tornarão viável a **colaboração remota em todos os níveis de conhecimento** técnico, estando o interessado com um _headset_ ou abrindo arquivos (saiba mais em: `DeviceLess/`).