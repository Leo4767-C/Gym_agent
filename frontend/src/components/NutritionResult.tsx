'use client';
import { Flame, Beef, Wheat, Droplets, UtensilsCrossed, Pill } from 'lucide-react';
import { SectionTitle } from './Shared';

function MacroCard({ label, value, unit, icon: Icon, color, dimColor }: { label:string; value:string|number; unit:string; icon:any; color:string; dimColor:string }) {
  return <div style={{background:'var(--surface-2)',border:'1px solid var(--border)',borderRadius:'var(--radius)',padding:16,textAlign:'center'}}>
    <div style={{width:32,height:32,borderRadius:8,background:dimColor,display:'flex',alignItems:'center',justifyContent:'center',margin:'0 auto 8px'}}>
      <Icon size={16} color={color} />
    </div>
    <div style={{fontSize:'1.3rem',fontWeight:800,color}}>{value}</div>
    <div style={{fontSize:'.65rem',color:'var(--text-3)',marginTop:1}}>{unit}</div>
    <div style={{fontSize:'.78rem',fontWeight:600,marginTop:4}}>{label}</div>
  </div>;
}

export default function NutritionResult({ advice, meals, supplements }: { advice:any; meals:any[]; supplements:string[] }) {
  const hasAdvice = advice?.daily_calories;
  return <>
    {hasAdvice && <>
      <SectionTitle>Thông tin dinh dưỡng</SectionTitle>
      <div style={{display:'grid',gridTemplateColumns:'repeat(auto-fill,minmax(130px,1fr))',gap:10,marginBottom:20}}>
        <MacroCard label="Calo/ngày" value={advice.daily_calories} unit="kcal" icon={Flame} color="var(--amber)" dimColor="var(--amber-dim)" />
        <MacroCard label="Protein" value={advice.protein_grams||0} unit="gram" icon={Beef} color="var(--red)" dimColor="var(--red-dim)" />
        <MacroCard label="Carbs" value={advice.carbs_grams||0} unit="gram" icon={Wheat} color="var(--blue)" dimColor="var(--blue-dim)" />
        <MacroCard label="Fat" value={advice.fat_grams||0} unit="gram" icon={Droplets} color="var(--green)" dimColor="var(--green-dim)" />
      </div>
    </>}
    {meals?.length>0 && <>
      <SectionTitle>Thực đơn gợi ý</SectionTitle>
      <div style={{display:'grid',gap:10,marginBottom:20}}>
        {meals.map((m:any,i:number) => (
          <div key={i} style={{background:'var(--surface-2)',border:'1px solid var(--border)',borderRadius:'var(--radius-sm)',padding:'14px 18px',animation:`fadeUp .35s ease ${i*.06}s both`,display:'flex',gap:14,alignItems:'flex-start'}}>
            <div style={{width:32,height:32,borderRadius:8,background:'var(--accent-dim)',display:'flex',alignItems:'center',justifyContent:'center',flexShrink:0}}>
              <UtensilsCrossed size={15} color="var(--accent)" />
            </div>
            <div style={{flex:1}}>
              <div style={{fontWeight:700,fontSize:'.85rem',color:'var(--accent)'}}>{m.meal_name}</div>
              <div style={{fontSize:'.8rem',color:'var(--text)',lineHeight:1.6,marginTop:2}}>{m.foods}</div>
              <div style={{display:'flex',gap:12,marginTop:6,fontSize:'.73rem',color:'var(--text-3)'}}>
                <span>{m.calories} kcal</span><span>{m.protein}g protein</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </>}
    {supplements?.length>0 && <>
      <SectionTitle>Thực phẩm bổ sung</SectionTitle>
      <div style={{display:'flex',flexWrap:'wrap',gap:6,marginBottom:20}}>
        {supplements.map((s,i) => (
          <span key={i} style={{display:'flex',alignItems:'center',gap:5,background:'var(--surface)',border:'1px solid var(--border)',padding:'5px 12px',borderRadius:999,fontSize:'.78rem',color:'var(--text-2)'}}>
            <Pill size={12}/>{s}
          </span>
        ))}
      </div>
    </>}
  </>;
}
