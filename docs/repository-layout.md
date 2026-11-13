# Organização do workspace e migração para Git

Data: 2026-11-13. Base: última entrega aprovada, `Lem_Qt_0.1.57_GeneralNotesAndSignaturePhoto.zip`.

## Diretórios

| Diretório | Responsabilidade |
| --- | --- |
| App | Repositório do cliente Qt: app/, documentação própria e snapshot shared/ |
| Server | Repositório da API: server/, deploy/, exemplos, documentação própria e snapshot shared/ |
| Common | Repositório de contrato, recursos, ferramentas e documentação comuns |
| ongoing_work | Builds, dependências, ambientes, scripts transitórios e resultados; sem repositório de produto |
| Brand_Images | Recursos de marca geridos pelo utilizador; não importados nem modificados nesta migração |

Os ZIPs anteriores são conservados na raiz como arquivo. Não criar mais pacotes ZIP por defeito. A futura disponibilização num serviço remoto Git exige que o utilizador indique o destino; nenhum remoto foi criado ou publicado.

A organização interna conserva os prefixos app/, server/, shared/ e deploy/ para manter os caminhos de recursos Qt, os scripts Docker e os caminhos da API. O código do cliente não é duplicado no servidor nem vice-versa. Testes que cruzam os dois componentes usam os clones irmãos ou LEM_APP_REPO / LEM_SERVER_REPO.

## Recursos comuns

Common/shared é a origem canónica. App/shared e Server/shared são snapshots versionados, inicialmente idênticos byte a byte. Esta escolha permite compilar e implantar cada componente a partir de um clone independente. A ferramenta sync_shared.py verifica por defeito; --write publica alterações nas cópias, sem eliminar ficheiros inesperados. Fazer commit dos snapshots nos componentes afetados.

Não usar Brand_Images como dependência implícita do produto. Recursos de marca escolhidos para uma funcionalidade futura devem ser incorporados deliberadamente no repositório responsável.

## Documentação

Guias exclusivos do cliente estão em App/docs. Guias exclusivos da API/instalação estão em Server/docs. Guias transversais e notas históricas comuns estão em Common/docs. As ligações Markdown relativas a ficheiros migrados foram ajustadas. Comandos históricos que ainda descrevem o antigo monorepositório são referências da versão documentada; os READMEs atuais indicam os novos caminhos.

## Git

Identidade local: Rodrigo Amaral <rodrigo.amaral@lem.com.pt>. Branch inicial main. A configuração é local a cada repositório; a configuração global do computador fica inalterada.

Builds anteriores não devem ser reutilizados: a cache do CMake contém caminhos absolutos antigos. Configurar um novo build dentro de ongoing_work e apontar o Qt Creator para App/app/CMakeLists.txt.
