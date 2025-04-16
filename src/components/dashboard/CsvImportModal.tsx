
import React, { useState } from 'react';
import { Upload, X, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { processCsvImport } from '@/data/mockCsvImport';
import { useToast } from '@/components/ui/use-toast';
import { Campaign } from '@/types/dashboard';

interface CsvImportModalProps {
  isOpen: boolean;
  onClose: () => void;
  onImportSuccess: (campaigns: Partial<Campaign>[]) => void;
}

export function CsvImportModal({ isOpen, onClose, onImportSuccess }: CsvImportModalProps) {
  const [file, setFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      validateAndSetFile(selectedFile);
    }
  };

  const validateAndSetFile = (selectedFile: File) => {
    if (!selectedFile.name.endsWith('.csv')) {
      setError('Por favor, selecione um arquivo CSV válido.');
      return;
    }
    
    setFile(selectedFile);
    setError(null);
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      validateAndSetFile(droppedFile);
    }
  };

  const handleImport = async () => {
    if (!file) return;
    
    setIsProcessing(true);
    setError(null);
    
    try {
      const importedCampaigns = await processCsvImport(file);
      
      toast({
        title: "Importação concluída",
        description: `O arquivo ${file.name} foi importado com sucesso.`,
      });
      
      onImportSuccess(importedCampaigns);
      onClose();
    } catch (err) {
      setError(`Erro ao importar o arquivo: ${(err as Error).message}`);
      toast({
        variant: "destructive",
        title: "Erro na importação",
        description: `Não foi possível processar o arquivo: ${(err as Error).message}`,
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleCancel = () => {
    setFile(null);
    setError(null);
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Importar Dados de Campanhas</DialogTitle>
          <DialogDescription>
            Carregue um arquivo CSV do Facebook Ads ou Google Ads para visualizar os dados.
          </DialogDescription>
        </DialogHeader>
        
        <div
          className={`
            mt-4 border-2 border-dashed rounded-lg p-8 text-center
            ${isDragging ? 'border-purple-400 bg-purple-50' : 'border-gray-300'}
            ${error ? 'border-red-300' : ''}
          `}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          {file ? (
            <div className="flex flex-col items-center">
              <CheckCircle2 className="h-10 w-10 text-green-500 mb-2" />
              <p className="text-sm font-medium mb-1">{file.name}</p>
              <p className="text-xs text-gray-500 mb-4">
                {(file.size / 1024).toFixed(2)} KB
              </p>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setFile(null)}
                className="text-xs"
              >
                <X className="h-3 w-3 mr-1" />
                Remover
              </Button>
            </div>
          ) : (
            <div className="flex flex-col items-center">
              <Upload className="h-10 w-10 text-purple-500 mb-2" />
              <p className="text-sm font-medium mb-1">
                Arraste e solte seu arquivo CSV aqui
              </p>
              <p className="text-xs text-gray-500 mb-4">
                ou clique para selecionar um arquivo
              </p>
              <Button
                variant="outline"
                size="sm"
                asChild
                className="text-xs"
              >
                <label>
                  Selecionar arquivo
                  <input
                    type="file"
                    className="hidden"
                    accept=".csv"
                    onChange={handleFileChange}
                  />
                </label>
              </Button>
            </div>
          )}
        </div>
        
        {error && (
          <div className="flex items-center text-red-500 mt-2 text-sm">
            <AlertCircle className="h-4 w-4 mr-1" />
            {error}
          </div>
        )}

        <DialogFooter className="flex space-x-2 sm:justify-end">
          <Button variant="outline" onClick={handleCancel}>
            Cancelar
          </Button>
          <Button
            disabled={!file || isProcessing}
            onClick={handleImport}
            className="bg-purple-600 hover:bg-purple-700"
          >
            {isProcessing ? "Processando..." : "Importar dados"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
