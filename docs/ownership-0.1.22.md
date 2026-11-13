# Propriedade de rascunhos e conflitos offline — 0.1.22

Atualizar o servidor e recompilar a app Lem. Não apagar nem reinicializar a base de dados.

## Utilização

- Só o proprietário atual pode editar respostas, fotografias ou concluir o rascunho. Um administrador também precisa de ser proprietário para estas ações.
- No menu do report, um administrador pode escolher **Transferir propriedade**, selecionar outro técnico com acesso ao contrato ou um administrador (incluindo ele próprio) e confirmar. O report precisa de estar sincronizado e em rascunho; a transferência requer ligação ao servidor.
- O servidor verifica novamente a revisão e as permissões no momento da transferência. Cada transferência regista o report, proprietário anterior, novo proprietário, administrador responsável e data. A revisão aumenta, mesmo quando uma transferência posterior devolve o report ao proprietário original.
- Reports fechados continuam imutáveis. Mantém-se a permissão anteriormente existente para administradores apagarem reports, incluindo fechados.
- Uma alteração offline que entre em conflito com a propriedade ou revisão do servidor fica protegida e deixa de ser reenviada automaticamente, mesmo após reiniciar a app. O report mostra o motivo e ações para consultar a versão do servidor e **Criar novo rascunho desta cópia**.
- A consulta do servidor apresenta as respostas e observações em modo de leitura, proprietário, revisão, estado e número de fotografias; não substitui as respostas nem fotografias locais.
- A cópia tem novo UUID, novos UUID de fotografias, ficheiros independentes, proprietário igual ao utilizador atual, novas datas e estado rascunho. Conserva respostas e observações; guarda `payload.source_report_id` como referência ao original. Não copia filas de eliminações, revisões ou dados transitórios de sincronização.
- Todas as fotografias da cópia local precisam de existir no dispositivo. Se faltar alguma já enviada, usar **Descarregar fotografias** e repetir a criação da cópia. A app não cria cópias parciais nem elimina o original. Fotografias nunca enviadas e cujos ficheiros estejam em falta precisam de ser recuperadas primeiro.
- Depois de criar uma cópia, pode voltar ao original e escolher **Abrir versão atual após criar cópia**. Esta ação só é permitida enquanto a cópia permanece completa e sem edições, e o original não foi novamente alterado. Caso contrário, é necessário criar outra cópia. O novo rascunho continua disponível no catálogo.

## Atualização e compatibilidade

Na raiz do pacote, executar `bash deploy/deploy.sh`, com os argumentos de ligação habituais, **sem `--reset-database`**. Recompilar/instalar também a app 0.1.22.

A nova tabela `report_ownership_transfers` é criada automaticamente no arranque; os reports, fotografias e utilizadores existentes são mantidos. Não são acrescentadas colunas obrigatórias a tabelas antigas. O histórico é independente da existência futura do report, permitindo manter o registo após uma eliminação administrativa.

Os envios de fotografias passam a exigir `base_revision` no formulário multipart. Apps anteriores precisam de ser atualizadas para enviar fotografias para este servidor. A verificação de proprietário é feita no servidor e repetida após obter o bloqueio do report. A transferência usa a mesma ordem de bloqueios que a gravação/eliminação; as atualizações incluem proprietário e revisão na condição de escrita.

## Verificação

- Testes FastAPI: proprietário exclusivo; administrador sem transferência; elegibilidade por contrato; revisão; transferências de ida/volta; rejeição de alterações e fotografias antigas; fecho; histórico e atualização de uma base de dados existente.
- Cliente C++ com API local descartável: alterações durante sincronização, confirmação perdida, transferência com outro dispositivo offline, conflito de revisão, consulta separada do servidor, cópia completa, IDs/ficheiros independentes e proteção de cópias entretanto alteradas.
- Persistência local: conflito e fotografias sobrevivem a reinício; cópia de um report fechado volta a rascunho com novas datas e referência de origem.
- QML em tamanhos de telefone e desktop: ações de conflito/transferência, botões em modo de leitura e fluxos anteriores.

Não foi possível validar um APK Android nem executar no dispositivo físico neste ambiente. A validação C++/QML usa Qt 6.10.2; o projeto mantém o requisito Qt 6.12 para compilação final.
