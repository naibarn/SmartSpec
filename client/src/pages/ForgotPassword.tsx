/**
 * Forgot Password Page - SmartSpec Pro
 * Design: Ethereal Gradient Flow
 * - Glassmorphism cards with aurora gradients
 * - Soft shadows and backdrop blur
 */

import { useState } from 'react';
import { Link } from 'wouter';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { toast } from 'sonner';
import {
  Sparkles,
  Mail,
  ArrowLeft,
  CheckCircle,
  Loader2,
  KeyRound,
  Shield,
} from 'lucide-react';

type Step = 'email' | 'sent' | 'reset' | 'success';

export default function ForgotPassword() {
  const [step, setStep] = useState<Step>('email');
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendCode = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      toast.error('Please enter your email address');
      return;
    }

    setIsLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsLoading(false);
    setStep('sent');
    toast.success('Reset code sent to your email');
  };

  const handleVerifyCode = async (e: React.FormEvent) => {
    e.preventDefault();
    if (code.length !== 6) {
      toast.error('Please enter a valid 6-digit code');
      return;
    }

    setIsLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    setIsLoading(false);
    setStep('reset');
  };

  const handleResetPassword = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (newPassword.length < 8) {
      toast.error('Password must be at least 8 characters');
      return;
    }
    
    if (newPassword !== confirmPassword) {
      toast.error('Passwords do not match');
      return;
    }

    setIsLoading(true);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setIsLoading(false);
    setStep('success');
    toast.success('Password reset successfully!');
  };

  return (
    <div className="min-h-screen flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden bg-gradient-to-br from-purple-600 via-pink-500 to-orange-400">
        {/* Animated Background */}
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-white/20 rounded-full blur-3xl animate-pulse" />
          <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-300/30 rounded-full blur-3xl animate-pulse delay-1000" />
        </div>

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center px-12 text-white">
          <Link href="/" className="flex items-center gap-3 mb-12">
            <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Sparkles className="w-6 h-6" />
            </div>
            <span className="text-2xl font-bold">SmartSpec Pro</span>
          </Link>

          <h1 className="text-4xl font-bold mb-6">
            Secure Account Recovery
          </h1>
          <p className="text-xl text-white/80 mb-8">
            We'll help you get back into your account safely and securely.
          </p>

          <div className="space-y-4">
            {[
              { icon: Mail, text: 'Receive a verification code via email' },
              { icon: KeyRound, text: 'Create a new secure password' },
              { icon: Shield, text: 'Your account stays protected' },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.2 }}
                className="flex items-center gap-3"
              >
                <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
                  <item.icon className="w-5 h-5" />
                </div>
                <span className="text-white/90">{item.text}</span>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Grid Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="h-full w-full" style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '50px 50px'
          }} />
        </div>
      </div>

      {/* Right Side - Form */}
      <div className="flex-1 flex items-center justify-center p-8 bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          {/* Mobile Logo */}
          <Link href="/" className="flex items-center gap-3 mb-8 lg:hidden">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">SmartSpec Pro</span>
          </Link>

          {/* Progress Steps */}
          <div className="flex items-center justify-center gap-2 mb-8">
            {['email', 'sent', 'reset', 'success'].map((s, index) => (
              <div key={s} className="flex items-center">
                <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-all ${
                  step === s 
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white' 
                    : ['email', 'sent', 'reset', 'success'].indexOf(step) > index
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-200 text-gray-500'
                }`}>
                  {['email', 'sent', 'reset', 'success'].indexOf(step) > index ? (
                    <CheckCircle className="w-4 h-4" />
                  ) : (
                    index + 1
                  )}
                </div>
                {index < 3 && (
                  <div className={`w-8 h-0.5 ${
                    ['email', 'sent', 'reset', 'success'].indexOf(step) > index
                      ? 'bg-green-500'
                      : 'bg-gray-200'
                  }`} />
                )}
              </div>
            ))}
          </div>

          {/* Form Card */}
          <div className="bg-white/70 backdrop-blur-xl rounded-3xl border border-white/50 shadow-xl shadow-purple-500/10 p-8">
            <AnimatePresence mode="wait">
              {/* Step 1: Enter Email */}
              {step === 'email' && (
                <motion.div
                  key="email"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Forgot your password?
                  </h2>
                  <p className="text-gray-600 mb-6">
                    No worries! Enter your email and we'll send you a reset code.
                  </p>

                  <form onSubmit={handleSendCode} className="space-y-4">
                    <div>
                      <Label htmlFor="email" className="text-gray-700">Email Address</Label>
                      <div className="relative mt-1">
                        <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="email"
                          type="email"
                          placeholder="you@example.com"
                          value={email}
                          onChange={(e) => setEmail(e.target.value)}
                          className="pl-10 h-12 bg-white/50 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                        />
                      </div>
                    </div>

                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full h-12 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Sending...
                        </>
                      ) : (
                        'Send Reset Code'
                      )}
                    </Button>
                  </form>

                  <div className="mt-6 text-center">
                    <Link href="/login" className="text-purple-600 hover:text-purple-700 font-medium inline-flex items-center gap-1">
                      <ArrowLeft className="w-4 h-4" />
                      Back to Sign In
                    </Link>
                  </div>
                </motion.div>
              )}

              {/* Step 2: Enter Code */}
              {step === 'sent' && (
                <motion.div
                  key="sent"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-100 to-pink-100 flex items-center justify-center mx-auto mb-6">
                    <Mail className="w-8 h-8 text-purple-600" />
                  </div>

                  <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">
                    Check your email
                  </h2>
                  <p className="text-gray-600 mb-6 text-center">
                    We sent a 6-digit code to<br />
                    <span className="font-medium text-gray-900">{email}</span>
                  </p>

                  <form onSubmit={handleVerifyCode} className="space-y-4">
                    <div>
                      <Label htmlFor="code" className="text-gray-700">Verification Code</Label>
                      <Input
                        id="code"
                        type="text"
                        placeholder="000000"
                        value={code}
                        onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                        className="h-12 text-center text-2xl tracking-widest bg-white/50 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                        maxLength={6}
                      />
                    </div>

                    <Button
                      type="submit"
                      disabled={isLoading || code.length !== 6}
                      className="w-full h-12 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Verifying...
                        </>
                      ) : (
                        'Verify Code'
                      )}
                    </Button>
                  </form>

                  <div className="mt-6 text-center">
                    <button
                      onClick={() => setStep('email')}
                      className="text-gray-500 hover:text-gray-700 text-sm"
                    >
                      Didn't receive the code? <span className="text-purple-600 font-medium">Resend</span>
                    </button>
                  </div>
                </motion.div>
              )}

              {/* Step 3: Reset Password */}
              {step === 'reset' && (
                <motion.div
                  key="reset"
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                >
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Create new password
                  </h2>
                  <p className="text-gray-600 mb-6">
                    Your new password must be at least 8 characters long.
                  </p>

                  <form onSubmit={handleResetPassword} className="space-y-4">
                    <div>
                      <Label htmlFor="newPassword" className="text-gray-700">New Password</Label>
                      <div className="relative mt-1">
                        <KeyRound className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="newPassword"
                          type="password"
                          placeholder="••••••••"
                          value={newPassword}
                          onChange={(e) => setNewPassword(e.target.value)}
                          className="pl-10 h-12 bg-white/50 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                        />
                      </div>
                    </div>

                    <div>
                      <Label htmlFor="confirmPassword" className="text-gray-700">Confirm Password</Label>
                      <div className="relative mt-1">
                        <KeyRound className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                        <Input
                          id="confirmPassword"
                          type="password"
                          placeholder="••••••••"
                          value={confirmPassword}
                          onChange={(e) => setConfirmPassword(e.target.value)}
                          className="pl-10 h-12 bg-white/50 border-gray-200 focus:border-purple-500 focus:ring-purple-500"
                        />
                      </div>
                    </div>

                    {/* Password Strength Indicator */}
                    <div className="space-y-2">
                      <div className="flex gap-1">
                        {[1, 2, 3, 4].map((level) => (
                          <div
                            key={level}
                            className={`h-1 flex-1 rounded-full ${
                              newPassword.length >= level * 3
                                ? level <= 2
                                  ? 'bg-red-500'
                                  : level === 3
                                  ? 'bg-yellow-500'
                                  : 'bg-green-500'
                                : 'bg-gray-200'
                            }`}
                          />
                        ))}
                      </div>
                      <p className="text-xs text-gray-500">
                        {newPassword.length === 0
                          ? 'Enter a password'
                          : newPassword.length < 6
                          ? 'Too weak'
                          : newPassword.length < 9
                          ? 'Could be stronger'
                          : newPassword.length < 12
                          ? 'Good password'
                          : 'Strong password'}
                      </p>
                    </div>

                    <Button
                      type="submit"
                      disabled={isLoading}
                      className="w-full h-12 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium"
                    >
                      {isLoading ? (
                        <>
                          <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                          Resetting...
                        </>
                      ) : (
                        'Reset Password'
                      )}
                    </Button>
                  </form>
                </motion.div>
              )}

              {/* Step 4: Success */}
              {step === 'success' && (
                <motion.div
                  key="success"
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="text-center py-4"
                >
                  <div className="w-20 h-20 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center mx-auto mb-6">
                    <CheckCircle className="w-10 h-10 text-white" />
                  </div>

                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Password Reset!
                  </h2>
                  <p className="text-gray-600 mb-8">
                    Your password has been successfully reset. You can now sign in with your new password.
                  </p>

                  <Link href="/login">
                    <Button className="w-full h-12 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white font-medium">
                      Sign In Now
                    </Button>
                  </Link>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
