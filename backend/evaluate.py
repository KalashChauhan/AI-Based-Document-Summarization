"""Evaluate a generated summary against a reference summary using ROUGE."""
import argparse
from rouge_score import rouge_scorer
from services.preprocessing_service import word_count

def main():
    parser=argparse.ArgumentParser(); 
    parser.add_argument('--source',required=True); 
    parser.add_argument('--summary',required=True); 
    parser.add_argument('--reference',required=True); 
    args=parser.parse_args()
    source=open(args.source,encoding='utf-8').read(); 
    summary=open(args.summary,encoding='utf-8').read(); 
    reference=open(args.reference,encoding='utf-8').read()
    scores=rouge_scorer.RougeScorer(['rouge1','rouge2','rougeL'],use_stemmer=True).score(reference,summary)
    print({key:round(value.fmeasure,4) for key,value in scores.items()}); 
    print({'original_words':word_count(source),'summary_words':word_count(summary),'compression_percent':round(100*(1-word_count(summary)/max(1,word_count(source))),2)})
if __name__=='__main__': main()
