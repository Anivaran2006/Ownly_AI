import { Card } from "@/components/ui/card";

interface KpiCardProps {
  label: string;
  value: string;
  helper: string;
  tone?: "default" | "attention";
}

export function KpiCard({ label, value, helper, tone = "default" }: KpiCardProps) {
  return (
    <Card className={tone === "attention" ? "bg-warning/10" : undefined}>
      <p className="text-sm font-semibold text-muted-foreground">{label}</p>
      <strong className="mt-4 block text-3xl tracking-normal">{value}</strong>
      <span className="mt-3 block text-sm text-muted-foreground">{helper}</span>
    </Card>
  );
}

