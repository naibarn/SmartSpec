import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function DashboardLayout() {
  return (
    <>
      <SEO title="DashboardLayout - SmartSpec Pro" description="SmartSpec Pro DashboardLayout" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">DashboardLayout (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
