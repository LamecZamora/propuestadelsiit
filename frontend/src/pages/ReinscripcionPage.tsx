import { useQuery } from "@tanstack/react-query";
import { CheckCircle2, XCircle } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type ReinscripcionResponse = {
  nombre: string;
  periodo: string;
  fecha: string | null;
  hora: string | null;
  mensaje_adicional: string | null;
  autorizado: boolean;
  adeudo_biblioteca: boolean;
  adeudo_escolares: boolean;
  adeudo_financieros: boolean;
  adeudo_encuesta: boolean;
};

function Adeudo({ label, tiene }: { label: string; tiene: boolean }) {
  return (
    <div className="flex flex-col items-center gap-1 rounded-lg border bg-card p-3">
      <span className="text-[10px] uppercase tracking-[0.14em] text-muted-foreground">{label}</span>
      {tiene ? (
        <span className="flex items-center gap-1 text-sm font-semibold text-destructive">
          <XCircle className="h-4 w-4" /> S
        </span>
      ) : (
        <span className="flex items-center gap-1 text-sm font-semibold text-success">
          <CheckCircle2 className="h-4 w-4" /> N
        </span>
      )}
    </div>
  );
}

export default function ReinscripcionPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["reinscripcion"],
    queryFn: () => apiFetch<ReinscripcionResponse>("/reinscripcion"),
  });

  return (
    <div className="mx-auto max-w-[900px] space-y-6">
      <PageHeader title="Horario de Reinscripción" subtitle={data ? `Periodo ${data.periodo}` : undefined} />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data ? (
        <>
          <Card className="overflow-hidden">
            <CardContent className="p-0">
              <div className="grid grid-cols-2 divide-x divide-y border-b sm:grid-cols-4">
                <Cell k="Nombre" v={data.nombre} />
                <Cell k="Fecha" v={data.fecha ?? "—"} />
                <Cell k="Hora" v={data.hora ?? "—"} />
                <Cell k="Autorizado" v={data.autorizado ? "Sí" : "No"} />
              </div>
              <div className="grid grid-cols-2 gap-3 p-4 sm:grid-cols-4">
                <Adeudo label="Biblioteca" tiene={data.adeudo_biblioteca} />
                <Adeudo label="Escolares" tiene={data.adeudo_escolares} />
                <Adeudo label="Financieros" tiene={data.adeudo_financieros} />
                <Adeudo label="Encuesta" tiene={data.adeudo_encuesta} />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="space-y-3 p-6 text-sm">
              <h2 className="font-display text-base font-semibold">Información importante</h2>
              <p className="text-primary">Ya tienes todo lo necesario para reinscribirte, espera tu hora y fecha asignada.</p>
              <ul className="list-inside list-[lower-alpha] space-y-1.5 text-muted-foreground">
                <li>Realiza tu pago oportunamente.</li>
                <li>No contar con adeudos de ningún tipo (S=Sí y N=No). En caso de contar con alguno, debes liquidarlos antes de las fechas de reinscripciones.</li>
                <li>Si adeuda escolar es &quot;S&quot;, significa que tienes dos especiales o especial reprobado o aprobaste solo 2 materias o menos en tu primer semestre.</li>
                <li>Deberás revisar la validación de pago 48 horas antes de tu fecha de reinscripción.</li>
              </ul>
            </CardContent>
          </Card>
        </>
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
