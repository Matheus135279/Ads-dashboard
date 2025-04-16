
import React, { useState, useEffect } from 'react';
import { subDays } from 'date-fns';

// Components
import { DashboardFilters } from '@/components/dashboard/DashboardFilters';
import { MetricCard } from '@/components/dashboard/MetricCard';
import { CampaignTable } from '@/components/dashboard/CampaignTable';
import { PerformanceChart } from '@/components/dashboard/PerformanceChart';
import { PlatformComparisonChart } from '@/components/dashboard/PlatformComparisonChart';
import { SpendDistributionChart } from '@/components/dashboard/SpendDistributionChart';
import { MetricSummary } from '@/components/dashboard/MetricSummary';
import { SidebarWrapper } from '@/components/dashboard/Sidebar';
import { CsvImportModal } from '@/components/dashboard/CsvImportModal';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useToast } from '@/components/ui/use-toast';

// Types and mock data
import { FilterOptions, Campaign } from '@/types/dashboard';
import { 
  allCampaigns, 
  filterCampaigns, 
  filterDailyMetrics, 
  dailyMetrics, 
  calculateTotals, 
  platformComparison 
} from '@/data/mockData';

// Icons
import { 
  DollarSign, 
  BarChart2, 
  MousePointer, 
  Percent, 
  Tag, 
  Users, 
  Eye, 
  Zap 
} from 'lucide-react';

export default function Index() {
  // Initialize default date range (last 30 days)
  const defaultDateRange = {
    from: subDays(new Date(), 30),
    to: new Date(),
  };

  // Initialize default filter state
  const [filters, setFilters] = useState<FilterOptions>({
    dateRange: defaultDateRange,
    platforms: ['facebook', 'google'],
    campaigns: allCampaigns.map(campaign => campaign.id),
    objectives: ['leads', 'sales', 'traffic', 'awareness'],
  });

  // Apply filters to get filtered campaigns and metrics
  const [filteredCampaigns, setFilteredCampaigns] = useState<Campaign[]>(allCampaigns);
  const [filteredDailyMetrics, setFilteredDailyMetrics] = useState(dailyMetrics);
  const [totals, setTotals] = useState(calculateTotals(allCampaigns));
  const [isCsvModalOpen, setIsCsvModalOpen] = useState(false);
  const { toast } = useToast();

  // Update filtered data when filters change
  useEffect(() => {
    const campaigns = filterCampaigns(allCampaigns, {
      dateRange: filters.dateRange,
      platforms: filters.platforms,
      campaignIds: filters.campaigns,
      objectives: filters.objectives,
    });
    
    const metrics = filterDailyMetrics(dailyMetrics, filters.dateRange);
    
    setFilteredCampaigns(campaigns);
    setFilteredDailyMetrics(metrics);
    setTotals(calculateTotals(campaigns));
  }, [filters]);

  // Handler for filter changes
  const handleFiltersChange = (newFilters: FilterOptions) => {
    setFilters(newFilters);
  };

  // Handlers for exports and imports
  const handleExportPdf = () => {
    toast({
      title: "Exportação PDF",
      description: "A funcionalidade de exportação PDF seria implementada com uma biblioteca de geração de PDF."
    });
  };

  const handleExportExcel = () => {
    toast({
      title: "Exportação Excel",
      description: "A funcionalidade de exportação Excel seria implementada com uma biblioteca de geração de planilhas."
    });
  };

  const handleOpenCsvModal = () => {
    setIsCsvModalOpen(true);
  };

  const handleImportSuccess = (importedCampaigns: Partial<Campaign>[]) => {
    toast({
      title: "Dados importados com sucesso",
      description: `${importedCampaigns.length} campanhas foram importadas.`,
    });
    
    // Em uma implementação real, atualizaríamos os dados com as campanhas importadas
    console.log('Campanhas importadas:', importedCampaigns);
  };

  // Campaign options for filter dropdowns
  const campaignOptions = allCampaigns.map(campaign => ({
    id: campaign.id,
    name: campaign.name,
  }));

  return (
    <SidebarWrapper>
      <div className="container mx-auto py-6 px-4">
        <div className="flex flex-col">
          <h1 className="text-3xl font-bold mb-2 text-purple-800">Dashboard de Desempenho de Anúncios</h1>
          <p className="text-muted-foreground mb-6">
            Analise e visualize o desempenho das suas campanhas no Facebook e Google Ads
          </p>
          
          {/* Filters Section */}
          <DashboardFilters
            filters={filters}
            campaignOptions={campaignOptions}
            onFiltersChange={handleFiltersChange}
            onExportPdf={handleExportPdf}
            onExportExcel={handleExportExcel}
            onImportCsv={handleOpenCsvModal}
          />
          
          {/* KPI Cards Section */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <MetricCard
              title="Gasto Total"
              value={`R$ ${totals.spend.toFixed(2)}`}
              icon={<DollarSign className="text-purple-500" />}
              description="Investimento total em campanhas"
            />
            <MetricCard
              title="Impressões"
              value={totals.impressions.toLocaleString()}
              icon={<Eye className="text-purple-500" />}
              description="Total de impressões entregues"
            />
            <MetricCard
              title="Cliques"
              value={totals.clicks.toLocaleString()}
              icon={<MousePointer className="text-purple-500" />}
              description="Total de cliques gerados"
            />
            <MetricCard
              title="Conversões"
              value={totals.conversions.toLocaleString()}
              icon={<Zap className="text-purple-500" />}
              description="Total de conversões obtidas"
            />
            <MetricCard
              title="CPM"
              value={`R$ ${totals.cpm.toFixed(2)}`}
              icon={<BarChart2 className="text-purple-500" />}
              description="Custo por 1.000 impressões"
            />
            <MetricCard
              title="CPC"
              value={`R$ ${totals.cpc.toFixed(2)}`}
              icon={<DollarSign className="text-purple-500" />}
              description="Custo por clique"
            />
            <MetricCard
              title="CTR"
              value={`${totals.ctr.toFixed(2)}%`}
              icon={<Percent className="text-purple-500" />}
              description="Taxa de cliques"
            />
            <MetricCard
              title="CPA"
              value={`R$ ${totals.cpa.toFixed(2)}`}
              icon={<Tag className="text-purple-500" />}
              description="Custo por aquisição"
            />
          </div>
          
          {/* Performance Charts Section */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <PerformanceChart
              data={filteredDailyMetrics}
              metric="spend"
              title="Gastos Diários"
              description="Gastos da campanha ao longo do tempo"
              color="#9b87f5"
            />
            <PerformanceChart
              data={filteredDailyMetrics}
              metric="clicks"
              title="Cliques Diários"
              description="Desempenho de cliques ao longo do tempo"
              color="#7E69AB"
            />
          </div>
          
          {/* Platform Analysis Section */}
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4 text-purple-800">Análise de Plataformas</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <SpendDistributionChart
                campaigns={filteredCampaigns}
                title="Distribuição de Gastos"
                description="Detalhamento de gastos por campanha"
              />
              <PlatformComparisonChart
                data={platformComparison}
                metrics={['spend', 'cpm', 'cpc', 'ctr', 'cpa']}
                title="Comparação de Plataformas"
                description="Comparação de métricas-chave entre plataformas"
              />
            </div>
          </div>
          
          {/* Campaign Metrics Analysis */}
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4 text-purple-800">Análise de Métricas de Campanha</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <MetricSummary
                campaigns={filteredCampaigns}
                metric="cpa"
                title="Custo por Aquisição"
                description="CPA por campanha"
              />
              <MetricSummary
                campaigns={filteredCampaigns}
                metric="conversions"
                title="Conversões"
                description="Total de conversões por campanha"
              />
            </div>
          </div>
          
          {/* Campaign Details Section */}
          <div className="mb-6">
            <h2 className="text-2xl font-bold mb-4 text-purple-800">Detalhes das Campanhas</h2>
            <Tabs defaultValue="all">
              <TabsList className="mb-4 bg-purple-100">
                <TabsTrigger value="all" className="data-[state=active]:bg-purple-600 data-[state=active]:text-white">Todas as Campanhas</TabsTrigger>
                <TabsTrigger value="facebook" className="data-[state=active]:bg-purple-600 data-[state=active]:text-white">Facebook</TabsTrigger>
                <TabsTrigger value="google" className="data-[state=active]:bg-purple-600 data-[state=active]:text-white">Google</TabsTrigger>
              </TabsList>
              <TabsContent value="all">
                <CampaignTable campaigns={filteredCampaigns} />
              </TabsContent>
              <TabsContent value="facebook">
                <CampaignTable 
                  campaigns={filteredCampaigns.filter(c => c.platform === 'facebook')} 
                />
              </TabsContent>
              <TabsContent value="google">
                <CampaignTable 
                  campaigns={filteredCampaigns.filter(c => c.platform === 'google')} 
                />
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </div>
      
      {/* CSV Import Modal */}
      <CsvImportModal 
        isOpen={isCsvModalOpen}
        onClose={() => setIsCsvModalOpen(false)}
        onImportSuccess={handleImportSuccess}
      />
    </SidebarWrapper>
  );
}
