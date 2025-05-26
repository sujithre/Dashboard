// Novartis Dashboard Vue application
document.addEventListener('DOMContentLoaded', function() {
    const app = new Vue({
        el: '#app',
        data: {
            // Tab navigation
            activeTab: 'overview',

            // Filter values
            filterStartDate: '',
            filterSubscription: '',
            filterApplication: '',
            filterServiceName: '',

            // Data collections
            top5Subscriptions: [],
            top5Applications: [],
            top5ServiceNames: [],
            top5Resources: [],
            costByDate: {
                dates: [],
                costs: []
            },
            allData: [],

            // Filter options
            uniqueDates: [],
            uniqueSubscriptions: [],
            uniqueApplications: [],
            uniqueServiceNames: [],

            // Total values
            subscriptionTotal: 0,
            applicationsTotal: 0,
            serviceNamesTotal: 0,
            resourcesTotal: 0,

            // Chart instances
            costByDateChart: null,

            // Overview metrics
            overviewMetrics: {
                subscriptionCount: 0,
                totalCost: 0
            },

            // Loading states
            isLoading: true
        },
        methods: {
            // Format numbers for display
            formatNumber(value) {
                // Convert to millions and format with 2 decimal places
                const millions = value / 1000000;
                return millions.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            },
            
            // Calculate percentage
            calculatePercentage(value, total) {
                if (total === 0) return 0;
                return ((value / total) * 100).toFixed(1);
            },
            
            // Clear all filters
            clearFilters() {
                this.filterStartDate = '';
                this.filterSubscription = '';
                this.filterApplication = '';
                this.filterServiceName = '';
                
                // Reload all data
                this.fetchAllData();
            },
            
            // Fetch data with filters
            fetchDataWithFilters() {
                // This is a placeholder for future implementation if needed
                // Currently using client-side filtering
                this.fetchAllData();
            },
            
            // Fetch top 5 subscriptions data
            fetchTop5Subscriptions() {
                fetch('/api/top5Subscriptions')
                    .then(response => response.json())
                    .then(data => {
                        this.top5Subscriptions = data.data;
                        this.subscriptionTotal = data.total;
                    })
                    .catch(error => {
                        console.error('Error fetching subscription data:', error);
                    });
            },
            
            // Fetch top 5 applications data
            fetchTop5Applications() {
                fetch('/api/top5Applications')
                    .then(response => response.json())
                    .then(data => {
                        this.top5Applications = data.data;
                        this.applicationsTotal = data.total;
                    })
                    .catch(error => {
                        console.error('Error fetching application data:', error);
                    });
            },
            
            // Fetch top 5 service names data
            fetchTop5ServiceNames() {
                fetch('/api/top5ServiceNames')
                    .then(response => response.json())
                    .then(data => {
                        this.top5ServiceNames = data.data;
                        this.serviceNamesTotal = data.total;
                    })
                    .catch(error => {
                        console.error('Error fetching service names data:', error);
                    });
            },
            
            // Fetch top 5 resources data
            fetchTop5Resources() {
                fetch('/api/top5Resources')
                    .then(response => response.json())
                    .then(data => {
                        this.top5Resources = data.data;
                        this.resourcesTotal = data.total;
                    })
                    .catch(error => {
                        console.error('Error fetching resources data:', error);
                    });
            },
            
            // Fetch cost by date data
            fetchCostByDate() {
                fetch('/api/SumofCost')
                    .then(response => response.json())
                    .then(data => {
                        this.costByDate = data;
                        this.renderCostByDateChart();
                    })
                    .catch(error => {
                        console.error('Error fetching cost by date data:', error);
                    });
            },
            
            // Fetch all data for filtering
            fetchAllData() {
                fetch('/api/data')
                    .then(response => response.json())
                    .then(data => {
                        this.allData = data;
                        this.processFilterOptions();
                        this.calculateOverviewMetrics();
                        this.isLoading = false;
                    })
                    .catch(error => {
                        console.error('Error fetching all data:', error);
                        this.isLoading = false;
                    });
            },
            
            // Process filter options from all data
            processFilterOptions() {
                // Extract unique values for filters
                this.uniqueDates = [...new Set(this.allData.map(item => item.StartDate))].filter(Boolean);
                this.uniqueSubscriptions = [...new Set(this.allData.map(item => item.SUBSCRIPTIONNAME))].filter(Boolean);
                this.uniqueApplications = [...new Set(this.allData.map(item => item.APPLICATION))].filter(Boolean);
                this.uniqueServiceNames = [...new Set(this.allData.map(item => item.ServiceName))].filter(Boolean);
            },
            
            // Calculate overview metrics
            calculateOverviewMetrics() {
                // Count unique subscriptions
                this.overviewMetrics.subscriptionCount = new Set(
                    this.allData.map(item => item.SubscriptionId)
                ).size;
                
                // Calculate total cost
                this.overviewMetrics.totalCost = this.allData.reduce(
                    (sum, item) => sum + parseFloat(item.Cost || 0), 0
                );
            },
            
            // Render cost by date chart
            renderCostByDateChart() {
                const ctx = document.getElementById('costByDateChart').getContext('2d');
                
                // Destroy existing chart if it exists
                if (this.costByDateChart) {
                    this.costByDateChart.destroy();
                }
                
                // Create new chart
                this.costByDateChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: this.costByDate.dates,
                        datasets: [{
                            label: 'Sum of Cost',
                            data: this.costByDate.costs,
                            backgroundColor: 'rgba(79, 70, 229, 0.2)',
                            borderColor: 'rgba(79, 70, 229, 1)',
                            borderWidth: 2,
                            tension: 0.3,
                            fill: true
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    callback: function(value) {
                                        return '$' + (value / 1000000).toFixed(2) + 'M';
                                    }
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        return '$' + (context.parsed.y / 1000000).toFixed(2) + 'M';
                                    }
                                }
                            },
                            legend: {
                                display: true
                            }
                        }
                    }
                });
            }
        },
        created() {
            // Fetch all data when the app is created
            this.fetchAllData();
            this.fetchTop5Subscriptions();
            this.fetchTop5Applications();
            this.fetchTop5ServiceNames();
            this.fetchTop5Resources();
            this.fetchCostByDate();
        }
    });
});
