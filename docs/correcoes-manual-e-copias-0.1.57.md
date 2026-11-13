# Correções sobre Lem Qt 0.1.57 — 2026-11-13

Atualizar cliente e servidor em conjunto. Este pacote mantém a versão base 0.1.57 e contém o código-fonte atualizado; não inclui um novo APK ou executável de distribuição.

## Alterações

- MAN.12: OK/NOK são avaliações independentes e nunca substituem o valor medido. É obrigatório indicar o valor ou N/A. Fotografia sempre obrigatória, incluindo N/A; vídeo não substitui fotografia.
- MAN.18: botões OK, NOK e N/A alinhados com MAN.17, sem a segunda fila duplicada de N/A. Alternar OK/NOK e editar o valor de terra preserva o outro campo.
- MAN.19: opções OK, NOK e N/A.
- QVE/medições: é possível pedir a cópia de um grupo enquanto o outro está a ser copiado, selecionando origens diferentes. A segunda operação fica em fila e inicia-se automaticamente após a primeira. As cópias conservam a origem, as evidências e a identificação independente de cada grupo. Não é uma fila persistente após fechar a aplicação.
- Rascunhos existentes da checklist v6 recebem as correções ao abrir/guardar, incluindo cópias independentes. Reports concluídos mantêm a checklist histórica. Texto antigo em MAN.19 deve ser substituído por uma das novas opções antes de guardar.
- Edição: apagar temporariamente o texto de uma medição já não elimina a avaliação OK/NOK.
- Servidor em Windows: o ficheiro temporário de vídeo é fechado antes de o ffprobe o abrir, corrigindo a rejeição de vídeos válidos.

## Verificação

- Seis testes nativos C++/Qt passaram: persistência, trabalho offline, medições, grupos/assinatura/PDF, cópias e regras manuais. Incluem rascunho v6 anterior e cópias em fila com origens diferentes.
- Testes QML passaram: regras 0.1.56/0.1.57, edição de medições (77 casos partilhados), grupos e assinatura. Verificam também que é possível abrir a segunda ação de cópia durante a primeira.
- Testes API das regras manuais, fotografia, histórico, filtros, assinatura/exportação e vídeos passaram. Os testes adicionais de regressões e interação entre funcionalidades também passaram na revisão.
- Testes antigos foram atualizados onde esperavam que OK/NOK substituísse uma leitura ou dispensavam fotografia em MAN.12.

A verificação foi feita em Windows com Qt/PySide 6.12.0 e dados fictícios. Não inclui validação num dispositivo Android nem produção de novos binários de distribuição.
