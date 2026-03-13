"use client";

import { useRef } from "react";
import { motion, useScroll } from "framer-motion";
import { ShieldAlert, Fingerprint, Activity, CheckCircle } from "lucide-react";
import clsx from "clsx";

const features = [
  {
    title: "Fake Messages Context",
    description: "Every day, millions of malicious messages are sent trying to scam citizens out of valuable information. CCAI blocks out the noise.",
    icon: ShieldAlert,
    color: "text-red-500",
    bgIcon: "bg-red-500/10",
  },
  {
    title: "Institution Impersonation Check",
    description: "Fraudsters spoof sender IDs. We use cryptographic checks and domain validation to ensure the sender is authentic.",
    icon: Fingerprint,
    color: "text-blue-500",
    bgIcon: "bg-blue-500/10",
  },
  {
    title: "Deep Fraud Signals",
    description: "Our AI evaluates semantic similarity and known attack patterns, uncovering sophisticated social engineering attempts.",
    icon: Activity,
    color: "text-purple-500",
    bgIcon: "bg-purple-500/10",
  },
  {
    title: "Transparent Scoring",
    description: "Every message is given an explainable 1-5 Authenticity Score, built on clear attributes like domain history and ML probability.",
    icon: CheckCircle,
    color: "text-green-500",
    bgIcon: "bg-green-500/10",
  },
];

export default function ScrollStory() {
  const containerRef = useRef<HTMLDivElement>(null);
  useScroll({
    target: containerRef,
    offset: ["start end", "end start"],
  });

  return (
    <div ref={containerRef} className="relative py-32 bg-background overflow-hidden">
      <div className="container mx-auto px-6 lg:px-12">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.8 }}
          className="text-center mb-24 relative z-10"
        >
          <h2 className="text-4xl md:text-6xl font-bold mb-6 tracking-tight">Understanding the Threat</h2>
          <p className="text-xl text-foreground/70 max-w-3xl mx-auto">
            Discover how CCAI identifies malicious communication to protect your digital identity.
          </p>
        </motion.div>

        <div className="relative z-10 space-y-32">
          {features.map((feature, idx) => {
            const isEven = idx % 2 === 0;
            return (
              <FeatureBlock
                key={idx}
                feature={feature}
                isEven={isEven}
                index={idx}
              />
            );
          })}
        </div>
      </div>
    </div>
  );
}

type Feature = (typeof features)[number];

function FeatureBlock({
  feature,
  isEven,
  index,
}: {
  feature: Feature;
  isEven: boolean;
  index: number;
}) {
  const Icon = feature.icon;

  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-100px" }}
      transition={{ duration: 0.8, ease: "easeOut" }}
      className={clsx(
        "flex flex-col md:flex-row items-center gap-12 lg:gap-24",
        isEven ? "" : "md:flex-row-reverse"
      )}
    >
      <div className="w-full md:w-1/2">
        <div className="glass-panel p-8 rounded-3xl overflow-hidden relative group">
          <div className="absolute inset-0 bg-gradient-to-br from-foreground/5 to-transparent opacity-50 transition-opacity group-hover:opacity-100" />
          <div
            className={clsx(
              "w-20 h-20 rounded-2xl flex items-center justify-center mb-6",
              feature.bgIcon
            )}
          >
            <Icon className={clsx("w-10 h-10", feature.color)} />
          </div>
          <h3 className="text-3xl font-bold mb-4">{feature.title}</h3>
          <p className="text-lg text-foreground/70 leading-relaxed">
            {feature.description}
          </p>
        </div>
      </div>
      
      <div className="w-full md:w-1/2 flex justify-center">
        {/* Abstract animated graphic */}
        <div className="relative w-64 h-64 lg:w-80 lg:h-80">
          <motion.div
            animate={{
              scale: [1, 1.05, 1],
              rotate: [0, 5, -5, 0],
            }}
            transition={{
              duration: 10 + index * 2,
              repeat: Infinity,
              ease: "linear"
            }}
            className={clsx(
              "absolute inset-0 rounded-full opacity-20 blur-3xl",
              feature.bgIcon
            )}
          />
          <div className="absolute inset-4 rounded-3xl border border-foreground/10 glass-panel flex items-center justify-center shadow-lg transform rotate-3 transition-transform hover:rotate-0 hover:scale-105 duration-500">
             <Icon className={clsx("w-24 h-24 opacity-80", feature.color)} />
          </div>
        </div>
      </div>
    </motion.div>
  );
}
