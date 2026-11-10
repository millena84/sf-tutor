# Lotes novos

Scripts de lotes carregados com `ferramentas/carga/` (a partir do lote 6). Veja o esqueleto em `ferramentas/README.md`.

| Script | O que faz |
|---|---|
| `exemplos_regras_e_horarios.py` | Exemplos XML escritos à mão para AssignmentRules, EscalationRules e BusinessHoursSettings (issue #20). |
| `escopo_temas.py` | `escopo` e `fora_do_escopo` de todos os temas (issue #34, fase 2). Reexecutável. |
| `referencias_temas.py` | Fontes e referências oficiais dos 14 temas de primeiro nível (issue #34, fase 3). Reexecutável. |
| `conteudo_temas.py` | Conteúdo específico por tema: `para_iniciantes`, `encadeamento` e `avancado`, cada bloco com fontes (issue #34). Piloto: Interface e Lightning pages e componentes. |
| `conteudo_pendentes.py` | Conteúdo dos temas internos que estavam sem fonte, lote 1 (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes2.py` | Lote 2 dos temas sem fonte: classificação e sensibilidade, retenção, consentimento, pastas e acesso, métricas (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes3.py` | Lote 3 dos temas sem fonte: colaboração, templates, recuperação de conhecimento, experiências web/portais/mobile, habilitação de recursos, metadados de configuração de dados (issue #34). Usado por `conteudo_temas.py`. |
| `conteudo_pendentes4.py` | Lote 4 dos temas sem fonte: serviço de campo, experiências externas, capacidades setoriais, outras áreas (issue #34). Usado por `conteudo_temas.py`. |
| `temas_internos.py` | Limpeza do dado genérico dos temas internos (issue #34, item 3): descrição, referências oficiais já registradas e nota de estado, um tema principal por vez. Reexecutável. |
