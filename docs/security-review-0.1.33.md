# Revisão de segurança — Lem 0.1.33

Data: 10-11-2026. Revisão do código da app Qt, API FastAPI, modelos/permissões,
importação, fotografias, exportação e configuração de deploy fornecidos no pacote.
Os testes usam apenas dados fictícios, SQLite temporário e serviços em loopback.
Não foram enviados ataques, scanners ou alterações ao servidor em produção.

## Resultado e prioridade

Foram corrigidas falhas de controlo e acrescentadas proteções com testes locais.
**Isto não é uma certificação de ausência de vulnerabilidades.** A correção interna
Qt descrita abaixo continua dependente do SDK utilizado para compilar a app.

| Área | Problema / condição de ataque | Alteração | Estado / evidência |
| --- | --- | --- | --- |
| Login — prioridade alta | Espaços no email alteravam a chave do limitador, mas eram retirados ao autenticar. Um atacante podia continuar a adivinhar a password do mesmo utilizador. O limite apenas por par IP/email também permitia distribuição por IP ou conta. | Normalização única; limites independentes por par (5/min), IP (30/min) e conta (20/min). Buckets limitados a 10000 e expiram em 60 s; capacidade excedida falha fechada. | Reprodução antiga: sete variantes devolveram 401, contornando o limite de cinco. Corrigido: variantes passam a 429; testes de IP/conta/capacidade/expiração. Não era possível entrar sem uma password válida. |
| Login — proteção adicional | Utilizador inexistente dispensava scrypt, oferecendo uma diferença de trabalho observável entre contas existentes/inexistentes. | Verificação contra hash fictício quando a conta não existe; resposta genérica conservada. | Teste confirma que ambos os casos passam pela função de verificação; não constitui prova de tempo perfeitamente constante em toda a rede/BD. |
| App/rede — prioridade média | Um redirecionamento 307 podia reenviar o corpo de um POST de login para outra origem. Exige redirecionamento pelo servidor/proxy configurado. | SameOriginRedirectPolicy em pedidos JSON e multipart. | Teste TCP local com o código Qt anterior envia um pedido para a segunda origem; a política nova bloqueia-o e permite redirecionamentos dentro da mesma origem. |
| Memória — prioridade média | Corpos JSON/multipart e respostas HTTP podiam consumir recursos antes das validações de domínio. A validação tardia de fotografia não limitava a resposta enquanto chegava. | Limites ASGI antes do parsing, incluindo streaming; leitura progressiva limitada na app e aborto em excesso. | Testes para corpo anunciado e em chunks; teste Qt com resposta chunked limitada. Não substitui o patch interno Qt para a CVE pendente. |
| Excel/XML — prioridade média, importação exige administrador | Ausência de proteção explícita e independente do parser contra DTD/entidades; tamanho ZIP e linhas não limitavam colunas/células declaradas. Um Excel de um fornecedor é entrada não confiável mesmo quando o administrador o importa. | defusedxml obrigatório; pré-validação XML streaming; rejeição de DTD/entidades e limites adicionais. | XML de teste com entidade e dimensões exageradas é rejeitado com 422; importações normais continuam a passar. Não foi executada uma bomba XML de grande dimensão. |
| Fotografias — consumo de memória | Cada validação da quota carregava todas as imagens do report, até 250 MB, apenas para as contar/somar. | COUNT/SUM(LENGTH) na BD; sem carregar BLOBs para esse cálculo. Image.open limitado a JPEG/PNG. | Fluxos reais de fotografias/quotas passam nos testes de API e de sincronização. |
| Caminhos locais — proteção adicional | IDs recebidos do servidor eram concatenados em nomes de ficheiros/pastas sem validar separadores. Um servidor/resposta manipulado poderia sair do namespace local previsto. Não foi encontrado um endpoint da API que permita ao técnico escolher IDs de fotografia não UUID. | Componentes locais estritos; identidades incompatíveis mapeadas para hash; rejeição de IDs de fotografias inválidos. | Teste C++ cobre ../, barra, barra invertida, percent-encoding e newline. Não protege contra um atacante que já controla o sistema de ficheiros ou o processo. |
| Android — proteção de dados | allowBackup=true permitia incluir dados da app nos conjuntos de backup pessoais/transferências do sistema. | allowBackup=false e exclusões explícitas nos formatos antigo/novo, cloud/D2D/cross-platform. | Manifesto e recursos XML verificados. Não foi testado backup num dispositivo físico; não é proteção contra root ou fabricantes que ignorem as regras. |
| Dependências | Pillow 11.3.0 está no intervalo de versões de avisos de segurança do fornecedor. | Pillow 13.0.0; defusedxml 0.7.1. | Auditoria das 25 dependências Python resolvidas sem avisos conhecidos na base consultada nesta data. Não foi demonstrada exploração de todas as CVEs de Pillow no fluxo JPEG/PNG da Lem. |

## Pendência externa: Qt 6.12.0

O aviso oficial **CVE-2026-116337**, publicado em 09-11-2026, afeta o tratamento
interno de respostas HTTP do Qt Network. Um servidor malicioso/comprometido pode
provocar consumo excessivo de memória. O aviso classifica o impacto como baixo e
indica que não existe mitigação equivalente ao patch. Os limites de resposta da
Lem são uma proteção distinta e **não são apresentados como correção desta CVE**.

O fornecedor indica Qt **6.12.1** ou os dois patches oficiais para Qt 6.12. No índice
de distribuição consultado nesta data figuram 6.12.0 e os patches; não se assume
que 6.12.1 já esteja disponível no Maintenance Tool.

- Aviso: https://www.qt.io/blog/security-issue-cve-2026-116337
- Patches/índice: https://download.qt.io/official_releases/qt/6.12/
- Patch 1: https://download.qt.io/official_releases/qt/6.12/CVE-2026-116337-qtbase-6.12-0001.diff
- Patch 2: https://download.qt.io/official_releases/qt/6.12/CVE-2026-116337-qtbase-6.12-0002.diff

Para Windows estático, aplicar os patches oficiais a uma árvore Qt correspondente
e reconstruir o Qt estático, depois Lem.exe. Para Android/Linux/Windows partilhado,
instalar kits corrigidos pelo fornecedor ou compilar kits correspondentes com os
patches. Não basta alterar o código da Lem ou copiar o EXE: o Qt está embutido no
EXE/APK. Esta entrega **não altera o SDK instalado no computador do utilizador** e
não inclui patches upstream modificados/inventados. CMake avisa quando o kit é
6.12.0; um kit com backport pode conservar esse número e requer confirmação própria.

Outros avisos consultados para Qt3D, QHttpServer, QtWebSockets e Qt5Compat não são
apresentados como falhas exploráveis da Lem: o projeto não utiliza esses módulos.
O código lê JSON, não QCborValue de entrada; não se afirma exploração da CVE de
conversão CBOR apenas por o QtCore ser dependência.

## Limites e comportamento

- Login: limites em memória correspondem ao deploy atual com **um worker**. Reinícios
  limpam contadores; não partilham estado entre múltiplas réplicas/workers. Se a
  arquitetura passar a vários workers, é necessário um limitador partilhado no
  gateway/serviço. Há possibilidade de bloqueio temporário de uma conta por abuso
  do próprio limite; expira após 60 s.
- Pedidos: login 4 KiB; outros JSON 512 KiB; multipart 21 MiB (ficheiro continua
  limitado a 20 MiB). O proxy mantém o limite global de 25 MB. O limite da app
  protege também uma execução local da API sem esse proxy.
- Respostas: fotografia 20 MiB, PDF/ZIP 350 MiB, restantes respostas 64 MiB.
  Excesso produz erro, conservando o trabalho local; não é truncado como sucesso.
  Um catálogo legítimo superior a 64 MiB exige paginação/ajuste futuro, não remover
  a proteção indiscriminadamente.
- Excel: máximo 100 MiB descomprimidos, 2000 entradas ZIP, 100000 linhas totais,
  256 colunas e 2000000 células declaradas; leitura com limites também quando faltam
  dimensões. Ficheiros maiores precisam de ser repartidos/regravados.
- Dados offline continuam disponíveis sem login, conforme requisito do produto.
  Não foi introduzida encriptação de cache nem bloqueio biométrico. Um dispositivo
  desbloqueado, comprometido ou com a conta do sistema acessível continua um risco.
- As exclusões Android não apagam dados existentes nem desligam a sincronização
  da Lem. Rascunhos ainda não sincronizados não são recuperados pelo backup pessoal
  do sistema: sincronizar antes de desinstalar/trocar de smartphone.
- Não foi encontrada fuga de tokens para ficheiros de sessão: o cliente guarda a
  identidade offline, mas mantém o bearer token em memória. Passwords no servidor
  usam scrypt com salt e tokens são guardados por digest; estes mecanismos foram
  mantidos. Reset de password pela CLI revoga sessões.

## Permissões verificadas

API exige token, contrato atribuído e associação report/fotografia. Foram testados:
utilizador fora do contrato, técnico não proprietário, administrador que precisa
transferir propriedade para editar, revisão antiga após transferência, report
fechado imutável, remoção por dono/admin e associação de fotografias. PDF/ZIP continuam
limitados a reports fechados. Queries SQL continuam parametrizadas pelo ORM e os
textos do PDF continuam escapados antes de ReportLab.

Isto não prova que todos os cenários concorrentes PostgreSQL estejam corretos;
os testes de API desta revisão usam SQLite. Não se executaram testes destrutivos,
força bruta ou upload malicioso no serviço real.

## Validação executada

- Suite servidor + deploy: **109 passaram, zero ignorados**, com PowerShell 7.6.6
  e o Excel original V0-2. Inclui os 14 testes de integração Excel e 14 testes
  PowerShell; ver [validação da importação](../../Server/docs/import-validation-2026-11-10.md) e
  [validação PowerShell](../../Server/docs/powershell-validation-2026-11-10.md). Um teste de domínio
  desatualizado foi corrigido e a descoberta automática ganhou cobertura própria;
  a deteção predefinida de ProjectPath foi também corrigida após o ensaio Windows,
  com teste sem parâmetro explícito.
- Seis testes de segurança API/importador/limitador incluídos nesse total.
- Teste C++ Qt 6.10.2: redirecionamento entre origens bloqueado; mesma origem
  permitida; corpo chunked limitado; IDs de cache inseguros rejeitados.
- O teste com a política de redirecionamento anterior falha: a segunda origem
  recebe um pedido. O login antigo também reproduziu sete tentativas por espaços.
- Cliente C++ recompilado localmente com Qt 6.10.2; smoke de persistência e integração
  offline contra API temporária, incluindo fotos, conflitos, transferências,
  ACK perdido, cópias e remoções. Não é uma compilação real Qt 6.12/Windows/Android.
- Recursos de backup Android verificados estruturalmente; APK e extração num
  smartphone não foram testados nesta revisão.
- `pip-audit -r server/requirements.txt`: 25 pacotes resolvidos, sem vulnerabilidades
  conhecidas no snapshot consultado; ver [resultado JSON](security/dependency-audit-2026-11-10.json).

Comandos principais, a partir da raiz Lem:

```sh
CHECKLIST_FILE="$PWD/shared/checklist-v1.json" PYTHONPATH="$PWD/server" python -m pytest server/tests deploy/tests -q
python app/tests/test_android_backup_policy.py
pip-audit -r server/requirements.txt
```

O alvo CMake `Lem-network-security-test` está disponível com `LEM_BUILD_TESTS=ON`.
Os testes de integração C++ existentes continuam documentados em `app/tests`.
Uma falha pré-existente no teste de remoção de protótipo em sistemas sem `/srv`
foi corrigida: diretório inexistente dá ValueError antes de qualquer comando Docker.
Nenhum protótipo real foi removido.

## Aplicar a versão

Atualizar o servidor com `deploy/deploy.sh` ou `deploy/deploy.ps1` do novo pacote.
Não há mudança de esquema; **não utilizar reset da base de dados** para esta revisão.
O deploy atualiza a política latest para 0.1.33, preservando uma versão superior
já configurada e a minimum existente. O mínimo por omissão continua 0.1.28; assim,
instalar a app e servidor sem bloquear imediatamente todos os técnicos antigos é
possível. O cabeçalho de versão não é prova criptográfica de um binário corrigido.

Compilar/distribuir a app 0.1.33 (Android code 135), usando o Qt corrigido quando
possível. Manter a configuração Android `LEM_ANDROID_OPENSSL_ROOT` da máquina.
Windows estático conserva o build por omissão e o verificador de DLLs corrigido.
As alterações de segurança do código são comuns às plataformas; não é preciso
reconfigurar a lógica funcional dos reports ou apagar os dados locais.

## Referências consultadas

- OWASP Authentication: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
- OWASP Bot Management: https://cheatsheetseries.owasp.org/cheatsheets/Bot_Management_and_Anti-Automation_Cheat_Sheet.html
- Qt redirect policy: https://doc.qt.io/qt-6/qnetworkrequest.html
- openpyxl/XML: https://openpyxl.readthedocs.io/en/stable/
- Pillow: https://github.com/python-pillow/Pillow/security/advisories/GHSA-v9pv-5gc8-w2m6
- Android backups: https://developer.android.com/identity/data/autobackup
