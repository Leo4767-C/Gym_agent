'use client';
import { BookOpen, AlertTriangle, Wind } from 'lucide-react';
import { SectionTitle, Tag } from './Shared';

export default function GuideResult({ guide }: { guide: any }) {
  if (!guide?.exercise_name) return null;
  return <>
    <SectionTitle>Hướng dẫn bài tập</SectionTitle>
    <div style={{background:'var(--surface-2)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',padding:22,marginBottom:20}}>
      <div style={{fontWeight:700,fontSize:'1rem',marginBottom:10,color:'var(--accent)'}}>{guide.exercise_name}</div>
      <div style={{display:'flex',gap:6,flexWrap:'wrap',marginBottom:18}}>
        <Tag>{guide.muscle_group}</Tag>
        <Tag>{guide.equipment}</Tag>
        <Tag>{guide.difficulty}</Tag>
        {guide.sets_reps_recommendation && <Tag color="var(--accent)">{guide.sets_reps_recommendation}</Tag>}
      </div>

      {guide.video_url && (
        <div style={{position:'relative',width:'100%',paddingBottom:'56.25%',marginBottom:24,borderRadius:'var(--radius-sm)',overflow:'hidden',boxShadow:'var(--shadow)'}}>
          <iframe 
            src={guide.video_url} 
            title={`Video hướng dẫn ${guide.exercise_name}`}
            style={{position:'absolute',top:0,left:0,width:'100%',height:'100%',border:0}} 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowFullScreen
          />
        </div>
      )}

      {guide.steps?.length>0 && <>
        <div style={{display:'flex',alignItems:'center',gap:6,fontWeight:600,fontSize:'.82rem',marginBottom:8}}><BookOpen size={14} color="var(--accent)"/>Các bước thực hiện</div>
        <ol style={{paddingLeft:20,fontSize:'.82rem',lineHeight:2.2,color:'var(--text-2)',marginBottom:18}}>
          {guide.steps.map((s:string,i:number)=><li key={i}>{s}</li>)}
        </ol>
      </>}
      {guide.common_mistakes?.length>0 && <>
        <div style={{display:'flex',alignItems:'center',gap:6,fontWeight:600,fontSize:'.82rem',marginBottom:8,color:'var(--amber)'}}><AlertTriangle size={14}/>Lỗi sai thường gặp</div>
        <ul style={{paddingLeft:20,fontSize:'.82rem',lineHeight:2.2,color:'var(--text-3)',marginBottom:18}}>
          {guide.common_mistakes.map((m:string,i:number)=><li key={i}>{m}</li>)}
        </ul>
      </>}
      {guide.breathing && <div style={{fontSize:'.82rem',color:'var(--text-3)',borderTop:'1px solid var(--border)',paddingTop:12,display:'flex',gap:6,alignItems:'flex-start'}}>
        <Wind size={14} color="var(--green)" style={{flexShrink:0,marginTop:2}}/> <span><strong style={{color:'var(--text)'}}>Cách thở:</strong> {guide.breathing}</span>
      </div>}
    </div>
  </>;
}
