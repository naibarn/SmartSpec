import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams, useParams } from 'react-router-dom';
import { Loader2, Sparkles, XCircle } from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { SEO } from '@/components/SEO';
import { FadeIn } from '@/components/Motion';
import { apiService } from '@/services/api';

export default function OAuthCallbackPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { provider } = useParams<{ provider: string }>();
  const [error, setError] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(true);

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code');
      const errorParam = searchParams.get('error');

      if (errorParam) {
        setError(`OAuth error: ${errorParam}`);
        setIsProcessing(false);
        return;
      }

      if (!code) {
        setError('No authorization code received');
        setIsProcessing(false);
        return;
      }

      if (!provider || !['google', 'github'].includes(provider)) {
        setError('Invalid OAuth provider');
        setIsProcessing(false);
        return;
      }

      try {
        let response;
        
        if (provider === 'google') {
          response = await apiService.handleGoogleCallback(code);
        } else if (provider === 'github') {
          response = await apiService.handleGithubCallback(code);
        }

        if (response) {
          // Store token
          localStorage.setItem('access_token', response.access_token);
          
          // Redirect to dashboard
          navigate('/dashboard');
        }
      } catch (err: any) {
        console.error('OAuth callback error:', err);
        setError(
          err.response?.data?.detail || 
          `Failed to complete ${provider} authentication. Please try again.`
        );
        setIsProcessing(false);
      }
    };

    handleCallback();
  }, [searchParams, provider, navigate]);

  return (
    <>
      <SEO
        title="OAuth Callback - SmartSpec Pro"
        description="Completing authentication..."
      />

      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-muted/20 p-4">
        <FadeIn>
          <Card className="w-full max-w-md">
            <CardHeader className="space-y-1">
              <div className="flex items-center justify-center mb-4">
                <Sparkles className="h-8 w-8 text-primary" />
              </div>
              <CardTitle className="text-2xl text-center">
                {isProcessing ? 'Completing sign in...' : 'Authentication Failed'}
              </CardTitle>
              <CardDescription className="text-center">
                {isProcessing
                  ? `Authenticating with ${provider}...`
                  : 'There was a problem signing you in'}
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              {isProcessing ? (
                <div className="flex items-center justify-center py-8">
                  <Loader2 className="h-12 w-12 animate-spin text-primary" />
                </div>
              ) : (
                <>
                  <div className="bg-destructive/10 text-destructive text-sm p-4 rounded-md flex items-start gap-3">
                    <XCircle className="h-5 w-5 flex-shrink-0 mt-0.5" />
                    <div>{error}</div>
                  </div>

                  <div className="space-y-2">
                    <Button
                      onClick={() => navigate('/login')}
                      className="w-full"
                    >
                      Back to Sign In
                    </Button>
                    <Button
                      onClick={() => navigate('/')}
                      variant="outline"
                      className="w-full"
                    >
                      Go to Home
                    </Button>
                  </div>
                </>
              )}
            </CardContent>
          </Card>
        </FadeIn>
      </div>
    </>
  );
}
