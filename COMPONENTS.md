# Component Documentation

## Vue.js Components

### Main Application Component

The dashboard uses Vue.js 2.6 for reactive data binding and user interactions. The main Vue instance is defined in `static/js/main.js`.

## Component Structure

### Data Properties

#### Navigation & State
- `activeTab` (String): Currently active tab ('overview', 'subscriptions', 'applications', 'services', 'resources')
- `isLoading` (Boolean): Loading state indicator

#### Filter Values
- `filterStartDate` (String): Selected start date filter
- `filterSubscription` (String): Selected subscription filter
- `filterApplication` (String): Selected application filter
- `filterServiceName` (String): Selected service name filter

#### Data Collections
- `top5Subscriptions` (Array): Top 5 subscriptions by cost
- `top5Applications` (Array): Top 5 applications by cost
- `top5ServiceNames` (Array): Top 5 service names by cost
- `top5Resources` (Array): Top 5 resource groups by cost
- `costByDate` (Object): Cost data aggregated by date with `dates` and `costs` arrays
- `allData` (Array): Complete dataset for filtering

#### Filter Options
- `uniqueDates` (Array): Available date options for filtering
- `uniqueSubscriptions` (Array): Available subscription options
- `uniqueApplications` (Array): Available application options
- `uniqueServiceNames` (Array): Available service name options

#### Totals
- `subscriptionTotal` (Number): Total cost for top 5 subscriptions
- `applicationsTotal` (Number): Total cost for top 5 applications
- `serviceNamesTotal` (Number): Total cost for top 5 service names
- `resourcesTotal` (Number): Total cost for top 5 resources

#### Chart Instances
- `costByDateChart` (Chart.js Instance): Line chart for cost trends

#### Overview Metrics
- `overviewMetrics` (Object): Contains `subscriptionCount` and `totalCost`

## Methods

### Data Formatting
- `formatNumber(value)`: Formats numbers to millions with 2 decimal places and comma separators
- `calculatePercentage(value, total)`: Calculates percentage with 1 decimal place

### Filtering
- `clearFilters()`: Resets all filter values and reloads data
- `fetchDataWithFilters()`: Applies current filters to fetch filtered data

### Data Fetching
- `fetchTop5Subscriptions()`: Fetches top 5 subscriptions from API
- `fetchTop5Applications()`: Fetches top 5 applications from API
- `fetchTop5ServiceNames()`: Fetches top 5 service names from API
- `fetchTop5Resources()`: Fetches top 5 resources from API
- `fetchCostByDate()`: Fetches cost data aggregated by date
- `fetchAllData()`: Fetches complete dataset for filtering

### Chart Management
- `renderCostByDateChart()`: Renders the cost trend line chart using Chart.js
- `updateCostByDateChart()`: Updates existing chart with new data

### Lifecycle Methods
- `mounted()`: Called when Vue instance is mounted; initializes data fetching

## UI Components

### Tab Navigation
The dashboard uses a tab-based navigation system with the following tabs:
- **Overview**: Displays summary metrics and overall cost trends
- **Subscriptions**: Shows top 5 subscriptions by cost
- **Applications**: Shows top 5 applications by cost
- **Services**: Shows top 5 service names by cost
- **Resources**: Shows top 5 resource groups by cost

### Filter Panel
Located in the sidebar, provides dropdown filters for:
- Start Date
- Subscription
- Application
- Service Name

Includes a "Clear Filters" button to reset all selections.

### Data Tables
Each tab displays data in a formatted table with:
- Item name
- Cost (formatted in millions)
- Percentage of total (where applicable)

### Charts
- **Cost Trend Chart**: Line chart showing daily cost trends
- Uses Chart.js with responsive sizing
- Displays costs in millions with proper formatting

## Styling

### Tailwind CSS Classes
The application uses Tailwind CSS utility classes for styling:
- `dashboard-card`: Custom card component styling
- `card-title`: Card title styling
- `data-table`: Table styling with hover effects
- `tab-active`: Active tab highlight
- `tab-inactive`: Inactive tab styling

### Custom Styles
Additional custom styles defined in `<style>` tags:
- Loading overlay with spinner animation
- Table hover effects
- Responsive layout adjustments

## Performance Considerations

### Client-Side Optimization
1. **Reactive Data Binding**: Vue.js automatically updates only changed DOM elements
2. **Single Data Fetch**: Data is fetched once on mount and cached in component state
3. **Efficient Rendering**: Tables and charts only re-render when data changes

### Chart Performance
- Chart instances are reused and updated rather than recreated
- Data points are limited to essential information
- Responsive design adapts to different screen sizes

## Integration with Backend

### API Endpoints Used
- `GET /api/top5Subscriptions`
- `GET /api/top5Applications`
- `GET /api/top5ServiceNames`
- `GET /api/top5Resources`
- `GET /api/SumofCost`
- `GET /api/data`

### Error Handling
All API calls include `.catch()` handlers that log errors to the console.

## Browser Compatibility
- Modern browsers supporting ES6+
- Vue.js 2.6 compatible
- Chart.js compatible
- Tailwind CSS compatible

## Future Enhancements
1. Add pagination for large datasets
2. Implement real-time data updates
3. Add export to CSV/PDF functionality
4. Enhanced filtering with date ranges
5. Cost forecasting and predictions
6. Drill-down capabilities for detailed analysis
