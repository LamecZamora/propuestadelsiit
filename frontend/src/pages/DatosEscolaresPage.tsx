import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { ApiError, apiFetch } from "@/lib/api-client";

type DatosEscolaresResponse = {
  numero_control: string;
  apellido_paterno: string;
  apellido_materno: string;
  nombre_pila: string;
  lugar_nacimiento: string;
  fecha_nacimiento: string;
  sexo: string;
  estado_civil: string;
  discapacidad: string;
  domicilio: string;
  colonia: string;
  codigo_postal: string;
  ciudad: string;
  entidad_federativa: string;
  telefono: string | null;
  curp: string;
  correo_personal: string;
  carrera: string;
  reticula: number;
  semestre: number;
  becado_por: string | null;
  materias_examen_especial: string | null;
  grado_academico: string;
  promedio_semestre_anterior: number;
  ingreso_mensual: number;
  integrantes_hogar: number;
  grupo_etnico: boolean;
  riesgo_abandono: string;
  nombre_padre: string | null;
  domicilio_padre: string | null;
  colonia_padre: string | null;
  ciudad_padre: string | null;
  entidad_padre: string | null;
  telefono_padre: string | null;
  nombre_madre: string | null;
  domicilio_madre: string | null;
  colonia_madre: string | null;
  ciudad_madre: string | null;
  entidad_madre: string | null;
  telefono_madre: string | null;
  empresa_nombre: string | null;
  empresa_domicilio: string | null;
  empresa_colonia: string | null;
  empresa_ciudad: string | null;
  empresa_entidad: string | null;
  empresa_telefono: string | null;
  puesto: string | null;
  antiguedad: string | null;
  jefe_inmediato: string | null;
  turno: string;
};

function Seccion({ titulo, children }: { titulo: string; children: React.ReactNode }) {
  return (
    <Card className="overflow-hidden">
      <CardContent className="p-0">
        <div className="bg-gradient-guinda px-5 py-2.5 text-primary-foreground">
          <div className="text-xs font-semibold uppercase tracking-[0.16em]">{titulo}</div>
        </div>
        <div className="grid grid-cols-2 divide-x divide-y sm:grid-cols-4">{children}</div>
      </CardContent>
    </Card>
  );
}

function Campo({ k, v }: { k: string; v: string | number | null }) {
  return (
    <div className="px-4 py-3">
      <div className="text-[10px] uppercase tracking-[0.14em] text-muted-foreground">{k}</div>
      <div className="mt-1 text-sm font-medium">{v === null || v === "" ? "—" : v}</div>
    </div>
  );
}

export default function DatosEscolaresPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["datos-escolares"],
    queryFn: () => apiFetch<DatosEscolaresResponse>("/datos"),
  });

  const sinDatos = error instanceof ApiError && error.status === 404;

  return (
    <div className="mx-auto max-w-[1100px] space-y-6">
      <PageHeader title="Datos Generales del Alumno" />

      {isLoading ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">Cargando…</CardContent></Card>
      ) : sinDatos ? (
        <Card><CardContent className="p-10 text-center text-sm text-muted-foreground">No hay datos escolares capturados todavía.</CardContent></Card>
      ) : error ? (
        <Card><CardContent className="p-10 text-center text-sm text-destructive">Error al cargar</CardContent></Card>
      ) : data ? (
        <>
          <Seccion titulo="Datos generales">
            <Campo k="Apellido paterno" v={data.apellido_paterno} />
            <Campo k="Apellido materno" v={data.apellido_materno} />
            <Campo k="Nombre" v={data.nombre_pila} />
            <Campo k="No. de control" v={data.numero_control} />
            <Campo k="Lugar de nacimiento" v={data.lugar_nacimiento} />
            <Campo k="Fecha de nacimiento" v={data.fecha_nacimiento} />
            <Campo k="Sexo" v={data.sexo} />
            <Campo k="Estado civil" v={data.estado_civil} />
            <Campo k="Discapacidad" v={data.discapacidad} />
            <Campo k="Domicilio actual" v={data.domicilio} />
            <Campo k="Colonia" v={data.colonia} />
            <Campo k="Código postal" v={data.codigo_postal} />
            <Campo k="Ciudad o localidad" v={data.ciudad} />
            <Campo k="Entidad federativa" v={data.entidad_federativa} />
            <Campo k="Teléfono" v={data.telefono} />
            <Campo k="CURP" v={data.curp} />
            <Campo k="Correo electrónico" v={data.correo_personal} />
          </Seccion>

          <Seccion titulo="Datos escolares">
            <Campo k="Carrera y retícula" v={`${data.carrera} (Ret-${data.reticula})`} />
            <Campo k="Semestre" v={data.semestre} />
            <Campo k="Becado por" v={data.becado_por} />
            <Campo k="Materia(s) en ex. especial" v={data.materias_examen_especial} />
            <Campo k="Grado académico" v={data.grado_academico} />
            <Campo k="Promedio semestre anterior" v={data.promedio_semestre_anterior.toFixed(2)} />
          </Seccion>

          <Seccion titulo="Datos socioeconómicos">
            <Campo k="Ingreso mensual" v={`$${data.ingreso_mensual.toFixed(0)}`} />
            <Campo k="Integrantes del hogar" v={data.integrantes_hogar} />
            <Campo k="Grupo étnico o afrodescendiente" v={data.grupo_etnico ? "Sí" : "No"} />
            <Campo k="Riesgo de abandono" v={data.riesgo_abandono} />
          </Seccion>

          <Seccion titulo="Datos familiares — Padre">
            <Campo k="Nombre" v={data.nombre_padre} />
            <Campo k="Domicilio" v={data.domicilio_padre} />
            <Campo k="Colonia" v={data.colonia_padre} />
            <Campo k="Ciudad" v={data.ciudad_padre} />
            <Campo k="Entidad federativa" v={data.entidad_padre} />
            <Campo k="Teléfono" v={data.telefono_padre} />
          </Seccion>

          <Seccion titulo="Datos familiares — Madre">
            <Campo k="Nombre" v={data.nombre_madre} />
            <Campo k="Domicilio" v={data.domicilio_madre} />
            <Campo k="Colonia" v={data.colonia_madre} />
            <Campo k="Ciudad" v={data.ciudad_madre} />
            <Campo k="Entidad federativa" v={data.entidad_madre} />
            <Campo k="Teléfono" v={data.telefono_madre} />
          </Seccion>

          <Seccion titulo="Datos del trabajo del alumno">
            <Campo k="Nombre de la empresa" v={data.empresa_nombre} />
            <Campo k="Domicilio" v={data.empresa_domicilio} />
            <Campo k="Colonia" v={data.empresa_colonia} />
            <Campo k="Ciudad" v={data.empresa_ciudad} />
            <Campo k="Entidad federativa" v={data.empresa_entidad} />
            <Campo k="Teléfono" v={data.empresa_telefono} />
            <Campo k="Puesto que ocupa" v={data.puesto} />
            <Campo k="Antigüedad" v={data.antiguedad} />
            <Campo k="Jefe inmediato superior" v={data.jefe_inmediato} />
            <Campo k="Turno" v={data.turno} />
          </Seccion>
        </>
      ) : null}
    </div>
  );
}
