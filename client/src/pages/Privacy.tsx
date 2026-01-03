/**
 * Privacy Policy Page - SmartSpec Pro
 * Data privacy and protection policies
 */

import { motion } from 'framer-motion';
import { Link } from 'wouter';
import { ArrowLeft, Shield, Eye, Database, Lock, Globe, Bell, Trash2, UserCheck } from 'lucide-react';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';

const sections = [
  {
    id: 'introduction',
    title: '1. Introduction',
    icon: Shield,
    content: `SmartSpec Pro ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our AI-powered code generation platform.

Please read this privacy policy carefully. By using SmartSpec Pro, you consent to the data practices described in this policy. If you do not agree with the terms of this privacy policy, please do not access the Service.`
  },
  {
    id: 'information-collected',
    title: '2. Information We Collect',
    icon: Database,
    content: `**Personal Information**
We may collect personal information that you voluntarily provide, including:
• Name and email address
• Company name and job title
• Billing and payment information
• Profile picture and preferences
• Communication preferences

**Usage Data**
We automatically collect certain information when you use the Service:
• Device information (browser type, operating system, device identifiers)
• IP address and approximate location
• Pages visited and features used
• Time spent on the Service
• Referral sources

**Generated Content**
We may collect and process:
• Code and prompts you submit for generation
• Generated outputs and results
• Project configurations and settings
• Feedback and ratings you provide`
  },
  {
    id: 'how-we-use',
    title: '3. How We Use Your Information',
    icon: Eye,
    content: `We use the information we collect to:

**Provide and Improve Services**
• Process your requests and generate code
• Personalize your experience
• Improve our AI models and algorithms
• Develop new features and services

**Communication**
• Send transactional emails (receipts, notifications)
• Provide customer support
• Send marketing communications (with your consent)
• Notify you of updates and changes

**Security and Compliance**
• Detect and prevent fraud or abuse
• Enforce our Terms of Service
• Comply with legal obligations
• Protect the rights and safety of users

**Analytics**
• Analyze usage patterns and trends
• Measure the effectiveness of features
• Generate aggregated, anonymized insights`
  },
  {
    id: 'data-sharing',
    title: '4. How We Share Your Information',
    icon: Globe,
    content: `We may share your information in the following circumstances:

**Service Providers**
We share data with third-party vendors who help us operate the Service:
• Cloud hosting providers (AWS, Google Cloud)
• Payment processors (Stripe)
• Analytics services
• Customer support tools
• Email delivery services

**Legal Requirements**
We may disclose information when required by law or to:
• Comply with legal processes
• Respond to government requests
• Protect our rights and property
• Prevent fraud or security threats

**Business Transfers**
In the event of a merger, acquisition, or sale of assets, your information may be transferred to the acquiring entity.

**With Your Consent**
We may share your information for other purposes with your explicit consent.

**We Do NOT Sell Your Data**
We do not sell, rent, or trade your personal information to third parties for their marketing purposes.`
  },
  {
    id: 'data-security',
    title: '5. Data Security',
    icon: Lock,
    content: `We implement robust security measures to protect your information:

**Technical Safeguards**
• Encryption in transit (TLS/SSL) and at rest (AES-256)
• Secure authentication with multi-factor authentication options
• Regular security audits and penetration testing
• Automated vulnerability scanning
• Access controls and logging

**Organizational Measures**
• Employee security training
• Background checks for personnel with data access
• Incident response procedures
• Regular security policy reviews

**Infrastructure Security**
• SOC 2 Type II compliant data centers
• Redundant systems and backups
• DDoS protection
• Network segmentation

While we strive to protect your information, no method of transmission over the Internet is 100% secure. We cannot guarantee absolute security.`
  },
  {
    id: 'data-retention',
    title: '6. Data Retention',
    icon: Database,
    content: `We retain your information for as long as necessary to:

• Provide the Service and fulfill the purposes described in this policy
• Comply with legal obligations
• Resolve disputes and enforce agreements
• Maintain business records

**Retention Periods**
• Account data: Retained while your account is active, plus 30 days after deletion
• Usage logs: 90 days
• Payment records: 7 years (legal requirement)
• Generated content: 30 days after deletion (unless saved to your account)
• Marketing preferences: Until you unsubscribe

You can request deletion of your data at any time through your account settings or by contacting us.`
  },
  {
    id: 'your-rights',
    title: '7. Your Privacy Rights',
    icon: UserCheck,
    content: `Depending on your location, you may have the following rights:

**Access and Portability**
• Request a copy of your personal data
• Receive your data in a portable format

**Correction**
• Update or correct inaccurate information
• Complete incomplete data

**Deletion**
• Request deletion of your personal data
• "Right to be forgotten" (where applicable)

**Restriction and Objection**
• Restrict processing of your data
• Object to certain processing activities
• Opt out of marketing communications

**Withdraw Consent**
• Withdraw previously given consent
• This does not affect prior lawful processing

**To Exercise Your Rights**
Contact us at privacy@smartspec.pro or use the settings in your account dashboard. We will respond within 30 days.`
  },
  {
    id: 'cookies',
    title: '8. Cookies and Tracking',
    icon: Eye,
    content: `We use cookies and similar technologies to:

**Essential Cookies**
• Maintain your session and authentication
• Remember your preferences
• Ensure security

**Analytics Cookies**
• Understand how you use the Service
• Measure feature effectiveness
• Improve user experience

**Marketing Cookies** (with consent)
• Deliver relevant advertisements
• Measure ad campaign effectiveness

**Managing Cookies**
You can control cookies through:
• Browser settings
• Our cookie preference center
• Opt-out links in marketing emails

Note that disabling certain cookies may affect Service functionality.`
  },
  {
    id: 'international',
    title: '9. International Data Transfers',
    icon: Globe,
    content: `Your information may be transferred to and processed in countries other than your own. We ensure appropriate safeguards are in place:

**Transfer Mechanisms**
• Standard Contractual Clauses (SCCs)
• Data Processing Agreements with vendors
• Compliance with applicable data protection laws

**EU/EEA Users**
For users in the European Economic Area, we comply with GDPR requirements for international transfers.

**California Residents**
We comply with the California Consumer Privacy Act (CCPA) and California Privacy Rights Act (CPRA).`
  },
  {
    id: 'children',
    title: '10. Children\'s Privacy',
    icon: Shield,
    content: `SmartSpec Pro is not intended for users under 18 years of age. We do not knowingly collect personal information from children.

If we learn that we have collected information from a child under 18, we will promptly delete that information. If you believe we have collected information from a child, please contact us immediately at privacy@smartspec.pro.`
  },
  {
    id: 'changes',
    title: '11. Changes to This Policy',
    icon: Bell,
    content: `We may update this Privacy Policy from time to time. We will notify you of changes by:

• Posting the new policy on this page
• Updating the "Last Updated" date
• Sending an email notification for material changes
• Displaying a notice in the Service

We encourage you to review this policy periodically. Your continued use of the Service after changes constitutes acceptance of the updated policy.`
  },
  {
    id: 'contact',
    title: '12. Contact Us',
    icon: Shield,
    content: `If you have questions or concerns about this Privacy Policy or our data practices, please contact us:

**Data Protection Officer**
Email: privacy@smartspec.pro

**General Inquiries**
Email: support@smartspec.pro
Contact Form: https://smartspec.pro/contact

**Mailing Address**
SmartSpec Pro Privacy Team
[Address will be provided upon request]

We aim to respond to all privacy-related inquiries within 30 days.`
  }
];

export default function Privacy() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20">
      <Navbar />
      
      <main className="pt-24 pb-20">
        <div className="container max-w-4xl">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-12"
          >
            <Link href="/" className="inline-flex items-center gap-2 text-gray-600 hover:text-purple-600 mb-6 transition-colors">
              <ArrowLeft className="w-4 h-4" />
              Back to Home
            </Link>
            
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-teal-500 to-emerald-500 flex items-center justify-center">
                <Shield className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-3xl md:text-4xl font-bold text-gray-900">
                  Privacy Policy
                </h1>
                <p className="text-gray-500">Last Updated: January 3, 2025</p>
              </div>
            </div>
            
            <p className="text-lg text-gray-600">
              Your privacy is important to us. This policy explains how we collect, use, and protect 
              your personal information when you use SmartSpec Pro.
            </p>
          </motion.div>

          {/* Quick Summary */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-gradient-to-br from-teal-50 to-emerald-50 rounded-2xl p-6 border border-teal-100 mb-8"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <Eye className="w-5 h-5 text-teal-600" />
              Privacy at a Glance
            </h2>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="flex items-start gap-2">
                <Lock className="w-4 h-4 text-teal-600 mt-0.5" />
                <span className="text-gray-600">Your data is encrypted and secure</span>
              </div>
              <div className="flex items-start gap-2">
                <Trash2 className="w-4 h-4 text-teal-600 mt-0.5" />
                <span className="text-gray-600">You can delete your data anytime</span>
              </div>
              <div className="flex items-start gap-2">
                <Globe className="w-4 h-4 text-teal-600 mt-0.5" />
                <span className="text-gray-600">We don't sell your personal data</span>
              </div>
              <div className="flex items-start gap-2">
                <UserCheck className="w-4 h-4 text-teal-600 mt-0.5" />
                <span className="text-gray-600">You control your privacy settings</span>
              </div>
            </div>
          </motion.div>

          {/* Table of Contents */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.15 }}
            className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 border border-gray-100 mb-8"
          >
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Table of Contents</h2>
            <div className="grid md:grid-cols-2 gap-2">
              {sections.map((section) => (
                <a
                  key={section.id}
                  href={`#${section.id}`}
                  className="text-gray-600 hover:text-teal-600 transition-colors text-sm py-1"
                >
                  {section.title}
                </a>
              ))}
            </div>
          </motion.div>

          {/* Content Sections */}
          <div className="space-y-8">
            {sections.map((section, index) => (
              <motion.section
                key={section.id}
                id={section.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 + index * 0.05 }}
                className="bg-white/80 backdrop-blur-sm rounded-2xl p-6 md:p-8 border border-gray-100"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-10 h-10 rounded-lg bg-teal-100 flex items-center justify-center">
                    <section.icon className="w-5 h-5 text-teal-600" />
                  </div>
                  <h2 className="text-xl font-semibold text-gray-900">{section.title}</h2>
                </div>
                <div className="prose prose-gray max-w-none">
                  {section.content.split('\n\n').map((paragraph, pIndex) => (
                    <p key={pIndex} className="text-gray-600 whitespace-pre-line mb-4 last:mb-0">
                      {paragraph}
                    </p>
                  ))}
                </div>
              </motion.section>
            ))}
          </div>

          {/* Footer Note */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.8 }}
            className="mt-12 text-center"
          >
            <p className="text-gray-500 text-sm">
              By using SmartSpec Pro, you acknowledge that you have read and understood this Privacy Policy.
            </p>
            <div className="flex justify-center gap-4 mt-4">
              <Link href="/terms" className="text-teal-600 hover:text-teal-700 font-medium">
                Terms of Service
              </Link>
              <span className="text-gray-300">|</span>
              <Link href="/contact" className="text-teal-600 hover:text-teal-700 font-medium">
                Contact Us
              </Link>
            </div>
          </motion.div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
