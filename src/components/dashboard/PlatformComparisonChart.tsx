
import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PlatformComparison } from '@/types/dashboard';

interface PlatformComparisonChartProps {
  data: PlatformComparison[];
  metrics: ('spend' | 'impressions' | 'clicks' | 'conversions' | 'cpm' | 'cpc' | 'ctr' | 'cpa')[];
  title: string;
  description?: string;
}

export function PlatformComparisonChart({
  data,
  metrics,
  title,
  description,
}: PlatformComparisonChartProps) {
  // Transform data to show platforms as categories
  const transformedData = metrics.map((metric) => {
    const item: any = { metric };
    
    data.forEach((platform) => {
      let value = platform[metric];
      
      // Format percentage and monetary values
      if (metric === 'ctr') {
        value = Number(value.toFixed(2));
      } else if (['spend', 'cpm', 'cpc', 'cpa'].includes(metric)) {
        value = Number(value.toFixed(2));
      }
      
      item[platform.platform] = value;
    });
    
    return item;
  });

  const getMetricName = (metric: string) => {
    const metricNames: Record<string, string> = {
      'spend': 'Spend ($)',
      'impressions': 'Impressions',
      'clicks': 'Clicks',
      'conversions': 'Conversions',
      'cpm': 'CPM ($)',
      'cpc': 'CPC ($)',
      'ctr': 'CTR (%)',
      'cpa': 'CPA ($)',
    };
    
    return metricNames[metric] || metric;
  };

  const formatTooltipValue = (value: number, metric: string) => {
    if (['spend', 'cpm', 'cpc', 'cpa'].includes(metric)) {
      return `$${value.toFixed(2)}`;
    } else if (metric === 'ctr') {
      return `${value.toFixed(2)}%`;
    } else if (value > 1000) {
      return value.toLocaleString();
    }
    
    return value;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <div className="h-[400px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={transformedData}
              margin={{ top: 20, right: 30, left: 20, bottom: 30 }}
              layout="vertical"
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" />
              <YAxis 
                dataKey="metric" 
                type="category" 
                width={100}
                tickFormatter={getMetricName}
              />
              <Tooltip 
                formatter={(value: number, name: string, props: any) => {
                  return [formatTooltipValue(value, props.payload.metric), name === 'facebook' ? 'Facebook' : 'Google'];
                }}
                labelFormatter={(label) => getMetricName(label)}
              />
              <Legend />
              <Bar dataKey="facebook" fill="#4267B2" name="Facebook" />
              <Bar dataKey="google" fill="#DB4437" name="Google" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
