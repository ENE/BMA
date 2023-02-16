# BMA - Blinks Modulation Assistant

O assistente para modulação de piscadas possibilita que uma pessoa portadora de [ELA] faça uso do [NeuroSky Mindwave Mobile 2][about-devices] como dispositivo de entrada _"switch"_ (F12) para o [ACAT].

**Em versões amadurecidas,** uma tela secundária do aplicativo, ou mesmo a principal, terá o intuito de **calibrar a detecção do gatilho** no processamento dos sinais EEG. Usando-se o dispositivo atualmente eleito, isso poderá ser alcançado conjugando-se os sinais com a informação dos níveis de atenção e meditação. No protótipo inicial, o qual se constitui uma base para novos desenvolvimentos que acrescentem algoritmos, dispositivos ou sensores, nós nos limitamos a usar a "detecção de piscada" que nos é entregue pronta pela Neurosky através de seu [SDK] — "kit de desenvolvimento de software".

Naqueles acréscimos futuros poderá ser adotada alguma aprendizagem de máquina como forma de se alcançar maior acurácia.

### Significado para a palavra "modulação"

Alguém que controle um braço robótico através do pensamento "modula", naquele intervalo de tempo, seus sinais cerebrais (EEG) para determinado **caráter que um software de computador entenda como entrada válida.** O mesmo raciocínio se aplica para sinais musculares (EMG) ou de proximidade ([IR][retrorreflexão]). Mesmo quando o software interpretador implementa alguma inteligência artificial, o conjunto da entrada tem seu domínio limitado.

Em nosso contexto, um assistente de modulação será aquilo — no caso, uma aplicativo — que proverá ao usuário algum feedback que o estimule em direção ao acerto na sua modulação desejada. Observar um medidor (barra ou ponteiro) desenhando-se em tela é ter um feedback visual. Ouvir um som em determinada frequência é ter um feedback auditivo. Sentir algo vibrando com determinada intensidade é ter um feedback tátil.

O primeiro protótipo do BMA fornece feedback visual; mas que na realidade ainda não é aproveitado plenamente, em tempo real, apenas _a posteriori_. Uma barra de _score_ (pontuação) sinaliza a **força de uma piscada já detectada**. Feedback mais útil levaria em consideração o processamento simultâneo dos sinais. A mera **intenção de piscar** já deveria fornecer feedback.

### Significado para a palavra "calibração"

Uma "calibração" então deve consistir em determinar, nos sinais de EEG, os **limiares mínimos e máximos** para o disparo do gatilho. Essa funcionalidade será possível se abandonarmos a detecção de piscada que nos tem sido dada pronta pela Neurosky, e realizarmos nosso próprio "processamento de sinais".

Trata-se da mesma **noção de ajuste** que a Intel demonstra nas telas do seu [exemplo][VCNL4010] de sensor customizado.

## Sem dispositivo?

Caso você não tenha _headset_ para os testes, dirija-se ao diretório ``DeviceLess``. Nele você encontrará conjuntos de dados (datasets) e orientações sobre como usá-los.

## Compartilhe conhecimento!

O [autor] deste projeto quer viabilizar a comunicação de seu pai, quem já começou a perder o movimento dos olhos. Entre 2017 e 2023 rastreamento ocular com [OptiKey] era bem sucedido.

[ELA]: https://pt.wikipedia.org/wiki/Esclerose_lateral_amiotr%C3%B3fica
[about-devices]: https://neurosky.com/biosensors/eeg-sensor/
[ACAT]: https://www.intel.com/content/www/us/en/developer/tools/open/acat/switches.html
[retrorreflexão]: https://pt.wikipedia.org/wiki/Sensor_de_proximidade#Sensores_%C3%93pticos_Retrorreflexivos
[VCNL4010]: https://www.intel.com/content/www/us/en/content-details/691339/acat-arduino-open-source-proximity-sensor-user-guide.html
[SDK]: https://store.neurosky.com/products/pc-developer-tools
[autor]: mailto:alexandre.mbm@gmail.com
[OptiKey]: https://github.com/OptiKey/OptiKey