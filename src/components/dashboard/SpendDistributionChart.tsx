
import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Campaign } from '@/types/dashboard';

interface SpendDistributionChartProps {
  campaigns: Campaign[];
  title: string;
  description?: string;
}

export function SpendDistributionChart({
  campaigns,
  title,
  description,
}: SpendDistributionChartProps) {
  // Prepare data for pie chart
  const data = campaigns.map((campaign) => ({
    name: campaign.name,
    value: campaign.metrics.spend,
    platform: campaign.platform,
  }));

  // Colors based on platform
  const COLORS = {
    facebook: ['#4267B2', '#5b7bd5', '#8b9dc3', '#dfe3ee'],
    google: ['#DB4437', '#F4B400', '#0F9D58', '#4285F4'],
  };

  const getColor = (index: number, platform: 'facebook' | 'google') => {
    const colorSet = COLORS[platform];
    return colorSet[index % colorSet.length];
  };

  const formatTooltipValue = (value: number) => {
    return `$${value.toFixed(2)}`;
  };

  const calculatePercentage = (value: number) => {
    const total = campaigns.reduce((sum, campaign) => sum + campaign.metrics.spend, 0);
    return total > 0 ? `${((value / total) * 100).toFixed(1)}%` : '0%';
  };

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-2 border border-gray-200 rounded shadow-sm">
          <p className="font-medium">{data.name}</p>
          <p>{formatTooltipValue(data.value)} ({calculatePercentage(data.value)})</p>
          <p className="text-xs capitalize">{data.platform}</p>
        </div>
      );
    }
    return null;
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {description && <CardDescription>{description}</CardDescription>}
      </CardHeader>
      <CardContent>
        <div className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={120}
                fill="#8884d8"
                dataKey="value"
                nameKey="name"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={getColor(index, entry.platform)}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend formatter={(value) => value} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
}
