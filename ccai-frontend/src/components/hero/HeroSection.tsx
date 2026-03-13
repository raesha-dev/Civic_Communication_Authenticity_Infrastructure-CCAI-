"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import Link from "next/link";
import { ArrowRight, ShieldCheck, Activity } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function HeroSection() {
  const { t } = useTranslation();
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end start"],
  });

  const y = useTransform(scrollYProgress, [0, 1], ["0%", "50%"]);
  const opacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <div
      ref={containerRef}
      className="relative min-h-screen flex items-center justify-center overflow-hidden bg-brand-navy dark:bg-black pt-20"
    >
      {/* Background animated elements */}
      <motion.div
        style={{ y, opacity }}
        className="absolute inset-0 pointer-events-none"
      >
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/20 rounded-full blur-[128px]" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-cyan-600/20 rounded-full blur-[128px]" />
      </motion.div>

      <div className="container relative z-10 px-6 py-32 mx-auto text-center flex flex-col items-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-panel text-white/90 text-sm font-medium mb-8"
        >
          <ShieldCheck className="w-4 h-4 text-green-400" />
          <span>{t("hero.badge", "Government Grade Authenticity Scoring")}</span>
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.2, ease: "easeOut" }}
          className="text-5xl md:text-7xl lg:text-8xl font-bold tracking-tighter text-white mb-6 max-w-5xl leading-tight"
        >
          {t("hero.title_start", "Verify Before You ")} <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">{t("hero.title_highlight", "Trust.")}</span>
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4, ease: "easeOut" }}
          className="text-lg md:text-xl text-white/70 max-w-2xl mb-12"
        >
          {t("hero.subtitle", "Protect yourself from misinformation and phishing. CCAI provides transparent, explainable AI verification for official government communications via SMS, Email, and Web.")}
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6, ease: "easeOut" }}
          className="flex flex-col sm:flex-row items-center gap-4"
        >
          <Link
            href="/verify"
            className="px-8 py-4 rounded-full bg-white text-black font-semibold flex items-center gap-2 hover:bg-gray-100 transition-transform active:scale-95"
          >
            {t("hero.btn_verify", "Verify a Message")} <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/dashboard"
            className="px-8 py-4 rounded-full glass-panel text-white font-semibold flex items-center gap-2 hover:bg-white/10 transition-transform active:scale-95"
          >
            <Activity className="w-4 h-4" /> {t("hero.btn_dashboard", "View Transparency")}
          </Link>
        </motion.div>
      </div>

      {/* Decorative lines / elements */}
      <div className="absolute bottom-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-white/20 to-transparent" />
    </div>
  );
}
