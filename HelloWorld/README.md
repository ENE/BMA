Você tem um **Mindwave Mobile 2** e quer começar a testá-lo para a finalidade deste projeto?

Primeiramente certifique-se de que ele esteja funcional em seu Windows 10. Instale o ThinkGear Connector (TGC) disponibilizado pela NeuroSky via SDK - kit de desenvolvimento de software. Após o pareamento bem sucedido nas Configurações de Bluetooth, atribua uma porta COM ao nosso dispositivo bluetooth, a mesma, tanto no Windows e como no TGC.

Uma dica é certificar-se de que tudo esteja em pleno funcionamento fazendo uso de algum dos aplicativos gratuitos que podem ser baixados da NeuroSky Store.

Então finalmente você testa um pouco deste projeto:

```console
$ python blinks.py
[PyNeuro] Connecting TCP Socket Host...
[PyNeuro] Scanning device..
[PyNeuro] Fitting Device..
[PyNeuro] Successfully Connected ..
blink: 33
blink: 188
blink: 43
blink: 69
blink: 62
blink: 50
blink: 32
blink: 164
[PyNeuro] Connection lost, trying to reconnect..
```

Isso mesmo, nosso "Hello World" é fazer, no terminal (modo texto), a captura de piscadas.

## Limitações do terminal

1) O programa acima NÃO funciona no Git Bash, apenas no Prompt de Comando. Ou os ``print(str)`` não acontecerão antes da thread principal ser encerrada com ``Control+C`` pelo usuário.

2) Na verdade, atualmente não é possível o programa auto-encerrar corretamente. O usuário precisa fazer um **Quit** no ThinkGear Connector, a partir do System Tray do Windows. Pois somente assim se consegue "matar" a thread independente (conexão e processamento).

3) Para terminal não-rico, como aqui, ou se codifica com a estratégia de callbacks ou sem ela. Até então não se viu como gerenciar terminal, loops e callbacks em simultâneo.