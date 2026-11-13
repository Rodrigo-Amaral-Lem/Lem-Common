# Atualização 0.1.57

Perguntas EST/SITE revistas, avaliação separada das leituras MAN.14–17, recorte dentro da área segura do Android e limpeza local que conserva os reports e respostas. Consulte [as notas](report-workflow-0.1.57.md). Atualize primeiro o servidor e depois recompile a app. Não é necessário reset.

# Atualização 0.1.56

Avaliações OK/NOK em MAN.14–18, fotografias e observações N/A nos testes de carga, cópia QVE local sem bloquear os outros campos, cópia de MAN.04–10 e seleção de vários ficheiros. Consulte [as notas](report-workflow-0.1.56.md). Atualize primeiro o servidor e depois a app.

# Atualização 0.1.55

Ficha de carregador comum a vários contratos, fabricante/modelo/série editáveis no report e atualização no fecho. Consulte [as notas de atualização](../../Server/docs/station-registry-0.1.55.md). Atualize primeiro o servidor e depois a app.

# Atualização 0.1.54

Sete grupos SEG, EST, SITE, QVE, MAN, CARG e FIN, cópia do QVE entre carregadores e assinatura do técnico. Consulte [as notas da versão](report-groups-0.1.54.md). Atualize primeiro o servidor e depois recompile a app.

> **0.1.53 R1 — câmara Android e recorte**: a câmara normal abre em fotografia/vídeo; ao regressar, selecione o ficheiro a anexar. Cinco controlos de evidência numa linha e pegas de recorte maiores, com margem de toque. Basta recompilar a app; servidor 0.1.53 sem alterações. [Instruções](../../App/docs/native-camera-0.1.53-r1.md).

> **0.1.53 — instalação e importação simplificadas**: escolha do nome da primeira conta no instalador; cabeçalho Stations fixo na primeira linha; pré-visualização de todos os carregadores e de todos os dados de origem. Atualize o servidor e recompile a app. Contas existentes são conservadas.

> **0.1.52 — photo crop and video evidence**: crop draft photographs with a touch preview; record videos using the Android camera or attach MP4/3GP on desktop/Android. Videos use the existing offline/deferred synchronization and cache controls. Deploy the server and rebuild all clients (minimum 0.1.52); no database reset needed. [Usage, limits and technical notes](evidence-media-0.1.52.md).

> **0.1.51 — import/retry review**: preserve console-enriched details during Excel re-import; serialize contract import commits after parsing; atomically update shared import profiles; return conflicts for racing contract/photo IDs; make repeated access assignments idempotent. Server-only fixes; existing 0.1.48–0.1.50 apps remain compatible. No reset. [Reproductions, checks and limits](import-retry-review-0.1.51.md).

> **0.1.50 — second bug review**: abort console deletion if a report changed during confirmation; protect the authoritative charger ID in new snapshots; normalize coordinates across console and Maps (including tiny numeric coordinates); add an explicit measurement/NA erase action. Deploy server and rebuild app for all fixes; 0.1.48/0.1.49 clients remain compatible. No data reset. [Reproductions and checks](second-review-0.1.50.md).

> **0.1.49 — cross-feature review**: fixes confirmed-account identity races, atomic forced contract purge, token revocation during authentication, password resets against removed accounts, console metadata/coordinate validation and duplicate-account conflicts. Server update required; 0.1.48 clients remain compatible. Existing data is retained. [Findings, evidence and test limitations](cross-feature-audit-0.1.49.md).

> **0.1.48 — Administração**: administradores podem criar outros administradores na app; Gestão separada por áreas e diagnóstico/demonstração só após 10 toques em Usar servidor Lem. No servidor, `bash deploy/manage-server.sh` gere contas, contratos, reports, proprietários e carregadores. Eliminações exigem APAGAR; passwords nunca são listadas em massa. Atualizar servidor e app, sem reset da base de dados. [Guia e comandos](../../Server/docs/administration-0.1.48.md).

> **0.1.46 — measurements and voltage NOK**: voltage fields allow up to 3 integer digits/2 decimals; earth resistance up to 5/2. Canonical V/Ω units, Não Aplicável option and red out-of-range voltage indication in UI and PDFs. N–T >=50 V is NOK. Update server and apps together; minimum/latest client 0.1.46, Android code 154. Keep existing data. See [rules and tests](measurements-0.1.46.md).

> **0.1.45 R1 — Docker deployment**: local first-install support for Ubuntu 26.04 LTS (resolute) alongside 24.04 (noble); API image tagged lem-api:0.1.45. See [local install and Docker image build/export](../../Server/docs/docker-server-ubuntu.md). This is source/build configuration, not a prebuilt container image. Qt app unchanged.

> **0.1.45 — Android client performance**: cache the active report projection, separate report/photo notifications, index photos by checkpoint and read Android camera results immediately on return. Original photo quality, durability and deferred upload rules are retained. Latest client 0.1.45, Android code 153. Deploy the version-policy update and rebuild the app. See [changes, measurements and tests](../../App/docs/android-performance-0.1.45.md).

> **0.1.44 — concurrency and session fixes**: handle report deletion during photograph changes with HTTP 410; prevent delayed responses from an old session/server from revoking a new login. Latest client 0.1.44, minimum 0.1.39, Android code 152. Deploy server and rebuild app without resetting data. See [continued review and reproduced regressions](source-review-0.1.44.md).

> **0.1.43 — source review and fixes**: plain-digit calendar years, correct N/A connector handling, recovered-photo validation against the target report, and trimmed required contract fields. App/server/deployment versions are aligned; Android code 151. Deploy server and rebuild app, preserving existing data. See [review, fixes and test coverage](source-review-0.1.43.md).

> **0.1.41 R1 — server client policy**: latest supported client is now 0.1.41; minimum remains 0.1.39. Deploy promotes an older pinned latest in .env without changing credentials or deleting data. App source/binaries are unchanged. Deploy this server update before logging in with app 0.1.41.

> **0.1.41 — startup robustness and background fix**: transparent PNG frame animations replace GIF decoding; the splash is an in-window overlay. Keeps the 89% / 5% / 5% / 1% selection. Android version code 149. Existing app 0.1.41 builds remain valid; deploy the R1 server policy update.

> **0.1.40 — startup variants**: each app launch selects exactly one screen: Lem logo (89%), greeting (5%), checklist (5%), or charging (1%). All assets work offline. Deploy the accompanying server policy update; no data reset is needed.

> **0.1.39 - per-connector load tests**: one independent PC03 question per physical connector, with #1/#2 only for repeated types and matching app/server/PDF validation. Beta checklist version 2; minimum client 0.1.39, Android code 147. Deploy server, rebuild app and discard old beta reports/local data. See [connector rules, setup and validation](connector-load-tests-0.1.39.md).

> **0.1.38 - cleaner report PDFs**: power and limitation display inline kVA; internal import metadata/device-origin text and photo filenames are omitted. Evidence checkpoint labels remain. Rebuild app and deploy server; no database reset. Android code 146. See [PDF presentation and validation](pdf-presentation-0.1.38.md).

> **0.1.37 R4 - open exported PDF**: successful PDF exports open automatically in the system viewer on desktop and Android. Failed exports never open a viewer; a launch failure keeps the PDF and shows a notice. Client-only; Android code 145. See [behaviour and validation](../../App/docs/pdf-auto-open-0.1.37-R4.md).

> **0.1.37 R3 - address and Maps navigation**: contract ID cards append the postal code and offer a navigation icon. Valid coordinates take priority; otherwise Maps receives the address. Client-only; Android code 144. See [behaviour and checks](../../App/docs/charger-navigation-0.1.37-R3.md).

> **0.1.37 R2 - serial label**: contract ID cards and import preview use **S/N** for the serial number on Android, Windows and Linux. Rebuild the app only; Android code 143.

> **0.1.37 R1 - desktop scrollbars**: reports, contract IDs and Management now have visible, draggable bars in the outer gutter. Client-only correction; no server update. Android code 142. See [cause and checks](../../App/docs/desktop-scrollbars-0.1.37-R1.md).

> **Interface and branding - 0.1.37**: cyan/grey Lem palette, compact logo header, clearer answer selection, quick search clearing, completion meter, simpler initial Management form and branded server/offline PDFs. Rebuild the app; deploy the server for server PDF/ZIP branding. No database reset. See [design decisions and validation](../../App/docs/ui-design-0.1.37.md).

> **Reviewed integration — 0.1.36**: client caching/search/sync recovery, validated image uploads, robust PDF/ZIP exports, bounded export/image admission and IPv6 login limits. 142 backend/deploy tests and native/QML regressions passed. Update server and rebuild app; no database reset. See [release validation and settings](release-0.1.36.md).

> **0.1.35 R2 — contract cards**: Android catalogue metadata reduced to ID, serial and address. All platforms show amber “Por fazer” or green “Concluído” when a charger has a closed report in its contract. Client UI only; rebuild app (Android code 139), no server update. See [contract catalogue](../../App/docs/contract-cards-0.1.35-R2.md).

> **0.1.35 R1 — local cleanup**: manual cleanup now removes fully synchronized drafts as well as closed reports and their private photos. Unpublished/unsent/conflicted work remains protected; server originals are retained. Rebuild app only (Android code 138); server version remains 0.1.35. See [cleanup correction](../../App/docs/local-cleanup-0.1.35-R1.md).

> **Bug fixes — 0.1.35**: invalid/out-of-range Excel header rows return validation errors; long PDF metadata can span pages; Android Back no longer uses the broader desktop key binding. 120 backend/deploy tests passed. Update server and rebuild app; no database reset. See [general review](bug-review-0.1.35.md).

> **0.1.34 R1 build configuration**: Android OpenSSL is automatically located in standard SDK folders, including Qt Creator per-ABI downloads. A persistent environment override is available for custom paths. No server update or database change is needed for this build-only revision. See [Android OpenSSL](../../App/docs/android-openssl.md).

> **Performance — 0.1.34**: bounded worker execution for Excel/photo endpoints, bulk charger lookups during imports, indexes for report/photo reads, and catalogue notifications isolated from unrelated status changes. Update server and rebuild app; no database reset. See [measurements and validation](performance-0.1.34.md).

> **Security review — 0.1.33**: normalized independent login limits, bounded request/response bodies, same-origin redirects, safe cache identifiers, hardened XLSX/XML handling, reduced photo-quota memory usage, Pillow 13.0.0 and Android backup exclusions. **Update server and app; no database reset.** An external Qt 6.12.0 Network advisory still requires upstream SDK patches: see [findings, tests and remaining action](security-review-0.1.33.md).

> **Windows single EXE**: static Qt/plugin/runtime build enabled by default on Windows, Windows Schannel HTTPS, external DLL import audit and isolated smoke test. Start with [Windows single-executable instructions](../../App/docs/windows-single-exe.md). Requires a separate static Qt build; source package, not a precompiled Windows EXE. R1 scroll fix/protocol 0.1.32 retained; no server update.

> **0.1.32 R1**: fixes the reproduced footer SafeArea/Translate binding loop that inflated page height while hiding Android menus. All four footer paddings are explicit, independent of its animated position. Protocol stays 0.1.32; no server update. Android build code 134. See [R1 cause and verification](../../App/docs/footer-safe-area-R1.md).

> Version **0.1.32**: explicit page Flickables bound to the last rendered question, stable footer height, and a rendered-end cap for variable-height catalogue rows. Natural swipe-to-end regression covers hidden menus. App-only behavior change: an existing server needs only its latest-client policy raised to 0.1.32, not a software/database upgrade. See [rendered page bounds](../../App/docs/rendered-bounds-0.1.32.md).

> Version **0.1.31**: stop report/catalogue/management pages at their real scroll bounds and remove duplicated footer padding. Final items remain reachable above the sync bar; menu animations keep a fixed reading viewport. Update client and server policy to admit 0.1.31; minimum remains 0.1.28. See [page-end limits](../../App/docs/scroll-limits-0.1.31.md).

> Version **0.1.30**: PDF/ZIP export is available only for closed reports. Draft export options are hidden; client validation, the local PDF renderer and both server endpoints reject drafts. Closed reports retain offline PDF export. Update client and server; no database reset. See [closed-report export](export-0.1.30.md).

> Version **0.1.29**: notifications stay above the visible footer on mobile and desktop; managed prototype server preferences migrate to Lem; account action restores the default server; desktop feature parity audited. Client/server latest version is 0.1.29; minimum remains 0.1.28. See [desktop parity and notifications](../../App/docs/desktop-feedback-0.1.29.md).

> Version **0.1.28**: server-controlled client compatibility, blocked login for unsupported releases, update reminders for supported older apps, Lem naming throughout app/server/deployment/docs, and a full-height Android page indicator protected against overshoot. **Update both app and server; use a clean prototype installation to remove previous deployment names.** See [compatibility and clean setup](compatibility-0.1.28.md).

> Version **0.1.27**: offline PDF with local evidence and no active session; persistent Android position indicator; horizontal group swipes; stable catalogue position; corrected voltage ranges. Update client and server; no database reset. See [field navigation and offline PDF](../../App/docs/field-work-0.1.27.md).

> Version **0.1.26**: OK/NOK/N/A and an eraser action share one stable row; Android action bars slide as overlays over a fixed scroll viewport, preventing question drift and scrollbar resizing. Client update only. See [stable scrolling](../../App/docs/stable-scroll-0.1.26.md).

> Version **0.1.25**: Android scroll-aware action bars on reports, charger selection and management; smooth collapse/reveal while the main Lem header stays fixed. Client update only; server unchanged. See [scroll-aware bars](../../App/docs/scroll-bars-0.1.25.md).

> Version **0.1.24**: single-row compact footer with **Sinc.**, an animated operation-status icon, smaller header surfaces and full Android touch targets. Client update only; server remains 0.1.23. See [compact bars](../../App/docs/compact-bars-0.1.24.md).

> Version **0.1.23**: unified `Lem` controller/source filenames and `lem` QML context; Android package ID is now `pt.lem.app`. **Android treats this as a separate app: synchronize pending work before switching.** See [rename notes](rename-0.1.23.md).

> **Documented source edition (0.1.22):** expanded formatting and English source comments, plus a [developer guide](developer/README.md) covering architecture, local state, synchronization, API/database, QML, platforms and tests. App behavior and version identifiers remain unchanged.

> Version **0.1.22**: exclusive draft ownership, administrator transfers with audit history, protected offline conflicts and independent report/photo copies. Update **server and client**, without resetting the database. See `docs/ownership-0.1.22.md`.

> Version **0.1.21**: detailed operation stages, batch progress and per-transfer byte progress in Operation status, with indeterminate server-wait state and independent throttled notifications. See `docs/operation-progress-0.1.21.md`. Client update only.

> Version **0.1.20**: client renamed to **Lem**, including UI, Android label, executable, QML module and source identifiers. Existing installation/data compatibility preserved. Server remains unchanged. See `docs/rename-lem-0.1.20.md`. Reconfigure CMake and build target `Lem`.

> Version **0.1.19**: LEM app icon based on the supplied logo and a nonblocking two-second logo startup screen. See `docs/branding-0.1.19.md` and `app/assets/README.md`. Client update only.

> Version **0.1.18**: immediate manual cleanup of synced closed report copies and photos, with draft protection; remove redundant Account menu item. See `docs/local-cleanup-0.1.18.md`. Client update only.

> Version **0.1.17**: menu buttons toggle closed correctly; direct Download photographs action on server-backed reports. See `docs/menu-photos-0.1.17.md`. Client update only.

> Version **0.1.16**: account/session icon in a single-row header, with distinct signed-in, signed-out and demo badges. See `docs/compact-account-0.1.16.md`. Client update only; server remains 0.1.15.

> Version **0.1.15**: delete owned drafts and, for administrators, closed reports with their photographs; revision checks, audit and stale-copy protection. See `docs/report-deletion-0.1.15.md`. Update server and client without resetting the database.

> Version **0.1.14**: responsive answer/observation controls with background local journaling, visible save state, and fewer QML updates. See `docs/responsiveness-0.1.14.md`. Rebuild the client; no server update required.

> Version **0.1.13**: compact zoom/delete/download photo icon actions, red delete affordance, and close icon in the photo viewer. See `docs/gui-0.1.13.md`. Client update only.

> Version **0.1.12**: camera/gallery icon buttons and Obs. in one row; removable optional observations; permanent, accurate sign-in status. See `docs/gui-0.1.12.md`. Client update only.

> Version **0.1.11**: batch new photographs when changing question group or leaving a report; keep attachments local while filling in the current group. See `docs/photo-sync-0.1.11.md`. Client update only; no server deployment or database reset required.

> Version **0.1.10**: fix the Linux linker collision between the LEM executable and the generated QML module directory. See `docs/build-linux-0.1.10.md`. No server deployment or database reset is required for this fix.

> Version **0.1.4** adds Android camera capture and drawn icons. See `docs/android-camera-icons.md` for updating and device checks.

> Version **0.1.3** adds explicit Android OpenSSL deployment. See `docs/android-openssl.md` before rebuilding the Android APK.

> Interface **0.1.2**: reports organizados por separadores PCxx/PGxx. Consulta `docs/interface-0.1.2.md` para navegação e atualização.

# Lem — aplicação de manutenção

Aplicação Qt para manutenção de PCVE, com API central, contratos e carregadores, checklist, evidências por item, importação Excel e exportação PDF/ZIP. Projeto novo, independente do Excel/macros e do protótipo anterior.

## Experimentar

Abrir `app/CMakeLists.txt` no Qt Creator com o kit Qt 6.12. Build/Run. Em Conta, selecionar **Ver demonstração local**, ou arrancar com `--demo`. A demonstração usa dados fictícios num espaço separado e não envia dados ao servidor.

Para usar com servidor: instalar a API, entrar como administrador, criar contrato, selecionar contrato, importar Excel, criar técnicos e atribuir contratos através da lista de utilizadores. O técnico entra, seleciona contrato/carregador, cria intervenção ou abre report existente. Cada alteração e fotografia é gravada localmente. **Sincronizar** envia rascunhos e fotografias; **Concluir report** valida e envia, ou conserva a conclusão local se estiver sem sessão/rede.

**No servidor** só aparece o estado concluído depois de todas as evidências serem enviadas e o fecho ser validado. Um report com NOK pode ser fechado, desde que haja observação: report concluído não significa instalação conforme.

O instalador de primeira instalação é `deploy/install-ubuntu.sh`: executar como `lem` com sudo num Ubuntu 24.04 novo. Instruções completas em `docs/servidor-ubuntu.md`.

## Incluído

- C++17 / Qt Quick / Qt 6.12, CMake e configurações para desktop e mobile.
- Contratos identificados por ano, semestre, empresa e tipo livre (TRE, O&M…).
- Carregadores identificados pelo ID externo dentro do contrato; permite contratos de anos/clientes diferentes com o mesmo ID.
- 69 checkpoints em oito grupos, baseados no PDF fornecido, com respostas OK/NOK/NA ou texto/medições, observações e várias fotografias por item.
- Rascunhos locais e cache por utilizador/servidor/contrato. Só os contratos e reports previamente descarregados ficam disponíveis sem rede.
- API FastAPI, PostgreSQL no deployment e SQLite para desenvolvimento/testes.
- Autenticação, perfis admin/técnico, atribuição de contratos, controlo de revisão e audit trail de gravações/importações.
- Importação `.xlsx/.xlsm` com reconhecimento automático do modelo Stations, validação dos dez atributos obrigatórios, mapeamento dos outros formatos, pré-visualização e confirmação. Guarda o último mapeamento por empresa; preserva as restantes colunas em `details.source`.
- Fotografias JPEG/PNG originais na base de dados. PDF inclui versões reduzidas e orientadas; ZIP contém PDF, JSON e ficheiros originais por checkpoint.
- PDF com identificação, cliente, dados técnicos, secções, resultados, observações e evidências. Sem marca, assinatura ou rodapé Infraspeak.
- Docker Compose para Ubuntu, HTTPS via Caddy e script de backup PostgreSQL.

## Documentação

- [Source-code developer guide (English)](developer/README.md)

- [Compilar Windows/Android/iOS e Linux](../../App/docs/compilar-qt.md)
- [Servidor Ubuntu](../../Server/docs/servidor-ubuntu.md)
- [Deploy a partir de PowerShell por SSH](../../Server/docs/deploy-powershell.md)
- [Deploy a partir do laptop Linux por SSH](../../Server/docs/deploy-linux.md)
- [Revisão de desempenho e sincronização 0.1.8](desempenho-0.1.8.md)
- [Fotografias offline e migração do servidor 0.1.9](../../App/docs/interface-0.1.9.md)
- [Modelo de dados e decisões](../../Server/docs/modelo-e-importacao.md)
- [Validação e limitações](validacao.md)

`examples/report-demonstracao.pdf` é uma saída do renderer com dados fictícios de teste; o bloco de imagem é uma evidência sintética. Não é um report real.

## Limites desta versão

É um protótipo funcional, não uma instalação já feita no servidor. Não inclui binários Windows/APK/IPA. Windows, Android e iOS precisam de builds e ensaios nos respetivos kits/dispositivos; iOS exige Mac/Xcode para compilar/assinar.

No Android, a captura usa a aplicação de câmara instalada; também existe seleção de ficheiros/galeria. Não há envio automático do PDF ao cliente. A exportação permite guardar o PDF/ZIP para envio pelo meio escolhido. PDF/ZIP requerem ligação ao servidor e sincronização prévia.

Reports fechados são imutáveis. Alterações posteriores devem gerar nova intervenção. Conflitos de propriedade/revisão conservam a cópia local, permitem consultar a versão do servidor em leitura e criar outro rascunho como cópia independente; não há merge automático. Não há agendamento, GPS, assinatura do técnico, notificações, bulk export, recuperação de password, revisão/aprovação ou portal do cliente.

Os dados locais não são cifrados nesta versão; usar dispositivos de teste com bloqueio de ecrã. O token de sessão não é persistido: depois de reiniciar, pode continuar offline e deve entrar novamente para sincronizar. A troca de utilizador isola os caches, mas não elimina os dados descarregados do disco.
