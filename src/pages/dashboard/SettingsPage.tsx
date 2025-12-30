import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function SettingsPage() {
  return (
    <>
      <SEO title="SettingsPage - SmartSpec Pro" description="SmartSpec Pro SettingsPage" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">SettingsPage (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
