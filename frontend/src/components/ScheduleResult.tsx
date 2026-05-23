'use client';
import { CalendarDays, Clock, StickyNote } from 'lucide-react';
import { SectionTitle } from './Shared';

export default function ScheduleResult({ schedule, goal }: { schedule: any[]; goal: string }) {
  if (!schedule?.length) return null;
  return <>
    <SectionTitle>Lịch tập tuần {goal ? `— ${goal}` : ''}</SectionTitle>
    <div style={{display:'grid',gap:10,marginBottom:20}}>
      {schedule.map((d:any, i:number) => (
        <div key={i} style={{background:'var(--surface-2)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',padding:'14px 18px',animation:`slideIn .3s ease ${i*.05}s both`,display:'flex',gap:16,alignItems:'flex-start'}}>
          <div style={{background:'var(--accent)',borderRadius:'var(--radius-sm)',padding:'10px 0',minWidth:52,textAlign:'center',fontWeight:800,fontSize:'.82rem',color:'#000',letterSpacing:'-0.01em'}}>
            {d.day}
          </div>
          <div style={{flex:1}}>
            <div style={{fontWeight:700,fontSize:'.88rem',color:'var(--accent)'}}>{d.focus}</div>
            {d.exercises?.length>0 && <div style={{fontSize:'.78rem',color:'var(--text-3)',marginTop:4}}>{d.exercises.join(' · ')}</div>}
            <div style={{display:'flex',gap:14,marginTop:6,fontSize:'.73rem',color:'var(--text-3)'}}>
              <span style={{display:'flex',alignItems:'center',gap:4}}><Clock size={11}/>{d.duration_minutes} phút</span>
              {d.notes && <span style={{display:'flex',alignItems:'center',gap:4}}><StickyNote size={11}/>{d.notes}</span>}
            </div>
          </div>
        </div>
      ))}
    </div>
  </>;
}
