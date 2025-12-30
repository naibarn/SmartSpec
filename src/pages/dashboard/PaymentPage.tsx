import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function PaymentPage() {
  return (
    <>
      <SEO title="PaymentPage - SmartSpec Pro" description="SmartSpec Pro PaymentPage" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">PaymentPage (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
