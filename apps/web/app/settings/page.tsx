import { KeyRound, Lock, Server, ShieldCheck } from "lucide-react";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const settings = [
  ["End-to-end document vault", "On", Lock],
  ["Multi-factor authentication", "Ready", ShieldCheck],
  ["Audit logs", "180 days", Server],
  ["AI document consent", "Ask each time", KeyRound]
] as const;

export default function SettingsPage() {
  return (
    <div>
      <section className="mb-5">
        <p className="mb-1 text-xs font-bold uppercase text-primary">Controls</p>
        <h1 className="text-3xl font-extrabold tracking-normal md:text-4xl">Security and integrations</h1>
      </section>

      <section className="grid gap-3 xl:grid-cols-2">
        <Card>
          <CardHeader>
            <div>
              <CardTitle>Security posture</CardTitle>
              <CardDescription>Ownly defaults to encrypted storage, short-lived sessions, and audit-ready access.</CardDescription>
            </div>
          </CardHeader>
          <div className="grid gap-2">
            {settings.map(([label, value, Icon]) => (
              <div key={label} className="grid grid-cols-[2.5rem_1fr_auto] items-center gap-3 rounded-lg border bg-muted/70 p-3">
                <span className="grid size-10 place-items-center rounded-lg bg-primary/15 text-primary">
                  <Icon className="size-4" />
                </span>
                <strong className="text-sm">{label}</strong>
                <span className="text-sm font-bold text-muted-foreground">{value}</span>
              </div>
            ))}
          </div>
        </Card>

        <Card>
          <CardHeader>
            <div>
              <CardTitle>Roadmap integrations</CardTitle>
              <CardDescription>Email, marketplace, drive, bank, QR, barcode, and mobile capture adapters are intentionally isolated.</CardDescription>
            </div>
          </CardHeader>
          <div className="grid gap-2 text-sm font-semibold">
            {["Gmail invoice detection", "Amazon import", "Flipkart import", "Google Drive import", "Bank transaction matching"].map((label) => (
              <div key={label} className="rounded-lg border bg-muted/70 p-4">{label}</div>
            ))}
          </div>
        </Card>
      </section>
    </div>
  );
}

