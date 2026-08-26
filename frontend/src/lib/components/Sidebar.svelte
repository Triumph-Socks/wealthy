<script lang="ts">
  import { Home, ShoppingCart, Tag, Store, PieChart, Settings } from 'lucide-svelte';
  
  const menuItems = [
    { icon: Home, label: 'Dashboard', href: '/' },
    { icon: ShoppingCart, label: 'Expenses', href: '/expenses' },
    { icon: Tag, label: 'Categories', href: '/categories' },
    { icon: Store, label: 'Shops', href: '/shops' },
    { icon: PieChart, label: 'Reports', href: '/reports' },
    { icon: Settings, label: 'Settings', href: '/settings' },
  ];
</script>

<div class="w-64 bg-slate-900 text-white flex flex-col">
  <div class="p-6 border-b border-slate-800">
    <h1 class="text-xl font-bold">Expense Tracker</h1>
  </div>
  
  <nav class="flex-1 p-4">
    <ul class="space-y-2">
      {#each menuItems as item}
        <li>
          <a 
            href={item.href}
            class="flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <svelte:component this={item.icon} class="w-5 h-5" />
            <span>{item.label}</span>
          </a>
        </li>
      {/each}
    </ul>
  </nav>
</div>
