Este diretório deverá propor solução a co-desenvolvedores que não disponham de _headset_ para fazer a aquisição de dados. Porém ele iniciará com a simples leitura conectada do dispositivo, ajudando a validar dependências.

# Principal dependência: PyNeuro

O [NeuroPy] de lihas recebeu seu último commit em 17 de Outubro de 2017. LieGeForTress disponibilizou um [port][NeuroPy-LieGeForTress] para Python 3 em 16 de Junho de 2020. Seguindo outro fluxo, um [projeto][NeuroPy-NeuroPy2.py] vencedor de "BCI com aprendizagem de máquina" publicara seu ``NeuroPy2.py`` em 12 de Março de 2020. Hoje em 2023 existe no PyPi o ilustre pacote [``neuropy3``][NeuroPy-neuropy3], de scmanjarrez e oriundo da obra de lihas.

Mas o neuropy3 está ambientado em Linux, fazendo uso direto de Bluetooth através do BlueZ e requerendo ``libbluetooth-dev``. Então, já que usamos Windows 10 por necessidade, tentaremos por enquanto desviar dores de cabeça. Optaremos pelo [PyNeuro], o qual connecta-se ao **ThinkGear Connector** (TGC), provedor de dados proposto e suportado pela NeuroSky.

Dentro de um Git Bash:

```console
$ pip install PyNeuro
Collecting PyNeuro
  Downloading PyNeuro-1.3.1-py3-none-any.whl (5.4 kB)
Installing collected packages: PyNeuro
Successfully installed PyNeuro-1.3.1
```

Instalada a dependência, possuindo um _headset_ você pode ir a [``../HelloWorld``](../HelloWorld).

[NeuroPy]: https://github.com/lihas/NeuroPy
[NeuroPy-LieGeForTress]: https://github.com/LieGeForTress/NeuroPy
[NeuroPy-NeuroPy2.py]: https://github.com/vlstyxz/Brain-Computer-Interface-with-Neurosky
[NeuroPy-neuropy3]: https://github.com/scmanjarrez/neuropy3
[PyNeuro]: https://github.com/ZACHSTRIVES/PyNeuro