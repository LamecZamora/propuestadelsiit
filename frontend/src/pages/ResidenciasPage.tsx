import { useQuery } from "@tanstack/react-query";
import { Building2 } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type ResidenciaResponse = {
  tiene_residencia: boolean;
  empresa: string | null;
  puesto: string | null;
  fecha_inicio: string | null;
  fecha_fin: string | null;
  estado: string | null;
};

export default function ResidenciasPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["residencias"],
    queryFn: () => apiFetch<ResidenciaResponse>("/residencias"),
  });

  return (
    <div className="mx-auto max-w-[700px] space-y-6">
      <PageHeader title="Residencia profesional" />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data && !data.tiene_residencia ? (
        <Card>
          <CardContent className="flex flex-col items-center gap-3 py-16 text-center">
            <div className="grid h-12 w-12 place-items-center rounded-2xl bg-primary-soft text-primary">
              <Building2 className="h-5 w-5" />
            </div>
            <p className="font-medium">No tiene Residencia Registrada</p>
          </CardContent>
        </Card>
      ) : data ? (
        <Card>
          <CardContent className="grid gap-4 p-6 sm:grid-cols-2">
            <Cell k="Empresa" v={data.empresa ?? "—"} />
            <Cell k="Puesto" v={data.puesto ?? "—"} />
            <Cell k="Fecha de inicio" v={data.fecha_inicio ?? "—"} />
            <Cell k="Fecha de fin" v={data.fecha_fin ?? "—"} />
            <Cell k="Estado" v={data.estado ?? "—"} />
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}

function Cell({ k, v }: { k: string; v: string }) {
  return (
    <div>
      <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">{k}</div>
      <div className="mt-1 text-sm font-medium">{v}</div>
    </div>
  );
}
