# Lem 0.1.28 — compatibilidade e instalação limpa

Esta versão precisa de **app e servidor atualizados**. As apps anteriores à 0.1.28
não enviam o header de versão e serão recusadas pelo novo servidor. Não existe
migração obrigatória de dados: este é um protótipo e pode ser instalado de raiz.

## Regras de versões

Antes de enviar email/password, a app pede ao servidor `GET /api/client-compatibility`.
O servidor controla a versão mínima compatível e a última versão suportada. Compara
números (por exemplo, 0.1.10 é posterior a 0.1.9), não texto.

| Situação | Resultado |
| --- | --- |
| Versão igual à última suportada | Login normal. |
| Entre a mínima e a última, inclusive | Login permitido; se for mais antiga que a última, aviso para atualizar quando possível. |
| Abaixo da mínima, acima da última ou sem identificação válida | Login bloqueado, com indicação da versão a instalar. |
| Política ausente/inválida ou servidor sem ligação | Não envia credenciais; informa que não foi possível verificar a compatibilidade. |
| Política muda entre verificação e login | O servidor volta a verificar o POST e pode recusar com HTTP 426. |
| Sessão existente com versão que passou a ser incompatível | O servidor recusa os pedidos; a app termina a sessão de comunicação e conserva os dados locais. |

A demonstração e os dados locais disponíveis continuam utilizáveis sem login,
incluindo o PDF offline quando as fotografias estão descarregadas. A verificação
não apaga rascunhos. O aviso de atualização é mostrado num diálogo e mantém-se
na área Conta; mensagens de sincronização não o substituem.

A política inicial está em `deploy/.env.example` e nos valores de Compose:

```dotenv
LEM_MIN_CLIENT_VERSION=0.1.28
LEM_LATEST_CLIENT_VERSION=0.1.28
LEM_UPDATE_URL=
```

Ao publicar uma atualização compatível, subir apenas `LEM_LATEST_CLIENT_VERSION`.
Quando houver uma quebra de compatibilidade, subir também a mínima. A máxima
suportada é a última publicada; uma app mais nova precisa de o servidor reconhecer
a sua versão. `LEM_UPDATE_URL` é opcional e deve ser um endereço HTTPS real para
descarregar a app ou consultar instruções. Não é criado um serviço de download.

Após editar `.env`, no servidor:

```bash
cd ~/apps/Lem/deploy
sudo docker compose up -d --force-recreate api
```

Exemplo futuro: mínima 0.1.28 e última 0.1.29 permitem a 0.1.28 com aviso, e a
0.1.29 sem aviso. Estes valores só devem ser publicados quando a versão existir.
Reiniciar a API aplica a política; não é necessário alterar a base de dados.

Pedidos manuais/Swagger também precisam de `X-Lem-Client-Version: 0.1.28`.
Os endpoints públicos de saúde e compatibilidade não exigem sessão nem versão.
Esta identificação é um controlo de versões, não substitui autenticação/permissões.

## Nomes atuais

O pacote, fontes, opções de build, testes, scripts, documentação e exemplos usam
Lem/LEM/lem. Exemplos: projeto Compose `lem`, base/utilizador PostgreSQL `lem`,
utilizador interno da imagem `lem`, prefixo de configuração `LEM_`, pasta `Lem`,
admin inicial `admin@lem.pt` e domínio predefinido `lem.rodrod.pt`.

Reconfigurar CMake e usar as opções atuais, por exemplo `LEM_BUILD_TESTS` e
`LEM_ANDROID_OPENSSL_ROOT`. A identidade Android mantém-se `pt.lem.app`.
Os nomes de marca embebidos nas imagens/documentos de demonstração foram revistos.

O deploy normal conserva a pasta e os volumes/configuração selecionados. Para não
conservar nomes anteriores no protótipo, usar uma instalação limpa. Os scripts não
alteram DNS, contas SSH ou outros serviços do computador. Definições escolhidas
pelo utilizador, incluindo o endereço guardado na app, não são substituídas à força.

## Recriar o protótipo no servidor

1. Configurar o DNS A/AAAA de `lem.rodrod.pt` para o servidor (ou escolher outro
   domínio real). Garantir que 80/443 estão livres após remover o protótipo.
2. Copiar/extrair o novo pacote para uma pasta temporária **fora da instalação antiga**.
   Entrar no servidor com um utilizador com sudo. O utilizador SSH pode ser o existente;
   os scripts de deploy aceitam `--user` / `-UserName` para o indicar.
3. A partir do novo pacote, inspecionar o protótipo selecionado:

```bash
python3 deploy/remove-prototype.py --installation "/caminho/absoluto/instalacao-antiga"
```

Para executar a remoção autorizada do protótipo e dos seus dados:

```bash
python3 deploy/remove-prototype.py --installation "/caminho/absoluto/instalacao-antiga" --delete
```

**Apaga a pasta selecionada, base de dados, fotografias, contas da app, volumes de
certificados e imagens locais desse projeto Compose.** Os nomes exatos são lidos da
configuração; não são adivinhados. Docker recusa remover um volume usado por outro
container. Uma falha interrompe o processo e conserva a pasta para diagnóstico.
Não usar contra uma instalação de produção. Não remove contas SSH, DNS ou outros
projetos Docker. O modo sem `--delete` só mostra o plano.

4. Colocar a pasta nova em `~/apps/Lem` e executar, como utilizador normal com sudo:

```bash
cd ~/apps/Lem
LEM_DOMAIN=lem.rodrod.pt bash deploy/install-ubuntu.sh
```

O instalador cria `.env`, base e volumes Lem, pede o email inicial e gera as passwords.
O proxy pede um novo certificado para o domínio. A emissão depende do DNS e das portas.
Não há ligação ao servidor real durante a preparação/testes deste pacote.

5. Instalar/compilar a app 0.1.28, colocar `https://lem.rodrod.pt` em Conta e entrar
   com o administrador novo. Com uma base nova, importar novamente os contratos/IDs;
   não reenviar rascunhos da base eliminada. Pode limpar/reinstalar a app de teste.
6. Para atualizações posteriores, usar os scripts normais do laptop:

```bash
bash deploy/deploy.sh --host lem.rodrod.pt --user lem --remote-path apps/Lem
```

Adaptar o utilizador SSH/chave às credenciais reais. Não é necessário usar o nome
predefinido para uma conta do sistema que já exista.

## Indicador lateral Android

O percurso ocupa toda a área abaixo do cabeçalho Lem, até ao fundo da aplicação,
independentemente dos menus. O marcador tem tamanho mínimo legível (48 píxeis lógicos).
A posição é limitada ao intervalo válido antes de a entregar ao ScrollBar, impedindo
que o arrasto elástico o comprima. No fim da página atinge o fundo do percurso.
O aparecimento/desaparecimento dos menus não muda a área de leitura.

## Verificações

- Políticas e bloqueio de pedidos/sessões em API descartável, incluindo versões sem header.
- Cliente C++ real: versão atual, antiga compatível, incompatível, endpoint ausente,
  resposta incompleta, versão devolvida incorreta e mudança de política antes do POST.
- Interface QML: avisos de versão, persistência na Conta, gestos entre grupos e indicador
  com percurso completo, tamanho mínimo e deslocação além dos extremos.
- Regressões de edição local/sincronização e deploy Linux; remoção do protótipo com Docker
  simulado, rejeição de caminhos perigosos e preservação de recursos alheios.
- Pacote revisto quanto a nomes anteriores, ligações locais e ausência de dados privados.

Testes nativos/QML em Qt 6.10.2 offscreen. Falta validar compilação final Qt 6.12,
gestos no Android físico, DNS/HTTPS/Docker reais e o fluxo PowerShell deste pacote.
