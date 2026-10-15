import type { Case } from './types';
export class ApiError extends Error {constructor(message:string,public state?:Case){super(message)}}
export async function request<T>(path:string,body?:unknown):Promise<T>{
 const res=await fetch('/api'+path,{method:body===undefined?'GET':'POST',headers:{'Content-Type':'application/json','X-BatchLens-Client':'workspace'},body:body===undefined?undefined:JSON.stringify(body)});
 const raw=await res.text(); let data; try{data=JSON.parse(raw)}catch{throw new ApiError(res.ok ? 'The server returned an incomplete response. Please retry.' : raw || 'Could not reach the API. Check that the backend is running.')}
 if(!res.ok){const detail=data.detail;throw new ApiError(typeof detail==='string'?detail:detail?.message||'Something went wrong. Please try again.',detail?.state)}return data;
}
export const assetUrl=(id:string,artifact:string)=>`/api/investigations/${id}/artifacts/${artifact}`;
