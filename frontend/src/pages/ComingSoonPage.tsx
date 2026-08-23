import { Construction } from "lucide-react";

export default function ComingSoonPage() {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-3 py-24 text-center">
      <div className="grid h-14 w-14 place-items-center rounded-2xl bg-primary-soft text-primary">
        <Construction className="h-6 w-6" />
      </div>
      <h1 className="font-display text-xl font-semibold">Próximamente</h1>
      <p className="text-sm text-muted-foreground">Este módulo se agregará en una fase posterior del proyecto.</p>
    </div>
  );
}
