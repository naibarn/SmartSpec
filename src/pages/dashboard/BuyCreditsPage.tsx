import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  CreditCard,
  Check,
  Zap,
  Shield,
  Lock,
  ArrowRight,
  Sparkles,
  TrendingUp
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

export default function BuyCreditsPage() {
  const [selectedPackage, setSelectedPackage] = useState<number | null>(null);
  const [customAmount, setCustomAmount] = useState('');
  const [step, setStep] = useState<'select' | 'payment' | 'confirm'>('select');

  const packages = [
    {
      id: 1,
      name: 'Starter',
      credits: 1000,
      price: 10,
      popular: false,
      description: 'Perfect for testing',
      features: [
        '~100 LLM API calls',
        'All providers available',
        'No expiration',
        'Email support',
      ],
      color: 'from-blue-500/20 to-blue-600/20',
      borderColor: 'border-blue-500/30',
    },
    {
      id: 2,
      name: 'Pro',
      credits: 5000,
      price: 49,
      popular: true,
      description: 'Most popular choice',
      features: [
        '~500 LLM API calls',
        'All providers available',
        'Priority support',
        'No expiration',
        '2% bonus credits',
      ],
      color: 'from-primary/20 to-primary/30',
      borderColor: 'border-primary',
    },
    {
      id: 3,
      name: 'Business',
      credits: 10000,
      price: 95,
      popular: false,
      description: 'For growing teams',
      features: [
        '~1,000 LLM API calls',
        'All providers available',
        'Priority support',
        'No expiration',
        '5% bonus credits',
      ],
      color: 'from-purple-500/20 to-purple-600/20',
      borderColor: 'border-purple-500/30',
    },
    {
      id: 4,
      name: 'Enterprise',
      credits: 50000,
      price: 450,
      popular: false,
      description: 'For large organizations',
      features: [
        '~5,000 LLM API calls',
        'All providers available',
        'Dedicated support',
        'No expiration',
        '10% bonus credits',
        'Custom billing',
      ],
      color: 'from-orange-500/20 to-orange-600/20',
      borderColor: 'border-orange-500/30',
    },
  ];

  const handleSelectPackage = (packageId: number) => {
    setSelectedPackage(packageId);
    setCustomAmount('');
  };

  const handleProceedToPayment = () => {
    if (selectedPackage || customAmount) {
      setStep('payment');
    }
  };

  const selectedPkg = packages.find((p) => p.id === selectedPackage);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Buy Credits</h1>
          <p className="text-muted-foreground mt-1">
            Choose a package or enter a custom amount
          </p>
        </div>
        {step === 'select' && (
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <Shield className="h-4 w-4 text-green-500" />
            <span>Secured by Stripe</span>
          </div>
        )}
      </div>

      {/* Step Indicator */}
      <div className="flex items-center justify-center space-x-4">
        <div className={`flex items-center space-x-2 ${step === 'select' ? 'text-primary' : 'text-muted-foreground'}`}>
          <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step === 'select' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
            1
          </div>
          <span className="font-medium">Select Package</span>
        </div>
        <ArrowRight className="h-4 w-4 text-muted-foreground" />
        <div className={`flex items-center space-x-2 ${step === 'payment' ? 'text-primary' : 'text-muted-foreground'}`}>
          <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step === 'payment' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
            2
          </div>
          <span className="font-medium">Payment</span>
        </div>
        <ArrowRight className="h-4 w-4 text-muted-foreground" />
        <div className={`flex items-center space-x-2 ${step === 'confirm' ? 'text-primary' : 'text-muted-foreground'}`}>
          <div className={`flex items-center justify-center w-8 h-8 rounded-full ${step === 'confirm' ? 'bg-primary text-primary-foreground' : 'bg-muted'}`}>
            3
          </div>
          <span className="font-medium">Confirm</span>
        </div>
      </div>

      {/* Step 1: Select Package */}
      {step === 'select' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Credit Packages */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {packages.map((pkg, index) => (
              <motion.div
                key={pkg.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card
                  className={`backdrop-blur-xl bg-gradient-to-br ${pkg.color} border-2 ${
                    selectedPackage === pkg.id ? pkg.borderColor : 'border-border/50'
                  } hover:border-primary/50 transition-all rounded-2xl cursor-pointer relative overflow-hidden`}
                  onClick={() => handleSelectPackage(pkg.id)}
                >
                  {pkg.popular && (
                    <div className="absolute top-0 right-0 bg-primary text-primary-foreground px-3 py-1 text-xs font-medium rounded-bl-xl">
                      Most Popular
                    </div>
                  )}
                  <CardContent className="p-6">
                    <div className="mb-4">
                      <h3 className="font-bold text-2xl mb-1">{pkg.name}</h3>
                      <p className="text-sm text-muted-foreground">{pkg.description}</p>
                    </div>

                    <div className="mb-6">
                      <div className="flex items-baseline space-x-2">
                        <span className="text-4xl font-bold">${pkg.price}</span>
                        <span className="text-muted-foreground">USD</span>
                      </div>
                      <p className="text-sm text-muted-foreground mt-1">
                        {pkg.credits.toLocaleString()} credits
                      </p>
                    </div>

                    <div className="space-y-2 mb-6">
                      {pkg.features.map((feature, i) => (
                        <div key={i} className="flex items-start space-x-2 text-sm">
                          <Check className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span>{feature}</span>
                        </div>
                      ))}
                    </div>

                    <Button
                      className={`w-full rounded-full ${
                        selectedPackage === pkg.id
                          ? 'bg-primary'
                          : 'bg-muted hover:bg-muted/80'
                      }`}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleSelectPackage(pkg.id);
                      }}
                    >
                      {selectedPackage === pkg.id ? (
                        <>
                          <Check className="mr-2 h-4 w-4" />
                          Selected
                        </>
                      ) : (
                        'Select Package'
                      )}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>

          {/* Custom Amount */}
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Custom Amount</CardTitle>
              <CardDescription>
                Enter a custom amount if you need a different quantity
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="flex items-end space-x-4">
                <div className="flex-1">
                  <Label htmlFor="custom-amount" className="mb-2 block">
                    Amount (USD)
                  </Label>
                  <Input
                    id="custom-amount"
                    type="number"
                    placeholder="Enter amount"
                    value={customAmount}
                    onChange={(e) => {
                      setCustomAmount(e.target.value);
                      setSelectedPackage(null);
                    }}
                    className="rounded-lg"
                    min="10"
                  />
                </div>
                <div className="flex-1">
                  <Label className="mb-2 block">Credits</Label>
                  <div className="h-10 px-3 rounded-lg bg-muted flex items-center">
                    <span className="font-medium">
                      {customAmount ? (parseInt(customAmount) * 100).toLocaleString() : '0'} credits
                    </span>
                  </div>
                </div>
              </div>
              <p className="text-sm text-muted-foreground mt-3">
                Rate: $1 = 100 credits • Minimum: $10
              </p>
            </CardContent>
          </Card>

          {/* Proceed Button */}
          <div className="flex justify-center">
            <Button
              size="lg"
              className="rounded-full px-8"
              disabled={!selectedPackage && !customAmount}
              onClick={handleProceedToPayment}
            >
              Proceed to Payment
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>

          {/* Security Features */}
          <div className="grid gap-4 md:grid-cols-3">
            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
              <CardContent className="p-4 flex items-center space-x-3">
                <div className="bg-green-500/10 p-2 rounded-lg">
                  <Shield className="h-5 w-5 text-green-500" />
                </div>
                <div>
                  <p className="font-medium text-sm">Secure Payment</p>
                  <p className="text-xs text-muted-foreground">PCI-DSS compliant</p>
                </div>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
              <CardContent className="p-4 flex items-center space-x-3">
                <div className="bg-blue-500/10 p-2 rounded-lg">
                  <Lock className="h-5 w-5 text-blue-500" />
                </div>
                <div>
                  <p className="font-medium text-sm">Encrypted</p>
                  <p className="text-xs text-muted-foreground">256-bit SSL</p>
                </div>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
              <CardContent className="p-4 flex items-center space-x-3">
                <div className="bg-purple-500/10 p-2 rounded-lg">
                  <Zap className="h-5 w-5 text-purple-500" />
                </div>
                <div>
                  <p className="font-medium text-sm">Instant Delivery</p>
                  <p className="text-xs text-muted-foreground">Credits added immediately</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </motion.div>
      )}

      {/* Step 2: Payment */}
      {step === 'payment' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-2xl mx-auto space-y-6"
        >
          {/* Order Summary */}
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Order Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Package</span>
                  <span className="font-medium">
                    {selectedPkg?.name || 'Custom Amount'}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">Credits</span>
                  <span className="font-medium">
                    {selectedPkg
                      ? selectedPkg.credits.toLocaleString()
                      : customAmount
                      ? (parseInt(customAmount) * 100).toLocaleString()
                      : '0'}
                  </span>
                </div>
                <div className="flex items-center justify-between pt-3 border-t border-border/50">
                  <span className="font-semibold text-lg">Total</span>
                  <span className="font-bold text-2xl">
                    ${selectedPkg?.price || customAmount || '0'}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Payment Form */}
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Payment Details</CardTitle>
              <CardDescription>
                Enter your payment information securely
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Stripe Elements will be integrated here */}
              <div className="p-8 rounded-xl border-2 border-dashed border-border/50 text-center">
                <CreditCard className="h-12 w-12 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-muted-foreground">
                  Stripe payment form will be integrated here
                </p>
                <p className="text-xs text-muted-foreground mt-2">
                  (Requires Stripe publishable key)
                </p>
              </div>

              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Lock className="h-4 w-4" />
                <span>Your payment information is encrypted and secure</span>
              </div>
            </CardContent>
          </Card>

          {/* Action Buttons */}
          <div className="flex items-center justify-between">
            <Button
              variant="outline"
              onClick={() => setStep('select')}
              className="rounded-full"
            >
              Back
            </Button>
            <Button
              size="lg"
              className="rounded-full px-8"
              onClick={() => setStep('confirm')}
            >
              Complete Payment
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
          </div>
        </motion.div>
      )}

      {/* Step 3: Confirmation */}
      {step === 'confirm' && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-lg mx-auto"
        >
          <Card className="backdrop-blur-xl bg-gradient-to-br from-green-500/10 to-green-600/10 border-2 border-green-500/30 rounded-2xl text-center">
            <CardContent className="p-12">
              <div className="mb-6">
                <div className="relative inline-block">
                  <div className="absolute inset-0 bg-green-500/20 blur-2xl rounded-full" />
                  <div className="relative bg-green-500/20 p-6 rounded-full">
                    <Sparkles className="h-16 w-16 text-green-500" />
                  </div>
                </div>
              </div>

              <h2 className="text-3xl font-bold mb-3">Payment Successful!</h2>
              <p className="text-muted-foreground mb-6">
                Your credits have been added to your account
              </p>

              <div className="bg-background/50 rounded-xl p-6 mb-6">
                <div className="flex items-center justify-between mb-3">
                  <span className="text-muted-foreground">Credits Added</span>
                  <span className="font-bold text-2xl text-green-500">
                    +{selectedPkg?.credits.toLocaleString() || (customAmount ? (parseInt(customAmount) * 100).toLocaleString() : '0')}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-muted-foreground">New Balance</span>
                  <span className="font-semibold text-xl">
                    {(12450 + (selectedPkg?.credits || 0)).toLocaleString()}
                  </span>
                </div>
              </div>

              <div className="flex flex-col space-y-3">
                <Button
                  size="lg"
                  className="rounded-full"
                  onClick={() => window.location.href = '/dashboard/credits'}
                >
                  <TrendingUp className="mr-2 h-5 w-5" />
                  View Credits
                </Button>
                <Button
                  variant="outline"
                  className="rounded-full"
                  onClick={() => setStep('select')}
                >
                  Buy More Credits
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}
