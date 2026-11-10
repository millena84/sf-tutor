// Rótulos pt-BR da interface. Não contém conteúdo técnico Salesforce: só nomes de categorias do contrato.
import type { TipoNo } from './data/tipos';

export const NOME_TIPO: Record<TipoNo | 'pagina', string> = {
  salesforce: 'Centro do mapa',
  nuvem: 'Nuvem / produto',
  // Tradução didática: nos dados os níveis se chamam classificação e subclassificação (00-especificacao-grafo.md).
  classificacao: 'Tema',
  subclassificacao: 'Tema',
  funcionalidade: 'Funcionalidade',
  metadata_type: 'Metadata type (XML)',
  estrutura_auxiliar: 'Estrutura auxiliar do XML',
  propriedade_xml: 'Propriedade XML',
  objeto_api: 'Objeto consultável via API',
  objeto_api_juncao: 'Objeto de junção (API)',
  campo_api: 'Campo de objeto API',
  pagina: 'Mais itens',
};

export const ICONE_TIPO: Record<TipoNo | 'pagina', string> = {
  salesforce: 'SF', nuvem: '', classificacao: '', subclassificacao: '', funcionalidade: '',
  metadata_type: 'XML', estrutura_auxiliar: '{ }', propriedade_xml: 'p', objeto_api: 'API', objeto_api_juncao: 'JUN', campo_api: 'c', pagina: '+',
};

export const ESTADO: Record<string, { rotulo: string; simbolo: string; explicacao: string }> = {
  verificado: { rotulo: 'Verificado', simbolo: '✓', explicacao: 'Confirmado em fonte oficial para a versão e o contexto declarados.' },
  desconhecido: { rotulo: 'Desconhecido', simbolo: '?', explicacao: 'Ainda não investigado ou sem evidência suficiente.' },
  nao_aplicavel: { rotulo: 'Não aplicável', simbolo: '–', explicacao: 'O atributo não faz sentido para este item.' },
  nao_exposto: { rotulo: 'Não exposto', simbolo: '⊘', explicacao: 'Uma fonte verificada documenta a indisponibilidade.' },
  bloqueado: { rotulo: 'Bloqueado', simbolo: '■', explicacao: 'Falta fonte, acesso, licença ou outra condição.' },
};
export const rotuloEstado = (e?: string): string => (e ? ESTADO[e]?.rotulo ?? e : 'Sem estado');

export const LIGACAO: Record<string, { rotulo: string; grupo: 'hierarquia' | 'representacao' | 'estrutura' | 'referencia' | 'correspondencia'; explicacao: string }> = {
  navegacao_classificacao: { rotulo: 'Agrupa (tema)', grupo: 'hierarquia', explicacao: 'Hierarquia didática do mapa: o centro leva aos temas.' },
  navegacao_subclassificacao: { rotulo: 'Agrupa (tema dentro de tema)', grupo: 'hierarquia', explicacao: 'Hierarquia didática: um tema reúne temas mais específicos.' },
  navegacao_nuvem: { rotulo: 'Nuvem / produto', grupo: 'hierarquia', explicacao: 'Hierarquia didática da visão por nuvem. Não afirma que os produtos dividem a mesma infraestrutura.' },
  nuvem_classificacao: { rotulo: 'Tema aplicável', grupo: 'hierarquia', explicacao: 'Tema que tem funcionalidades desta nuvem.' },
  nuvem_subclassificacao: { rotulo: 'Tema aplicável (dentro de tema)', grupo: 'hierarquia', explicacao: 'Tema mais específico que tem funcionalidades desta nuvem.' },
  nuvem_funcionalidade: { rotulo: 'Funcionalidade na nuvem', grupo: 'hierarquia', explicacao: 'Funcionalidade associada à nuvem no cadastro da nuvem. A mesma funcionalidade pode aparecer em várias nuvens com o mesmo conteúdo.' },
  classificacao_principal: { rotulo: 'Tema principal', grupo: 'hierarquia', explicacao: 'Lugar principal da funcionalidade na organização didática.' },
  classificacao_secundaria: { rotulo: 'Tema secundário', grupo: 'hierarquia', explicacao: 'A funcionalidade também aparece neste tema; é a mesma ficha da ocorrência principal.' },
  representacao_xml: { rotulo: 'Representada por XML', grupo: 'representacao', explicacao: 'Metadata type que representa a funcionalidade como configuração implantável.' },
  representacao_objeto_api: { rotulo: 'Representada por objeto API', grupo: 'representacao', explicacao: 'Objeto consultável via API ligado à funcionalidade. Não é tabela física privada.' },
  propriedade: { rotulo: 'Propriedade', grupo: 'estrutura', explicacao: 'Propriedade documentada do metadata type ou da estrutura.' },
  campo: { rotulo: 'Campo', grupo: 'estrutura', explicacao: 'Campo documentado do objeto.' },
  tipo_composto: { rotulo: 'Tipo composto', grupo: 'estrutura', explicacao: 'A propriedade usa uma estrutura auxiliar do XML (tipo composto), detalhada como nó próprio.' },
  referencia_campo: { rotulo: 'Referência', grupo: 'referencia', explicacao: 'Um campo guarda o Id de um registro do objeto de destino (lookup), ou uma propriedade do XML cita outro componente pelo nome.' },
  correspondencia_xml_api: { rotulo: 'Correspondência XML ↔ API', grupo: 'correspondencia', explicacao: 'Correspondência documentada entre o metadata type e o objeto/campo API, com a natureza indicada.' },
  representacao_comum: { rotulo: 'Mesmo conceito XML ↔ API', grupo: 'correspondencia', explicacao: 'Metadata type e objeto API descrevem o mesmo conceito por caminhos diferentes; correspondência campo a campo não comprovada.' },
};

export const FORMA_DEFAULT: Record<string, string> = {
  valor: 'Valor declarado',
  ausente_no_xml: 'Ausente no XML',
  null: 'null',
  false: 'false',
  string_vazia: 'String vazia',
  nao_declarado_na_fonte: 'Não declarado na fonte (não presumir false nem vazio)',
  desconhecido: 'Desconhecido',
  nao_aplicavel: 'Não aplicável',
};

export const OBRIGATORIEDADE: Record<string, string> = {
  sim: 'Obrigatório', nao: 'Não obrigatório', condicional: 'Condicional', desconhecida: 'Desconhecida', nao_aplicavel: 'Não aplicável',
};

export const NATUREZA_DOMINIO: Record<string, string> = {
  enum_fechado: 'Lista fechada de valores', lista_dinamica: 'Lista dinâmica (depende da org)', texto_livre: 'Texto livre', booleano: 'Booleano',
  numerico: 'Número', data_hora: 'Data/hora', identificador: 'Identificador', referencia: 'Referência a registro', tipo_composto: 'Tipo composto',
  desconhecida: 'Desconhecida', nao_aplicavel: 'Não aplicável',
};

export const ORIGEM: Record<string, string> = {
  padrao_plataforma: 'Padrão da plataforma', customizado: 'Customizado', nao_aplicavel: 'Não aplicável',
};

export const NATUREZA_RECOMENDACAO: Record<string, string> = {
  oficial: 'Orientação oficial', inferencia_tecnica: 'Inferência técnica fundamentada', preferencia_projeto: 'Preferência do projeto',
};

export const TIPO_LICENCA: Record<string, string> = {
  licenca_usuario: 'Licença de usuário', licenca_permission_set: 'Licença de permission set', edicao: 'Edição', add_on: 'Add-on', licenca_recurso: 'Feature license (licença de recurso)',
};

export const PROPRIEDADES_API: [string, string][] = [
  ['create', 'Create (aceita na criação)'], ['update', 'Update (aceita na atualização)'], ['nillable', 'Nillable (aceita nulo)'],
  ['defaulted_on_create', 'Defaulted on create (recebe valor na criação)'], ['filter', 'Filter (filtra em SOQL)'], ['group', 'Group (agrupa)'],
  ['sort', 'Sort (ordena)'], ['restricted_picklist', 'Restricted picklist'], ['id_lookup', 'idLookup (identifica registro em upsert)'],
];

export const NOME_API: Record<string, string> = { padrao: 'API padrão', tooling: 'Tooling API' };

/** Na legenda, os dois níveis de tema têm formas diferentes e precisam de nomes distintos. */
export const NOME_TIPO_LEGENDA: Partial<Record<TipoNo | 'pagina', string>> = {
  classificacao: 'Tema',
  subclassificacao: 'Tema dentro de outro tema',
};

/**
 * Estado do recorte de um tema (camada "Nível avançado" de "Sobre este tema").
 * Hoje não há estado "parcial" no catálogo: "parcialmente conferido" só aparece quando o tema
 * tem referências oficiais registradas mas ainda não está verificado.
 */
export const RECORTE: Record<'conferido' | 'parcial' | 'curadoria', { rotulo: string; explicacao: string }> = {
  conferido: { rotulo: 'Conferido com fonte oficial', explicacao: 'O recorte deste tema foi comparado com referências oficiais registradas.' },
  parcial: { rotulo: 'Parcialmente conferido', explicacao: 'Há referências oficiais registradas, mas o recorte ainda não foi conferido por completo.' },
  curadoria: { rotulo: 'Curadoria do projeto', explicacao: 'Recorte proposto pelo projeto; ainda não conferido com fonte oficial.' },
};

export function estadoRecorte(estado: unknown, temReferencias: boolean): { rotulo: string; explicacao: string } {
  return RECORTE[estado === 'verificado' ? 'conferido' : temReferencias ? 'parcial' : 'curadoria'];
}

/** Rótulos dos itens do "Nível avançado" (campo avancado[].tipo). */
export const TIPO_AVANCADO: Record<string, string> = {
  decisao: 'Decisão', seguranca: 'Segurança', implantacao: 'Implantação', testes: 'Testes', limite: 'Limite', escala: 'Escala', atencao: 'Ponto de atenção',
};
