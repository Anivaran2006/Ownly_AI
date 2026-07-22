import type { Metadata } from "next";
import "./globals.css";
import { Sidebar } from "@/components/dashboard/sidebar";
import { Topbar } from "@/components/dashboard/topbar";

export const metadata: Metadata = {
  title: "Ownly",
  description: "Own everything. Find anything."
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>
        <div className="flex min-h-screen">
          <Sidebar />
          <main className="min-w-0 flex-1 px-4 pb-10 md:px-8">
            <Topbar />
            {children}
          </main>
        </div>
      </body>
    </html>
  );
}

