# Observações gerais e assinatura por fotografia — 2026-11-13

Inclui todas as correções anteriores e as seguintes alterações:

- QVE.14: «QVE - Observações gerais», com observação, fotografias e vídeos opcionais, sem OK/NOK/N/A.
- MAN.21: «Observações gerais da manutenção», com observação, fotografias e vídeos opcionais, sem OK/NOK/N/A.
- Os dois itens podem ficar vazios sem impedir a conclusão. São adicionados também aos rascunhos v6 existentes; os reports concluídos mantêm o histórico.
- Desktop: botão «Anexar fotografia da assinatura» no item do técnico. Indicar primeiro o nome do técnico e selecionar uma imagem JPG/PNG da assinatura. A imagem é preparada como PNG e associada ao técnico, utilizando o mesmo fluxo de gravação, sincronização, substituição e exportação da assinatura desenhada. Alterar o nome invalida a assinatura anterior. A opção de desenhar mantém-se disponível.
- Fotografias: ampliar, eliminar e recortar ficam na mesma linha, com botões de 42 × 42 px e espaçamento de 6 px no cartão de 140 px.

Verificação: compilação completa com Qt 6.12.0/MinGW 15.1; teste QML de campos opcionais, seletor da fotografia da assinatura e alinhamento dos botões; 12 testes API de observações/média, conclusão, assinatura e exportação PDF/ZIP. Testes nativos de arranque e grupos incluem importação JPG como assinatura, substituição, conservação após reinício e invalidação ao alterar o nome.

Atualizar cliente e servidor em conjunto. Pacote de código-fonte; não inclui um novo APK ou executável de distribuição.
