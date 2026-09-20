import React, {useEffect,useState} from 'react';
import {history,removeSummary} from '../services/api';
import SummaryCard from '../components/SummaryCard';
export default function History(){
    const[items,setItems]=useState([]),[detail,setDetail]=useState(null),[error,setError]=useState('');
    const load=()=>history().then(r=>setItems(r.data.items)).catch(()=>setError('Could not load history.'));
    useEffect(load,[]);const del=async id=>{await removeSummary(id);
        if(detail?.id===id)setDetail(null);load()};
        return <main>
            <h1>Summary history</h1>
            {error&&<p className="error">{error}</p>}
            {!items.length&&!error&&<p>No summaries yet.</p>}
            <div className="history">{items.map(x=><article className="card" key={x.id}><b>{x.filename}</b><small>{new Date(x.created_at+'Z').toLocaleString()} · {x.summary_length}</small><p>{x.summary.slice(0,160)}…</p><button onClick={()=>setDetail(x)}>View</button><button className="danger" onClick={()=>del(x.id)}>Delete</button></article>)}</div>{detail&&<SummaryCard item={detail}/>}</main>}
