// Tipos do contrato sf-tutor-site 1.0.0 (ai-help/claude/insumos-grafo/gerado/site/manifest.json).
// Os cadastros (entidades) são cópias dos JSONs do catálogo; aqui só tipamos o que a interface usa.

export type TipoNo =
  | 'salesforce' | 'nuvem' | 'classificacao' | 'subclassificacao' | 'funcionalidade'
  | 'metadata_type' | 'estrutura_auxiliar' | 'propriedade_xml'
  | 'objeto_api' | 'objeto_api_juncao' | 'campo_api';

export type Estado = 'verificado' | 'desconhecido' | 'nao_aplicavel' | 'nao_exposto' | 'bloqueado' | string;

export interface NoBase {
  id: string;
  tipo: TipoNo;
  rotulo: string;
  rotulo_tecnico?: string;
  rotulo_curto?: string;
  sigla?: string;
  /** logo exibido por referência ao endereço oficial (config/marcas.json); só centro e nuvens */
  logo?: { url: string; formato: string; marca: string };
  /** temas (#34): estado do recorte calculado pelo gerador */
  recorte?: 'conferido' | 'parcial' | 'curadoria';
  estado?: Estado;
  grupo_cor?: string;
  resumo?: string;
  apis?: string[];
  tipo_tecnico?: string;
  explicacao?: string;
}

export interface Aresta {
  origem: string;
  destino: string;
  tipo: string;
  rel_id?: string;
  estado?: Estado;
  natureza?: string;
  papel?: string;
  motivo?: string;
  via?: string[];
}

export interface ItemBusca {
  id: string;
  tipo: TipoNo;
  rotulo: string;
  textos: string[];
  pai?: string;
  descricao?: string;
}

export interface ArvoreVisao {
  id: string;
  filhos?: ArvoreVisao[];
  ocorrencia?: 'principal' | 'secundaria';
}

export interface Visoes {
  por_funcionalidade: ArvoreVisao;
  por_nuvem: ArvoreVisao;
}

export interface Manifesto {
  contrato: { nome: string; versao: string };
  versao_base: Record<string, unknown>;
  arquivos: Record<string, string>;
  contagens: { nos_por_tipo: Record<string, number>; entidades: number; fontes: number; arestas: number; arestas_base: number };
  regras: string[];
  nota: string;
}

export interface Fonte {
  titulo: string;
  url: string;
  tipo?: string;
  versao?: string;
  data_verificacao?: string;
  metodo?: string;
}

export interface InfoBuild {
  commit: string | null;
  data_build: string;
  origem: string;
  sintetico?: boolean;
}

/** Afirmação com estado de verificação (comum.schema.json#/$defs/afirmacao). */
export interface Afirmacao {
  estado?: Estado;
  valor?: unknown;
  nota?: string;
  condicao?: string;
  evidencias?: { fonte: string; secao?: string; nota?: string }[];
  [k: string]: unknown;
}

export type Entidade = Record<string, unknown> & { id: string };

export interface DadosBase {
  manifesto: Manifesto;
  nos: NoBase[];
  arestas: Aresta[];
  visoes: Visoes;
  busca: ItemBusca[];
  fontes: Record<string, Fonte>;
  cobertura: Record<string, unknown>;
  build: InfoBuild;
}
