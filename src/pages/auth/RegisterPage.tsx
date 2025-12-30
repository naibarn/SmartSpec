import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { FcGoogle } from 'react-icons/fc';
import { FaGithub } from 'react-icons/fa';
import { Loader2, Sparkles, CheckCircle2 } from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';
import { FadeIn, SlideInLeft } from '@/components/Motion';
import { registerSchema, type RegisterFormData } from '@/lib/validations';
import { useAuth } from '@/contexts/AuthContext';
import { apiService } from '@/services/api';

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const password = watch('password');

  const onSubmit = async (data: RegisterFormData) => {
    setIsLoading(true);
    setError(null);

    try {
      await registerUser({
        email: data.email,
        password: data.password,
        full_name: data.full_name,
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGoogleSignup = async () => {
    try {
      const { authorization_url } = await apiService.getGoogleAuthUrl();
      window.location.href = authorization_url;
    } catch (err) {
      setError('Failed to initiate Google signup');
    }
  };

  const handleGithubSignup = async () => {
    try {
      const { authorization_url } = await apiService.getGithubAuthUrl();
      window.location.href = authorization_url;
    } catch (err) {
      setError('Failed to initiate GitHub signup');
    }
  };

  // Password strength indicators
  const passwordStrength = {
    length: password?.length >= 8,
    uppercase: /[A-Z]/.test(password || ''),
    lowercase: /[a-z]/.test(password || ''),
    number: /\d/.test(password || ''),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password || ''),
  };

  return (
    <>
      <SEO
        title="Sign Up - SmartSpec Pro"
        description="Create your SmartSpec Pro account"
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
              <CardTitle className="text-2xl text-center">Create an account</CardTitle>
              <CardDescription className="text-center">
                Get started with SmartSpec Pro today
              </CardDescription>
            </CardHeader>

            <CardContent className="space-y-4">
              {/* OAuth Buttons */}
              <div className="grid grid-cols-2 gap-4">
                <Button
                  variant="outline"
                  onClick={handleGoogleSignup}
                  disabled={isLoading}
                  className="w-full"
                >
                  <FcGoogle className="mr-2 h-5 w-5" />
                  Google
                </Button>
                <Button
                  variant="outline"
                  onClick={handleGithubSignup}
                  disabled={isLoading}
                  className="w-full"
                >
                  <FaGithub className="mr-2 h-5 w-5" />
                  GitHub
                </Button>
              </div>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">
                    Or continue with email
                  </span>
                </div>
              </div>

              {/* Error Message */}
              {error && (
                <SlideInLeft>
                  <div className="bg-destructive/10 text-destructive text-sm p-3 rounded-md">
                    {error}
                  </div>
                </SlideInLeft>
              )}

              {/* Register Form */}
              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="full_name">Full Name</Label>
                  <Input
                    id="full_name"
                    type="text"
                    placeholder="John Doe"
                    {...register('full_name')}
                    disabled={isLoading}
                  />
                  {errors.full_name && (
                    <p className="text-sm text-destructive">{errors.full_name.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Input
                    id="email"
                    type="email"
                    placeholder="name@example.com"
                    {...register('email')}
                    disabled={isLoading}
                  />
                  {errors.email && (
                    <p className="text-sm text-destructive">{errors.email.message}</p>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <Input
                    id="password"
                    type="password"
                    placeholder="••••••••"
                    {...register('password')}
                    disabled={isLoading}
                  />
                  {errors.password && (
                    <p className="text-sm text-destructive">{errors.password.message}</p>
                  )}

                  {/* Password Strength Indicators */}
                  {password && (
                    <div className="space-y-1 text-xs">
                      <div className="flex items-center gap-2">
                        <CheckCircle2
                          className={`h-3 w-3 ${
                            passwordStrength.length ? 'text-green-500' : 'text-muted-foreground'
                          }`}
                        />
                        <span>At least 8 characters</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2
                          className={`h-3 w-3 ${
                            passwordStrength.uppercase ? 'text-green-500' : 'text-muted-foreground'
                          }`}
                        />
                        <span>One uppercase letter</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2
                          className={`h-3 w-3 ${
                            passwordStrength.lowercase ? 'text-green-500' : 'text-muted-foreground'
                          }`}
                        />
                        <span>One lowercase letter</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2
                          className={`h-3 w-3 ${
                            passwordStrength.number ? 'text-green-500' : 'text-muted-foreground'
                          }`}
                        />
                        <span>One number</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <CheckCircle2
                          className={`h-3 w-3 ${
                            passwordStrength.special ? 'text-green-500' : 'text-muted-foreground'
                          }`}
                        />
                        <span>One special character</span>
                      </div>
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  <Label htmlFor="confirmPassword">Confirm Password</Label>
                  <Input
                    id="confirmPassword"
                    type="password"
                    placeholder="••••••••"
                    {...register('confirmPassword')}
                    disabled={isLoading}
                  />
                  {errors.confirmPassword && (
                    <p className="text-sm text-destructive">{errors.confirmPassword.message}</p>
                  )}
                </div>

                <Button type="submit" className="w-full" disabled={isLoading}>
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Creating account...
                    </>
                  ) : (
                    'Create account'
                  )}
                </Button>
              </form>

              <div className="text-center text-sm">
                Already have an account?{' '}
                <Link to="/login" className="text-primary hover:underline font-medium">
                  Sign in
                </Link>
              </div>
            </CardContent>
          </Card>
        </FadeIn>
      </div>
    </>
  );
}
