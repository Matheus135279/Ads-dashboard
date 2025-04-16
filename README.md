
# Traffic Dashboard Analyzer

A modern, responsive dashboard for analyzing paid traffic from Facebook Ads and Google Ads campaigns. This dashboard provides comprehensive analytics and visualization of key performance metrics to help you optimize your advertising efforts.

## Features

- **Interactive Filtering**: Filter by date range, platform, campaign, and objective
- **KPI Cards**: Visualize key metrics in easy-to-read cards
- **Performance Charts**: Track spend, clicks, impressions, and conversions over time
- **Platform Comparison**: Compare Facebook and Google Ads performance side by side
- **Spend Distribution**: See how your budget is allocated across campaigns
- **Detailed Campaign Table**: View all campaigns with their key metrics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **CSV Import**: Upload your campaign data via CSV files
- **Export Functionality**: Export dashboard data as PDF or Excel
- **Secure Access**: Basic login functionality for data security

## Metrics Included

- Total Spend
- Impressions
- Clicks
- Conversions
- CPM (Cost per thousand impressions)
- CPC (Cost per click)
- CTR (Click-through rate)
- CPA (Cost per acquisition)
- Conversion Rate
- ROAS (Return on ad spend)
- Reach (Facebook)
- Engagement metrics

## Technologies Used

- **React**: Frontend framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Responsive charting library
- **Shadcn UI**: Modern UI component library
- **React Day Picker**: Date range selection

## Getting Started

1. Clone the repository
2. Install dependencies: `npm install`
3. Start the development server: `npm run dev`
4. Open your browser to: `http://localhost:8080`

## Using the Dashboard

1. Log in using the demo credentials (username/password containing "demo")
2. Use the filters at the top to refine your data view
3. Explore the different sections of the dashboard:
   - KPI Cards: Quick overview of key metrics
   - Performance Charts: Data visualization over time
   - Platform Analysis: Compare platforms and see spend distribution
   - Campaign Details: Detailed campaign metrics in tabular format

## Adding Your Own Data

In a real implementation, you would:

1. Connect to Facebook and Google Ads APIs for real-time data
2. Or import data via CSV files using the import functionality
3. Implement proper authentication for security

For this demo, mock data is provided to showcase the dashboard capabilities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
