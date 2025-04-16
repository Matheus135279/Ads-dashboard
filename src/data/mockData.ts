
import { Campaign, DailyMetric } from '../types/dashboard';
import { addDays, format, subDays } from 'date-fns';

// Generate dates for the last 30 days
const generateDates = (daysCount: number) => {
  const today = new Date();
  const dates = [];
  
  for (let i = daysCount; i >= 0; i--) {
    dates.push(format(subDays(today, i), 'yyyy-MM-dd'));
  }
  
  return dates;
};

const dates = generateDates(30);

// Mock data for Facebook campaigns
export const facebookCampaigns: Campaign[] = [
  {
    id: 'fb-campaign-1',
    name: 'Summer Sale Promotion',
    platform: 'facebook',
    objective: 'sales',
    startDate: dates[0],
    endDate: dates[30],
    metrics: {
      spend: 1250.45,
      impressions: 185000,
      clicks: 4350,
      conversions: 218,
      cpm: 6.76,
      cpc: 0.29,
      ctr: 2.35,
      cpa: 5.73,
      conversionRate: 5.01,
      roas: 3.8,
      reach: 94500,
      engagement: {
        likes: 1450,
        comments: 320,
        shares: 175
      }
    }
  },
  {
    id: 'fb-campaign-2',
    name: 'Lead Generation Campaign',
    platform: 'facebook',
    objective: 'leads',
    startDate: dates[5],
    endDate: dates[30],
    metrics: {
      spend: 850.20,
      impressions: 120000,
      clicks: 3100,
      conversions: 310,
      cpm: 7.08,
      cpc: 0.27,
      ctr: 2.58,
      cpa: 2.74,
      conversionRate: 10.00,
      roas: 2.1,
      costPerLead: 2.74,
      reach: 65000,
      engagement: {
        likes: 980,
        comments: 210,
        shares: 95
      }
    }
  },
  {
    id: 'fb-campaign-3',
    name: 'Brand Awareness',
    platform: 'facebook',
    objective: 'awareness',
    startDate: dates[10],
    endDate: dates[30],
    metrics: {
      spend: 650.80,
      impressions: 220000,
      clicks: 2200,
      conversions: 45,
      cpm: 2.96,
      cpc: 0.30,
      ctr: 1.00,
      cpa: 14.46,
      conversionRate: 2.05,
      roas: 1.2,
      reach: 145000,
      videoViews: 65000,
      engagement: {
        likes: 2350,
        comments: 450,
        shares: 320
      }
    }
  }
];

// Mock data for Google campaigns
export const googleCampaigns: Campaign[] = [
  {
    id: 'g-campaign-1',
    name: 'Search - Brand Terms',
    platform: 'google',
    objective: 'traffic',
    startDate: dates[0],
    endDate: dates[30],
    metrics: {
      spend: 980.25,
      impressions: 45000,
      clicks: 5800,
      conversions: 195,
      cpm: 21.78,
      cpc: 0.17,
      ctr: 12.89,
      cpa: 5.03,
      conversionRate: 3.36,
      roas: 4.2
    }
  },
  {
    id: 'g-campaign-2',
    name: 'Search - Product Terms',
    platform: 'google',
    objective: 'sales',
    startDate: dates[5],
    endDate: dates[30],
    metrics: {
      spend: 1580.60,
      impressions: 68000,
      clicks: 4200,
      conversions: 285,
      cpm: 23.24,
      cpc: 0.38,
      ctr: 6.18,
      cpa: 5.55,
      conversionRate: 6.79,
      roas: 5.1
    }
  },
  {
    id: 'g-campaign-3',
    name: 'Display Remarketing',
    platform: 'google',
    objective: 'leads',
    startDate: dates[10],
    endDate: dates[30],
    metrics: {
      spend: 720.35,
      impressions: 195000,
      clicks: 1850,
      conversions: 135,
      cpm: 3.69,
      cpc: 0.39,
      ctr: 0.95,
      cpa: 5.34,
      conversionRate: 7.30,
      roas: 2.8,
      costPerLead: 5.34
    }
  }
];

// Combine all campaigns
export const allCampaigns = [...facebookCampaigns, ...googleCampaigns];

// Generate daily metrics data
export const dailyMetrics: DailyMetric[] = dates.map((date, index) => {
  // Create more realistic data with some variance and trends
  const multiplier = Math.sin(index / 5) * 0.3 + 1; // Creates a wave pattern
  const weekdayEffect = new Date(date).getDay() === 0 || new Date(date).getDay() === 6 ? 0.7 : 1; // Lower on weekends
  
  return {
    date,
    spend: Math.round((200 + index * 2) * multiplier * weekdayEffect * 100) / 100,
    impressions: Math.round((28000 + index * 500) * multiplier * weekdayEffect),
    clicks: Math.round((750 + index * 15) * multiplier * weekdayEffect),
    conversions: Math.round((38 + index * 0.8) * multiplier * weekdayEffect)
  };
});

// Helper function to get platform totals
export const getPlatformTotals = (platform: 'facebook' | 'google') => {
  const campaigns = platform === 'facebook' ? facebookCampaigns : googleCampaigns;
  
  return campaigns.reduce((acc, campaign) => {
    return {
      spend: acc.spend + campaign.metrics.spend,
      impressions: acc.impressions + campaign.metrics.impressions,
      clicks: acc.clicks + campaign.metrics.clicks,
      conversions: acc.conversions + campaign.metrics.conversions,
      cpm: 0, // Will calculate after
      cpc: 0, // Will calculate after
      ctr: 0, // Will calculate after
      cpa: 0  // Will calculate after
    };
  }, {
    spend: 0,
    impressions: 0,
    clicks: 0,
    conversions: 0,
    cpm: 0,
    cpc: 0,
    ctr: 0,
    cpa: 0
  });
};

// Calculate platform comparison data
export const platformComparison = ['facebook', 'google'].map(platform => {
  const totals = getPlatformTotals(platform as 'facebook' | 'google');
  
  return {
    platform: platform as 'facebook' | 'google',
    ...totals,
    cpm: totals.impressions > 0 ? (totals.spend / totals.impressions) * 1000 : 0,
    cpc: totals.clicks > 0 ? totals.spend / totals.clicks : 0,
    ctr: totals.impressions > 0 ? (totals.clicks / totals.impressions) * 100 : 0,
    cpa: totals.conversions > 0 ? totals.spend / totals.conversions : 0
  };
});

// Function to filter campaigns based on filter criteria
export const filterCampaigns = (
  campaigns: Campaign[], 
  filters: {
    dateRange?: { from?: Date; to?: Date; },
    platforms?: Array<'facebook' | 'google'>,
    campaignIds?: string[],
    objectives?: Array<'leads' | 'sales' | 'traffic' | 'awareness'>
  }
) => {
  return campaigns.filter(campaign => {
    // Filter by date range
    if (filters.dateRange?.from || filters.dateRange?.to) {
      const campaignStart = new Date(campaign.startDate);
      const campaignEnd = new Date(campaign.endDate);
      
      if (filters.dateRange.from && campaignEnd < filters.dateRange.from) {
        return false;
      }
      
      if (filters.dateRange.to && campaignStart > filters.dateRange.to) {
        return false;
      }
    }
    
    // Filter by platform
    if (filters.platforms && filters.platforms.length > 0) {
      if (!filters.platforms.includes(campaign.platform)) {
        return false;
      }
    }
    
    // Filter by campaign IDs
    if (filters.campaignIds && filters.campaignIds.length > 0) {
      if (!filters.campaignIds.includes(campaign.id)) {
        return false;
      }
    }
    
    // Filter by objectives
    if (filters.objectives && filters.objectives.length > 0) {
      if (!filters.objectives.includes(campaign.objective)) {
        return false;
      }
    }
    
    return true;
  });
};

// Function to filter daily metrics based on date range
export const filterDailyMetrics = (
  metrics: DailyMetric[],
  dateRange?: { from?: Date; to?: Date; }
) => {
  if (!dateRange?.from && !dateRange?.to) {
    return metrics;
  }
  
  return metrics.filter(metric => {
    const metricDate = new Date(metric.date);
    
    if (dateRange.from && metricDate < dateRange.from) {
      return false;
    }
    
    if (dateRange.to && metricDate > dateRange.to) {
      return false;
    }
    
    return true;
  });
};

// Function to calculate totals from filtered campaigns
export const calculateTotals = (campaigns: Campaign[]) => {
  const totals = campaigns.reduce((acc, campaign) => {
    return {
      spend: acc.spend + campaign.metrics.spend,
      impressions: acc.impressions + campaign.metrics.impressions,
      clicks: acc.clicks + campaign.metrics.clicks,
      conversions: acc.conversions + campaign.metrics.conversions
    };
  }, {
    spend: 0,
    impressions: 0,
    clicks: 0,
    conversions: 0
  });
  
  return {
    ...totals,
    cpm: totals.impressions > 0 ? (totals.spend / totals.impressions) * 1000 : 0,
    cpc: totals.clicks > 0 ? totals.spend / totals.clicks : 0,
    ctr: totals.impressions > 0 ? (totals.clicks / totals.impressions) * 100 : 0,
    cpa: totals.conversions > 0 ? totals.spend / totals.conversions : 0,
    conversionRate: totals.clicks > 0 ? (totals.conversions / totals.clicks) * 100 : 0,
    roas: calculateAverageRoas(campaigns)
  };
};

// Helper function to calculate average ROAS across campaigns
const calculateAverageRoas = (campaigns: Campaign[]) => {
  if (campaigns.length === 0) return 0;
  
  const totalRoas = campaigns.reduce((acc, campaign) => {
    return acc + campaign.metrics.roas;
  }, 0);
  
  return totalRoas / campaigns.length;
};
