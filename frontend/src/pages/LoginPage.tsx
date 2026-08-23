import { ArrowRight, CalendarDays, ClipboardList, GraduationCap, Loader2, ShieldCheck, Sparkles, Wifi } from "lucide-react";
import { type FormEvent, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { toast } from "sonner";

import { useAuth } from "@/auth/AuthContext";
import { SiitLogo } from "@/components/SiitLogo";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ApiError } from "@/lib/api-client";

const featurettes = [
  { icon: ClipboardList, label: "Calificaciones" },
  { icon: CalendarDays, label: "Horario" },
  { icon: GraduationCap, label: "Kardex" },
  { icon: Wifi, label: "Cuenta internet" },
];

export default function LoginPage() {
  const { isAuthenticated, login } = useAuth();
  const navigate = useNavigate();
  const [matricula, setMatricula] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  if (isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    try {
      await login(matricula, password);
      toast.success("Bienvenido");
      navigate("/dashboard");
    } catch (error) {
      if (error instanceof ApiError && error.status === 401) {
        toast.error("Número de control o contraseña incorrectos");
      } else {
        toast.error("No se pudo conectar con el servidor. Intenta de nuevo.");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b bg-background/70 backdrop-blur">
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <SiitLogo />
          <a
            href="https://www.itdurango.edu.mx"
            className="hidden text-xs font-medium uppercase tracking-[0.16em] text-primary md:inline-flex items-center gap-1"
          >
            ITD.edu.mx <ArrowRight className="h-3 w-3" />
          </a>
        </div>
      </header>

      <section className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0 -z-10">
          <div className="absolute -top-32 -right-24 h-[520px] w-[520px] rounded-full bg-primary-soft blur-3xl opacity-70" />
          <div className="absolute top-40 -left-32 h-[400px] w-[400px] rounded-full bg-accent blur-3xl opacity-60" />
        </div>

        <div className="mx-auto grid max-w-7xl items-center gap-12 px-6 py-16 lg:grid-cols-[1.05fr_1fr] lg:py-24">
          <div>
            <div className="inline-flex items-center gap-2 rounded-full border bg-card px-3 py-1 text-xs font-medium text-muted-foreground shadow-card">
              <Sparkles className="h-3.5 w-3.5 text-primary" />
              Nueva experiencia 2026 · TecNM
            </div>
            <h1 className="mt-5 font-display text-5xl font-semibold leading-[1.05] tracking-tight md:text-6xl">
              Tu vida académica,
              <br />
              <span className="text-primary">por fin, en un solo lugar.</span>
            </h1>
            <p className="mt-5 max-w-xl text-base text-muted-foreground md:text-lg">
              El Sistema Integral de Información del Instituto Tecnológico de Durango — rediseñado.
            </p>

            <div className="mt-8 grid grid-cols-2 gap-3 sm:grid-cols-4">
              {featurettes.map((f) => (
                <div key={f.label} className="flex flex-col items-start gap-2 rounded-2xl border bg-card p-4 shadow-card">
                  <div className="grid h-9 w-9 place-items-center rounded-lg bg-primary-soft text-primary">
                    <f.icon className="h-4 w-4" />
                  </div>
                  <div className="text-sm font-medium">{f.label}</div>
                </div>
              ))}
            </div>

            <div className="mt-10 flex items-center gap-2 text-xs text-muted-foreground">
              <ShieldCheck className="h-4 w-4 text-success" />
              Sesión con JWT propio · sin proveedores externos
            </div>
          </div>

          <div className="lg:justify-self-end w-full max-w-md">
            <div className="rounded-3xl border bg-card p-2 shadow-elegant">
              <div className="rounded-2xl bg-gradient-soft p-6">
                <h2 className="font-display text-2xl font-semibold">Iniciar sesión</h2>
                <p className="mt-1 text-sm text-muted-foreground">Ingresa con tu número de control y contraseña.</p>

                <form onSubmit={handleSubmit} className="mt-6 space-y-4">
                  <div className="space-y-1.5">
                    <Label htmlFor="matricula" className="text-xs uppercase tracking-[0.14em] text-muted-foreground">
                      No. de control
                    </Label>
                    <Input
                      id="matricula"
                      value={matricula}
                      onChange={(e) => setMatricula(e.target.value)}
                      className="h-11"
                      placeholder="22040251"
                      autoComplete="username"
                      required
                    />
                  </div>

                  <div className="space-y-1.5">
                    <Label htmlFor="password" className="text-xs uppercase tracking-[0.14em] text-muted-foreground">
                      Contraseña
                    </Label>
                    <Input
                      id="password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      type="password"
                      className="h-11"
                      placeholder="••••••••"
                      autoComplete="current-password"
                      required
                    />
                  </div>

                  <Button type="submit" disabled={loading} className="h-11 w-full bg-gradient-guinda text-primary-foreground hover:opacity-95">
                    {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <>Entrar al portal <ArrowRight className="ml-1 h-4 w-4" /></>}
                  </Button>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="mx-auto max-w-7xl px-6 py-10 text-xs text-muted-foreground">
        © {new Date().getFullYear()} Instituto Tecnológico de Durango · Tecnológico Nacional de México
      </footer>
    </div>
  );
}
