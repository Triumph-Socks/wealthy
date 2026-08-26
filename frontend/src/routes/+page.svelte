<script lang="ts">
  import { onMount } from 'svelte';
  import { DollarSign, TrendingUp, ShoppingCart, AlertCircle } from 'lucide-svelte';
  import StatCard from '$lib/components/StatCard.svelte';
  import { dashboardApi } from '$lib/api';
  
  let stats = $state({
    total_expenses: 0,
    this_month: 0,
    avg_daily: 0,
    categories_count: 0
  });
  
  let spendingTrend = $state({ labels: [], data: [] });
  let categoryBreakdown = $state({ labels: [], data: [] });
  
  onMount(async () => {
    try {
      const [statsData, trendData, categoryData] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getSpendingTrend(),
        dashboardApi.getCategoryBreakdown()
      ]);
      
      stats = statsData;
      spendingTrend = trendData;
      categoryBreakdown = categoryData;
      
      renderCharts();
    } catch (err) {
      console.error('Error loading dashboard data:', err);
    }
  });
  
  let trendChart: any;
  let categoryChart: any;
  
  async function renderCharts() {
    const { Chart, registerables } = await import('chart.js');
    Chart.register(...registerables);
    
    const trendCtx = document.getElementById('trendChart') as HTMLCanvasElement;
    if (trendCtx && spendingTrend.data.length > 0) {
      trendChart = new Chart(trendCtx, {
        type: 'line',
        data: {
          labels: spendingTrend.labels,
          datasets: [{
            label: 'Expenses',
            data: spendingTrend.data,
            borderColor: '#0353a4',
            backgroundColor: 'rgba(3, 83, 164, 0.1)',
            tension: 0.4,
            fill: true
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false }
          },
          scales: {
            y: { beginAtZero: true }
          }
        }
      });
    }
    
    const categoryCtx = document.getElementById('categoryChart') as HTMLCanvasElement;
    if (categoryCtx && categoryBreakdown.data.length > 0) {
      categoryChart = new Chart(categoryCtx, {
        type: 'doughnut',
        data: {
          labels: categoryBreakdown.labels,
          datasets: [{
            data: categoryBreakdown.data,
            backgroundColor: [
              '#0466c8', '#0353a4', '#023e7d', '#002855', '#001845'
            ]
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom' }
          }
        }
      });
    }
  }
</script>

<div class="space-y-8">
  <div>
    <h1 class="text-2xl font-bold text-slate-900">Dashboard</h1>
    <p class="text-slate-600 mt-1">Track your expenses and budgets</p>
  </div>
  
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <StatCard 
      title="Total Expenses" 
      value={`$${stats.total_expenses.toFixed(2)}`}
      icon={DollarSign}
      color="blue"
    />
    <StatCard 
      title="This Month" 
      value={`$${stats.this_month.toFixed(2)}`}
      icon={TrendingUp}
      color="green"
    />
    <StatCard 
      title="Avg Daily" 
      value={`$${stats.avg_daily.toFixed(2)}`}
      icon={ShoppingCart}
      color="purple"
    />
    <StatCard 
      title="Categories" 
      value={stats.categories_count}
      icon={AlertCircle}
      color="orange"
    />
  </div>
  
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div class="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
      <h2 class="text-lg font-semibold text-slate-900 mb-4">Spending Trend</h2>
      <canvas id="trendChart" height="200"></canvas>
    </div>
    
    <div class="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
      <h2 class="text-lg font-semibold text-slate-900 mb-4">Category Breakdown</h2>
      <canvas id="categoryChart" height="200"></canvas>
    </div>
  </div>
</div>
