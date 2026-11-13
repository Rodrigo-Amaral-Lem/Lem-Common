# LEM Common — contrato, recursos e ferramentas partilhados

- `shared/`: checklist, casos de teste de conectores/medições e branding já incorporado no produto. É a origem canónica das cópias em App e Server.
- `tools/`: sincronização de recursos e ferramentas comuns de auditoria.
- `docs/`: documentação transversal e histórico que afeta cliente e servidor.

Usar `../ongoing_work/` para comandos, builds e resultados temporários. A partir desse diretório:

```powershell
python ../Common/tools/sync_shared.py          # verificar
python ../Common/tools/sync_shared.py --write  # publicar alterações locais nas cópias versionadas
```

Os três repositórios usam cópias explícitas dos recursos para permitir clones e releases independentes, sem symlinks, submódulos ou dependências de caminhos externos na execução. Rever os diffs e fazer commit em cada repositório afetado ao alterar o contrato.

Consultar [organização e migração](docs/repository-layout.md). Os repositórios são locais, sem remotes configurados. Os ZIPs existentes permanecem como arquivo das versões anteriores; o trabalho futuro é feito por Git.
