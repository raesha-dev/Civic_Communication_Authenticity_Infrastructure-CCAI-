import HeroSection from "@/components/hero/HeroSection";
import ScrollStory from "@/components/hero/ScrollStory";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      <HeroSection />
      <ScrollStory />
    </div>
  );
}
