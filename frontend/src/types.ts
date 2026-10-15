export type Artifact={id:string;name:string;file:string;kind:string;label:string;description:string;size:string};
export type Candidate={value:string|null;quote:string;provider:string;label:string;artifact_id:string;status:string;reviewed_value?:string};
export type Row={id:string;destination:string;units:number;batch:string|null;category:string;reason:string;evidence:string[]};
export type Scope={revision:number;engine_version:string;rows:Row[];totals:Record<string,number>};
export type Proposal={id:string;created_at:string;revision:number;scope:Scope;note:string;suspect_lot:string};
export type Case={id:string;revision:number;created_at:string;baseline:boolean;suspect_lot:string|null;resolved_batch:string|null;added_clear_slip:boolean;candidates:Record<string,Candidate>;history:{id:string;at:string;title:string;detail:string;revision:number}[];proposals:Proposal[];scope:Scope;artifacts:Artifact[];batches:Record<string,string>;mode:'demo'|'gemini';model_attempts:number;scenario_version:string};
