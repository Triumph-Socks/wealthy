<script lang="ts">
  export let title: string;
  export let value: string | number;
  export let icon: any;
  export let color: 'blue' | 'green' | 'purple' | 'orange' = 'blue';
  
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600'
  };
</script>

<div class="bg-white rounded-lg p-6 shadow-sm border border-slate-200">
  <div class="flex items-center justify-between">
    <div>
      <p class="text-sm font-medium text-slate-600">{title}</p>
      <p class="text-2xl font-bold text-slate-900 mt-1">{value}</p>
    </div>
    <div class="p-3 rounded-lg {colorClasses[color]}">
      <svelte:component this={icon} class="w-6 h-6" />
    </div>
  </div>
</div>
