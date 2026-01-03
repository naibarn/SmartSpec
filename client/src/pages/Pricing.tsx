/**
 * Pricing Page - Enhanced Ethereal Gradient Flow Design
 * Features: Aurora gradients, glassmorphism, animated backgrounds, premium cards
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'wouter';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Switch } from '@/components/ui/switch';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import {
  Check,
  X,
  Sparkles,
  Zap,
  Building2,
  HelpCircle,
  ArrowRight,
  Crown,
  Star,
  Shield,
  Rocket,
  Gift,
  CreditCard,
  Users,
  Infinity,
  Headphones,
  Code2,
  Image,
  Video,
  Cpu
} from 'lucide-react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const plans = [
  {
    name: 'Starter',
    description: 'Perfect for trying out SmartSpec',
    monthlyPrice: 0,
    yearlyPrice: 0,
    credits: 10,
    features: [
      { name: 'AI Code Generation', included: true, highlight: false },
      { name: '10 Credits/month', included: true, highlight: false },
      { name: 'Basic Models (GPT-4o-mini)', included: true, highlight: false },
      { name: 'Community Support', included: true, highlight: false },
      { name: 'Public Gallery Access', included: true, highlight: false },
      { name: 'Priority Support', included: false, highlight: false },
      { name: 'Advanced Models', included: false, highlight: false },
      { name: 'Team Collaboration', included: false, highlight: false },
    ],
    cta: 'Get Started Free',
    popular: false,
    icon: Sparkles,
    gradient: 'from-slate-500 to-slate-600',
    bgGradient: 'from-slate-50 to-slate-100',
    borderColor: 'border-slate-200',
    accentColor: 'text-slate-600'
  },
  {
    name: 'Pro',
    description: 'For professional developers',
    monthlyPrice: 29,
    yearlyPrice: 290,
    credits: 500,
    features: [
      { name: 'Everything in Starter', included: true, highlight: false },
      { name: '500 Credits/month', included: true, highlight: true },
      { name: 'Advanced Models (GPT-4, Claude)', included: true, highlight: true },
      { name: 'Priority Email Support', included: true, highlight: false },
      { name: 'Image Generation (DALL-E, Midjourney)', included: true, highlight: true },
      { name: 'Video Generation', included: true, highlight: true },
      { name: 'API Access', included: true, highlight: false },
      { name: 'Team Collaboration (3 seats)', included: true, highlight: false },
    ],
    cta: 'Start 14-Day Trial',
    popular: true,
    icon: Zap,
    gradient: 'from-violet-500 via-purple-500 to-fuchsia-500',
    bgGradient: 'from-violet-50 via-purple-50 to-fuchsia-50',
    borderColor: 'border-violet-300',
    accentColor: 'text-violet-600'
  },
  {
    name: 'Enterprise',
    description: 'For teams and organizations',
    monthlyPrice: 199,
    yearlyPrice: 1990,
    credits: 5000,
    features: [
      { name: 'Everything in Pro', included: true, highlight: false },
      { name: '5,000+ Credits/month', included: true, highlight: true },
      { name: 'All AI Models Access', included: true, highlight: true },
      { name: 'Dedicated Account Manager', included: true, highlight: true },
      { name: 'Custom Model Training', included: true, highlight: true },
      { name: 'On-Premise Deployment', included: true, highlight: false },
      { name: 'Unlimited Team Members', included: true, highlight: true },
      { name: 'SLA & Priority Support', included: true, highlight: false },
    ],
    cta: 'Contact Sales',
    popular: false,
    icon: Building2,
    gradient: 'from-teal-500 via-emerald-500 to-cyan-500',
    bgGradient: 'from-teal-50 via-emerald-50 to-cyan-50',
    borderColor: 'border-teal-200',
    accentColor: 'text-teal-600'
  }
];

const faqs = [
  {
    question: 'What are credits and how do they work?',
    answer: 'Credits are the currency used for AI operations in SmartSpec. Different operations consume different amounts of credits. For example, generating code uses 1 credit, while generating images uses 1-2 credits depending on quality. Unused credits roll over to the next month for paid plans.'
  },
  {
    question: 'Can I upgrade or downgrade my plan?',
    answer: 'Yes, you can change your plan at any time. When upgrading, you\'ll be charged the prorated difference. When downgrading, the new rate takes effect at your next billing cycle.'
  },
  {
    question: 'Is there a free trial for paid plans?',
    answer: 'Yes! All paid plans come with a 14-day free trial. No credit card required to start. You can explore all features before committing.'
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards (Visa, MasterCard, American Express), PayPal, and bank transfers for Enterprise plans. All payments are processed securely through Stripe.'
  },
  {
    question: 'Do you offer refunds?',
    answer: 'We offer a 30-day money-back guarantee for annual plans. If you\'re not satisfied, contact our support team for a full refund within the first 30 days.'
  },
  {
    question: 'What happens if I run out of credits?',
    answer: 'You can purchase additional credit packs at any time, or upgrade to a higher plan. We\'ll notify you when you\'re running low on credits so you\'re never caught off guard.'
  }
];

const creditPacks = [
  { credits: 100, price: 10, perCredit: 0.10, popular: false },
  { credits: 500, price: 40, perCredit: 0.08, popular: true },
  { credits: 1000, price: 70, perCredit: 0.07, popular: false },
  { credits: 5000, price: 300, perCredit: 0.06, popular: false },
];

const comparisonFeatures: Array<{
  feature: string;
  free: string | boolean;
  pro: string | boolean;
  enterprise: string | boolean;
  icon: React.ComponentType<{ className?: string }>;
}> = [
  { feature: 'Monthly Credits', free: '10', pro: '500', enterprise: '5,000+', icon: CreditCard },
  { feature: 'AI Code Generation', free: true, pro: true, enterprise: true, icon: Code2 },
  { feature: 'Image Generation', free: false, pro: true, enterprise: true, icon: Image },
  { feature: 'Video Generation', free: false, pro: true, enterprise: true, icon: Video },
  { feature: 'API Access', free: false, pro: true, enterprise: true, icon: Cpu },
  { feature: 'Team Members', free: '1', pro: '3', enterprise: 'Unlimited', icon: Users },
  { feature: 'Support Level', free: 'Community', pro: 'Priority', enterprise: 'Dedicated', icon: Headphones },
  { feature: 'Custom Integrations', free: false, pro: false, enterprise: true, icon: Shield },
];

export default function Pricing() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <Navbar />
      
      {/* Hero Section with Aurora Background */}
      <section className="relative pt-32 pb-20 overflow-hidden">
        {/* Animated Aurora Background */}
        <div className="absolute inset-0">
          <div className="absolute inset-0 bg-gradient-to-br from-violet-100/40 via-transparent to-teal-100/40" />
          <motion.div 
            className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-gradient-to-br from-violet-400/20 via-purple-400/20 to-fuchsia-400/20 rounded-full blur-3xl"
            animate={{
              x: [0, 50, 0],
              y: [0, 30, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: 15,
              repeat: Number.POSITIVE_INFINITY,
              ease: "easeInOut"
            }}
          />
          <motion.div 
            className="absolute top-20 right-1/4 w-[500px] h-[500px] bg-gradient-to-br from-teal-400/20 via-emerald-400/20 to-cyan-400/20 rounded-full blur-3xl"
            animate={{
              x: [0, -40, 0],
              y: [0, 50, 0],
              scale: [1, 1.15, 1],
            }}
            transition={{
              duration: 18,
              repeat: Number.POSITIVE_INFINITY,
              ease: "easeInOut"
            }}
          />
          <motion.div 
            className="absolute bottom-0 left-1/2 -translate-x-1/2 w-[800px] h-[400px] bg-gradient-to-t from-pink-300/10 via-orange-300/10 to-transparent rounded-full blur-3xl"
            animate={{
              scale: [1, 1.05, 1],
              opacity: [0.3, 0.5, 0.3],
            }}
            transition={{
              duration: 10,
              repeat: Number.POSITIVE_INFINITY,
              ease: "easeInOut"
            }}
          />
        </div>
        
        {/* Floating Particles */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {[...Array(20)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 rounded-full bg-gradient-to-br from-violet-400 to-teal-400 opacity-30"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${Math.random() * 100}%`,
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.2, 0.5, 0.2],
              }}
              transition={{
                duration: 3 + Math.random() * 2,
                repeat: Number.POSITIVE_INFINITY,
                delay: Math.random() * 2,
              }}
            />
          ))}
        </div>
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-4xl mx-auto"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.1 }}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-violet-500/10 via-purple-500/10 to-fuchsia-500/10 border border-violet-200/50 backdrop-blur-sm mb-6"
            >
              <Crown className="w-4 h-4 text-violet-600" />
              <span className="text-sm font-semibold bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent">
                Simple, Transparent Pricing
              </span>
              <span className="px-2 py-0.5 text-xs font-medium bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white rounded-full">
                No Hidden Fees
              </span>
            </motion.div>

            {/* Main Heading */}
            <motion.h1 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-5xl sm:text-6xl md:text-7xl font-bold mb-6 tracking-tight"
            >
              <span className="text-gray-900">Choose Your</span>
              <br />
              <span className="bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 bg-clip-text text-transparent">
                Perfect Plan
              </span>
            </motion.h1>

            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto"
            >
              Start free and scale as you grow. All plans include core AI features 
              with flexible credits that never expire.
            </motion.p>
            
            {/* Billing Toggle */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="inline-flex items-center gap-4 p-2 rounded-2xl bg-white/80 backdrop-blur-sm border border-gray-200 shadow-lg shadow-gray-200/50"
            >
              <span className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                !isYearly 
                  ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white shadow-lg shadow-violet-500/30' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}>
                Monthly
              </span>
              <Switch
                checked={isYearly}
                onCheckedChange={setIsYearly}
                className="data-[state=checked]:bg-gradient-to-r data-[state=checked]:from-violet-500 data-[state=checked]:to-fuchsia-500"
              />
              <span className={`px-4 py-2 rounded-xl text-sm font-medium transition-all duration-300 ${
                isYearly 
                  ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white shadow-lg shadow-violet-500/30' 
                  : 'text-gray-600 hover:text-gray-900'
              }`}>
                Yearly
              </span>
              {isYearly && (
                <motion.span 
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="px-3 py-1.5 text-xs font-bold bg-gradient-to-r from-emerald-400 to-teal-500 text-white rounded-full shadow-lg shadow-emerald-500/30"
                >
                  Save 17%
                </motion.span>
              )}
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-16 relative">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8 max-w-7xl mx-auto">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.15 }}
                className={`relative group ${plan.popular ? 'md:-mt-4 md:mb-4' : ''}`}
              >
                {/* Popular Badge */}
                {plan.popular && (
                  <div className="absolute -top-5 left-1/2 -translate-x-1/2 z-20">
                    <motion.div
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="px-6 py-2 text-sm font-bold bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 text-white rounded-full shadow-xl shadow-violet-500/40 flex items-center gap-2"
                    >
                      <Star className="w-4 h-4 fill-current" />
                      Most Popular
                    </motion.div>
                  </div>
                )}

                {/* Card */}
                <div className={`relative h-full rounded-3xl overflow-hidden transition-all duration-500 ${
                  plan.popular 
                    ? 'bg-gradient-to-b from-white to-violet-50/50 border-2 border-violet-300 shadow-2xl shadow-violet-500/20 hover:shadow-violet-500/30' 
                    : 'bg-white/80 backdrop-blur-sm border border-gray-200 shadow-xl shadow-gray-200/50 hover:shadow-2xl hover:shadow-gray-300/50 hover:border-gray-300'
                }`}>
                  {/* Gradient Overlay for Popular */}
                  {plan.popular && (
                    <div className="absolute inset-0 bg-gradient-to-b from-violet-500/5 via-transparent to-fuchsia-500/5 pointer-events-none" />
                  )}

                  <div className="relative p-8">
                    {/* Icon */}
                    <div className={`w-16 h-16 rounded-2xl mb-6 flex items-center justify-center bg-gradient-to-br ${plan.gradient} shadow-lg ${
                      plan.popular ? 'shadow-violet-500/40' : 'shadow-gray-300/50'
                    }`}>
                      <plan.icon className="w-8 h-8 text-white" />
                    </div>

                    {/* Plan Name & Description */}
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                    <p className="text-gray-600 mb-6">{plan.description}</p>

                    {/* Price */}
                    <div className="mb-8">
                      <div className="flex items-baseline gap-2">
                        <span className={`text-5xl font-bold ${plan.popular ? 'bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent' : 'text-gray-900'}`}>
                          ${isYearly ? Math.round(plan.yearlyPrice / 12) : plan.monthlyPrice}
                        </span>
                        <span className="text-gray-500 text-lg">/month</span>
                      </div>
                      {isYearly && plan.yearlyPrice > 0 && (
                        <p className="text-sm text-gray-500 mt-2">
                          ${plan.yearlyPrice} billed annually
                        </p>
                      )}
                      <div className={`inline-flex items-center gap-2 mt-3 px-3 py-1.5 rounded-full text-sm font-semibold ${
                        plan.popular 
                          ? 'bg-violet-100 text-violet-700' 
                          : 'bg-gray-100 text-gray-700'
                      }`}>
                        <Zap className="w-4 h-4" />
                        {plan.credits.toLocaleString()} credits/month
                      </div>
                    </div>

                    {/* Features */}
                    <ul className="space-y-4 mb-8">
                      {plan.features.map((feature) => (
                        <li key={feature.name} className="flex items-start gap-3">
                          {feature.included ? (
                            <div className={`w-5 h-5 rounded-full flex items-center justify-center flex-shrink-0 mt-0.5 ${
                              feature.highlight 
                                ? 'bg-gradient-to-br from-violet-500 to-fuchsia-500' 
                                : 'bg-emerald-500'
                            }`}>
                              <Check className="w-3 h-3 text-white" />
                            </div>
                          ) : (
                            <div className="w-5 h-5 rounded-full bg-gray-200 flex items-center justify-center flex-shrink-0 mt-0.5">
                              <X className="w-3 h-3 text-gray-400" />
                            </div>
                          )}
                          <span className={`text-sm ${
                            feature.included 
                              ? feature.highlight ? 'text-gray-900 font-medium' : 'text-gray-700'
                              : 'text-gray-400'
                          }`}>
                            {feature.name}
                          </span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA Button */}
                    <Button 
                      className={`w-full py-6 text-base font-semibold rounded-xl transition-all duration-300 ${
                        plan.popular 
                          ? 'bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 text-white hover:from-violet-600 hover:via-purple-600 hover:to-fuchsia-600 shadow-lg shadow-violet-500/30 hover:shadow-xl hover:shadow-violet-500/40' 
                          : 'bg-gray-900 text-white hover:bg-gray-800'
                      }`}
                      size="lg"
                    >
                      {plan.cta}
                      <ArrowRight className="ml-2 w-5 h-5" />
                    </Button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Credit Packs Section */}
      <section className="py-20 relative overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-gray-50 via-violet-50/30 to-gray-50" />
        <motion.div 
          className="absolute top-1/2 left-0 w-96 h-96 bg-violet-400/10 rounded-full blur-3xl -translate-y-1/2"
          animate={{ x: [-50, 50, -50] }}
          transition={{ duration: 20, repeat: Number.POSITIVE_INFINITY }}
        />
        <motion.div 
          className="absolute top-1/2 right-0 w-96 h-96 bg-teal-400/10 rounded-full blur-3xl -translate-y-1/2"
          animate={{ x: [50, -50, 50] }}
          transition={{ duration: 20, repeat: Number.POSITIVE_INFINITY }}
        />

        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-teal-500/10 to-emerald-500/10 border border-teal-200/50 text-teal-700 text-sm font-medium mb-4">
              <CreditCard className="w-4 h-4" />
              Flexible Credits
            </span>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Need More Credits?</h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Purchase additional credit packs anytime. The more you buy, the more you save.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-6xl mx-auto">
            {creditPacks.map((pack, index) => (
              <motion.div
                key={pack.credits}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="relative group"
              >
                {pack.popular && (
                  <div className="absolute -top-3 left-1/2 -translate-x-1/2 z-10">
                    <span className="px-3 py-1 text-xs font-bold bg-gradient-to-r from-teal-500 to-emerald-500 text-white rounded-full shadow-lg">
                      Best Value
                    </span>
                  </div>
                )}
                <div className={`relative h-full rounded-2xl p-6 transition-all duration-300 ${
                  pack.popular 
                    ? 'bg-gradient-to-b from-teal-50 to-emerald-50 border-2 border-teal-300 shadow-xl shadow-teal-500/20' 
                    : 'bg-white border border-gray-200 shadow-lg hover:shadow-xl hover:border-gray-300'
                }`}>
                  <div className={`w-12 h-12 rounded-xl mb-4 flex items-center justify-center ${
                    pack.popular 
                      ? 'bg-gradient-to-br from-teal-500 to-emerald-500' 
                      : 'bg-gray-100'
                  }`}>
                    <Zap className={`w-6 h-6 ${pack.popular ? 'text-white' : 'text-gray-600'}`} />
                  </div>
                  <div className={`text-4xl font-bold mb-1 ${
                    pack.popular 
                      ? 'bg-gradient-to-r from-teal-600 to-emerald-600 bg-clip-text text-transparent' 
                      : 'text-gray-900'
                  }`}>
                    {pack.credits.toLocaleString()}
                  </div>
                  <div className="text-gray-500 text-sm mb-4">credits</div>
                  <div className="text-3xl font-bold text-gray-900 mb-1">${pack.price}</div>
                  <div className="text-sm text-gray-500 mb-6">
                    ${pack.perCredit.toFixed(2)} per credit
                  </div>
                  <Button 
                    variant={pack.popular ? 'default' : 'outline'} 
                    className={`w-full ${
                      pack.popular 
                        ? 'bg-gradient-to-r from-teal-500 to-emerald-500 hover:from-teal-600 hover:to-emerald-600 text-white' 
                        : ''
                    }`}
                  >
                    Buy Now
                  </Button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison Table */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-violet-500/10 to-fuchsia-500/10 border border-violet-200/50 text-violet-700 text-sm font-medium mb-4">
              <Shield className="w-4 h-4" />
              Full Comparison
            </span>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Compare All Features</h2>
            <p className="text-xl text-gray-600">
              See exactly what you get with each plan
            </p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="max-w-5xl mx-auto"
          >
            <div className="bg-white rounded-3xl border border-gray-200 shadow-xl overflow-hidden">
              {/* Table Header */}
              <div className="grid grid-cols-4 bg-gradient-to-r from-gray-50 to-gray-100 border-b border-gray-200">
                <div className="p-6 font-semibold text-gray-900">Features</div>
                <div className="p-6 text-center font-semibold text-gray-900">Starter</div>
                <div className="p-6 text-center font-semibold bg-gradient-to-b from-violet-100 to-violet-50 text-violet-700 border-x border-violet-200">
                  Pro
                  <span className="block text-xs font-normal text-violet-500 mt-1">Recommended</span>
                </div>
                <div className="p-6 text-center font-semibold text-gray-900">Enterprise</div>
              </div>

              {/* Table Body */}
              {comparisonFeatures.map((row, index) => (
                <div 
                  key={row.feature} 
                  className={`grid grid-cols-4 ${index !== comparisonFeatures.length - 1 ? 'border-b border-gray-100' : ''}`}
                >
                  <div className="p-5 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center">
                      <row.icon className="w-4 h-4 text-gray-600" />
                    </div>
                    <span className="font-medium text-gray-900">{row.feature}</span>
                  </div>
                  <div className="p-5 flex items-center justify-center">
                    {typeof row.free === 'boolean' ? (
                      row.free ? (
                        <div className="w-6 h-6 rounded-full bg-emerald-100 flex items-center justify-center">
                          <Check className="w-4 h-4 text-emerald-600" />
                        </div>
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <X className="w-4 h-4 text-gray-400" />
                        </div>
                      )
                    ) : (
                      <span className="text-gray-700 font-medium">{row.free}</span>
                    )}
                  </div>
                  <div className="p-5 flex items-center justify-center bg-violet-50/50 border-x border-violet-100">
                    {typeof row.pro === 'boolean' ? (
                      row.pro ? (
                        <div className="w-6 h-6 rounded-full bg-violet-100 flex items-center justify-center">
                          <Check className="w-4 h-4 text-violet-600" />
                        </div>
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <X className="w-4 h-4 text-gray-400" />
                        </div>
                      )
                    ) : (
                      <span className="text-violet-700 font-semibold">{row.pro}</span>
                    )}
                  </div>
                  <div className="p-5 flex items-center justify-center">
                    {typeof row.enterprise === 'boolean' ? (
                      row.enterprise ? (
                        <div className="w-6 h-6 rounded-full bg-teal-100 flex items-center justify-center">
                          <Check className="w-4 h-4 text-teal-600" />
                        </div>
                      ) : (
                        <div className="w-6 h-6 rounded-full bg-gray-100 flex items-center justify-center">
                          <X className="w-4 h-4 text-gray-400" />
                        </div>
                      )
                    ) : (
                      <span className="text-gray-700 font-medium">{row.enterprise}</span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-20 relative overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-gray-50 to-white" />
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-orange-500/10 to-amber-500/10 border border-orange-200/50 text-orange-700 text-sm font-medium mb-4">
              <HelpCircle className="w-4 h-4" />
              Got Questions?
            </span>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">Frequently Asked Questions</h2>
            <p className="text-xl text-gray-600">
              Everything you need to know about our pricing and plans
            </p>
          </motion.div>

          <div className="max-w-3xl mx-auto">
            <Accordion type="single" collapsible className="space-y-4">
              {faqs.map((faq, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 10 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.05 }}
                >
                  <AccordionItem 
                    value={`item-${index}`} 
                    className="bg-white rounded-2xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow px-6 overflow-hidden"
                  >
                    <AccordionTrigger className="text-left hover:no-underline py-5 text-gray-900 font-medium">
                      {faq.question}
                    </AccordionTrigger>
                    <AccordionContent className="text-gray-600 pb-5">
                      {faq.answer}
                    </AccordionContent>
                  </AccordionItem>
                </motion.div>
              ))}
            </Accordion>
          </div>
        </div>
      </section>

      {/* Enterprise CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="relative max-w-5xl mx-auto"
          >
            {/* Background Card */}
            <div className="absolute inset-0 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 rounded-3xl transform rotate-1" />
            <div className="relative bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-3xl p-10 sm:p-14 overflow-hidden">
              {/* Decorative Elements */}
              <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
              <div className="absolute bottom-0 left-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
              
              <div className="relative flex flex-col lg:flex-row items-center gap-10">
                <div className="flex-1 text-center lg:text-left">
                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 backdrop-blur-sm text-white text-sm font-medium mb-6">
                    <Building2 className="w-4 h-4" />
                    Enterprise Solutions
                  </div>
                  <h2 className="text-4xl sm:text-5xl font-bold text-white mb-4">
                    Need a Custom Solution?
                  </h2>
                  <p className="text-xl text-white/80 mb-8 max-w-xl">
                    Get dedicated support, custom integrations, on-premise deployment, 
                    and volume discounts tailored to your organization.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                    <Button 
                      size="lg" 
                      className="bg-white text-violet-600 hover:bg-gray-100 px-8 py-6 text-base font-semibold shadow-xl"
                    >
                      Contact Sales
                      <ArrowRight className="ml-2 w-5 h-5" />
                    </Button>
                    <Button 
                      size="lg" 
                      variant="outline" 
                      className="border-2 border-white/50 text-white hover:bg-white/10 px-8 py-6 text-base font-semibold"
                    >
                      Schedule Demo
                    </Button>
                  </div>
                </div>
                
                {/* Stats */}
                <div className="grid grid-cols-2 gap-6">
                  {[
                    { value: '99.9%', label: 'Uptime SLA' },
                    { value: '24/7', label: 'Support' },
                    { value: '500+', label: 'Enterprise Clients' },
                    { value: '<1hr', label: 'Response Time' },
                  ].map((stat, index) => (
                    <div key={index} className="text-center p-4 rounded-2xl bg-white/10 backdrop-blur-sm">
                      <div className="text-3xl font-bold text-white">{stat.value}</div>
                      <div className="text-sm text-white/70">{stat.label}</div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
