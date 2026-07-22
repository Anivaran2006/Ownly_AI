"use client";

import { Bell, Camera, Search } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function Topbar() {
  const [query, setQuery] = useState("");

  return (
    <header className="sticky top-0 z-20 flex flex-col gap-3 bg-background/90 py-4 backdrop-blur-xl md:flex-row md:items-center">
      <form
        className="relative flex-1"
        onSubmit={(event) => {
          event.preventDefault();
          if (query.trim()) {
            window.location.href = `/products?q=${encodeURIComponent(query.trim())}`;
          }
        }}
      >
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          className="pl-10"
          placeholder="Find my laptop invoice, warranties expiring next month..."
          aria-label="Search Ownly"
        />
      </form>
      <div className="flex items-center gap-2">
        <Button variant="secondary" onClick={() => (window.location.href = "/scanner")}>
          <Camera className="size-4" />
          Scan
        </Button>
        <button
          type="button"
          aria-label="Notifications"
          className="relative grid size-10 place-items-center rounded-lg border bg-card transition hover:bg-muted"
        >
          <Bell className="size-4" />
          <span className="absolute right-2 top-2 size-2 rounded-full bg-primary" />
        </button>
        <Link
          href="/#family"
          className="grid size-10 place-items-center rounded-lg bg-gradient-to-br from-accent to-primary text-sm font-extrabold text-white"
          aria-label="Open profile"
        >
          AM
        </Link>
      </div>
    </header>
  );
}
