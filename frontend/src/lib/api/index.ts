import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

export interface DashboardStats {
  total_expenses: number;
  this_month: number;
  avg_daily: number;
  categories_count: number;
}

export interface SpendingTrend {
  labels: string[];
  data: number[];
}

export interface CategoryBreakdown {
  labels: string[];
  data: number[];
}

export interface Expense {
  id: number;
  product: {
    id: number;
    name: string;
    category: {
      id: number;
      name: string;
    };
  };
  shop: {
    id: number;
    name: string;
  };
  quantity: number;
  price_per_unit: number;
  total_price: number;
  purchase_date: string;
  notes: string;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const dashboardApi = {
  async getStats(): Promise<DashboardStats> {
    const response = await api.get('/dashboard/stats/');
    return response.data;
  },
  
  async getSpendingTrend(): Promise<SpendingTrend> {
    const response = await api.get('/dashboard/spending-trend/');
    return response.data;
  },
  
  async getCategoryBreakdown(): Promise<CategoryBreakdown> {
    const response = await api.get('/dashboard/category-breakdown/');
    return response.data;
  },
};

export const expenseApi = {
  async getAll(params?: {
    category?: string;
    shop?: string;
    start_date?: string;
    end_date?: string;
  }): Promise<Expense[]> {
    const response = await api.get('/expenses/', { params });
    return response.data;
  },
  
  async getById(id: number): Promise<Expense> {
    const response = await api.get(`/expenses/${id}/`);
    return response.data;
  },
  
  async create(expense: Partial<Expense>): Promise<Expense> {
    const response = await api.post('/expenses/', expense);
    return response.data;
  },
  
  async update(id: number, expense: Partial<Expense>): Promise<Expense> {
    const response = await api.put(`/expenses/${id}/`, expense);
    return response.data;
  },
  
  async delete(id: number): Promise<void> {
    await api.delete(`/expenses/${id}/`);
  },
};

export const categoryApi = {
  async getAll() {
    const response = await api.get('/categories/');
    return response.data;
  },
};

export const shopApi = {
  async getAll() {
    const response = await api.get('/shops/');
    return response.data;
  },
};
