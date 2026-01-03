/**
 * Email Verification Page - SmartSpec Pro
 * Verify user email after signup
 */

import { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'wouter';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import {
  Mail,
  CheckCircle2,
  XCircle,
  RefreshCw,
  ArrowRight,
  Sparkles,
  Clock,
  Shield,
} from 'lucide-react';

type VerificationStatus = 'pending' | 'verifying' | 'success' | 'error' | 'expired';

export default function VerifyEmail() {
  const [, setLocation] = useLocation();
  const [status, setStatus] = useState<VerificationStatus>('pending');
  const [email, setEmail] = useState('user@example.com');
  const [code, setCode] = useState(['', '', '', '', '', '']);
  const [isResending, setIsResending] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Get email from URL params or session
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const emailParam = params.get('email');
    if (emailParam) {
      setEmail(emailParam);
    }
    
    // Auto-verify if token is in URL
    const token = params.get('token');
    if (token) {
      verifyWithToken(token);
    }
  }, []);

  // Countdown timer for resend
  useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const verifyWithToken = async (token: string) => {
    setStatus('verifying');
    
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));
    
    // For demo, randomly succeed or fail
    if (Math.random() > 0.2) {
      setStatus('success');
      toast.success('Email verified successfully!');
      setTimeout(() => setLocation('/dashboard'), 2000);
    } else {
      setStatus('expired');
      toast.error('Verification link has expired');
    }
  };

  const handleCodeChange = (index: number, value: string) => {
    if (value.length > 1) {
      // Handle paste
      const chars = value.slice(0, 6).split('');
      const newCode = [...code];
      chars.forEach((char, i) => {
        if (index + i < 6) {
          newCode[index + i] = char;
        }
      });
      setCode(newCode);
      const nextIndex = Math.min(index + chars.length, 5);
      inputRefs.current[nextIndex]?.focus();
    } else {
      const newCode = [...code];
      newCode[index] = value;
      setCode(newCode);
      
      // Auto-focus next input
      if (value && index < 5) {
        inputRefs.current[index + 1]?.focus();
      }
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent) => {
    if (e.key === 'Backspace' && !code[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handleVerifyCode = async () => {
    const fullCode = code.join('');
    if (fullCode.length !== 6) {
      toast.error('Please enter the complete 6-digit code');
      return;
    }

    setStatus('verifying');
    
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));
    
    // For demo, check if code is "123456"
    if (fullCode === '123456') {
      setStatus('success');
      toast.success('Email verified successfully!');
      setTimeout(() => setLocation('/dashboard'), 2000);
    } else {
      setStatus('error');
      toast.error('Invalid verification code');
      setCode(['', '', '', '', '', '']);
      inputRefs.current[0]?.focus();
    }
  };

  const handleResendCode = async () => {
    setIsResending(true);
    
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1000));
    
    setIsResending(false);
    setCountdown(60);
    setStatus('pending');
    setCode(['', '', '', '', '', '']);
    toast.success('Verification code sent! Check your inbox.');
  };

  const renderContent = () => {
    switch (status) {
      case 'success':
        return (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center"
          >
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center">
              <CheckCircle2 className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Email Verified!</h2>
            <p className="text-gray-600 mb-6">
              Your email has been successfully verified. Redirecting to dashboard...
            </p>
            <div className="flex justify-center">
              <RefreshCw className="w-5 h-5 text-purple-600 animate-spin" />
            </div>
          </motion.div>
        );

      case 'error':
      case 'expired':
        return (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="text-center"
          >
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-red-400 to-rose-500 flex items-center justify-center">
              <XCircle className="w-10 h-10 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              {status === 'expired' ? 'Link Expired' : 'Verification Failed'}
            </h2>
            <p className="text-gray-600 mb-6">
              {status === 'expired' 
                ? 'This verification link has expired. Please request a new one.'
                : 'The verification code you entered is incorrect. Please try again.'}
            </p>
            <Button
              onClick={handleResendCode}
              disabled={isResending || countdown > 0}
              className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700"
            >
              {isResending ? (
                <>
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                  Sending...
                </>
              ) : countdown > 0 ? (
                `Resend in ${countdown}s`
              ) : (
                <>
                  <Mail className="w-4 h-4 mr-2" />
                  Send New Code
                </>
              )}
            </Button>
          </motion.div>
        );

      case 'verifying':
        return (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-center"
          >
            <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-purple-400 to-pink-500 flex items-center justify-center">
              <RefreshCw className="w-10 h-10 text-white animate-spin" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Verifying...</h2>
            <p className="text-gray-600">Please wait while we verify your email.</p>
          </motion.div>
        );

      default:
        return (
          <>
            {/* Icon */}
            <div className="w-16 h-16 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Mail className="w-8 h-8 text-white" />
            </div>

            {/* Title */}
            <h2 className="text-2xl font-bold text-gray-900 mb-2 text-center">
              Verify Your Email
            </h2>
            <p className="text-gray-600 text-center mb-2">
              We've sent a 6-digit code to
            </p>
            <p className="text-purple-600 font-medium text-center mb-8">
              {email}
            </p>

            {/* Code Input */}
            <div className="flex justify-center gap-2 mb-6">
              {code.map((digit, index) => (
                <input
                  key={index}
                  ref={(el) => { inputRefs.current[index] = el; }}
                  type="text"
                  inputMode="numeric"
                  maxLength={6}
                  value={digit}
                  onChange={(e) => handleCodeChange(index, e.target.value.replace(/\D/g, ''))}
                  onKeyDown={(e) => handleKeyDown(index, e)}
                  className="w-12 h-14 text-center text-2xl font-bold border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-2 focus:ring-purple-200 outline-none transition-all"
                />
              ))}
            </div>

            {/* Verify Button */}
            <Button
              onClick={handleVerifyCode}
              disabled={code.join('').length !== 6}
              className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 h-12 text-lg mb-4"
            >
              Verify Email
              <ArrowRight className="w-5 h-5 ml-2" />
            </Button>

            {/* Resend */}
            <div className="text-center">
              <p className="text-gray-500 text-sm mb-2">Didn't receive the code?</p>
              <button
                onClick={handleResendCode}
                disabled={isResending || countdown > 0}
                className="text-purple-600 hover:text-purple-700 font-medium text-sm disabled:text-gray-400 disabled:cursor-not-allowed"
              >
                {isResending ? (
                  'Sending...'
                ) : countdown > 0 ? (
                  `Resend in ${countdown}s`
                ) : (
                  'Resend Code'
                )}
              </button>
            </div>

            {/* Demo Hint */}
            <div className="mt-6 p-3 bg-purple-50 rounded-lg text-center">
              <p className="text-xs text-purple-600">
                <Sparkles className="w-3 h-3 inline mr-1" />
                Demo: Use code <span className="font-mono font-bold">123456</span> to verify
              </p>
            </div>
          </>
        );
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20 flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-purple-600 via-pink-500 to-orange-400">
          <div className="absolute inset-0 opacity-20">
            <svg className="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
              <defs>
                <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
                  <path d="M 10 0 L 0 0 0 10" fill="none" stroke="white" strokeWidth="0.5" />
                </pattern>
              </defs>
              <rect width="100" height="100" fill="url(#grid)" />
            </svg>
          </div>
        </div>

        <div className="relative z-10 flex flex-col justify-center p-12 text-white">
          <Link href="/" className="flex items-center gap-2 mb-12">
            <div className="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <Sparkles className="w-6 h-6" />
            </div>
            <span className="text-xl font-bold">SmartSpec Pro</span>
          </Link>

          <h1 className="text-4xl font-bold mb-4">
            Almost There!
          </h1>
          <p className="text-xl text-white/80 mb-8">
            Just one more step to unlock your AI-powered development experience.
          </p>

          <div className="space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
                <Mail className="w-5 h-5" />
              </div>
              <span>Check your inbox for the verification code</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
                <Clock className="w-5 h-5" />
              </div>
              <span>Code expires in 15 minutes</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-lg bg-white/20 flex items-center justify-center">
                <Shield className="w-5 h-5" />
              </div>
              <span>Your account is secure and protected</span>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Verification Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          {/* Mobile Logo */}
          <div className="lg:hidden flex items-center justify-center gap-2 mb-8">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">SmartSpec Pro</span>
          </div>

          {/* Card */}
          <div className="bg-white/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl border border-white/50">
            {renderContent()}
          </div>

          {/* Help Link */}
          <p className="text-center text-gray-500 text-sm mt-6">
            Having trouble?{' '}
            <Link href="/contact" className="text-purple-600 hover:text-purple-700 font-medium">
              Contact Support
            </Link>
          </p>
        </motion.div>
      </div>
    </div>
  );
}
