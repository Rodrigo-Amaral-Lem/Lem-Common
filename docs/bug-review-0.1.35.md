# Verificação geral — Lem 0.1.35

Data: 10-11-2026. Revisão do código e testes locais da app/API/deploy, partindo
da 0.1.34 R1. Não foi alterado o servidor do utilizador nem apagada qualquer BD.

## Falhas encontradas e corrigidas

| Área | Reprodução / efeito anterior | Correção |
| --- | --- | --- |
| Importação Excel | Cabeçalho na linha 100 numa folha com poucos registos levantava StopIteration e provocava erro interno em vez de validação | Cabeçalho inexistente/vazio recebe HTTP 422; nenhuma alteração parcial |
| Número da linha de cabeçalho | 1,5 era truncado para 1; booleanos podiam ser interpretados como números; infinito causava OverflowError | Aceitar apenas inteiro ou texto convertível para inteiro, entre 1 e 100; rejeitar valores inválidos com 422 |
| PDF/ZIP do servidor | Localização válida mas muito longa fazia uma linha da tabela exceder uma página, causando ReportLab LayoutError | Permitir divisão da linha de metadados entre páginas, sem truncar o texto |
| Navegação Android | StandardKey.Back pode incluir Backspace e outros atalhos de teclado, além do gesto/tecla Back | Usar apenas a sequência Back em Android; conservar o atalho padrão em desktop |

O problema PDF foi reproduzido com texto sintético longo na localização. A
correção está no gerador comum ao PDF e ao PDF incluído no ZIP. O limite de
texto do Excel não foi aumentado e a geração local Qt não foi alterada.

O ajuste de Back segue a documentação Qt 6.12. O teste em Qt Quick confirma que
a sequência Android é apenas Back, que Backspace mantém o report aberto e que
Back navega para o catálogo. Não foi feita uma reprodução com teclado físico
ligado a um smartphone Android nesta revisão.

## Validação

- A versão inicial passou os 112 testes existentes de servidor/deploy.
- A versão corrigida passou **120 testes de servidor/deploy, zero ignorados**,
  incluindo oito regressões novas, Excel original e simulações PowerShell 7.6.6.
- As novas regressões verificam cabeçalhos inválidos, ausência de alterações
  parciais e importação válida posterior; o PDF longo termina corretamente e
  contém várias páginas.
- Verificações Qt Quick: respostas, notas, fotografias, grupos, swipes,
  preservação de posição, botões/rodapé, limites de scroll, mensagens, exportação
  limitada a reports fechados e avisos de versão. Os testes de navegação afetados
  pelo atalho foram repetidos após a alteração e passaram sem avisos QML.
- Configuração Android OpenSSL: **13 testes CMake aprovados**; descoberta
  automática, múltiplas ABIs, prioridade de configuração e rejeição de binários
  incompatíveis conservadas.
- Windows standalone: **8 testes aprovados** de verificador PE e configuração
  CMake simulada. Não foi gerado/testado um novo EXE Windows nesta revisão.
- Política XML de backup Android verificada estruturalmente.
- Integração C++/API temporária aprovada: gravações lentas sem bloquear respostas,
  edição mais recente durável, conflitos, transferências, cópia independente,
  remoção, confirmação perdida, envio diferido, downloads limitados e cache.
- PDF local sem sessão aprovado, com fotografias e notas longas; evidência em
  falta/corrompida mantém o destino existente intacto. Recuperação de armazenamento
  local e compatibilidade de login também passaram.

Os testes nativos usam Qt 6.10.2 em Linux. O controlador C++ não foi alterado;
os objetos já compilados foram reutilizados e os testes adicionais ligados a
esses objetos. Não se apresenta este ensaio como compilação do APK Qt 6.12 ou
teste físico de Windows/Android/iOS. Os avisos Python registados dizem respeito
a depreciações de bibliotecas e extensões Excel; não foram falhas dos testes.

## Aplicar

Atualizar o servidor pelo deploy normal para corrigir importação e PDF/ZIP.
Recompilar a app **0.1.35**, Android code **137**, para o ajuste do atalho.
**Não é necessário reset da base de dados.** A versão mínima continua 0.1.28;
latest passa para 0.1.35 sem reduzir uma versão superior configurada.

A descoberta automática de OpenSSL e as melhorias de desempenho da 0.1.34
foram conservadas. As mensagens gráficas do smartphone que não produzem sintomas
não motivaram alteração do backend gráfico. Esta revisão não atualiza as
bibliotecas OpenSSL nem o SDK Qt instalados no laptop; consultar também a
[revisão de segurança](security-review-0.1.33.md).

Referência para Back em Qt 6.12:
https://doc.qt.io/qt-6/android-platform-notes.html#back-key-and-back-gesture
