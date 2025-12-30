import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function DashboardHome() {
  return (
    <>
      <SEO title="Dashboard - SmartSpec Pro" description="SmartSpec Pro Dashboard" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">Dashboard (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
