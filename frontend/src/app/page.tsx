// Initial home landing page scaffold showcasing brand tokens and development state
import Link from "next/link";
import { ShieldCheck, MessageCircle, Sparkles, ArrowRight } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col justify-between p-6 md:p-12 max-w-7xl mx-auto">
      {/* Brand Header */}
      <header className="flex items-center justify-between py-4 border-b border-white/10">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-gold-600 to-gold-400 flex items-center justify-center font-display font-black text-pitch-950 text-base">
            A
          </div>
          <span className="font-display font-bold tracking-widest text-lg uppercase text-offwhite-50">
            Apex<span className="text-gold-400">Pitch</span>
          </span>
        </div>
        <div className="flex items-center gap-6 text-sm text-offwhite-300">
          <span className="hidden sm:inline-flex items-center gap-1.5 text-xs uppercase tracking-wider text-gold-400 font-semibold bg-gold-400/10 px-3 py-1 rounded-full border border-gold-400/20">
            <Sparkles className="w-3.5 h-3.5" /> Phase 0 Scaffolding Ready
          </span>
          <Link
            href="/admin"
            className="text-xs uppercase tracking-wider text-offwhite-400 hover:text-gold-400 transition-colors"
          >
            Admin Portal
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <div className="my-auto py-16 text-center space-y-6">
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-pitch-800 border border-white/10 text-xs font-medium text-gold-400 tracking-wide uppercase">
          Elite Footwear & Official Kits
        </div>
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-display font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
          Precision Boots. <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-gold-300 via-gold-400 to-amber-500">
            Legendary Jerseys.
          </span>
        </h1>
        <p className="max-w-2xl mx-auto text-offwhite-300 text-base sm:text-lg">
          Browse professional-grade boots & match-edition jerseys. Instant sizing consultation
          and direct ordering over WhatsApp.
        </p>

        <div className="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://wa.me/1234567890"
            target="_blank"
            rel="noopener noreferrer"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-gold-400 hover:bg-gold-300 text-pitch-950 font-semibold transition-all duration-200 shadow-glow hover:scale-[1.02]"
          >
            <MessageCircle className="w-5 h-5 fill-pitch-950" />
            Contact On WhatsApp
          </a>
          <Link
            href="/catalogue"
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-pitch-800 hover:bg-pitch-700 text-offwhite-100 font-semibold border border-white/10 transition-colors"
          >
            Browse Catalogue
            <ArrowRight className="w-4 h-4 text-gold-400" />
          </Link>
        </div>
      </div>

      {/* Trust Badges */}
      <footer className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-12 border-t border-white/10 text-xs text-offwhite-400">
        <div className="flex items-center gap-3 p-4 rounded-lg bg-pitch-800/40 border border-white/5">
          <ShieldCheck className="w-5 h-5 text-gold-400 shrink-0" />
          <div>
            <div className="font-semibold text-offwhite-200">100% Authentic Gear</div>
            <div>Direct source player-issue and stadium editions</div>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4 rounded-lg bg-pitch-800/40 border border-white/5">
          <MessageCircle className="w-5 h-5 text-gold-400 shrink-0" />
          <div>
            <div className="font-semibold text-offwhite-200">Direct WhatsApp Ordering</div>
            <div>Zero friction, instant stock check, personalized sizing</div>
          </div>
        </div>
        <div className="flex items-center gap-3 p-4 rounded-lg bg-pitch-800/40 border border-white/5">
          <Sparkles className="w-5 h-5 text-gold-400 shrink-0" />
          <div>
            <div className="font-semibold text-offwhite-200">Global Ground Types</div>
            <div>FG, AG, SG, TF, and Indoor Court studs in stock</div>
          </div>
        </div>
      </footer>
    </main>
  );
}
