export function SiitLogo({ className = "" }: { className?: string }) {
  return (
    <div className={`flex items-center gap-2.5 ${className}`}>
      <div className="relative grid h-9 w-9 place-items-center rounded-xl bg-gradient-guinda text-primary-foreground shadow-card">
        <span className="font-display text-sm font-bold tracking-tight">IT</span>
        <span className="absolute -right-1 -top-1 h-2.5 w-2.5 rounded-full bg-warning ring-2 ring-background" />
      </div>
      <div className="leading-tight">
        <div className="font-display text-base font-semibold tracking-tight">SIIT</div>
        <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">ITD · TecNM</div>
      </div>
    </div>
  );
}
