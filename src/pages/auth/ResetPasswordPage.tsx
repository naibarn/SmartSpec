import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function ResetPasswordPage() {
  return (
    <>
      <SEO title="Reset Password - SmartSpec Pro" description="Reset your password" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">Reset Password (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
