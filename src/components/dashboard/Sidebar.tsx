
import React from 'react';
import { 
  BarChart2, 
  DollarSign, 
  Home, 
  MousePointer, 
  Settings, 
  LineChart, 
  PieChart, 
  Users,
  ChevronLeft,
  ChevronRight,
  FileUp
} from 'lucide-react';
import { 
  Sidebar, 
  SidebarContent, 
  SidebarFooter, 
  SidebarGroup, 
  SidebarGroupContent, 
  SidebarGroupLabel, 
  SidebarHeader, 
  SidebarMenu, 
  SidebarMenuButton, 
  SidebarMenuItem, 
  SidebarProvider, 
  SidebarTrigger,
  useSidebar
} from '@/components/ui/sidebar';

export function SidebarWrapper({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full">
        <DashboardSidebar />
        <main className="flex-1 overflow-x-hidden">
          <div className="flex items-center p-4 border-b border-border">
            <SidebarTrigger className="mr-2" />
            <h1 className="text-lg font-medium">Dashboard de Desempenho de Anúncios</h1>
          </div>
          {children}
        </main>
      </div>
    </SidebarProvider>
  );
}

function DashboardSidebar() {
  const { state } = useSidebar();

  return (
    <Sidebar variant="sidebar" collapsible="icon" className="border-r border-border">
      <SidebarHeader className="flex items-center justify-center p-4">
        <div className={`overflow-hidden transition-all ${state === "expanded" ? "w-auto" : "w-0"}`}>
          <img 
            src="/lovable-uploads/hublever-logo.png" 
            alt="HubLever Logo" 
            className="h-8 mx-auto"
          />
        </div>
        {state === "collapsed" && (
          <div className="flex items-center justify-center w-8 h-8 rounded-full bg-purple-100 text-purple-600">
            <BarChart2 className="w-4 h-4" />
          </div>
        )}
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Dashboard</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Visão Geral">
                  <Home className="text-purple-600" />
                  <span>Visão Geral</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Campanhas">
                  <BarChart2 className="text-purple-600" />
                  <span>Campanhas</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Desempenho">
                  <LineChart className="text-purple-600" />
                  <span>Desempenho</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Plataformas">
                  <PieChart className="text-purple-600" />
                  <span>Plataformas</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Importar CSV">
                  <FileUp className="text-purple-600" />
                  <span>Importar CSV</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
        
        <SidebarGroup>
          <SidebarGroupLabel>Métricas</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Gastos">
                  <DollarSign className="text-purple-600" />
                  <span>Gastos</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Cliques">
                  <MousePointer className="text-purple-600" />
                  <span>Cliques</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Conversões">
                  <Users className="text-purple-600" />
                  <span>Conversões</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              <SidebarMenuItem>
                <SidebarMenuButton tooltip="Configurações">
                  <Settings className="text-purple-600" />
                  <span>Configurações</span>
                </SidebarMenuButton>
              </SidebarMenuItem>
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarFooter>
    </Sidebar>
  );
}
