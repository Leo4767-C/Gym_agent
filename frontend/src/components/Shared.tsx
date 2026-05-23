'use client';
import { MessageSquareQuote, Brain, ChevronDown } from 'lucide-react';
import { useState } from 'react';

export function MotiveBanner({ text }: { text: string }) {
  if (!text) return null;
  return (
    <div style={{background:'var(--accent-dim)',border:'1px solid rgba(124,92,252,0.15)',borderRadius:'var(--radius)',padding:'16px 20px',marginBottom:20,display:'flex',gap:14,alignItems:'flex-start'}}>
      <MessageSquareQuote size={18} color="var(--accent)" style={{flexShrink:0,marginTop:2}} />
      <p style={{fontSize:'.9rem',fontWeight:500,lineHeight:1.7,color:'var(--text)'}}>{text}</p>
    </div>
  );
}

export function ThoughtProcess({ text }: { text: string }) {
  const [open, setOpen] = useState(false);
  if (!text) return null;
  return (
    <div style={{background:'var(--surface)',border:'1px solid var(--border)',borderRadius:'var(--radius)',marginBottom:20,overflow:'hidden'}}>
      <button onClick={()=>setOpen(!open)} style={{width:'100%',padding:'12px 16px',background:'none',border:'none',color:'var(--text)',cursor:'pointer',display:'flex',alignItems:'center',gap:8,fontSize:'.85rem',fontWeight:600}}>
        <Brain size={15} color="var(--text-3)" />
        Quá trình suy nghĩ
        <ChevronDown size={14} color="var(--text-3)" style={{marginLeft:'auto',transform:open?'rotate(180deg)':'none',transition:'transform .2s'}} />
      </button>
      {open && <div style={{padding:'0 16px 14px',fontSize:'.82rem',color:'var(--text-3)',lineHeight:1.8,whiteSpace:'pre-wrap'}}>{text}</div>}
    </div>
  );
}

export function MetaBar({ latency, model }: { latency: number; model: string }) {
  return (
    <div style={{display:'flex',gap:16,fontSize:'.75rem',color:'var(--text-3)',padding:'12px 0',borderTop:'1px solid var(--border)',marginTop:8}}>
      <span>Latency: {latency}ms</span>
      <span>Model: {model}</span>
    </div>
  );
}

export function SectionTitle({ children }: { children: React.ReactNode }) {
  return <div style={{fontSize:'.7rem',fontWeight:700,letterSpacing:'.06em',textTransform:'uppercase',color:'var(--text-3)',marginBottom:10}}>{children}</div>;
}

export function Tag({ children, color = 'var(--text-2)' }: { children: React.ReactNode; color?: string }) {
  return <span style={{background:'var(--surface-2)',border:'1px solid var(--border)',padding:'3px 10px',borderRadius:999,fontSize:'.73rem',color}}>{children}</span>;
}
