# LEM 0.1.8 — trabalho no terreno sem esperar pela sincronização

## Resultado da revisão

A app já guardava rascunhos no dispositivo, mas usava o mesmo estado ocupado para operações de rede e edição. Ao sincronizar, bloqueava respostas, fotografias e a abertura da intervenção seguinte. Abrir um report do servidor também descarregava todas as fotografias antes de mostrar o formulário. No fim de cada sincronização voltava a obter o catálogo. Estes comportamentos criavam dependências desnecessárias da ligação móvel.

Esta versão separa o trabalho local do envio, conserva a fila em disco e reduz os pedidos e o trabalho de interface. Não há medições de velocidade num telefone físico; os resultados abaixo são verificações funcionais e contagens de operações em ambiente local, não percentagens de aceleração.

## Quando se comunica com o servidor

| Momento | Comportamento na 0.1.8 |
|---|---|
| Iniciar sessão | Autentica e atualiza a lista de contratos. Recupera os rascunhos e alterações pendentes do dispositivo. |
| Escolher um contrato já descarregado | Mostra imediatamente os dados locais. Atualiza o catálogo em segundo plano se a cópia tiver mais de 15 minutos. Um contrato nunca descarregado precisa de rede uma vez. |
| Carregar em Atualizar | Força uma atualização do catálogo; não é necessário fazê-lo em cada intervenção. |
| Preencher uma resposta ou observação | Guarda atomicamente o report editado num pequeno ficheiro local. Agenda envio após cerca de 8 segundos sem novas alterações, respeitando o atraso de repetição após falhas. |
| Anexar ou remover uma fotografia | Guarda a operação local e agenda o mesmo envio automático. A câmara continua a ser a ação principal no Android. |
| Mudar de grupo ou abrir um report já guardado | Usa os dados locais, sem pedido de rede. Mantém respostas e posição de scroll. |
| Concluir um report | Valida e guarda o fecho localmente antes de iniciar/tentar o envio. O técnico pode abrir outra intervenção enquanto a anterior é enviada. Concluído no dispositivo não significa confirmado pelo servidor. |
| Sincronizar manualmente | Força uma tentativa, mesmo durante o intervalo de repetição. Se não houver pendentes, não descarrega novamente contratos/carregadores. |
| Terminar um envio | Confirma apenas o que foi recebido. Não recarrega o catálogo. Alterações feitas durante o envio ficam pendentes para o ciclo seguinte. |
| Abrir pela primeira vez um report antigo | Obtém o texto, respostas e metadados das fotografias. Não descarrega automaticamente os ficheiros de imagem. |
| Descarregar uma fotografia antiga | Obtém apenas a fotografia pedida. Há no máximo dois downloads simultâneos; verifica o digest quando fornecido pelo servidor. A fotografia fica disponível localmente. |
| Atualizar report do servidor, no menu do report | Atualização explícita de um report sem alterações locais pendentes. Não substitui trabalho ainda por enviar. |
| Exportar PDF/ZIP | Continua a usar o servidor, depois de os dados e fotografias estarem sincronizados. |

O envio de cada report começa pelo texto e segue para remoções/fotografias e, quando aplicável, confirmação do fecho. Os reports da fila são tratados sequencialmente; não existe nesta versão uma prioridade global que envie o texto de todos os reports antes de todas as fotografias.

## Falhas, concorrência e dados locais

- `busy` continua a representar operações que precisam de bloquear a ação atual. `syncing` é separado: o envio automático não desativa respostas, fotografias ou revisão local.
- Cada alteração local tem uma sequência. A confirmação de uma versão anterior do report não substitui respostas recentes, não volta a anexar uma fotografia removida durante o upload e não marca como enviado um trabalho posterior.
- O report atual não muda quando termina o envio de outro report. Pode iniciar-se outra intervenção durante o envio.
- Um registo da última tentativa permite recuperar um PUT cuja resposta se perdeu, inclusive se o técnico já escreveu respostas novas. UUIDs de fotografias/remoções conservam a idempotência existente.
- Falhas transitórias usam intervalos de 30, 60, 120 segundos, etc., até 10 minutos. Novas edições não encurtam esse intervalo. Recuperação de conectividade pode antecipar uma tentativa. O botão manual também permite tentar de imediato.
- Sessão expirada pede nova autenticação; não apaga os dados. Conflitos, falta de autorização e dados rejeitados precisam de atenção e não são reenviados continuamente em ciclo. Outros reports podem continuar a ser enviados.
- O estado de rede fornecido pelo sistema é uma indicação. Se não existir backend de conectividade, a fila continua a funcionar por tentativas. O botão manual não fica dependente dessa indicação.
- Não se grava a password nem se acrescenta armazenamento do token de sessão em texto simples. Depois de reiniciar a app pode ser necessário entrar novamente para enviar; os dados locais continuam disponíveis para trabalhar sem rede.

Os ficheiros de edição por report complementam o `cache.json` existente. Ao carregar, uma edição com sequência mais recente prevalece. Depois de um checkpoint completo bem-sucedido, os ficheiros de edição correspondentes são limpos. Não é introduzida uma espera de vários segundos para guardar o texto: os oito segundos aplicam-se ao envio, não à gravação local.

## Armazenamento no smartphone

A maior parte do espaço é ocupada pelas fotografias, não pela checklist. Por isso:

- O catálogo do contrato e os reports consultados/produzidos continuam locais; não se descarrega automaticamente todo o histórico fotográfico dos contratos.
- Apenas cópias privadas de fotografias de reports **concluídos, sem alterações pendentes e com upload confirmado** são candidatas à limpeza.
- Fotografias do report atualmente aberto, de rascunhos ou com envios/remoções pendentes ficam protegidas.
- Cópias elegíveis são removidas após sete dias sem utilização conhecida ou, começando pelas mais antigas, quando as fotografias locais ultrapassam 256 MiB (aproximadamente 268 MB). O ficheiro original na galeria e a fotografia no servidor não são apagados por esta limpeza.
- Este valor é um **objetivo de cache, não um limite rígido da app**. Rascunhos, pendentes, o report aberto e ficheiros não elegíveis podem ultrapassá-lo; não se apaga trabalho para cumprir a quota. O número mostrado em Conta refere-se aos ficheiros privados de fotografias da conta atual, não à totalidade do armazenamento da aplicação nem às outras contas.
- As respostas/metadados ficam disponíveis depois da limpeza. As fotografias podem voltar a ser descarregadas a pedido. Para consultar um report antigo sem rede, descarregar antes as fotografias necessárias.
- As fotografias anexadas mantêm a qualidade/original conforme a versão anterior. Não foi introduzida compressão destrutiva para poupar espaço.

Conta mostra o espaço das fotografias e permite executar a mesma limpeza segura. Não desinstalar nem apagar os dados da app quando houver trabalho pendente.

## Outros custos reduzidos

- O formulário cria controlos apenas para o grupo visível: no PC01 inicial são 13 itens, em vez de controlos para os 69 itens. A informação dos outros grupos continua guardada e é recriada ao selecioná-los.
- O catálogo não é filtrado/renderizado enquanto o ecrã do report está aberto. Os resumos de reports são agrupados por carregador numa passagem, em vez de percorrer todos os reports para cada carregador. O estado local de fecho/envio é refletido na lista sem esperar por atualização do servidor.
- Escrever deixa de regravar o ficheiro global com todos os reports a cada tecla. O checkpoint global ainda é usado em operações de catálogo e confirmações de envio; uma futura migração para SQLite pode reduzir mais esse custo quando o histórico crescer.
- No servidor, a lista do contrato usa duas consultas em lote para os dados do catálogo, além da autenticação/permissões. Deixa de fazer uma consulta de reports por carregador e não carrega `payload`/`template` completos apenas para obter os resumos. Não há alteração de esquema da base de dados.

## Limite importante do Android

“Segundo plano” nesta entrega significa **sem bloquear a interface enquanto o processo da app pode executar**. Não foi introduzido um serviço Android nem WorkManager. Se o Android suspender/terminar o processo, não se garante envio com a app fechada ou o ecrã bloqueado. A fila conserva-se em disco e retoma quando a app volta a executar e tem sessão/rede. O próximo passo para envios independentes da interface é um mecanismo nativo de trabalho persistente, com credenciais protegidas e política de bateria/dados móveis. Também ficam para uma fase posterior a seleção Wi-Fi/dados móveis, preparação explícita de vários contratos para uma jornada e resolução assistida de conflitos entre dispositivos.

## Instalar

O pacote contém código fonte, não um APK. Recompilar a app com o kit Qt 6.12/OpenSSL habitual, incluindo o novo `src/LemOffline.cpp` através do CMake atualizado. Confirmar 0.1.8 em Conta; versionCode Android 108. O identificador de pacote e as pastas de dados permanecem os mesmos. Foi acrescentada a permissão normal `ACCESS_NETWORK_STATE` para observar a conectividade.

Para obter também a otimização do catálogo no servidor, a partir do projeto extraído no laptop Linux:

```bash
bash deploy/deploy.sh
```

No Windows continua disponível `deploy/deploy.ps1`. Atualizar sem reset; não há migração nem necessidade de apagar a base de dados. A app 0.1.8 mantém os endpoints da API 0.1.7; a atualização conjunta é recomendada para obter todos os ganhos.

## Validação

- Cliente C++ compilado e executado com Qt 6.10.2 em Linux, mais QML em PySide6/Qt 6.10.2. Não foi compilado/instalado um APK nesta entrega.
- API HTTP local descartável com atrasos deliberados: edição e nova fotografia enquanto um PUT está em curso; remoção durante upload; passagem a outra intervenção; conclusão enquanto um rascunho anterior está a ser enviado; confirmação que não substitui trabalho posterior; recuperação de resposta perdida; envio automático sem carregar no botão.
- Abertura local sem bloqueio; report remoto sem ficheiros de imagem; exatamente um download quando explicitamente pedido. A contagem confirmou ausência de nova obtenção do catálogo no fim dos envios.
- 50 alterações de observações não regravaram o checkpoint global; o texto foi recuperado por outra instância do backend. Limpeza de uma cópia confirmada antiga, conservação dos metadados e proteção de um rascunho com ficheiro de dimensão lógica superior a 256 MiB. Os ficheiros grandes da fixture são esparsos.
- QML em largura de desktop e telemóvel: edição/fotografias/revisão continuam ativas durante `syncing`; formulário dos grupos inativos não é criado; navegação, observações NOK, remoções, validação e scroll preservados. Renderizações a 390×844, 320×844 e 844×390 inspecionadas.
- API/deploy: 32 testes aprovados; 26 opcionais ignorados por dependerem de PowerShell ou do Excel externo. Inclui a consulta em lote com 20 carregadores, sem obter payloads de reports. Mais 7 testes de configuração Android/OpenSSL aprovados.
- Integração anterior do cliente repetida: upload, remoção sincronizada, substituição, fecho, ZIP e download por outro cliente.

Para repetir os novos testes, ativar `LEM_BUILD_TESTS`, compilar `LEM-offline-test` e executar:

```bash
QT_QPA_PLATFORM=offscreen ./LEM-offline-test
python app/tests/test_offline_sync.py /caminho/para/LEM-offline-test
python app/tests/test_report_tabs.py report mobile
python app/tests/test_report_tabs.py report
```

O teste HTTP usa exclusivamente `127.0.0.1:18765`, base de dados temporária e credenciais públicas de fixture. Nunca o apontar ao servidor de produção. Não houve acesso/alteração ao servidor do utilizador. Falta validar bateria, rede móvel instável, suspensão/retoma, reconexão e armazenamento real num Android físico; não se apresentam tempos/percentagens de aceleração que não tenham sido medidos nesse ambiente.

## Referências da revisão

- [Android — Offline-first](https://developer.android.com/topic/architecture/data-layer/offline-first): dados locais imediatos, filas duráveis e reconciliação.
- [Qt — QNetworkInformation](https://doc.qt.io/qt-6/qnetworkinformation.html): indicação de conectividade e limitações da deteção.
- [Android — permissões de rede](https://developer.android.com/develop/connectivity/network-ops/connecting): INTERNET e ACCESS_NETWORK_STATE.
- [SQLAlchemy — limitar colunas carregadas](https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html): evitar carregar colunas volumosas para consultas de resumo.
