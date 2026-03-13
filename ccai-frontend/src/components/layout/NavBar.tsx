"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { ShieldCheck, Menu, X, Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { cn } from "@/lib/utils";
import { useTranslation } from "react-i18next";

export default function NavBar() {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenu, setMobileMenu] = useState(false);
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);
  const pathname = usePathname();
  const { t, i18n } = useTranslation();

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => setMounted(true));
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const navLinks = [
    { name: t("nav.verify", "Verify"), path: "/verify" },
    { name: t("nav.dashboard", "Dashboard"), path: "/dashboard" },
    { name: t("nav.methodology", "Methodology"), path: "/methodology" },
    { name: t("nav.appeals", "Appeals"), path: "/appeals" },
    { name: t("nav.registry", "Registry"), path: "/registry" },
  ];

  return (
    <header
      className={cn(
        "fixed top-0 w-full z-50 transition-all duration-300",
        scrolled ? "glass-panel shadow-sm py-3" : "bg-transparent py-5"
      )}
    >
      <div className="container mx-auto px-6 lg:px-12 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 group">
          <ShieldCheck className="w-8 h-8 text-blue-500 group-hover:text-blue-400 transition-colors" />
          <span className="font-bold text-xl tracking-tight hidden sm:block">CCAI</span>
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.path}
              className={cn(
                "text-sm font-medium transition-colors hover:text-blue-500",
                pathname === link.path ? "text-blue-500" : "text-foreground/80"
              )}
            >
              {link.name}
            </Link>
          ))}
          
          <div className="flex items-center gap-2 border-l border-foreground/10 pl-4">
            {mounted && (
              <button
                onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
                className="p-2 rounded-full hover:bg-foreground/5 transition-colors"
                aria-label="Toggle Theme"
              >
                {theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
              </button>
            )}
            
            {mounted && (
              <select 
                className="bg-transparent text-sm border-none outline-none cursor-pointer"
                value={i18n.language}
                onChange={(e) => i18n.changeLanguage(e.target.value)}
              >
                <option value="en">EN</option>
                <option value="es">ES</option>
                <option value="fr">FR</option>
                <option value="hi">HI</option>
              </select>
            )}
          </div>
        </nav>

        {/* Mobile menu toggle */}
        <button
          className="md:hidden p-2 rounded-md hover:bg-foreground/5"
          onClick={() => setMobileMenu(!mobileMenu)}
          aria-label="Toggle Menu"
        >
          {mobileMenu ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile Nav */}
      <div
        className={cn(
          "md:hidden absolute top-full left-0 w-full bg-background border-b border-foreground/10 transition-all duration-300 overflow-hidden",
          mobileMenu ? "max-h-96 py-4" : "max-h-0"
        )}
      >
        <div className="flex flex-col px-6 gap-4">
          {navLinks.map((link) => (
            <Link
              key={link.name}
              href={link.path}
              onClick={() => setMobileMenu(false)}
              className="text-base font-medium py-2 hover:text-blue-500"
            >
              {link.name}
            </Link>
          ))}
        </div>
      </div>
    </header>
  );
}
