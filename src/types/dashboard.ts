
export interface Campaign {
  id: string;
  name: string;
  platform: 'facebook' | 'google';
  objective: 'leads' | 'sales' | 'traffic' | 'awareness';
  startDate: string;
  endDate: string;
  metrics: CampaignMetrics;
}

export interface CampaignMetrics {
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
  cpm: number;
  cpc: number;
  ctr: number;
  cpa: number;
  conversionRate: number;
  roas: number;
  costPerLead?: number;
  reach?: number;
  videoViews?: number;
  engagement?: {
    likes: number;
    comments: number;
    shares: number;
  };
}

export interface DailyMetric {
  date: string;
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
}

export interface PlatformComparison {
  platform: 'facebook' | 'google';
  spend: number;
  impressions: number;
  clicks: number;
  conversions: number;
  cpm: number;
  cpc: number;
  ctr: number;
  cpa: number;
}

export interface FilterOptions {
  dateRange: {
    from: Date;
    to?: Date;
  };
  platforms: Array<'facebook' | 'google'>;
  campaigns: string[];
  objectives: Array<'leads' | 'sales' | 'traffic' | 'awareness'>;
}
