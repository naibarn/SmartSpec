import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  CreditCard,
  Download,
  MoreVertical,
  Plus,
  CheckCircle2,
  Clock,
  XCircle,
  FileText,
  Calendar,
  DollarSign
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';

export default function PaymentsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterStatus, setFilterStatus] = useState('all');

  // Mock data
  const paymentMethods = [
    {
      id: 1,
      type: 'visa',
      last4: '4242',
      expiry: '12/25',
      isDefault: true,
    },
    {
      id: 2,
      type: 'mastercard',
      last4: '5555',
      expiry: '08/26',
      isDefault: false,
    },
  ];

  const transactions = [
    {
      id: 'inv_001',
      date: '2025-01-15',
      description: 'Pro Package - 5,000 credits',
      amount: 49.00,
      status: 'paid',
      paymentMethod: 'Visa •••• 4242',
      invoice: true,
    },
    {
      id: 'inv_002',
      date: '2025-01-10',
      description: 'Starter Package - 1,000 credits',
      amount: 10.00,
      status: 'paid',
      paymentMethod: 'Visa •••• 4242',
      invoice: true,
    },
    {
      id: 'inv_003',
      date: '2025-01-05',
      description: 'Custom Amount - 2,500 credits',
      amount: 25.00,
      status: 'paid',
      paymentMethod: 'Mastercard •••• 5555',
      invoice: true,
    },
    {
      id: 'inv_004',
      date: '2024-12-28',
      description: 'Business Package - 10,000 credits',
      amount: 95.00,
      status: 'paid',
      paymentMethod: 'Visa •••• 4242',
      invoice: true,
    },
    {
      id: 'inv_005',
      date: '2024-12-20',
      description: 'Pro Package - 5,000 credits',
      amount: 49.00,
      status: 'refunded',
      paymentMethod: 'Visa •••• 4242',
      invoice: true,
    },
    {
      id: 'inv_006',
      date: '2024-12-15',
      description: 'Starter Package - 1,000 credits',
      amount: 10.00,
      status: 'pending',
      paymentMethod: 'Visa •••• 4242',
      invoice: false,
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'paid':
        return 'text-green-500 bg-green-500/10';
      case 'pending':
        return 'text-orange-500 bg-orange-500/10';
      case 'refunded':
        return 'text-blue-500 bg-blue-500/10';
      case 'failed':
        return 'text-red-500 bg-red-500/10';
      default:
        return 'text-gray-500 bg-gray-500/10';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'paid':
        return <CheckCircle2 className="h-4 w-4" />;
      case 'pending':
        return <Clock className="h-4 w-4" />;
      case 'refunded':
      case 'failed':
        return <XCircle className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const getCardIcon = () => {
    // In real app, use actual card brand icons based on type
    return <CreditCard className="h-6 w-6" />;
  };

  const filteredTransactions = transactions.filter((t) => {
    const matchesSearch = t.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      t.id.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesFilter = filterStatus === 'all' || t.status === filterStatus;
    return matchesSearch && matchesFilter;
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Payments & Billing</h1>
          <p className="text-muted-foreground mt-1">
            Manage payment methods and view billing history
          </p>
        </div>
        <Button className="rounded-full">
          <Plus className="mr-2 h-4 w-4" />
          Add Payment Method
        </Button>
      </div>

      {/* Payment Methods */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Payment Methods</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {paymentMethods.map((method, index) => (
            <motion.div
              key={method.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className={`backdrop-blur-xl bg-card/50 border-2 ${
                method.isDefault ? 'border-primary' : 'border-border/50'
              } hover:border-primary/50 transition-all rounded-2xl`}>
                <CardContent className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="bg-primary/10 p-3 rounded-xl">
                      {getCardIcon()}
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                          <MoreVertical className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        {!method.isDefault && (
                          <DropdownMenuItem>Set as Default</DropdownMenuItem>
                        )}
                        <DropdownMenuItem>Edit</DropdownMenuItem>
                        <DropdownMenuItem className="text-red-500">
                          Remove
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Card Number</span>
                      <span className="font-medium">•••• {method.last4}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-muted-foreground">Expires</span>
                      <span className="font-medium">{method.expiry}</span>
                    </div>
                  </div>

                  {method.isDefault && (
                    <div className="mt-4 pt-4 border-t border-border/50">
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-primary/20 text-primary">
                        Default
                      </span>
                    </div>
                  )}
                </CardContent>
              </Card>
            </motion.div>
          ))}

          {/* Add New Card */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: paymentMethods.length * 0.1 }}
          >
            <Card className="backdrop-blur-xl bg-card/50 border-2 border-dashed border-border/50 hover:border-primary/50 transition-all rounded-2xl cursor-pointer h-full">
              <CardContent className="p-6 flex flex-col items-center justify-center h-full min-h-[180px]">
                <div className="bg-primary/10 p-3 rounded-xl mb-3">
                  <Plus className="h-6 w-6 text-primary" />
                </div>
                <p className="font-medium">Add New Card</p>
                <p className="text-sm text-muted-foreground">
                  Visa, Mastercard, Amex
                </p>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>

      {/* Billing History */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Billing History</h2>
        
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Transactions</CardTitle>
                <CardDescription>View and download your invoices</CardDescription>
              </div>
              <Button variant="outline" className="rounded-full">
                <Download className="mr-2 h-4 w-4" />
                Export All
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {/* Filters */}
            <div className="flex items-center space-x-4 mb-6">
              <div className="flex-1">
                <Input
                  placeholder="Search transactions..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="rounded-lg"
                />
              </div>
              <Select value={filterStatus} onValueChange={setFilterStatus}>
                <SelectTrigger className="w-[180px] rounded-lg">
                  <SelectValue placeholder="Filter by status" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Status</SelectItem>
                  <SelectItem value="paid">Paid</SelectItem>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="refunded">Refunded</SelectItem>
                  <SelectItem value="failed">Failed</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Transactions List */}
            <div className="space-y-3">
              {filteredTransactions.map((transaction, index) => (
                <motion.div
                  key={transaction.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05 }}
                  className="p-4 rounded-xl border border-border/50 hover:border-primary/50 transition-all"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      <div className="bg-primary/10 p-2 rounded-lg">
                        <FileText className="h-5 w-5 text-primary" />
                      </div>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <p className="font-medium">{transaction.description}</p>
                          <span className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-xs font-medium ${getStatusColor(transaction.status)}`}>
                            {getStatusIcon(transaction.status)}
                            <span className="capitalize">{transaction.status}</span>
                          </span>
                        </div>
                        <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                          <span className="flex items-center">
                            <Calendar className="h-3 w-3 mr-1" />
                            {new Date(transaction.date).toLocaleDateString('en-US', {
                              year: 'numeric',
                              month: 'short',
                              day: 'numeric',
                            })}
                          </span>
                          <span className="flex items-center">
                            <CreditCard className="h-3 w-3 mr-1" />
                            {transaction.paymentMethod}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            {transaction.id}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center space-x-4">
                      <div className="text-right">
                        <p className="font-semibold text-lg">
                          ${transaction.amount.toFixed(2)}
                        </p>
                      </div>
                      
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                            <MoreVertical className="h-4 w-4" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          {transaction.invoice && (
                            <>
                              <DropdownMenuItem>
                                <Download className="mr-2 h-4 w-4" />
                                Download Invoice
                              </DropdownMenuItem>
                              <DropdownMenuItem>
                                <FileText className="mr-2 h-4 w-4" />
                                View Details
                              </DropdownMenuItem>
                            </>
                          )}
                          {transaction.status === 'paid' && (
                            <DropdownMenuItem className="text-orange-500">
                              Request Refund
                            </DropdownMenuItem>
                          )}
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Pagination */}
            <div className="flex items-center justify-between mt-6 pt-6 border-t border-border/50">
              <p className="text-sm text-muted-foreground">
                Showing {filteredTransactions.length} of {transactions.length} transactions
              </p>
              <div className="flex items-center space-x-2">
                <Button variant="outline" size="sm" className="rounded-lg" disabled>
                  Previous
                </Button>
                <Button variant="outline" size="sm" className="rounded-lg">
                  Next
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-green-500/10 p-3 rounded-lg">
                <DollarSign className="h-6 w-6 text-green-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Spent</p>
                <p className="text-2xl font-bold">$238.00</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-500/10 p-3 rounded-lg">
                <FileText className="h-6 w-6 text-blue-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Invoices</p>
                <p className="text-2xl font-bold">6</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-orange-500/10 p-3 rounded-lg">
                <Calendar className="h-6 w-6 text-orange-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Last Payment</p>
                <p className="text-2xl font-bold">Jan 15</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
