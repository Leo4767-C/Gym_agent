'use client';
import { Dumbbell, Wifi, WifiOff, Upload } from 'lucide-react';
import type { HealthResponse } from '@/types';

export default function Header({ health, onOpenUpload }: { health: HealthResponse | null, onOpenUpload: () => void }) {
  const online = health?.status === 'ok';
  return (
    <header style={{background:'var(--surface)',borderBottom:'1px solid var(--border)',padding:'14px 32px',display:'flex',alignItems:'center',justifyContent:'space-between',position:'sticky',top:0,zIndex:100,backdropFilter:'blur(16px)'}}>
      <div style={{display:'flex',alignItems:'center',gap:12}}>
        <div style={{width:36,height:36,borderRadius:10,background:'var(--accent-dim)',border:'1px solid rgba(124,92,252,0.2)',display:'flex',alignItems:'center',justifyContent:'center'}}>
          <Dumbbell size={18} color="var(--accent)" />
        </div>
        <div>
          <div style={{fontWeight:700,fontSize:'.95rem',letterSpacing:'-0.01em'}}>AI Personal Trainer</div>
          <div style={{fontSize:'.7rem',color:'var(--text-3)'}}>Ollama · ChromaDB · RAG</div>
        </div>
      </div>
      <div style={{display:'flex',alignItems:'center',gap:12}}>
        <button onClick={onOpenUpload} style={{display:'flex',alignItems:'center',gap:6,background:'var(--surface-2)',border:'1px solid var(--border)',padding:'6px 12px',borderRadius:999,fontSize:'.75rem',color:'var(--text-2)',cursor:'pointer'}}>
          <Upload size={13} /> Nạp Dữ liệu
        </button>
        <div style={{display:'flex',alignItems:'center',gap:8,padding:'6px 14px',borderRadius:999,background:'var(--surface-2)',border:'1px solid var(--border)',fontSize:'.78rem',color:'var(--text-2)'}}>
          {online ? <Wifi size={13} color="var(--green)" /> : <WifiOff size={13} color="var(--text-3)" />}
          {health===null?'Connecting…':online?`Online · ${health.db_docs} exercises`:'Offline'}
        </div>
      </div>
    </header>
  );
}
