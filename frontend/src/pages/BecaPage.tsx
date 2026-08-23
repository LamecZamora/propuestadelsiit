import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, XCircle } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type BecaResponse = {
  numero_control: string;
  nombre: string;
  semestre: number;
  periodo: string;
  promedio_acumulado: number;
  carrera: string;
  especialidad: string;
  curp: string;
  beca_pronabes: boolean;
};

export default function BecaPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["beca"], queryFn: () => apiFetch<BecaResponse>("/beca") });

  return (
    <div className="mx-auto max-w-[900px] space-y-6">
      <PageHeader title="Modificación de datos CURP y la elección de beca" subtitle="Verifica el CURP" />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data ? (
        <Card className="overflow-hidden">
          <CardContent className="p-0">
            <div className="grid grid-cols-2 divide-x divide-y border-b sm:grid-cols-4">
              <Cell k="No. Control S.E.P." v={data.numero_control} />
              <Cell k="Nombre del Alumno" v={data.nombre} />
              <Cell k="Semestre" v={String(data.semestre)} />
              <Cell k="Periodo Escolar" v={data.periodo} />
              <Cell k="Carrera" v={data.carrera} />
              <Cell k="Especialidad" v={data.especialidad} />
              <Cell k="Prom. Acum." v={data.promedio_acumulado.toFixed(2)} />
            </div>
            <div className="grid gap-4 p-6 sm:grid-cols-2">
              <div>
                <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">CURP</div>
                <div className="mt-1 rounded-md border bg-secondary/40 px-3 py-2 font-mono text-sm">{data.curp}</div>
              </div>
              <div>
                <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">Opción para Beca PRONABES</div>
                <div className="mt-1 flex items-center gap-2 rounded-md border bg-secondary/40 px-3 py-2 text-sm font-medium">
                  {data.beca_pronabes ? (
                    <>
                      <CheckCircle2 className="h-4 w-4 text-success" /> Sí
                    </>
                  ) : (
                    <>
                      <XCircle className="h-4 w-4 text-muted-foreground" /> No
                    </>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ) : null}
    </div>
  );
}

function Cell({ k, v }: { k: string; v: string }) {
  return (
    <div className="px-5 py-3">
      <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">{k}</div>
      <div className="mt-1 text-sm font-medium truncate">{v}</div>
    </div>
  );
}
