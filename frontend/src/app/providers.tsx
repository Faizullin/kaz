"use client";

import { ThemeProvider } from "next-themes";
import { UserProvider } from "@/lib/auth/provider";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" enableSystem={false} defaultTheme="dark">
      <UserProvider>{children}</UserProvider>
    </ThemeProvider>
  );
}
