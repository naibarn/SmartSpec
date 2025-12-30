import { useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { Loader2, Sparkles, CheckCircle } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';
import { FadeIn, SlideInLeft } from '@/components/Motion';
import { 
  forgotPasswordSchema, 
  resetPasswordSchema,
  type ForgotPasswordFormData,
  type ResetPasswordFormData 
} from '@/lib/validations';
import { apiService } from '@/services/api';

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  // Forgot Password Form
  const {
    register: registerForgot,
    handleSubmit: handleSubmitForgot,
    formState: { errors: errorsForgot },
  } = useForm<ForgotPasswordFormData>({
    resolver: zodResolver(forgotPasswordSchema),
  });

  // Reset Password Form
  const {
    register: registerReset,
    handleSubmit: handleSubmitReset,
    formState: { errors: errorsReset },
  } = useForm<ResetPasswordFormData>({
    resolver: zodResolver(resetPasswordSchema),
  });

  const onSubmitForgot = async (data: ForgotPasswordFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await apiService.forgotPassword(data.email);
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to send reset email. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const onSubmitReset = async (data: ResetPasswordFormData) => {
    if (!token) {
      setError('Invalid reset token');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await apiService.resetPassword(token, data.password);
      setSuccess(true);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to reset password. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <SEO
        title="Reset Password - SmartSpec Pro"
        description="Reset your SmartSpec Pro password"
      />

      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-muted/20 p-4">
        <div className="absolute top-4 right-4">
          <ThemeToggle />
        </div>

        <FadeIn>
          <Card className="w-full max-w-md">
            <CardHeader className="space-y-1">
              <div className="flex items-center justify-center mb-4">
                <Link to="/" className="flex items-center space-x-2">
                  <Sparkles className="h-8 w-8 text-primary" />
                  <span className="text-2xl font-bold">SmartSpec Pro</span>
                </Link>
              </div>
              <CardTitle className="text-2xl text-center">
                {token ? 'Reset your password' : 'Forgot password?'}
              </CardTitle>
              <CardDescription className="text-center">
                {token
                  ? 'Enter your new password below'
                  : "Enter your email and we'll send you a reset link"}
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* Success Message */}
              {success && (
                <SlideInLeft>
                  <div className="bg-green-500/10 text-green-600 dark:text-green-400 text-sm p-3 rounded-md flex items-center gap-2">
                    <CheckCircle className="h-4 w-4" />
                    <div>
                      {token
                        ? 'Password reset successfully! You can now sign in with your new password.'
                        : 'Reset link sent! Check your email for instructions.'}
                    </div>
                  </div>
                </SlideInLeft>
              )}

              {/* Error Message */}
              {error && (
                <SlideInLeft>
                  <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md">
                    {error}
                  </div>
                </SlideInLeft>
              )}

              {!success && !token && (
                /* Forgot Password Form */
                <form onSubmit={handleSubmitForgot(onSubmitForgot)} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      placeholder="name@example.com"
                      {...registerForgot('email')}
                      disabled={isLoading}
                    />
                    {errorsForgot.email && (
                      <p className="text-sm text-destructive">{errorsForgot.email.message}</p>
                    )}
                  </div>

                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Sending...
                      </>
                    ) : (
                      'Send reset link'
                    )}
                  </Button>
                </form>
              )}

              {!success && token && (
                /* Reset Password Form */
                <form onSubmit={handleSubmitReset(onSubmitReset)} className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="password">New Password</Label>
                    <Input
                      id="password"
                      type="password"
                      placeholder="••••••••"
                      {...registerReset('password')}
                      disabled={isLoading}
                    />
                    {errorsReset.password && (
                      <p className="text-sm text-destructive">{errorsReset.password.message}</p>
                    )}
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="confirmPassword">Confirm New Password</Label>
                    <Input
                      id="confirmPassword"
                      type="password"
                      placeholder="••••••••"
                      {...registerReset('confirmPassword')}
                      disabled={isLoading}
                    />
                    {errorsReset.confirmPassword && (
                      <p className="text-sm text-destructive">
                        {errorsReset.confirmPassword.message}
                      </p>
                    )}
                  </div>

                  <Button type="submit" className="w-full" disabled={isLoading}>
                    {isLoading ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                        Resetting...
                      </>
                    ) : (
                      'Reset password'
                    )}
                  </Button>
                </form>
              )}

              {success && (
                <div className="text-center">
                  <Link to="/login">
                    <Button className="w-full">Go to Sign In</Button>
                  </Link>
                </div>
              )}

              {!success && (
                <div className="text-center text-sm">
                  Remember your password?{' '}
                  <Link to="/login" className="text-primary hover:underline font-medium">
                    Sign in
                  </Link>
                </div>
              )}
            </CardContent>
          </Card>
        </FadeIn>
      </div>
    </>
  );
}
