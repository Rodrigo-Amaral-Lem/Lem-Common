# Ordem dos grupos e segurança — 2026-11-13

Complemento às correções anteriores sobre a base 0.1.57. Atualizar cliente e servidor em conjunto.

- Ordem: SEG, SITE, QVE, EST, MAN, CARG e FIN.
- SEG.02–SEG.06: mantém OK/NOK/N/A, sem opções para anexar fotografias/vídeos ou adicionar observações. NOK nestes itens não exige observação. Evidências antigas permanecem conservadas.
- SEG.07: «Observações gerais de segurança», com fotografias opcionais e campo de observação opcional, sem OK/NOK/N/A. Pode ficar totalmente vazio sem impedir a conclusão.
- Aplicação também aos rascunhos v6 existentes; reports concluídos conservam a checklist histórica.

Verificação: 41 testes API passaram (segurança, regras manuais, assinaturas/exportação e grupos); testes QML de segurança, grupos e regras manuais passaram. Testes nativos de persistência e regras manuais executados com Qt 6.12.0.

Pacote de código-fonte; não contém novo APK ou executável de distribuição. Sem teste num dispositivo Android.
