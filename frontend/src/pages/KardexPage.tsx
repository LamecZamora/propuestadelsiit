import { useQuery } from "@tanstack/react-query";
import { Download, FileText } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type KardexMateria = {
  no: number;
  clave: string;
  nombre: string;
  creditos: number;
  final: number | null;
  estado: string;
  evaluacion: string | null;
  observaciones: string | null;
};
type KardexPeriodo = { periodo: string; promedio: number; creditos_cursados: number; creditos_aprobados: number; rows: KardexMateria[] };
type KardexResponse = {
  perfil: {
    nombre: string;
    numero_control: string;
    carrera: string;
    semestre: number;
    plan_estudios: string;
    reticula: number;
    especialidad: string;
  };
  periodos: KardexPeriodo[];
  resumen: { promedio_aritmetico: number; promedio_certificado: number; creditos_cursados: number; creditos_aprobados: number };
};

export default function KardexPage() {
  const { data, isLoading, error } = useQuery({ queryKey: ["kardex"], queryFn: () => apiFetch<KardexResponse>("/kardex") });

  const perfil = data?.perfil;
  const periodos = data?.periodos ?? [];
  const resumen = data?.resumen;

  return (
    <div className="mx-auto max-w-[1200px] space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <PageHeader title="Seguimiento del alumno" subtitle="Departamento de Servicios Escolares · Kardex" />
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" /> Descargar PDF
        </Button>
      </div>

      <Card className="overflow-hidden">
        <CardContent className="p-0">
          <div className="grid grid-cols-2 divide-x divide-y border-b sm:grid-cols-4">
            <Cell k="No. de control" v={perfil?.numero_control ?? "—"} />
            <Cell k="Nombre" v={perfil?.nombre ?? "—"} />
            <Cell k="Semestre" v={perfil ? `${perfil.semestre}º` : "—"} />
            <Cell k="Periodo escolar" v={periodos.at(-1)?.periodo ?? "—"} />
            <Cell k="Carrera" v={perfil?.carrera ?? "—"} />
            <Cell k="Retícula" v={perfil ? String(perfil.reticula) : "—"} />
            <Cell k="Especialidad" v={perfil?.especialidad ?? "—"} />
            <Cell k="Prom. acumulado" v={resumen ? resumen.promedio_certificado.toFixed(2) : "—"} />
          </div>
        </CardContent>
      </Card>

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando kardex…</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar kardex</CardContent></Card>
      ) : periodos.length === 0 ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Sin historial todavía.</CardContent></Card>
      ) : (
        <div className="space-y-5">
          {periodos.map((p) => (
            <Card key={p.periodo} className="overflow-hidden">
              <CardContent className="p-0">
                <div className="bg-gradient-guinda px-5 py-2.5 text-primary-foreground">
                  <div className="flex items-center justify-between text-xs font-semibold uppercase tracking-[0.16em]">
                    <span>{p.periodo}</span>
                    <span className="opacity-80">{p.rows.length} materias</span>
                  </div>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full min-w-[960px] text-sm">
                    <thead>
                      <tr className="bg-secondary/60 text-left text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                        <th className="px-4 py-2.5 w-10">No.</th>
                        <th className="px-4 py-2.5 w-24">Clave</th>
                        <th className="px-4 py-2.5">Materia</th>
                        <th className="px-4 py-2.5 w-16 text-center">Cred.</th>
                        <th className="px-4 py-2.5 w-24 text-center">Calif.</th>
                        <th className="px-4 py-2.5 w-28">Evaluación</th>
                        <th className="px-4 py-2.5 w-32">Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      {p.rows.map((r) => {
                        const reprobado = r.estado === "no_acreditada" || (r.final !== null && r.final < 70);
                        const display = r.final === null ? (r.estado === "no_acreditada" ? "NA" : "—") : r.final.toFixed(0);
                        return (
                          <tr key={`${p.periodo}-${r.clave}-${r.no}`} className="border-t hover:bg-secondary/30">
                            <td className="px-4 py-2.5 text-muted-foreground">{r.no}</td>
                            <td className="px-4 py-2.5 font-mono text-[12px]">{r.clave}</td>
                            <td className="px-4 py-2.5 font-medium">
                              {r.nombre}
                              {r.observaciones && (
                                <div className="text-[10px] font-normal uppercase tracking-[0.08em] text-warning">{r.observaciones}</div>
                              )}
                            </td>
                            <td className="px-4 py-2.5 text-center font-mono">{r.creditos}</td>
                            <td className={`px-4 py-2.5 text-center font-mono font-semibold ${reprobado ? "text-destructive" : ""}`}>{display}</td>
                            <td className="px-4 py-2.5 text-xs text-muted-foreground">{r.evaluacion ?? "—"}</td>
                            <td className="px-4 py-2.5 text-xs text-muted-foreground capitalize">{r.estado.replace(/_/g, " ")}</td>
                          </tr>
                        );
                      })}
                    </tbody>
                    <tfoot>
                      <tr className="border-t bg-primary-soft/60 text-xs">
                        <td colSpan={4} className="px-4 py-2 text-right font-semibold uppercase tracking-[0.14em] text-primary">Promedio del periodo</td>
                        <td className="px-4 py-2 text-center font-mono font-semibold">{p.promedio.toFixed(2)}</td>
                        <td className="px-4 py-2 text-right font-semibold uppercase tracking-[0.14em] text-primary">Cr. cur./apr.</td>
                        <td className="px-4 py-2 font-mono">{p.creditos_cursados} / {p.creditos_aprobados}</td>
                      </tr>
                    </tfoot>
                  </table>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {resumen && (
        <Card>
          <CardContent className="grid gap-4 p-6 md:grid-cols-4">
            <Stat label="Promedio aritmético" value={resumen.promedio_aritmetico.toFixed(2)} />
            <Stat label="Promedio certificado" value={resumen.promedio_certificado.toFixed(2)} highlight />
            <Stat label="Créditos cursados" value={String(resumen.creditos_cursados)} />
            <Stat label="Créditos aprobados" value={String(resumen.creditos_aprobados)} />
          </CardContent>
        </Card>
      )}

      <p className="flex items-center justify-center gap-2 text-center text-[11px] text-muted-foreground">
        <FileText className="h-3 w-3" />
        Este documento no es oficial y no es válido. No contiene sellos ni firmas oficiales de la institución.
      </p>
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

function Stat({ label, value, highlight }: { label: string; value: string; highlight?: boolean }) {
  return (
    <div className={`rounded-xl border p-4 ${highlight ? "bg-gradient-guinda text-primary-foreground" : "bg-card"}`}>
      <div className={`text-[10px] uppercase tracking-[0.18em] ${highlight ? "opacity-80" : "text-muted-foreground"}`}>{label}</div>
      <div className="mt-1 font-display text-2xl font-semibold">{value}</div>
    </div>
  );
}
