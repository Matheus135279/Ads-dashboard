
import React from 'react';
import { Campaign } from '@/types/dashboard';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';

interface CampaignTableProps {
  campaigns: Campaign[];
}

export function CampaignTable({ campaigns }: CampaignTableProps) {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Campaign</TableHead>
            <TableHead>Platform</TableHead>
            <TableHead>Objective</TableHead>
            <TableHead className="text-right">Spend</TableHead>
            <TableHead className="text-right">Impressions</TableHead>
            <TableHead className="text-right">Clicks</TableHead>
            <TableHead className="text-right">CTR</TableHead>
            <TableHead className="text-right">Conv.</TableHead>
            <TableHead className="text-right">CPA</TableHead>
            <TableHead className="text-right">ROAS</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {campaigns.map((campaign) => (
            <TableRow key={campaign.id}>
              <TableCell className="font-medium">{campaign.name}</TableCell>
              <TableCell>
                <Badge variant={campaign.platform === 'facebook' ? 'secondary' : 'outline'}>
                  {campaign.platform === 'facebook' ? 'Facebook' : 'Google'}
                </Badge>
              </TableCell>
              <TableCell>
                <Badge variant="outline" className={cn(
                  campaign.objective === 'sales' && "bg-green-50 text-green-700 border-green-200",
                  campaign.objective === 'leads' && "bg-blue-50 text-blue-700 border-blue-200",
                  campaign.objective === 'traffic' && "bg-amber-50 text-amber-700 border-amber-200",
                  campaign.objective === 'awareness' && "bg-purple-50 text-purple-700 border-purple-200"
                )}>
                  {campaign.objective}
                </Badge>
              </TableCell>
              <TableCell className="text-right">${campaign.metrics.spend.toFixed(2)}</TableCell>
              <TableCell className="text-right">{campaign.metrics.impressions.toLocaleString()}</TableCell>
              <TableCell className="text-right">{campaign.metrics.clicks.toLocaleString()}</TableCell>
              <TableCell className="text-right">{campaign.metrics.ctr.toFixed(2)}%</TableCell>
              <TableCell className="text-right">{campaign.metrics.conversions}</TableCell>
              <TableCell className="text-right">${campaign.metrics.cpa.toFixed(2)}</TableCell>
              <TableCell className="text-right">{campaign.metrics.roas.toFixed(1)}x</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}

// Helper function for Badge styling
function cn(...classes: (string | boolean | undefined)[]) {
  return classes.filter(Boolean).join(' ');
}
