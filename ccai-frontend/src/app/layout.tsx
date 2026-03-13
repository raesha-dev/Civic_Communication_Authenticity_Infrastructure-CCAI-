import type { Metadata } from "next";
import "./globals.css";
import { ThemeProvider } from "next-themes";
import NavBar from "@/components/layout/NavBar";
import "@/i18n/config";

export const metadata: Metadata = {
  title: "CCAI - Verify Before You Trust",
  description: "Civic Communication Authenticity Infrastructure (CCAI). Verify the authenticity of digital communications with explainable AI scoring.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="antialiased bg-background text-foreground min-h-screen flex flex-col">
        <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
          <NavBar />
          <main className="flex-1 w-full">{children}</main>
        </ThemeProvider>
      </body>
    </html>
  );
}
