'use client';
import { Target, Wrench, Timer, RotateCcw, Lightbulb } from 'lucide-react';
import { SectionTitle } from './Shared';

export default function WorkoutResult({ plan }: { plan: any[] }) {
  if (!plan?.length) return null;
  return <>
    <SectionTitle>Kế hoạch tập — {plan.length} bài</SectionTitle>
    <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(280px,1fr))',gap:14,marginBottom:20}}>
      {plan.map((ex:any,i:number) => (
        <div key={i} style={{background:'var(--surface-2)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',padding:'18px 20px',animation:`fadeUp .35s ease ${i*.06}s both`,transition:'border-color .15s,transform .15s,box-shadow .15s'}}
          onMouseEnter={e=>{e.currentTarget.style.borderColor='var(--accent)';e.currentTarget.style.transform='translateY(-2px)';e.currentTarget.style.boxShadow='0 4px 12px var(--accent-dim)'}}
          onMouseLeave={e=>{e.currentTarget.style.borderColor='var(--border)';e.currentTarget.style.transform='translateY(0)';e.currentTarget.style.boxShadow='none'}}>
          <div style={{fontWeight:700,fontSize:'.9rem',marginBottom:4,color:'var(--accent)'}}>{ex.exercise_name}</div>
          <div style={{display:'flex',alignItems:'center',gap:6,fontSize:'.75rem',color:'var(--text-3)',marginBottom:14,textTransform:'uppercase',letterSpacing:'0.05em'}}>
            <Target size={12}/>{ex.muscle_group}
            <span style={{color:'var(--border-2)'}}>·</span>
            <Wrench size={12}/>{ex.equipment}
          </div>
          <div style={{display:'flex',gap:8,marginBottom:14}}>
            {[{v:ex.sets,l:'Sets'},{v:ex.reps,l:'Reps'},{v:`${ex.rest_seconds}s`,l:'Rest'}].map(s=>(
              <div key={s.l} style={{background:'var(--surface-3)',border:'1px solid var(--border-2)',borderRadius:'var(--radius-xs)',padding:'7px 12px',textAlign:'center',flex:1}}>
                <div style={{fontWeight:700,fontSize:'.85rem',color:'var(--text)'}}>{s.v}</div>
                <div style={{fontSize:'.65rem',color:'var(--text-3)',marginTop:1,textTransform:'uppercase'}}>{s.l}</div>
              </div>
            ))}
          </div>
          <div style={{fontSize:'.78rem',color:'var(--text-3)',lineHeight:1.6,borderTop:'1px solid var(--border)',paddingTop:10,display:'flex',gap:6,alignItems:'flex-start'}}>
            <Lightbulb size={13} style={{flexShrink:0,marginTop:2}} color="var(--amber)"/>
            <span>{ex.coaching_tip}</span>
          </div>
        </div>
      ))}
    </div>
  </>;
}
