'use client';
import { Send, Loader2, Dumbbell } from 'lucide-react';
import { useRef, useEffect } from 'react';

const QUICK = [
  { label: 'Tập ngực mới bắt đầu', value: 'Tôi muốn tập ngực với tạ đơn, mới bắt đầu' },
  { label: 'Macro tăng cơ', value: 'Tôi nặng 70kg muốn tăng cơ, nên ăn gì?' },
  { label: 'Lịch giảm cân', value: 'Lên lịch tập tuần cho người muốn giảm cân' },
  { label: 'Form Squat', value: 'Hướng dẫn cách squat đúng form' },
];

interface Props {
  input: string;
  setInput: (v: string) => void;
  loading: boolean;
  onSend: () => void;
}

export default function ChatInput({ input, setInput, loading, onSend }: Props) {
  const ref = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (ref.current) {
      ref.current.style.height = 'auto';
      ref.current.style.height = `${Math.min(ref.current.scrollHeight, 200)}px`;
    }
  }, [input]);

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      {/* Quick Prompts (only show if input is empty and not loading) */}
      {!input && !loading && (
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8, marginBottom: 12, justifyContent: 'center' }}>
          {QUICK.map(q => (
            <button 
              key={q.label} 
              onClick={() => { setInput(q.value); ref.current?.focus(); }}
              style={{ background: 'var(--surface)', border: '1px solid var(--border)', color: 'var(--text-2)', padding: '6px 14px', borderRadius: 999, fontSize: '.8rem', cursor: 'pointer', transition: 'all .2s' }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = 'var(--accent)'; e.currentTarget.style.color = 'var(--text)'; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = 'var(--border)'; e.currentTarget.style.color = 'var(--text-2)'; }}
            >
              {q.label}
            </button>
          ))}
        </div>
      )}

      {/* Input Box - ChatGPT Style */}
      <div 
        style={{
          background: 'var(--surface)',
          border: '1px solid var(--border-2)',
          borderRadius: 24,
          padding: '8px 8px 8px 16px',
          display: 'flex',
          alignItems: 'flex-end',
          boxShadow: 'var(--shadow)',
          position: 'relative',
          transition: 'box-shadow 0.2s, border-color 0.2s',
        }}
        onFocus={(e) => {
          e.currentTarget.style.borderColor = 'var(--accent)';
          e.currentTarget.style.boxShadow = '0 0 15px var(--accent-dim)';
        }}
        onBlur={(e) => {
          e.currentTarget.style.borderColor = 'var(--border-2)';
          e.currentTarget.style.boxShadow = 'var(--shadow)';
        }}
      >
        <textarea 
          ref={ref} 
          value={input} 
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              onSend();
            }
          }}
          placeholder="Nhập mục tiêu tập luyện của bạn (Shift+Enter để xuống dòng)..."
          rows={1}
          style={{
            flex: 1,
            background: 'transparent',
            border: 'none',
            color: 'var(--text)',
            padding: '10px 0',
            fontFamily: 'inherit',
            fontSize: '.95rem',
            resize: 'none',
            outline: 'none',
            maxHeight: 200,
            lineHeight: 1.5,
          }}
        />
        
        <button 
          onClick={onSend} 
          disabled={loading || !input.trim()}
          style={{
            background: loading || !input.trim() ? 'var(--surface-3)' : 'var(--accent)',
            color: loading || !input.trim() ? 'var(--text-3)' : '#000', // Black text on neon green looks good
            border: 'none',
            borderRadius: '50%',
            width: 36,
            height: 36,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: loading || !input.trim() ? 'not-allowed' : 'pointer',
            transition: 'all .2s',
            marginLeft: 8,
            flexShrink: 0,
            marginBottom: 4,
          }}
        >
          {loading ? <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }}/> : <Send size={18} style={{marginLeft: -2, marginTop: 1}}/>}
        </button>
      </div>
    </div>
  );
}
