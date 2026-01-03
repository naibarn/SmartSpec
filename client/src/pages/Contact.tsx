/**
 * Contact Page - SmartSpec Pro
 * Contact form with support options
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { toast } from 'sonner';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import {
  Mail,
  MessageSquare,
  Phone,
  MapPin,
  Send,
  Clock,
  CheckCircle,
  HelpCircle,
  Bug,
  Lightbulb,
  Building2,
} from 'lucide-react';

type ContactType = 'general' | 'support' | 'sales' | 'bug' | 'feature';

interface ContactTypeOption {
  id: ContactType;
  label: string;
  icon: React.ReactNode;
  description: string;
}

const contactTypes: ContactTypeOption[] = [
  {
    id: 'general',
    label: 'General Inquiry',
    icon: <MessageSquare className="w-5 h-5" />,
    description: 'Questions about SmartSpec Pro',
  },
  {
    id: 'support',
    label: 'Technical Support',
    icon: <HelpCircle className="w-5 h-5" />,
    description: 'Help with your account or features',
  },
  {
    id: 'sales',
    label: 'Sales & Enterprise',
    icon: <Building2 className="w-5 h-5" />,
    description: 'Pricing, plans, and enterprise solutions',
  },
  {
    id: 'bug',
    label: 'Report a Bug',
    icon: <Bug className="w-5 h-5" />,
    description: 'Found something not working?',
  },
  {
    id: 'feature',
    label: 'Feature Request',
    icon: <Lightbulb className="w-5 h-5" />,
    description: 'Suggest new features or improvements',
  },
];

const contactInfo = [
  {
    icon: <Mail className="w-6 h-6" />,
    title: 'Email',
    value: 'support@smartspec.pro',
    link: 'mailto:support@smartspec.pro',
  },
  {
    icon: <Phone className="w-6 h-6" />,
    title: 'Phone',
    value: '+1 (555) 123-4567',
    link: 'tel:+15551234567',
  },
  {
    icon: <MapPin className="w-6 h-6" />,
    title: 'Office',
    value: 'San Francisco, CA',
    link: null,
  },
  {
    icon: <Clock className="w-6 h-6" />,
    title: 'Response Time',
    value: 'Within 24 hours',
    link: null,
  },
];

export default function Contact() {
  const [selectedType, setSelectedType] = useState<ContactType>('general');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    subject: '',
    message: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 1500));

    setIsSubmitting(false);
    setIsSubmitted(true);
    toast.success('Message sent successfully! We\'ll get back to you soon.');

    // Reset form after delay
    setTimeout(() => {
      setIsSubmitted(false);
      setFormData({
        name: '',
        email: '',
        company: '',
        subject: '',
        message: '',
      });
    }, 3000);
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20">
      <Navbar />

      {/* Hero Section */}
      <section className="pt-32 pb-16 px-4">
        <div className="container max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm border border-purple-100 text-sm text-purple-600 mb-6">
              <MessageSquare className="w-4 h-4" />
              We'd love to hear from you
            </span>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Get in{' '}
              <span className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
                Touch
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Have questions about SmartSpec Pro? Our team is here to help you
              build amazing applications faster.
            </p>
          </motion.div>
        </div>
      </section>

      {/* Contact Info Cards */}
      <section className="py-8 px-4">
        <div className="container max-w-6xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {contactInfo.map((info, index) => (
              <motion.div
                key={info.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
              >
                {info.link ? (
                  <a
                    href={info.link}
                    className="block p-6 bg-white/60 backdrop-blur-sm rounded-2xl border border-white/50 shadow-lg shadow-purple-500/5 hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-300 group"
                  >
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white mb-4 group-hover:scale-110 transition-transform">
                      {info.icon}
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {info.title}
                    </h3>
                    <p className="text-gray-600 text-sm">{info.value}</p>
                  </a>
                ) : (
                  <div className="p-6 bg-white/60 backdrop-blur-sm rounded-2xl border border-white/50 shadow-lg shadow-purple-500/5">
                    <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white mb-4">
                      {info.icon}
                    </div>
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {info.title}
                    </h3>
                    <p className="text-gray-600 text-sm">{info.value}</p>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Form Section */}
      <section className="py-16 px-4">
        <div className="container max-w-6xl mx-auto">
          <div className="grid lg:grid-cols-3 gap-8">
            {/* Contact Type Selector */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              className="lg:col-span-1"
            >
              <h2 className="text-2xl font-bold text-gray-900 mb-6">
                How can we help?
              </h2>
              <div className="space-y-3">
                {contactTypes.map((type) => (
                  <button
                    key={type.id}
                    onClick={() => setSelectedType(type.id)}
                    className={`w-full p-4 rounded-xl text-left transition-all duration-300 ${
                      selectedType === type.id
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg shadow-purple-500/30'
                        : 'bg-white/60 backdrop-blur-sm border border-white/50 hover:border-purple-200 hover:shadow-md'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div
                        className={`${
                          selectedType === type.id
                            ? 'text-white'
                            : 'text-purple-500'
                        }`}
                      >
                        {type.icon}
                      </div>
                      <div>
                        <h3
                          className={`font-semibold ${
                            selectedType === type.id
                              ? 'text-white'
                              : 'text-gray-900'
                          }`}
                        >
                          {type.label}
                        </h3>
                        <p
                          className={`text-sm ${
                            selectedType === type.id
                              ? 'text-white/80'
                              : 'text-gray-500'
                          }`}
                        >
                          {type.description}
                        </p>
                      </div>
                    </div>
                  </button>
                ))}
              </div>
            </motion.div>

            {/* Contact Form */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="lg:col-span-2"
            >
              <div className="bg-white/70 backdrop-blur-xl rounded-3xl border border-white/50 shadow-xl shadow-purple-500/10 p-8">
                {isSubmitted ? (
                  <motion.div
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="text-center py-16"
                  >
                    <div className="w-20 h-20 rounded-full bg-gradient-to-br from-green-400 to-emerald-500 flex items-center justify-center mx-auto mb-6">
                      <CheckCircle className="w-10 h-10 text-white" />
                    </div>
                    <h3 className="text-2xl font-bold text-gray-900 mb-2">
                      Message Sent!
                    </h3>
                    <p className="text-gray-600">
                      Thank you for reaching out. We'll get back to you within
                      24 hours.
                    </p>
                  </motion.div>
                ) : (
                  <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Your Name *
                        </label>
                        <Input
                          name="name"
                          value={formData.name}
                          onChange={handleChange}
                          placeholder="John Doe"
                          required
                          className="bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Email Address *
                        </label>
                        <Input
                          name="email"
                          type="email"
                          value={formData.email}
                          onChange={handleChange}
                          placeholder="john@example.com"
                          required
                          className="bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                        />
                      </div>
                    </div>

                    <div className="grid md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Company (Optional)
                        </label>
                        <Input
                          name="company"
                          value={formData.company}
                          onChange={handleChange}
                          placeholder="Your Company"
                          className="bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                          Subject *
                        </label>
                        <Input
                          name="subject"
                          value={formData.subject}
                          onChange={handleChange}
                          placeholder="How can we help?"
                          required
                          className="bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400"
                        />
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        Message *
                      </label>
                      <Textarea
                        name="message"
                        value={formData.message}
                        onChange={handleChange}
                        placeholder="Tell us more about your inquiry..."
                        rows={6}
                        required
                        className="bg-white/50 border-gray-200 focus:border-purple-400 focus:ring-purple-400 resize-none"
                      />
                    </div>

                    <div className="flex items-center justify-between pt-4">
                      <p className="text-sm text-gray-500">
                        * Required fields
                      </p>
                      <Button
                        type="submit"
                        disabled={isSubmitting}
                        className="bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white px-8 py-3 rounded-xl shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-300"
                      >
                        {isSubmitting ? (
                          <>
                            <span className="animate-spin mr-2">⏳</span>
                            Sending...
                          </>
                        ) : (
                          <>
                            <Send className="w-4 h-4 mr-2" />
                            Send Message
                          </>
                        )}
                      </Button>
                    </div>
                  </form>
                )}
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="py-16 px-4">
        <div className="container max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h2>
            <p className="text-gray-600">
              Quick answers to common questions
            </p>
          </motion.div>

          <div className="space-y-4">
            {[
              {
                q: 'How quickly will I receive a response?',
                a: 'We typically respond to all inquiries within 24 hours during business days. For urgent technical issues, Pro and Enterprise customers receive priority support.',
              },
              {
                q: 'Do you offer phone support?',
                a: 'Phone support is available for Enterprise customers. All other plans have access to email and chat support.',
              },
              {
                q: 'Can I schedule a demo?',
                a: 'Yes! Select "Sales & Enterprise" from the contact options and mention you\'d like a demo in your message. We\'ll set up a personalized walkthrough.',
              },
              {
                q: 'Where can I find documentation?',
                a: 'Visit our Docs page for comprehensive guides, API references, and tutorials. You can also search our knowledge base for specific topics.',
              },
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="bg-white/60 backdrop-blur-sm rounded-2xl border border-white/50 p-6"
              >
                <h3 className="font-semibold text-gray-900 mb-2">{faq.q}</h3>
                <p className="text-gray-600">{faq.a}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
