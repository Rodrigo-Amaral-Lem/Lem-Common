> Atualização 0.1.23: a identificação Android atual é `pt.lem.app`, uma instalação separada. Sincronizar trabalho pendente antes de trocar. As notas de compatibilidade desta página descrevem a entrega histórica.

# Ícone e abertura — 0.1.19

O ícone usa uma versão limpa do logótipo LEM fornecido, sem o texto pequeno inferior. Foram preparados ícones Android por densidade e adaptativos, ícone de janela/desktop Linux e ICO Windows. O original está conservado em `app/assets/lem-original.png` e os ficheiros de trabalho em `app/assets/`.

Na abertura, o logótipo surge centrado, sem deformação nem cortes, num ecrã claro que cobre toda a área da aplicação, incluindo o cabeçalho e o rodapé. Permanece dois segundos e depois abre a interface normal. O temporizador permite que o processamento continue e a camada inicial impede toques acidentais nos controlos por baixo. Aparece apenas ao criar a janela, não sempre que se regressa da câmara ou de outra app. As barras do sistema Android e o ecrã de arranque nativo continuam sob controlo do sistema operativo.

O nome LEM e o identificador Android pt.lem.app mantêm-se. O arranque de teste `--smoke-test` e as capturas `--screenshot` ignoram a espera para conservar os testes automáticos existentes.

Verificação: QML em desktop e dimensões Android, logótipo carregado, ecrã visível antes de terminar o intervalo e fechado depois, cobertura da janela e bloqueio de toques na interface; temporizador de controlo confirma que o ciclo de eventos continua ativo. Inspeção visual a 390 × 844. Dimensões dos PNG, resoluções do ICO e referências XML Android verificadas. Não foi executada compilação Android/Windows nesta revisão; confirmar no Qt Creator a apresentação no launcher e no equipamento físico.

Atualizar apenas o cliente. O servidor mantém a versão 0.1.15.
