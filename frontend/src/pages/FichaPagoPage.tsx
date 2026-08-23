import { useQuery } from "@tanstack/react-query";
import { Printer } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ApiError, apiFetch } from "@/lib/api-client";

type FichaPagoResponse = {
  numero_control: string;
  nombre: string;
  carrera: string;
  periodo: string;
  concepto: string;
  monto: number;
  referencia_bancaria: string;
  fecha_vencimiento: string;
};

export default function FichaPagoPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["ficha-pago"],
    queryFn: () => apiFetch<FichaPagoResponse>("/ficha-pago"),
  });

  const sinFicha = error instanceof ApiError && error.status === 404;

  return (
    <div className="mx-auto max-w-[700px] space-y-6">
      <PageHeader title="Ficha de Depósito" subtitle="Departamento de Recursos Financieros" />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : sinFicha ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">No hay ficha de depósito generada para este periodo.</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data ? (
        <Card className="overflow-hidden">
          <CardContent className="p-0">
            <div className="grid grid-cols-2 divide-x divide-y border-b">
              <Cell k="No. de Control" v={data.numero_control} />
              <Cell k="Nombre" v={data.nombre} />
              <Cell k="Concepto" v={data.concepto} />
              <Cell k="Periodo" v={data.periodo} />
              <Cell k="Monto a pagar" v={`$${data.monto.toFixed(2)}`} destacado />
              <Cell k="Fecha de vencimiento" v={data.fecha_vencimiento} />
            </div>
            <div className="p-5">
              <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">Referencia bancaria (Banorte)</div>
              <div className="mt-1 font-mono text-sm">{data.referencia_bancaria}</div>
            </div>
          </CardContent>
        </Card>
      ) : null}

      {data && (
        <Button variant="outline" size="sm">
          <Printer className="mr-2 h-4 w-4" /> Imprimir ficha
        </Button>
      )}

      <p className="text-[11px] text-muted-foreground">
        Imprime dos copias y acude a cualquier sucursal Banorte donde podrás realizar tu pago. Verifica tu monto a pagar; si existiera algún
        problema, acude al Centro de Cómputo.
      </p>
    </div>
  );
}

function Cell({ k, v, destacado }: { k: string; v: string; destacado?: boolean }) {
  return (
    <div className="px-5 py-3">
      <div className="text-[10px] uppercase tracking-[0.16em] text-muted-foreground">{k}</div>
      <div className={`mt-1 text-sm font-medium ${destacado ? "text-lg font-semibold text-primary" : ""}`}>{v}</div>
    </div>
  );
}
