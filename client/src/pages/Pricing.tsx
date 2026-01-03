/**
 * Pricing Page
 * Design: Ethereal Gradient Flow
 * Features: Plan comparison, FAQ, enterprise contact
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
  Crown
} from 'lucide-react';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const plans = [
  {
    name: 'Free',
    description: 'Perfect for trying out SmartSpec',
    monthlyPrice: 0,
    yearlyPrice: 0,
    credits: 10,
    features: [
      { name: 'AI Code Generation', included: true },
      { name: '10 Credits/month', included: true },
      { name: 'Basic Models', included: true },
      { name: 'Community Support', included: true },
      { name: 'Public Gallery Access', included: true },
      { name: 'Priority Support', included: false },
      { name: 'Advanced Models', included: false },
      { name: 'Team Collaboration', included: false },
      { name: 'Custom Integrations', included: false },
    ],
    cta: 'Get Started',
    popular: false,
    icon: Sparkles
  },
  {
    name: 'Pro',
    description: 'For professional developers',
    monthlyPrice: 29,
    yearlyPrice: 290,
    credits: 500,
    features: [
      { name: 'AI Code Generation', included: true },
      { name: '500 Credits/month', included: true },
      { name: 'Advanced Models', included: true },
      { name: 'Priority Support', included: true },
      { name: 'Public Gallery Access', included: true },
      { name: 'Image & Video Generation', included: true },
      { name: 'API Access', included: true },
      { name: 'Team Collaboration', included: false },
      { name: 'Custom Integrations', included: false },
    ],
    cta: 'Start Pro Trial',
    popular: true,
    icon: Zap
  },
  {
    name: 'Enterprise',
    description: 'For teams and organizations',
    monthlyPrice: 199,
    yearlyPrice: 1990,
    credits: 5000,
    features: [
      { name: 'AI Code Generation', included: true },
      { name: '5,000 Credits/month', included: true },
      { name: 'All Models', included: true },
      { name: 'Dedicated Support', included: true },
      { name: 'Public Gallery Access', included: true },
      { name: 'Image & Video Generation', included: true },
      { name: 'Full API Access', included: true },
      { name: 'Team Collaboration', included: true },
      { name: 'Custom Integrations', included: true },
    ],
    cta: 'Contact Sales',
    popular: false,
    icon: Building2
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
  { credits: 100, price: 10, perCredit: 0.10 },
  { credits: 500, price: 40, perCredit: 0.08 },
  { credits: 1000, price: 70, perCredit: 0.07 },
  { credits: 5000, price: 300, perCredit: 0.06 },
];

export default function Pricing() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-16 overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0 bg-gradient-to-b from-violet-500/5 via-transparent to-transparent" />
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl" />
        <div className="absolute top-40 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl" />
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-3xl mx-auto"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <Crown className="w-4 h-4" />
              Simple, Transparent Pricing
            </span>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6">
              Choose Your <span className="gradient-text">Perfect Plan</span>
            </h1>
            <p className="text-lg text-muted-foreground mb-8">
              Start free and scale as you grow. All plans include core features with no hidden fees.
            </p>
            
            {/* Billing Toggle */}
            <div className="flex items-center justify-center gap-4">
              <span className={`text-sm ${!isYearly ? 'text-foreground font-medium' : 'text-muted-foreground'}`}>
                Monthly
              </span>
              <Switch
                checked={isYearly}
                onCheckedChange={setIsYearly}
              />
              <span className={`text-sm ${isYearly ? 'text-foreground font-medium' : 'text-muted-foreground'}`}>
                Yearly
              </span>
              {isYearly && (
                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                  Save 17%
                </span>
              )}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Pricing Cards */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {plans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="relative"
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 -translate-x-1/2 z-10">
                    <span className="px-4 py-1 text-sm font-medium bg-gradient-to-r from-violet-500 to-teal-400 text-white rounded-full shadow-lg">
                      Most Popular
                    </span>
                  </div>
                )}
                <Card className={`h-full ${plan.popular ? 'glass-card border-violet-500/50 shadow-xl shadow-violet-500/10' : 'glass-card'}`}>
                  <CardHeader className="text-center pb-4">
                    <div className={`w-14 h-14 rounded-xl mx-auto mb-4 flex items-center justify-center ${
                      plan.popular 
                        ? 'bg-gradient-to-br from-violet-500 to-teal-400' 
                        : 'bg-muted'
                    }`}>
                      <plan.icon className={`w-7 h-7 ${plan.popular ? 'text-white' : 'text-muted-foreground'}`} />
                    </div>
                    <CardTitle className="text-2xl">{plan.name}</CardTitle>
                    <p className="text-sm text-muted-foreground">{plan.description}</p>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    {/* Price */}
                    <div className="text-center">
                      <div className="flex items-baseline justify-center gap-1">
                        <span className="text-4xl font-bold">
                          ${isYearly ? Math.round(plan.yearlyPrice / 12) : plan.monthlyPrice}
                        </span>
                        <span className="text-muted-foreground">/month</span>
                      </div>
                      {isYearly && plan.yearlyPrice > 0 && (
                        <p className="text-sm text-muted-foreground mt-1">
                          ${plan.yearlyPrice} billed annually
                        </p>
                      )}
                      <p className="text-sm text-primary font-medium mt-2">
                        {plan.credits.toLocaleString()} credits/month
                      </p>
                    </div>

                    {/* Features */}
                    <ul className="space-y-3">
                      {plan.features.map((feature) => (
                        <li key={feature.name} className="flex items-center gap-3">
                          {feature.included ? (
                            <Check className="w-5 h-5 text-green-500 flex-shrink-0" />
                          ) : (
                            <X className="w-5 h-5 text-muted-foreground/50 flex-shrink-0" />
                          )}
                          <span className={feature.included ? '' : 'text-muted-foreground/50'}>
                            {feature.name}
                          </span>
                        </li>
                      ))}
                    </ul>

                    {/* CTA */}
                    <Button 
                      className={`w-full ${
                        plan.popular 
                          ? 'bg-gradient-to-r from-violet-500 to-teal-400 text-white hover:from-violet-600 hover:to-teal-500' 
                          : ''
                      }`}
                      variant={plan.popular ? 'default' : 'outline'}
                      size="lg"
                    >
                      {plan.cta}
                      <ArrowRight className="ml-2 w-4 h-4" />
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Credit Packs */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Need More Credits?</h2>
            <p className="text-muted-foreground">
              Purchase additional credit packs anytime. The more you buy, the more you save.
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 max-w-5xl mx-auto">
            {creditPacks.map((pack, index) => (
              <motion.div
                key={pack.credits}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="glass-card text-center hover:shadow-lg transition-shadow">
                  <CardContent className="p-6">
                    <div className="text-3xl font-bold gradient-text mb-2">
                      {pack.credits.toLocaleString()}
                    </div>
                    <div className="text-sm text-muted-foreground mb-4">credits</div>
                    <div className="text-2xl font-bold mb-1">${pack.price}</div>
                    <div className="text-xs text-muted-foreground mb-4">
                      ${pack.perCredit.toFixed(2)} per credit
                    </div>
                    <Button variant="outline" size="sm" className="w-full">
                      Buy Now
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Feature Comparison */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Compare Plans</h2>
            <p className="text-muted-foreground">
              See which plan is right for you
            </p>
          </motion.div>

          <div className="overflow-x-auto">
            <table className="w-full max-w-4xl mx-auto">
              <thead>
                <tr className="border-b">
                  <th className="text-left py-4 px-4">Feature</th>
                  <th className="text-center py-4 px-4">Free</th>
                  <th className="text-center py-4 px-4">Pro</th>
                  <th className="text-center py-4 px-4">Enterprise</th>
                </tr>
              </thead>
              <tbody>
                {[
                  { feature: 'Monthly Credits', free: '10', pro: '500', enterprise: '5,000' },
                  { feature: 'AI Code Generation', free: true, pro: true, enterprise: true },
                  { feature: 'Image Generation', free: false, pro: true, enterprise: true },
                  { feature: 'Video Generation', free: false, pro: true, enterprise: true },
                  { feature: 'API Access', free: false, pro: true, enterprise: true },
                  { feature: 'Team Members', free: '1', pro: '3', enterprise: 'Unlimited' },
                  { feature: 'Support', free: 'Community', pro: 'Priority', enterprise: 'Dedicated' },
                  { feature: 'Custom Integrations', free: false, pro: false, enterprise: true },
                ].map((row) => (
                  <tr key={row.feature} className="border-b">
                    <td className="py-4 px-4 font-medium">{row.feature}</td>
                    <td className="text-center py-4 px-4">
                      {typeof row.free === 'boolean' ? (
                        row.free ? <Check className="w-5 h-5 text-green-500 mx-auto" /> : <X className="w-5 h-5 text-muted-foreground/50 mx-auto" />
                      ) : row.free}
                    </td>
                    <td className="text-center py-4 px-4">
                      {typeof row.pro === 'boolean' ? (
                        row.pro ? <Check className="w-5 h-5 text-green-500 mx-auto" /> : <X className="w-5 h-5 text-muted-foreground/50 mx-auto" />
                      ) : row.pro}
                    </td>
                    <td className="text-center py-4 px-4">
                      {typeof row.enterprise === 'boolean' ? (
                        row.enterprise ? <Check className="w-5 h-5 text-green-500 mx-auto" /> : <X className="w-5 h-5 text-muted-foreground/50 mx-auto" />
                      ) : row.enterprise}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <HelpCircle className="w-4 h-4" />
              FAQ
            </span>
            <h2 className="text-3xl font-bold mb-4">Frequently Asked Questions</h2>
            <p className="text-muted-foreground">
              Everything you need to know about our pricing
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
                  <AccordionItem value={`item-${index}`} className="glass-card rounded-xl px-6">
                    <AccordionTrigger className="text-left hover:no-underline">
                      {faq.question}
                    </AccordionTrigger>
                    <AccordionContent className="text-muted-foreground">
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
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-card rounded-2xl p-8 sm:p-12 text-center max-w-4xl mx-auto"
          >
            <Building2 className="w-16 h-16 mx-auto mb-6 text-primary" />
            <h2 className="text-3xl font-bold mb-4">Need a Custom Solution?</h2>
            <p className="text-muted-foreground mb-8 max-w-2xl mx-auto">
              We offer custom enterprise plans with dedicated support, custom integrations, 
              on-premise deployment options, and volume discounts.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-violet-500 to-teal-400 text-white">
                Contact Sales
                <ArrowRight className="ml-2 w-4 h-4" />
              </Button>
              <Button size="lg" variant="outline">
                Schedule Demo
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
