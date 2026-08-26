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
  
  let loading = $state(true);
  let error = $state<string | null>(null);
  
  onMount(async () => {
    try {
      loading = true;
      error = null;
      
      const [statsData, trendData, categoryData] = await Promise.all([
        dashboardApi.getStats(),
        dashboardApi.getSpendingTrend(),
        dashboardApi.getCategoryBreakdown()
      ]);
      
      stats = statsData;
      spendingTrend = trendData;
      categoryBreakdown = categoryData;
      
      // Wait for DOM to render before initializing charts
      setTimeout(() => {
        renderCharts();
      }, 0);
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      error = 'Failed to load dashboard data. Please try again later.';
    } finally {
      loading = false;
    }
  });
  
  let trendChart: any;
  let categoryChart: any;
  
  async function renderCharts() {
    const { Chart, registerables } = await import('chart.js');
    Chart.register(...registerables);
    
    const trendCtx = document.getElementById('trendChart') as HTMLCanvasElement;
    if (trendCtx && spendingTrend.data.length > 0) {
      // Destroy existing chart if it exists
      if (trendChart) {
        trendChart.destroy();
      }
      
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
          maintainAspectRatio: false,
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
      // Destroy existing chart if it exists
      if (categoryChart) {
        categoryChart.destroy();
      }
      
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
          maintainAspectRatio: false,
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
  
  {#if loading}
    <div class="flex items-center justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <span class="ml-3 text-slate-600">Loading dashboard data...</span>
    </div>
  {:else if error}
    <div class="bg-red-50 border border-red-200 rounded-lg p-4">
      <div class="flex items-center gap-2 text-red-600">
        <AlertCircle class="w-5 h-5" />
        <p>{error}</p>
      </div>
    </div>
  {:else}
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
        <div class="h-[200px]">
          <canvas id="trendChart"></canvas>
        </div>
      </div>
      
      <div class="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
        <h2 class="text-lg font-semibold text-slate-900 mb-4">Category Breakdown</h2>
        <div class="h-[200px]">
          <canvas id="categoryChart"></canvas>
        </div>
      </div>
    </div>
  {/if}
</div>
