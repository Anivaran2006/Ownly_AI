import Link from "next/link";
import { BarChart3, Boxes, Camera, Home, Settings, Shield, Tag, Users } from "lucide-react";

const nav = [
  { href: "/", label: "Dashboard", icon: Home },
  { href: "/scanner", label: "Scanner", icon: Camera },
  { href: "/products", label: "Products", icon: Boxes },
  { href: "/#warranties", label: "Warranties", icon: Shield },
  { href: "/#analytics", label: "Analytics", icon: BarChart3 },
  { href: "/#resale", label: "Resale", icon: Tag },
  { href: "/#family", label: "Family", icon: Users },
  { href: "/settings", label: "Settings", icon: Settings }
];

export function Sidebar() {
  return (
    <aside className="sticky top-0 hidden h-screen w-72 shrink-0 border-r bg-card/75 p-5 backdrop-blur-2xl lg:flex lg:flex-col">
      <Link href="/" className="flex items-center gap-3">
        <span className="grid size-11 place-items-center rounded-lg bg-gradient-to-br from-foreground to-primary text-background">
          <Boxes className="size-5" />
        </span>
        <span>
          <span className="block text-xl font-extrabold">Ownly</span>
          <span className="block text-xs text-muted-foreground">Own everything. Find anything.</span>
        </span>
      </Link>

      <nav className="mt-8 grid gap-1">
        {nav.map((item) => (
          <Link
            key={item.href + item.label}
            href={item.href}
            className="flex min-h-11 items-center gap-3 rounded-lg px-3 text-sm font-semibold text-muted-foreground transition hover:bg-muted hover:text-foreground"
          >
            <item.icon className="size-4" />
            {item.label}
          </Link>
        ))}
      </nav>

      <div className="mt-auto rounded-lg border bg-muted/60 p-4">
        <div className="flex items-center gap-2 text-sm font-semibold">
          <span className="size-2 rounded-full bg-primary shadow-[0_0_0_4px_hsl(var(--primary)/0.14)]" />
          Private vault active
        </div>
        <p className="mt-2 text-xs leading-5 text-muted-foreground">
          Documents are routed through encrypted storage and audit-ready access controls.
        </p>
      </div>
    </aside>
  );
}
