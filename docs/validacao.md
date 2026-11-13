> Validação do descarregamento e migração de nomes 0.1.9: consultar `interface-0.1.9.md`.

> Validação da sincronização/desempenho 0.1.8: consultar `desempenho-0.1.8.md`.

> Validação da remoção de fotografias 0.1.7: consultar `interface-0.1.7.md`.

> Validação específica da interface 0.1.6: consultar `interface-0.1.6.md`. As secções abaixo conservam o histórico das entregas anteriores.

# Validação 0.1

Ensaiado nesta entrega:

- Build C++/QML real com Qt 6.12.0/GCC em Linux.
- CTest: arranque QML, modelo com oito secções e persistência de resposta/fotografia após reconstrução do backend, fecho incompleto bloqueado.
- API: pré-visualização sem gravar; importação atómica e reimportação sem duplicados; perfil guardado; acesso por contrato; permissões admin; conflito de revisão; fecho incompleto e NOK sem observações bloqueados; report fechado imutável; snapshots mantidos após alterações no catálogo; autenticação/logout.
- Upload repetido idempotente e recuperação dos bytes da fotografia a partir da base de dados.
- PDF e ZIP, com original exatamente conservado dentro do ZIP.
- Integração ponta a ponta do cliente C++ contra uma API HTTP local: login, contrato, importação Excel, report, fotografia, fecho, ZIP e download do report/fotografia por um segundo cliente.
- Renderização/inspeção visual das páginas do PDF e do formulário em largura de telemóvel.

Não ensaiado: compilação/deployment Windows/Android/iOS, seleção de fotos/exportação em dispositivos físicos, HTTPS no domínio real, PostgreSQL e Docker Compose em execução, concorrência/carga prolongadas. Nenhuma instalação foi efetuada no Ubuntu do utilizador.

## Repetir os testes

```bash
python -m pip install -r server/requirements.txt pytest httpx
python -m pytest server/tests -q
cmake -S app -B app/build/tests -DLEM_BUILD_TESTS=ON \
  -DCMAKE_PREFIX_PATH="$HOME/Qt/6.12.0/gcc_64"
cmake --build app/build/tests --parallel
ctest --test-dir app/build/tests --output-on-failure
```

O teste de integração está disponível em `app/build/tests/lem-client-smoke --network --xlsx <ficheiro>`. Usar apenas uma API **descartável**, em `http://127.0.0.1:18765`, com `ADMIN_EMAIL=admin@lem.pt`, password de fixture `IntegrationPassword123!`, base vazia e um XLSX com folha `Parque`, cabeçalhos `Identificador`, `Modelo`, `Série` e dois IDs únicos. Este teste cria dados; nunca executar contra o servidor operacional. A password de fixture é pública e não deve ser usada no servidor.

## Próxima validação

1. Receber exemplos Excel de cada cliente e confirmar mapeamentos/zeros/fórmulas.
2. Instalar numa base de ensaio no Ubuntu e validar HTTPS, PostgreSQL, permissões e backup/restauro.
3. Testar Windows/MinGW, Android e iOS, com perda de rede e reinício durante uploads.
4. Rever checklist/fotografias obrigatórias e o PDF com técnicos antes do piloto.

## Correção de contraste

Paleta clara explícita aplicada antes de carregar QML, com texto escuro e cores próprias para atributos, botões, seleções e estados desativados. Verificados visualmente formulário e gestão. O tema escuro do sistema deixa de fornecer texto branco aos cartões/fundos claros da app.

## Atualização Stations / LEM (19-10-2026)

Testado o XLSM original em modo de leitura: 51 IDs, sem duplicados e com as dez colunas obrigatórias preenchidas. Passaram 18 testes da API, incluindo remoção isolada de cada um dos dez atributos, células exatas no erro, atributos opcionais vazios, zero em M, preservação de tomadas repetidas, importação atómica de 51 carregadores e reimportação sem duplicados. Passaram também build Qt 6.12.0 e os dois testes CTest.

Os testes do ficheiro real são opcionais e não incluem os dados do cliente no projeto distribuído:

```bash
STATIONS_TEST_WORKBOOK=/caminho/Import_Sheet_V0-1.xlsm python -m pytest server/tests -q
```

O título da janela e do cabeçalho é LEM. Mantém-se a identidade interna de armazenamento para conservar as definições e os rascunhos das instalações existentes.

## Deploy PowerShell / SSH

Seis testes do deploy passaram com PowerShell 7.5.4 em Linux e comandos SSH/SCP/Docker/curl simulados. Testado empacotamento real, caminhos/chave com espaços, preservação de .env, backup normal, normalização LF, permissões de leitura para o container não-root, reset limitado ao volume pgdata e interrupção antes de operações destrutivas quando há falha de build, domínio errado ou volume de outro projeto. Não executado em Windows/PowerShell 5.1 nem com Docker real/no servidor do utilizador. Ver `docs/deploy-powershell.md`.

Correção de ZIP Windows: 12 testes do deploy passaram, incluindo separadores Windows simulados, caminhos normalizados duplicados e travessia de diretórios; erros de validação interrompem antes de executar Docker.
