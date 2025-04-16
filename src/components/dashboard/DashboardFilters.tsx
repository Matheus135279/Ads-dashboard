
import React from 'react';
import { DateRange } from 'react-day-picker';
import { DateRangePicker } from '@/components/DateRangePicker';
import { FilterOptions } from '@/types/dashboard';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Download, FileUp } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';

interface DashboardFiltersProps {
  filters: FilterOptions;
  campaignOptions: Array<{ id: string; name: string }>;
  onFiltersChange: (filters: FilterOptions) => void;
  onExportPdf: () => void;
  onExportExcel: () => void;
  onImportCsv: () => void;
}

export function DashboardFilters({
  filters,
  campaignOptions,
  onFiltersChange,
  onExportPdf,
  onExportExcel,
  onImportCsv,
}: DashboardFiltersProps) {
  const handleDateRangeChange = (range: DateRange | undefined) => {
    onFiltersChange({
      ...filters,
      dateRange: range || { from: new Date() },
    });
  };

  const handlePlatformChange = (value: string) => {
    const platforms: Array<'facebook' | 'google'> = value === 'all' 
      ? ['facebook', 'google'] 
      : [value as 'facebook' | 'google'];
    
    onFiltersChange({
      ...filters,
      platforms,
    });
  };

  const handleCampaignChange = (value: string) => {
    const campaigns = value === 'all' 
      ? campaignOptions.map(campaign => campaign.id)
      : [value];
    
    onFiltersChange({
      ...filters,
      campaigns,
    });
  };

  const handleObjectiveChange = (value: string) => {
    const objectives: Array<'leads' | 'sales' | 'traffic' | 'awareness'> = value === 'all' 
      ? ['leads', 'sales', 'traffic', 'awareness'] 
      : [value as 'leads' | 'sales' | 'traffic' | 'awareness'];
    
    onFiltersChange({
      ...filters,
      objectives,
    });
  };

  const getPlatformValue = () => {
    if (filters.platforms.length === 2) return 'all';
    if (filters.platforms.length === 1) return filters.platforms[0];
    return 'all';
  };

  const getCampaignValue = () => {
    if (filters.campaigns.length === campaignOptions.length) return 'all';
    if (filters.campaigns.length === 1) return filters.campaigns[0];
    return 'all';
  };

  const getObjectiveValue = () => {
    if (filters.objectives.length === 4) return 'all';
    if (filters.objectives.length === 1) return filters.objectives[0];
    return 'all';
  };

  return (
    <Card className="mb-6">
      <CardContent className="pt-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 items-start">
          <div className="space-y-1">
            <label className="text-sm font-medium">Período</label>
            <DateRangePicker 
              dateRange={filters.dateRange} 
              onDateRangeChange={handleDateRangeChange} 
            />
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium">Plataforma</label>
            <Select 
              onValueChange={handlePlatformChange} 
              defaultValue={getPlatformValue()}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecionar plataforma" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas as Plataformas</SelectItem>
                <SelectItem value="facebook">Facebook</SelectItem>
                <SelectItem value="google">Google</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium">Campanha</label>
            <Select 
              onValueChange={handleCampaignChange} 
              defaultValue={getCampaignValue()}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecionar campanha" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todas as Campanhas</SelectItem>
                {campaignOptions.map((campaign) => (
                  <SelectItem key={campaign.id} value={campaign.id}>
                    {campaign.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-1">
            <label className="text-sm font-medium">Objetivo</label>
            <Select 
              onValueChange={handleObjectiveChange} 
              defaultValue={getObjectiveValue()}
            >
              <SelectTrigger>
                <SelectValue placeholder="Selecionar objetivo" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Todos os Objetivos</SelectItem>
                <SelectItem value="leads">Leads</SelectItem>
                <SelectItem value="sales">Vendas</SelectItem>
                <SelectItem value="traffic">Tráfego</SelectItem>
                <SelectItem value="awareness">Conscientização</SelectItem>
              </SelectContent>
            </Select>
          </div>
          
          <div className="flex items-end gap-2">
            <Button variant="outline" onClick={onExportPdf} className="flex-1">
              <Download className="h-4 w-4 mr-2" />
              PDF
            </Button>
            <Button variant="outline" onClick={onExportExcel} className="flex-1">
              <Download className="h-4 w-4 mr-2" />
              Excel
            </Button>
            <Button variant="outline" onClick={onImportCsv} className="flex-1">
              <FileUp className="h-4 w-4 mr-2" />
              CSV
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
