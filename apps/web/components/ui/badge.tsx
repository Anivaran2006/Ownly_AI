import * as React from "react";
import { cn } from "@/lib/utils";

type BadgeTone = "default" | "ok" | "warning" | "risk" | "info";

const tones: Record<BadgeTone, string> = {
  default: "bg-muted text-muted-foreground",
  ok: "bg-primary/15 text-primary",
  warning: "bg-warning/15 text-warning",
  risk: "bg-risk/15 text-risk",
  info: "bg-accent/15 text-accent"
};

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  tone?: BadgeTone;
}

export function Badge({ className, tone = "default", ...props }: BadgeProps) {
  return (
    <span
      className={cn("inline-flex min-h-8 items-center rounded-full px-3 text-xs font-bold", tones[tone], className)}
      {...props}
    />
  );
}

