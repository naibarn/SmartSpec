import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function FeaturesPage() {
  return (
    <>
      <SEO
        title="Features - SmartSpec Pro"
        description="Explore SmartSpec Pro features"
      />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">Features Page (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
