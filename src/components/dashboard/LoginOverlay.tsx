
import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';

export function LoginOverlay() {
  const handleStart = () => {
    // Remove authentication check
    window.location.reload();
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-background/80 backdrop-blur-sm z-50">
      <Card className="w-[350px]">
        <CardHeader>
          <CardTitle>Traffic Performance Dashboard</CardTitle>
          <CardDescription>
            Click below to access the dashboard
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <p className="mb-4">Welcome to the Traffic Performance Dashboard</p>
        </CardContent>
        <CardFooter>
          <Button onClick={handleStart} className="w-full">
            Start Exploring
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
}
