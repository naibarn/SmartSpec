import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function AnalyticsPage() {
  return (
    <>
      <SEO title="AnalyticsPage - SmartSpec Pro" description="SmartSpec Pro AnalyticsPage" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">AnalyticsPage (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
