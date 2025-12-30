import { Card, CardContent } from '@/components/ui/card';
import { Construction } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  phase: string;
}

export function PlaceholderPage({ title, phase }: PlaceholderPageProps) {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{title}</h1>
        <p className="text-muted-foreground mt-1">
          This page will be implemented in {phase}
        </p>
      </div>

      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardContent className="p-12">
          <div className="text-center">
            <Construction className="h-16 w-16 text-muted-foreground mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-2">Coming Soon</h3>
            <p className="text-muted-foreground">
              This feature is under development and will be available soon.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
