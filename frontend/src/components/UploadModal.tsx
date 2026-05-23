'use client';
import { useState, useRef } from 'react';
import { X, UploadCloud, Loader2, Database, Apple } from 'lucide-react';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export default function UploadModal({ isOpen, onClose, onSuccess }: Props) {
  const [file, setFile] = useState<File | null>(null);
  const [collection, setCollection] = useState<'exercises' | 'nutrition'>('nutrition');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!isOpen) return null;

  const handleUpload = async () => {
    if (!file) {
      setError('Vui lòng chọn một file.');
      return;
    }
    
    setLoading(true);
    setError('');
    setSuccessMsg('');
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('collection_type', collection);
    
    try {
      const res = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });
      
      const data = await res.json();
      
      if (!res.ok) {
        throw new Error(data.detail || 'Upload failed');
      }
      
      setSuccessMsg(`Thành công! Đã nạp ${data.chunks_added} chunks vào ChromaDB.`);
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      setTimeout(() => {
        onSuccess();
        // Keep open so they can see success message, but let them close it
      }, 1000);
      
    } catch (err: any) {
      setError(err.message || 'Có lỗi xảy ra khi upload file.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{position:'fixed',top:0,left:0,width:'100vw',height:'100vh',background:'rgba(0,0,0,0.7)',backdropFilter:'blur(4px)',display:'flex',alignItems:'center',justifyContent:'center',zIndex:999}}>
      <div style={{background:'var(--surface)',width:'100%',maxWidth:480,borderRadius:'var(--radius)',border:'1px solid var(--border)',boxShadow:'var(--shadow-lg)',overflow:'hidden',animation:'fadeUp .2s ease'}}>
        
        {/* Header */}
        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',padding:'16px 20px',borderBottom:'1px solid var(--border)'}}>
          <h2 style={{fontSize:'1rem',fontWeight:700,display:'flex',alignItems:'center',gap:8}}>
            <Database size={18} color="var(--accent)" />
            Data Ingestion (Nạp dữ liệu)
          </h2>
          <button onClick={onClose} style={{background:'none',border:'none',color:'var(--text-3)',cursor:'pointer'}}><X size={18} /></button>
        </div>
        
        {/* Body */}
        <div style={{padding:'24px 20px'}}>
          <p style={{fontSize:'.85rem',color:'var(--text-3)',marginBottom:20}}>
            Upload các file Raw Data (PDF, CSV, JSON, TXT) để dạy cho AI kiến thức mới mà không cần code lại.
          </p>
          
          <div style={{marginBottom:16}}>
            <label style={{display:'block',fontSize:'.8rem',fontWeight:600,marginBottom:8}}>Loại kiến thức:</label>
            <div style={{display:'flex',gap:12}}>
              <label style={{flex:1,display:'flex',alignItems:'center',gap:8,padding:'12px',border:`1px solid ${collection==='nutrition'?'var(--accent)':'var(--border)'}`,borderRadius:'var(--radius-sm)',background:collection==='nutrition'?'var(--accent-dim)':'var(--bg)',cursor:'pointer'}}>
                <input type="radio" name="col" checked={collection==='nutrition'} onChange={()=>setCollection('nutrition')} style={{display:'none'}} />
                <Apple size={16} color={collection==='nutrition'?'var(--accent)':'var(--text-3)'} />
                <span style={{fontSize:'.85rem',fontWeight:500,color:collection==='nutrition'?'var(--accent)':'var(--text-2)'}}>Dinh dưỡng</span>
              </label>
              <label style={{flex:1,display:'flex',alignItems:'center',gap:8,padding:'12px',border:`1px solid ${collection==='exercises'?'var(--accent)':'var(--border)'}`,borderRadius:'var(--radius-sm)',background:collection==='exercises'?'var(--accent-dim)':'var(--bg)',cursor:'pointer'}}>
                <input type="radio" name="col" checked={collection==='exercises'} onChange={()=>setCollection('exercises')} style={{display:'none'}} />
                <Database size={16} color={collection==='exercises'?'var(--accent)':'var(--text-3)'} />
                <span style={{fontSize:'.85rem',fontWeight:500,color:collection==='exercises'?'var(--accent)':'var(--text-2)'}}>Bài tập Gym</span>
              </label>
            </div>
          </div>
          
          <div style={{marginBottom:24}}>
            <label style={{display:'block',fontSize:'.8rem',fontWeight:600,marginBottom:8}}>Chọn file (PDF, CSV, JSON, TXT):</label>
            <input 
              type="file" 
              ref={fileInputRef}
              accept=".pdf,.csv,.json,.txt"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              style={{width:'100%',padding:'10px',border:'1px dashed var(--border-2)',borderRadius:'var(--radius-sm)',background:'var(--bg)',color:'var(--text-2)',fontSize:'.85rem'}}
            />
          </div>
          
          {error && <div style={{fontSize:'.8rem',color:'var(--red)',marginBottom:16,padding:'10px',background:'var(--red-dim)',borderRadius:'var(--radius-sm)'}}>{error}</div>}
          {successMsg && <div style={{fontSize:'.8rem',color:'var(--green)',marginBottom:16,padding:'10px',background:'var(--green-dim)',borderRadius:'var(--radius-sm)'}}>{successMsg}</div>}
          
          <button 
            onClick={handleUpload} 
            disabled={loading || !file}
            style={{width:'100%',padding:'12px',background:(loading||!file)?'var(--surface-3)':'var(--text)',color:(loading||!file)?'var(--text-3)':'var(--bg)',border:'none',borderRadius:'var(--radius-sm)',fontWeight:600,cursor:(loading||!file)?'not-allowed':'pointer',display:'flex',alignItems:'center',justifyContent:'center',gap:8}}
          >
            {loading ? <Loader2 size={16} style={{animation:'spin 1s linear infinite'}} /> : <UploadCloud size={16} />}
            {loading ? 'Đang phân tích và nạp dữ liệu...' : 'Bắt đầu Nạp dữ liệu'}
          </button>
        </div>
      </div>
    </div>
  );
}
