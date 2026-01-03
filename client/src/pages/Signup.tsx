/**
 * Signup Page - SmartSpec Pro
 * User registration with plan selection
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'wouter';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Checkbox } from '@/components/ui/checkbox';
import { toast } from 'sonner';
import {
  Mail,
  Lock,
  User,
  Eye,
  EyeOff,
  ArrowRight,
  Sparkles,
  Github,
  Chrome,
  Check,
  Building2,
} from 'lucide-react';

type PlanType = 'free' | 'pro';

interface Plan {
  id: PlanType;
  name: string;
  price: string;
  period: string;
  features: string[];
  popular?: boolean;
}

const plans: Plan[] = [
  {
    id: 'free',
    name: 'Free',
    price: '$0',
    period: 'forever',
    features: [
      '10 AI generations/month',
      'Basic templates',
      'Community support',
    ],
  },
  {
    id: 'pro',
    name: 'Pro',
    price: '$29',
    period: '/month',
    features: [
      '500 AI generations/month',
      'All premium templates',
      'Priority support',
      'Team collaboration',
    ],
    popular: true,
  },
];

export default function Signup() {
  const [step, setStep] = useState<1 | 2>(1);
  const [selectedPlan, setSelectedPlan] = useState<PlanType>('free');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    company: '',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [agreeTerms, setAgreeTerms] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!agreeTerms) {
      toast.error('Please agree to the terms and conditions');
      return;
    }

    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    toast.success('Account created successfully! Please check your email to verify.');
    setIsLoading(false);
  };

  const handleSocialSignup = (provider: string) => {
    toast.info(`${provider} signup coming soon!`);
  };

  const isPasswordStrong = (password: string) => {
    return password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20 flex">
      {/* Left Side - Branding */}
      <div className="hidden lg:flex lg:w-1/2 relative overflow-hidden">
        {/* Background Pattern */}
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

        {/* Content */}
        <div className="relative z-10 flex flex-col justify-center p-12 text-white">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <Link href="/" className="flex items-center gap-3 mb-12">
              <div className="w-12 h-12 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-bold">SmartSpec Pro</span>
            </Link>

            <h1 className="text-4xl font-bold mb-6">
              Start building with AI today
            </h1>
            <p className="text-xl text-white/80 mb-8">
              Join thousands of developers who are shipping faster with SmartSpec Pro.
            </p>

            {/* Stats */}
            <div className="grid grid-cols-3 gap-6">
              {[
                { value: '10K+', label: 'Developers' },
                { value: '50K+', label: 'Projects' },
                { value: '99.9%', label: 'Uptime' },
              ].map((stat, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 + index * 0.1 }}
                  className="text-center"
                >
                  <div className="text-3xl font-bold">{stat.value}</div>
                  <div className="text-white/70 text-sm">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Decorative Elements */}
        <div className="absolute bottom-0 right-0 w-96 h-96 bg-white/10 rounded-full blur-3xl" />
        <div className="absolute top-20 right-20 w-64 h-64 bg-pink-500/20 rounded-full blur-3xl" />
      </div>

      {/* Right Side - Signup Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center p-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-md"
        >
          {/* Mobile Logo */}
          <Link href="/" className="flex items-center gap-3 mb-8 lg:hidden">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <span className="text-xl font-bold text-gray-900">SmartSpec Pro</span>
          </Link>

          <div className="bg-white/70 backdrop-blur-xl rounded-3xl border border-white/50 shadow-xl shadow-purple-500/10 p-8">
            {/* Step Indicator */}
            <div className="flex items-center justify-center gap-3 mb-8">
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                step >= 1 ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white' : 'bg-gray-200 text-gray-500'
              }`}>
                1
              </div>
              <div className={`w-12 h-1 rounded ${step >= 2 ? 'bg-gradient-to-r from-purple-500 to-pink-500' : 'bg-gray-200'}`} />
              <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                step >= 2 ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white' : 'bg-gray-200 text-gray-500'
              }`}>
                2
              </div>
            </div>

            {step === 1 ? (
              <>
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Create your account</h2>
                  <p className="text-gray-600">
                    Already have an account?{' '}
                    <Link href="/login" className="text-purple-600 hover:text-purple-700 font-medium">
                      Sign in
                    </Link>
                  </p>
                </div>

                {/* Social Signup Buttons */}
                <div className="grid grid-cols-2 gap-3 mb-6">
                  <Button
                    variant="outline"
                    onClick={() => handleSocialSignup('Google')}
                    className="bg-white hover:bg-gray-50 border-gray-200"
                  >
                    <Chrome className="w-5 h-5 mr-2 text-[#4285F4]" />
                    Google
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => handleSocialSignup('GitHub')}
                    className="bg-white hover:bg-gray-50 border-gray-200"
                  >
                    <Github className="w-5 h-5 mr-2" />
                    GitHub
                  </Button>
                </div>

                {/* Divider */}
                <div className="relative mb-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-200" />
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-4 bg-white text-gray-500">or continue with email</span>
                  </div>
                </div>

                {/* Signup Form Step 1 */}
                <form onSubmit={(e) => { e.preventDefault(); setStep(2); }} className="space-y-5">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Full Name
                    </label>
                    <div className="relative">
                      <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <Input
                        name="name"
                        value={formData.name}
                        onChange={handleChange}
                        placeholder="John Doe"
                        required
                        className="pl-10 bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <Input
                        name="email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange}
                        placeholder="you@example.com"
                        required
                        className="pl-10 bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Password
                    </label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <Input
                        name="password"
                        type={showPassword ? 'text' : 'password'}
                        value={formData.password}
                        onChange={handleChange}
                        placeholder="••••••••"
                        required
                        className="pl-10 pr-10 bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                      </button>
                    </div>
                    {formData.password && (
                      <div className={`mt-2 text-xs ${isPasswordStrong(formData.password) ? 'text-green-600' : 'text-orange-500'}`}>
                        {isPasswordStrong(formData.password)
                          ? '✓ Strong password'
                          : 'Password should be 8+ characters with uppercase and number'}
                      </div>
                    )}
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Company (Optional)
                    </label>
                    <div className="relative">
                      <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                      <Input
                        name="company"
                        value={formData.company}
                        onChange={handleChange}
                        placeholder="Your Company"
                        className="pl-10 bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                      />
                    </div>
                  </div>

                  <Button
                    type="submit"
                    className="w-full bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white py-3 rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-300"
                  >
                    Continue
                    <ArrowRight className="w-4 h-4 ml-2" />
                  </Button>
                </form>
              </>
            ) : (
              <>
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Choose your plan</h2>
                  <p className="text-gray-600">
                    You can always upgrade later
                  </p>
                </div>

                {/* Plan Selection */}
                <div className="space-y-4 mb-6">
                  {plans.map((plan) => (
                    <button
                      key={plan.id}
                      onClick={() => setSelectedPlan(plan.id)}
                      className={`w-full p-4 rounded-xl text-left transition-all duration-300 relative ${
                        selectedPlan === plan.id
                          ? 'bg-gradient-to-r from-purple-500/10 to-pink-500/10 border-2 border-purple-500'
                          : 'bg-white/50 border-2 border-gray-200 hover:border-purple-200'
                      }`}
                    >
                      {plan.popular && (
                        <span className="absolute -top-2 right-4 px-2 py-0.5 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-medium rounded-full">
                          Popular
                        </span>
                      )}
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-3">
                          <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            selectedPlan === plan.id
                              ? 'border-purple-500 bg-purple-500'
                              : 'border-gray-300'
                          }`}>
                            {selectedPlan === plan.id && <Check className="w-3 h-3 text-white" />}
                          </div>
                          <span className="font-semibold text-gray-900">{plan.name}</span>
                        </div>
                        <div className="text-right">
                          <span className="text-2xl font-bold text-gray-900">{plan.price}</span>
                          <span className="text-gray-500 text-sm">{plan.period}</span>
                        </div>
                      </div>
                      <div className="ml-8 space-y-1">
                        {plan.features.map((feature, index) => (
                          <div key={index} className="flex items-center gap-2 text-sm text-gray-600">
                            <Check className="w-4 h-4 text-green-500" />
                            {feature}
                          </div>
                        ))}
                      </div>
                    </button>
                  ))}
                </div>

                {/* Terms Agreement */}
                <div className="flex items-start gap-2 mb-6">
                  <Checkbox
                    id="terms"
                    checked={agreeTerms}
                    onCheckedChange={(checked) => setAgreeTerms(checked as boolean)}
                    className="mt-0.5"
                  />
                  <label htmlFor="terms" className="text-sm text-gray-600 cursor-pointer">
                    I agree to the{' '}
                    <Link href="/terms" className="text-purple-600 hover:underline">
                      Terms of Service
                    </Link>{' '}
                    and{' '}
                    <Link href="/privacy" className="text-purple-600 hover:underline">
                      Privacy Policy
                    </Link>
                  </label>
                </div>

                {/* Action Buttons */}
                <div className="flex gap-3">
                  <Button
                    variant="outline"
                    onClick={() => setStep(1)}
                    className="flex-1"
                  >
                    Back
                  </Button>
                  <Button
                    onClick={handleSubmit}
                    disabled={isLoading || !agreeTerms}
                    className="flex-1 bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white shadow-lg shadow-purple-500/30"
                  >
                    {isLoading ? (
                      <>
                        <span className="animate-spin mr-2">⏳</span>
                        Creating...
                      </>
                    ) : (
                      <>
                        Create Account
                        <ArrowRight className="w-4 h-4 ml-2" />
                      </>
                    )}
                  </Button>
                </div>
              </>
            )}
          </div>
        </motion.div>
      </div>
    </div>
  );
}
