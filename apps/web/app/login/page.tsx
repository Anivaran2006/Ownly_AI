import Link from "next/link";
import { Boxes, Lock, Mail, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";

export default function LoginPage() {
  return (
    <div className="mx-auto grid min-h-[calc(100vh-6rem)] max-w-6xl items-center gap-8 py-10 lg:grid-cols-[0.9fr_1.1fr]">
      <section>
        <div className="flex items-center gap-3">
          <span className="grid size-12 place-items-center rounded-lg bg-gradient-to-br from-foreground to-primary text-background">
            <Boxes className="size-5" />
          </span>
          <div>
            <strong className="block text-2xl">Ownly</strong>
            <span className="text-sm text-muted-foreground">Own everything. Find anything.</span>
          </div>
        </div>
        <h1 className="mt-8 text-4xl font-extrabold tracking-normal md:text-5xl">
          Your household inventory, protected and searchable.
        </h1>
        <p className="mt-4 max-w-xl text-base leading-7 text-muted-foreground">
          Upload invoices and receipts, then let Ownly create product profiles with warranty, return, manual, repair, and resale intelligence.
        </p>
        <div className="mt-6 grid gap-3 sm:grid-cols-3">
          {["Encrypted vault", "Family roles", "AI search"].map((label) => (
            <div key={label} className="rounded-lg border bg-card/80 p-4 text-sm font-semibold">
              <Shield className="mb-3 size-4 text-primary" />
              {label}
            </div>
          ))}
        </div>
      </section>

      <Card className="mx-auto w-full max-w-md">
        <CardHeader>
          <div>
            <p className="mb-1 text-xs font-bold uppercase text-primary">Welcome back</p>
            <CardTitle>Sign in to Ownly</CardTitle>
            <CardDescription>Use email today. Google OAuth hooks are ready in the API.</CardDescription>
          </div>
        </CardHeader>
        <form className="grid gap-4">
          <label className="grid gap-2 text-sm font-semibold">
            Email
            <span className="relative">
              <Mail className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input className="pl-10" type="email" defaultValue="demo@ownly.app" />
            </span>
          </label>
          <label className="grid gap-2 text-sm font-semibold">
            Password
            <span className="relative">
              <Lock className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
              <Input className="pl-10" type="password" placeholder="Enter your password" />
            </span>
          </label>
          <Button type="button">Continue</Button>
        </form>
        <p className="mt-5 text-sm text-muted-foreground">
          First run? Use the API seed helper from `app.services.seed` or register through `/v1/auth/register`.
        </p>
        <Link href="/" className="mt-4 inline-block text-sm font-bold text-primary">
          View dashboard
        </Link>
      </Card>
    </div>
  );
}
