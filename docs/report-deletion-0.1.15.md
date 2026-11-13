# Apagar reports — 0.1.15

No menu do report, escolha **Apagar rascunho…** ou, como administrador, **Apagar report fechado…**. A confirmação explica que o report e as fotografias associadas serão apagados definitivamente. Os originais na galeria permanecem.

- Técnico: apenas os seus próprios rascunhos.
- Administrador: qualquer rascunho ou report fechado.
- Rascunho exclusivamente local, nunca enviado: pode apagar sem rede.
- Report já enviado ou com tentativa de envio anterior: necessita de sessão e ligação ao servidor. Se a remoção falhar, a cópia local é conservada. Uma revisão diferente bloqueia a remoção até sincronizar ou atualizar o report.

A remoção fica indisponível durante transferências para evitar conflitos com operações em curso. A API valida as permissões e a revisão, independentemente do que a interface apresenta. Pedidos repetidos após perda da confirmação não repetem a remoção nem o registo de auditoria.

O servidor apaga o report e os dados binários das fotografias na mesma transação. Mantém apenas um pequeno registo do identificador apagado, carregador, autor, estado e data, mais a auditoria, para impedir que um dispositivo com dados antigos volte a criar esse report. Os metadados do catálogo comunicam as remoções; a sincronização de uma cópia apagada recebe HTTP 410. A app remove então a cópia local. Um dispositivo sem ligação pode manter temporariamente uma cópia anterior até voltar a atualizar/sincronizar.

A cache local conserva identificadores apagados para impedir a recuperação de diários antigos após reinício. Só elimina ficheiros da pasta privada da app, após confirmar a gravação da remoção no dispositivo.

## Atualizar

Atualizar **servidor e app**. No laptop Linux, a partir da pasta LEM:

```bash
bash deploy/deploy.sh
```

Não usar a opção de reset. A nova tabela `deleted_reports` é criada automaticamente no arranque do servidor, conservando os dados existentes. Depois, recompilar e instalar a app 0.1.15 com a mesma chave de assinatura Android.

## Verificação

Testes da API: técnico autor, outro técnico, técnico sem contrato, administrador, rascunhos e fechados, conflito de revisão, repetição, remoção das fotografias, auditoria e bloqueio de recriação. Cliente C++: remoção offline, recuperação após reinício com diário antigo, remoção no servidor, limpeza de cópia alterada durante sincronização e atualização do catálogo. Testes QML em dimensões de Android e desktop: permissões, confirmação e cancelamento. Não foi executada uma compilação Android nesta revisão.
