import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';

export default function LoginPage() {
  return (
    <>
      <SEO title="Login - SmartSpec Pro" description="Sign in to SmartSpec Pro" />
      <FadeIn>
        <div className="min-h-screen flex items-center justify-center">
          <h1 className="text-4xl font-bold">Login Page (Coming Soon)</h1>
        </div>
      </FadeIn>
    </>
  );
}
