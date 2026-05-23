'use client';
import { useState, useEffect, useRef } from 'react';
import { Loader2, AlertCircle, Dumbbell, Apple, CalendarDays, BookOpen, History, Plus, User, Bot, Upload, Wifi, WifiOff } from 'lucide-react';
import type { ChatResponse, HealthResponse } from '@/types';
// Removed Header import
import ChatInput from '@/components/ChatInput';
import { MotiveBanner, ThoughtProcess, MetaBar } from '@/components/Shared';
import WorkoutResult from '@/components/WorkoutResult';
import NutritionResult from '@/components/NutritionResult';
import ScheduleResult from '@/components/ScheduleResult';
import GuideResult from '@/components/GuideResult';
import UploadModal from '@/components/UploadModal';

const API = 'http://localhost:8000';

const TYPE_LABELS: Record<string, { label: string; Icon: any }> = {
  workout_plan:   { label: 'Kế hoạch tập', Icon: Dumbbell },
  nutrition:      { label: 'Dinh dưỡng', Icon: Apple },
  schedule:       { label: 'Lịch tập tuần', Icon: CalendarDays },
  exercise_guide: { label: 'Hướng dẫn bài tập', Icon: BookOpen },
};

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  result?: ChatResponse;
}

export default function Home() {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [streamStatus, setStreamStatus] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [error, setError] = useState('');
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const fetchHealth = async () => {
    try { const r = await fetch(`${API}/api/health`); setHealth(await r.json()); }
    catch { setHealth(null); }
  };

  useEffect(() => {
    fetchHealth();
    const id = setInterval(fetchHealth, 30000);
    return () => clearInterval(id);
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  const send = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setLoading(true);
    setStreamStatus('Đang phân tích câu hỏi...');
    setError('');

    // Add user message to chat history
    const newMessages: ChatMessage[] = [...messages, { role: 'user', content: userMsg }];
    setMessages(newMessages);

    // Build history array for API (last 10 turns)
    const history = newMessages.slice(-20).map(m => ({
      role: m.role,
      content: m.role === 'user' ? m.content : (m.result?.thought_process || m.content).slice(0, 300),
    }));

    try {
      // Use streaming endpoint
      const res = await fetch(`${API}/api/chat/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg, history }),
      });

      if (!res.ok) {
        const e = await res.json();
        throw new Error(e.detail || `HTTP ${res.status}`);
      }

      const reader = res.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error('No reader');

      let buffer = '';
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const payload = JSON.parse(line.slice(6));

          if (payload.event === 'thinking') {
            setStreamStatus(payload.message);
          } else if (payload.event === 'result') {
            const resultData = payload.data as ChatResponse;
            setMessages(prev => [
              ...prev,
              {
                role: 'assistant',
                content: resultData.motivational_message || 'OK',
                result: resultData,
              },
            ]);
            setStreamStatus('');
          } else if (payload.event === 'error') {
            throw new Error(payload.message);
          }
        }
      }
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
      setStreamStatus('');
    }
  };

  const online = health?.status === 'ok';

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', background: 'var(--bg)' }}>
      {/* Sidebar */}
      <div style={{ width: 260, background: 'var(--surface-2)', borderRight: '1px solid var(--border)', display: 'flex', flexDirection: 'column', flexShrink: 0 }}>
        <div style={{ padding: 16 }}>
          <button 
            onClick={() => setMessages([])} 
            style={{ width: '100%', background: 'var(--surface-3)', border: '1px solid var(--border-2)', color: 'var(--text)', padding: '12px 16px', borderRadius: 'var(--radius)', display: 'flex', alignItems: 'center', gap: 12, cursor: 'pointer', fontSize: '.9rem', fontWeight: 500, transition: 'all 0.2s' }}
            onMouseOver={(e) => e.currentTarget.style.background = 'var(--border)'}
            onMouseOut={(e) => e.currentTarget.style.background = 'var(--surface-3)'}
          >
            <Plus size={18} /> Chat Mới
          </button>
        </div>
        
        <div style={{ flex: 1, overflowY: 'auto', padding: '0 16px' }}>
          {/* Recent chats placeholder */}
        </div>

        <div style={{ padding: 16, borderTop: '1px solid var(--border)', display: 'flex', flexDirection: 'column', gap: 12 }}>
          <button onClick={() => setIsUploadOpen(true)} style={{ display: 'flex', alignItems: 'center', gap: 10, background: 'transparent', border: 'none', color: 'var(--text-2)', fontSize: '.85rem', cursor: 'pointer', padding: '8px 0' }}>
            <Upload size={16} /> Nạp Dữ Liệu
          </button>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: '.8rem', color: 'var(--text-3)' }}>
            {online ? <Wifi size={14} color="var(--green)" /> : <WifiOff size={14} color="var(--text-3)" />}
            {health === null ? 'Đang kết nối...' : online ? `Trực tuyến · ${health.db_docs} Docs` : 'Ngoại tuyến'}
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', position: 'relative' }}>
        <UploadModal isOpen={isUploadOpen} onClose={() => setIsUploadOpen(false)} onSuccess={fetchHealth} />

        <div style={{ flex: 1, overflowY: 'auto', padding: '40px 0' }}>
          <div style={{ maxWidth: 800, margin: '0 auto', padding: '0 20px' }}>
            
            {messages.length === 0 && (
              <div style={{ textAlign: 'center', marginTop: '20vh', color: 'var(--text-2)' }}>
                <Dumbbell size={48} color="var(--accent)" style={{ opacity: 0.8, marginBottom: 20 }} />
                <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: 8, color: 'var(--text)' }}>AI Personal Trainer</h1>
                <p style={{ fontSize: '.95rem' }}>Tôi có thể giúp bạn lên lịch tập, tính macro, hoặc chỉnh form ngay hôm nay.</p>
              </div>
            )}

            {messages.map((msg, idx) => {
              const t = msg.result ? TYPE_LABELS[msg.result.response_type] : null;
              const isUser = msg.role === 'user';
              
              return (
                <div key={idx} style={{ display: 'flex', gap: 20, padding: '24px 0', borderBottom: isUser ? 'none' : '1px solid var(--border)', animation: 'fadeIn .3s ease' }}>
                  {/* Avatar */}
                  <div style={{ width: 36, height: 36, borderRadius: '6px', background: isUser ? 'var(--surface-3)' : 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, boxShadow: isUser ? 'none' : '0 0 10px var(--accent-glow)' }}>
                    {isUser ? <User size={20} color="var(--text-2)" /> : <Dumbbell size={20} color="#000" />}
                  </div>
                  
                  {/* Content */}
                  <div style={{ flex: 1, minWidth: 0 }}>
                    {isUser ? (
                      <div style={{ fontSize: '1rem', lineHeight: 1.6, color: 'var(--text)', paddingTop: 6 }}>
                        {msg.content}
                      </div>
                    ) : (
                      <div style={{ fontSize: '.95rem', lineHeight: 1.6, color: 'var(--text-2)' }}>
                        {msg.result ? (
                          <>
                            {t && (
                              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 16 }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'var(--accent-dim)', border: '1px solid var(--accent-glow)', padding: '4px 12px', borderRadius: 999, fontSize: '.75rem', fontWeight: 600, color: 'var(--accent)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                                  <t.Icon size={14} />{t.label}
                                </div>
                              </div>
                            )}
                            <MotiveBanner text={msg.result.motivational_message} />
                            <ThoughtProcess text={msg.result.thought_process} />
                            
                            <div style={{ marginTop: 20 }}>
                              {msg.result.response_type === 'workout_plan' && <WorkoutResult plan={msg.result.workout_plan} />}
                              {msg.result.response_type === 'nutrition' && <NutritionResult advice={msg.result.nutrition_advice} meals={msg.result.meal_plan} supplements={msg.result.supplements} />}
                              {msg.result.response_type === 'schedule' && <ScheduleResult schedule={msg.result.weekly_schedule} goal={msg.result.goal} />}
                              {msg.result.response_type === 'exercise_guide' && <GuideResult guide={msg.result.exercise_guide} />}
                            </div>
                            
                            <div style={{ marginTop: 16 }}>
                              <MetaBar latency={msg.result.latency_ms} model={health?.model ?? '—'} />
                            </div>
                          </>
                        ) : null}
                      </div>
                    )}
                  </div>
                </div>
              );
            })}



            {/* Loading Indicator */}
            {loading && (
              <div style={{ display: 'flex', gap: 20, padding: '24px 0' }}>
                <div style={{ width: 36, height: 36, borderRadius: '6px', background: 'var(--accent)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0, opacity: 0.7 }}>
                  <Loader2 size={18} color="#000" style={{ animation: 'spin 1s linear infinite' }} />
                </div>
                <div style={{ flex: 1, paddingTop: 8 }}>
                  <p style={{ color: 'var(--accent)', fontSize: '.9rem', fontWeight: 500, animation: 'pulse 1.5s infinite' }}>{streamStatus || 'AI đang xử lý...'}</p>
                </div>
              </div>
            )}

            {error && (
              <div style={{ background: 'var(--red-dim)', border: '1px solid rgba(248,113,113,.2)', borderRadius: 'var(--radius)', padding: '16px 20px', display: 'flex', gap: 10, alignItems: 'flex-start', margin: '24px 0' }}>
                <AlertCircle size={16} color="var(--red)" style={{ flexShrink: 0, marginTop: 2 }} />
                <span style={{ fontSize: '.85rem', color: 'var(--red)' }}>{error}</span>
              </div>
            )}

            <div ref={bottomRef} style={{ height: 40 }} />
          </div>
        </div>

        {/* Chat Input Container */}
        <div style={{ padding: '0 20px 32px 20px', background: 'linear-gradient(180deg, transparent 0%, var(--bg) 20%)', position: 'absolute', bottom: 0, width: '100%' }}>
          <div style={{ maxWidth: 800, margin: '0 auto' }}>
            <ChatInput input={input} setInput={setInput} loading={loading} onSend={send} />
            <div style={{ textAlign: 'center', fontSize: '.7rem', color: 'var(--text-3)', marginTop: 12 }}>
              AI Personal Trainer có thể mắc lỗi. Vui lòng kiểm tra lại thông tin quan trọng.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
