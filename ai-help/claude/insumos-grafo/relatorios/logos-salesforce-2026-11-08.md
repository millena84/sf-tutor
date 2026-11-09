# Logos da Salesforce e das nuvens: origem e termos (2026-11-08)

As diretrizes do tutorial (doc do projeto `claude/diretrizes-tutorial-visual.md`, itens 2 e 3) pedem:
- o logo de nuvem da Salesforce no nó central;
- o logo de cada produto nos nós de nuvem.

O MVP não atendeu a esse pedido e usou um placeholder. Este registro diz o que foi verificado e o que falta.

## O que foi verificado

- **Diretrizes de uso de marcas da Salesforce** (https://www.salesforce.com/company/legal/tmcusageguidelines/):
  - valem para qualquer terceiro, inclusive desenvolvedores e publicadores;
  - dizem que a maioria dos usos exige permissão escrita, por contrato ou por licença específica.
- **Partner Branding Guidelines** (https://partners.salesforce.com/s/Partner_Branding_Guidelines.pdf, revisão de fev/2018):
  - orientam não usar logos atuais ou antigos da Salesforce sem permissão;
  - orientam não criar logos parecidos.
- **simple-icons 16.37.0** (pacote npm, CC0): **não** traz o ícone da Salesforce. Não há fonte aberta de uso livre por esse caminho.
- **Ambiente do Claude:** o shell não acessa sites fora da lista liberada (npm, PyPI, GitHub). Daqui não dá para baixar o arquivo oficial do portal de marca.

## Caminhos possíveis (decisão da Millena)

1. **Arquivos oficiais fornecidos pela Millena**, com a origem e os termos registrados, por exemplo do portal de marca ou de material de Trailhead/parceiro a que ela tenha acesso. O site já tem o aviso de não afiliação.
2. **Pedido de permissão** à Salesforce para uso educacional.
3. **Manter só o nome em texto** (uso referencial) nos nós de marca, sem logo.

Não é opção redesenhar ou imitar os logos: as próprias diretrizes proíbem, e o prompt da tarefa 2 também.
