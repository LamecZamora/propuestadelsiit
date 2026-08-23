import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type ExtraescolarResponse = { culturales: string[]; deportivas: string[] };

function Catalogo({ titulo, items }: { titulo: string; items: string[] }) {
  return (
    <Card>
      <CardContent className="p-0">
        <div className="bg-gradient-guinda px-5 py-2.5 text-primary-foreground">
          <div className="text-xs font-semibold uppercase tracking-[0.16em]">{titulo}</div>
        </div>
        <div className="grid grid-cols-2 gap-px bg-border sm:grid-cols-4">
          {items.map((item) => (
            <button
              key={item}
              type="button"
              className="bg-card px-3 py-4 text-center text-xs font-medium text-primary transition hover:bg-primary-soft"
            >
              {item}
            </button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

export default function ExtraescolarPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["extraescolar"],
    queryFn: () => apiFetch<ExtraescolarResponse>("/extraescolar"),
  });

  return (
    <div className="mx-auto max-w-[1100px] space-y-6">
      <PageHeader title="Actividades extraescolares" subtitle="Selecciona una actividad cultural o deportiva para inscribirte" />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data ? (
        <>
          <Catalogo titulo="Actividades culturales" items={data.culturales} />
          <Catalogo titulo="Actividades deportivas" items={data.deportivas} />
        </>
      ) : null}
    </div>
  );
}
