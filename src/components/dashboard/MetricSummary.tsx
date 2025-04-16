
import React from 'react';
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Campaign } from '@/types/dashboard';

interface MetricSummaryProps {
  campaigns: Campaign[];
  metric: 'cpc' | 'cpm' | 'ctr' | 'cpa' | 'conversions' | 'spend';
  title: string;
  description?: string;
  formatValue?: (value: number) => string;
}

export function MetricSummary({
  campaigns,
  metric,
  title,
  description,
  formatValue,
}: MetricSummaryProps) {
  // Prepare data for chart
  const data = campaigns.map((campaign) => ({
    name: campaign.name.length > 20 ? campaign.name.substring(0, 20) + '...' : campaign.name,
    value: campaign.metrics[metric],
    platform: campaign.platform,
  }));

  // Sort data for better visualization
  data.sort((a, b) => b.value - a.value);

  // Default formatter
  const defaultFormatter = (value: number) => {
    if (metric === 'ctr') {
      return `${value.toFixed(2)}%`;
    } else if (['spend', 'cpc', 'cpm', 'cpa'].includes(metric)) {
      return `$${value.toFixed(2)}`;
    }
    return value.toLocaleString();
  };

  // Use provided formatter or default
  const formatter = formatValue || defaultFormatter;

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={data}
              layout="vertical"
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis 
                dataKey="name" 
                type="category" 
                width={150}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                formatter={(value: number) => [formatter(value), title]}
                labelFormatter={(label) => `Campaign: ${label}`}
              />
              <Bar 
                dataKey="value" 
                fill="#8884d8"
                name={title}
                // Use fill based on platform
                isAnimationActive={true}
                animationDuration={500}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
