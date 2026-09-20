import React from 'react';
export default function SummaryCard({item}){
    const copy=()=>navigator.clipboard.writeText(item.summary);
    const download=()=>{
        const url=URL.createObjectURL(new Blob([item.summary],{type:'text/plain'}));
        const a=document.createElement('a');
        a.href=url;
        a.download='summary.txt';
        a.click();
        URL.revokeObjectURL(url)
    };
    let compression=item.word_count?Math.round((1-item.summary_word_count/item.word_count)*100):0;
    return <section className="card result">
        <div className="meta">
            <b>{item.filename}</b>
            <span>{item.word_count} original words</span>
            <span>{item.summary_word_count} summary words</span>
            <span>{compression}% shorter</span>
        </div>
        <h2>Generated summary</h2>
        <p>{item.summary}</p>
        <button onClick={copy}>Copy</button>
        <button className="secondary" onClick={download}>Download .txt</button>
    </section>
}
