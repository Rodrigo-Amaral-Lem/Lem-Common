# Lem 0.1.30 — exportação apenas de reports concluídos

As opções **Exportar PDF** e **PDF + fotografias (ZIP)** não aparecem no menu de
um rascunho, em Android, Windows ou Linux. Só ficam disponíveis quando o report
está concluído (`status: closed`).

A app verifica o estado antes de abrir o diálogo de gravação e volta a verificar
quando o utilizador escolhe o destino. O gerador PDF local também recusa rascunhos.
No servidor, ambos os endpoints verificam a autorização e recusam rascunhos com
HTTP 409, antes de gerar ficheiros ou carregar fotografias.

Um report concluído continua a permitir **PDF offline e sem sessão**, desde que
os seus dados e fotografias estejam no dispositivo. O ZIP continua a exigir sessão
e report sincronizado no servidor. A possibilidade de concluir localmente sem rede
não foi alterada. Estas regras aplicam-se também aos administradores.

Atualizar app e servidor. A última versão suportada passa para 0.1.30; a mínima
continua 0.1.28. O deploy normal promove uma última versão fixada anteriormente,
como descrito na 0.1.29. Não é necessário apagar a base de dados.

Verificação: opções ausentes em rascunhos e presentes em reports concluídos nas
interfaces desktop/mobile; recusa nativa antes de criar o ficheiro; endpoints PDF/ZIP
recusam rascunhos e continuam a exportar reports concluídos; PDF nativo concluído
sem sessão, com evidência e observações longas. Testes Qt 6.10.2 offscreen/Linux;
compilação Qt 6.12 e dispositivo Android/Windows físico por validar nesta entrega.
