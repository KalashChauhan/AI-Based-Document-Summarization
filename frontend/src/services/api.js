import axios from 'axios';
const api=axios.create({baseURL:import.meta.env.VITE_API_URL||'http://localhost:5000/api'});
export const summarizeFile=(file,summary_length)=>{
    const data=new FormData();
    data.append('file',file);
    data.append('summary_length',summary_length);
    return api.post('/summarize',data)
};
export const summarizeText=(text,summary_length)=>api.post('/summarize-text',{text,summary_length});
export const history=()=>api.get('/history'); 
export const getSummary=id=>api.get(`/history/${id}`); 
export const removeSummary=id=>api.delete(`/history/${id}`);
