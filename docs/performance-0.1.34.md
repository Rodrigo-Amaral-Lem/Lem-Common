# Desempenho — Lem 0.1.34

Revisão e medições locais em 10-11-2026. Foram analisados a lista de carregadores,
edição e persistência de reports, anexos, cache, sincronização, importação Excel,
consultas da API e exportação. Não foi efetuado deploy nem teste de carga contra
o servidor do utilizador.

## Alterações

| Área | Trabalho anterior | Alteração |
| --- | --- | --- |
| Importação confirmada | Uma consulta aos carregadores por ID; reimportação pode também provocar autoflush por linha | Uma leitura limitada ao contrato e mapa em memória; transação e validação integral conservadas |
| Excel e upload de fotografias | SQLAlchemy síncrono, XML, hashing e Pillow dentro de endpoints async, bloqueando o ciclo de eventos | Endpoints síncronos executados pelo worker pool limitado do FastAPI; leitura limitada de UploadFile.file |
| Consultas de reports/fotos | Sem índices específicos para charger_id/report_id | Índices em reports(charger_id, updated), photos(report_id) e deleted_reports(charger_id) |
| Lista de carregadores na app | Qualquer changed() voltava a executar filtragem/JSON.stringify no QML, mesmo se só mudasse uma mensagem | Projeção de metadados em cache e chargersChanged() apenas quando a lista realmente difere |

A criação de reports, remoção, alteração de estado ou catálogo continua a atualizar
a lista imediatamente. A seleção e posição de scroll são conservadas pelo código
existente. A cache adicional é apenas da lista atualmente apresentada; não cria
outras cópias das fotografias.

## Medições

Comparação entre 0.1.33 e 0.1.34 no mesmo ambiente Linux/Python 3.12/SQLite
temporário, com dados sintéticos. Três repetições medidas após uma importação
inicial. Tempos incluem pedido local, leitura Excel, validação e transação.

| Medida | Antes | Depois |
| --- | --- | --- |
| Consultas SELECT de carregadores numa reimportação de 1000 IDs | 1000 | 1 |
| Mediana da reimportação de 1000 IDs | 315,15 ms | 100,09 ms |
| Mediana de /api/health durante análise com atraso controlado de 750 ms | 752,07 ms | 1,45 ms |

A reimportação medida foi cerca de 3,1 vezes mais rápida. Não é uma previsão do
tempo num smartphone, PostgreSQL ou ligação móvel. No ensaio concorrente, foi
injetado um atraso de 750 ms no analisador, não num ficheiro real: mede a capacidade
de responder a outros pedidos enquanto o trabalho demora. Não demonstra mais
velocidade de CPU nem garante latência sob saturação do worker pool ou da BD.
As amostras estão em [resultados JSON](performance/measurements-2026-11-10.json).

Na app, 1000 notificações de estado sem alteração da lista produziram **zero**
chargersChanged(), em cerca de 9 ms no teste nativo local. Antes, o QML era chamado
por changed() em cada uma dessas notificações, ainda que acabasse por manter o
mesmo modelo. Não se mediu FPS num smartphone físico.

## Validação

- **112 testes de servidor/deploy aprovados**, sem ignorados, incluindo o Excel
  original e os testes PowerShell 7.6.6.
- Novo teste com 100 IDs verifica uma só consulta em criação e reimportação,
  preservando os totais e a ausência de duplicados.
- Análise e parsing de Excel executados realmente fora do ciclo de eventos ASGI.
- Atualização de índices testada numa BD existente, repetida e sem perda do
  registo de controlo.
- Cliente C++ recompilado com Qt 6.10.2: persistência e notificações da lista
  verificadas. Não é uma compilação do APK ou EXE Windows Qt 6.12.
- Integração local C++/API: escrita simulada de 500 ms não bloqueia respostas;
  última edição conservada, conflitos e transferências de propriedade,
  fecho/remoção, resposta perdida, cache, envio diferido e download/cancelamento
  de fotografias aprovados.
- QML móvel: respostas, notas, fotografias, grupos e navegação aprovados sem avisos.
- Regressão de scroll: catálogo/report, último elemento acessível com rodapé
  visível/escondido, listas curtas/vazias e desktop aprovados sem avisos.

## Sincronização e armazenamento

Foram conservadas as otimizações já existentes: catálogo local por 15 minutos,
abertura de reports locais sem esperar pela rede, fotografias obtidas apenas
quando necessárias, downloads em lote com concorrência limitada, e envio de
novas fotografias diferido até à saída do grupo. A sincronização não volta a
descarregar todo o catálogo no final de cada lote. Gravações rápidas de respostas
continuam a usar o diário por report e um único escritor assíncrono.

Não foram alteradas as regras de propriedade/revisão, limites de segurança,
qualidade das imagens ou política de limpeza local. Não se introduziu cache
partilhada de permissões nem mais workers de servidor, porque o limitador de
login atual mantém estado em memória num único processo.

## Aplicar

Atualizar o servidor através do deploy normal e recompilar a app 0.1.34
(Android code 136). **Não utilizar reset da base de dados.** Os três índices
são criados uma vez no arranque e conservados nos arranques seguintes, incluindo
instalações existentes. A primeira criação pode aumentar o tempo de arranque
numa BD grande e usa criação normal de índices, sem CONCURRENTLY; não foi medida
num PostgreSQL de produção. Não há remoção de dados ou alteração do formato API.

O servidor mantém compatibilidade mínima 0.1.28 e promove latest para 0.1.34 sem
reduzir um valor superior já configurado. As correções e a pendência externa
do SDK Qt continuam descritas na [revisão de segurança](security-review-0.1.33.md).

## Referências técnicas

- FastAPI, endpoints síncronos e worker pool: https://fastapi.tiangolo.com/async/
- FastAPI, UploadFile.file: https://fastapi.tiangolo.com/tutorial/request-files/
- Qt, limites de resolução e carregamento assíncrono de imagens (já aplicados): https://doc.qt.io/qt-6/qml-qtquick-image.html
