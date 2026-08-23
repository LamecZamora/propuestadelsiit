import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type AvanceCelda = { clave: string; nombre: string; estado: string; calificacion_display: string | null };
type AvanceColumna = { semestre: number; materias: AvanceCelda[] };
type AvanceResponse = {
  perfil: {
    nombre: string;
    numero_control: string;
    carrera: string;
    semestre: number;
    reticula: number;
    especialidad: string;
    promedio_acumulado: number;
  };
  columnas: AvanceColumna[];
};

const ESTILOS_ESTADO: Record<string, string> = {
  acreditada: "border-success/30 bg-success/10 text-success",
  cursando: "border-primary/30 bg-primary-soft text-primary",
  cursando_sin_acreditar: "border-warning/40 bg-warning/15 text-warning-foreground",
  curso_especial: "border-destructive/30 bg-destructive/10 text-destructive",
  curso_especial_reprobado: "border-destructive/40 bg-destructive/15 text-destructive",
  examen_especial: "border-warning/40 bg-warning/15 text-warning-foreground",
  examen_especial_reprobado: "border-destructive/40 bg-destructive/15 text-destructive",
  posible_seleccionar: "border-dashed border-border bg-secondary/60 text-muted-foreground",
  no_permitida: "border-dashed border-border bg-muted text-muted-foreground/60",
};

const ETIQUETAS_ESTADO: Record<string, string> = {
  acreditada: "Acreditada",
  cursando: "Cursando",
  cursando_sin_acreditar: "Cursada sin acreditar · prioridad",
  curso_especial: "A curso especial",
  curso_especial_reprobado: "Cur. esp. reprobado",
  examen_especial: "A examen especial",
  examen_especial_reprobado: "Ex. esp. reprobado",
  posible_seleccionar: "Materia posible si requisitos OK",
  no_permitida: "No permitida hasta avance",
};

export default function AvancePage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["avance"], queryFn: () => apiFetch<AvanceResponse>("/avance") });

  const perfil = data?.perfil;
  const columnas = data?.columnas ?? [];

  return (
    <div className="mx-auto max-w-[1400px] space-y-6">
      <PageHeader title="Avance reticular" subtitle="Retícula del plan de estudios y estado de cada materia" />

      <Card className="overflow-hidden">
        <CardContent className="p-0">
          <div className="grid grid-cols-2 divide-x divide-y border-b sm:grid-cols-4">
            <Cell k="No. de control" v={perfil?.numero_control ?? "—"} />
            <Cell k="Nombre" v={perfil?.nombre ?? "—"} />
            <Cell k="Semestre" v={perfil ? `${perfil.semestre}º` : "—"} />
            <Cell k="Prom. acumulado" v={perfil ? perfil.promedio_acumulado.toFixed(2) : "—"} />
            <Cell k="Carrera" v={perfil?.carrera ?? "—"} />
            <Cell k="Retícula" v={perfil ? String(perfil.reticula) : "—"} />
            <Cell k="Especialidad" v={perfil?.especialidad ?? "—"} />
          </div>
        </CardContent>
      </Card>

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando avance reticular…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar avance reticular</CardContent></Card>
      ) : columnas.length === 0 ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Sin datos de retícula todavía.</CardContent></Card>
      ) : (
        <div className="overflow-x-auto pb-2">
          <div className="grid grid-flow-col auto-cols-[180px] gap-3">
            {columnas.map((columna) => (
              <div key={columna.semestre} className="space-y-2">
                <div className="rounded-lg bg-gradient-guinda px-3 py-2 text-center text-xs font-semibold uppercase tracking-[0.12em] text-primary-foreground">
                  Semestre {columna.semestre}
                </div>
                {columna.materias.map((materia) => (
                  <div
                    key={materia.clave}
                    className={`rounded-lg border p-2.5 text-xs leading-tight ${ESTILOS_ESTADO[materia.estado] ?? "border-border bg-card"}`}
                    title={ETIQUETAS_ESTADO[materia.estado] ?? materia.estado}
                  >
                    <div className="font-mono text-[10px] opacity-70">{materia.clave}</div>
                    <div className="font-medium">{materia.nombre}</div>
                    {materia.calificacion_display && <div className="mt-1 font-mono text-[11px]">{materia.calificacion_display}</div>}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      )}

      <Card>
        <CardContent className="flex flex-wrap gap-3 p-4">
          {Object.entries(ETIQUETAS_ESTADO).map(([estado, etiqueta]) => (
            <div key={estado} className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
              <span className={`h-3 w-3 rounded border ${ESTILOS_ESTADO[estado]}`} />
              {etiqueta}
            </div>
          ))}
        </CardContent>
      </Card>
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
