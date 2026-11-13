# Fotografias por grupo — 0.1.11

As novas fotografias ficam guardadas imediatamente no dispositivo. O report com fotografias novas aguarda uma mudança de grupo de perguntas (PC01, PC02, PG01, etc.) ou a saída da página do report para ser enviado em segundo plano. Voltar da câmara, esperar alguns segundos ou escrever outra resposta não inicia esse envio.

O botão **Sincronizar** permite antecipar o envio de todos os reports pendentes. **Concluir report** mantém as validações e envia o report e as evidências. Sem ligação, tudo permanece local e a fila já autorizada volta a tentar quando houver rede.

Um envio já em curso termina o lote que começou. Fotografias acrescentadas entretanto aguardam a próxima mudança de grupo, saída do report ou sincronização manual. As fotografias não enviadas e a indicação de que aguardam navegação sobrevivem ao reinício da app. Depois de reiniciar, abra o rascunho e mude de grupo, ou use Sincronizar.

Ao anexar uma fotografia, grava-se apenas o ficheiro e o diário do report correspondente, em vez de regravar todo o catálogo e todos os reports locais. O original da galeria mantém-se intacto.

Atualização apenas do cliente. Não é necessário atualizar o servidor nem limpar a base de dados. O identificador Android mantém-se para conservar os dados locais. No Linux, use um diretório de build sem o antigo conflito entre o executável e a pasta QML (ver build-linux-0.1.10.md).

Validação: cliente C++ com API HTTP e base de dados descartáveis; pausa superior ao anterior temporizador automático sem envio de fotografias; envio por mudança de grupo; nova fotografia durante um lote aguarda a próxima mudança; envio manual; reinício e recuperação local; regressões de remoção, conflitos, descarga e cache. Interface QML testada em dimensões de desktop e Android. Não substitui o teste da compilação Android no equipamento.
