import api from './axios'

export const adminApi = {
  // Dashboard
  getDashboard: (params = {}) => api.get('/admin-panel/dashboard/', { params }),

  // Products
  getProducts: (params = {}) => api.get('/admin-panel/products/', { params }),
  getProduct: (id) => api.get(`/admin-panel/products/${id}/`),
  createProduct: (data) => api.post('/admin-panel/products/', data),
  updateProduct: (id, data) => api.patch(`/admin-panel/products/${id}/`, data),
  deleteProduct: (id) => api.delete(`/admin-panel/products/${id}/`),
  addProductImage: (id, data) => api.post(`/admin-panel/products/${id}/images/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteProductImage: (id, imgId) => api.delete(`/admin-panel/products/${id}/images/${imgId}/`),
  setProductMainImage: (id, imgId) => api.put(`/admin-panel/products/${id}/images/${imgId}/set_main/`),
  addProductColor: (id, data) => api.post(`/admin-panel/products/${id}/colors/`, data),
  updateProductColor: (id, colorId, data) => api.patch(`/admin-panel/products/${id}/colors/${colorId}/`, data),
  deleteProductColor: (id, colorId) => api.delete(`/admin-panel/products/${id}/colors/${colorId}/`),

  // Ombor (qoldiq)
  getStockSummary: () => api.get('/admin-panel/stock/summary/'),

  // Categories
  getCategories: () => api.get('/admin-panel/categories/'),
  createCategory: (data) => api.post('/admin-panel/categories/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateCategory: (id, data) => api.patch(`/admin-panel/categories/${id}/`, data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  deleteCategory: (id) => api.delete(`/admin-panel/categories/${id}/`),

  // Car models (Mashina turlari)
  getCarModels: () => api.get('/admin-panel/car-models/'),
  createCarModel: (data) => api.post('/admin-panel/car-models/', data),
  updateCarModel: (id, data) => api.patch(`/admin-panel/car-models/${id}/`, data),
  deleteCarModel: (id) => api.delete(`/admin-panel/car-models/${id}/`),

  // Orders
  getOrders: (params = {}) => api.get('/admin-panel/orders/', { params }),
  getOrder: (id) => api.get(`/admin-panel/orders/${id}/`),
  updateOrderStatus: (id, data) => api.put(`/admin-panel/orders/${id}/status/`, data),

  // Customers
  getCustomers: (params = {}) => api.get('/admin-panel/customers/', { params }),

  // Reports
  getReports: (params = {}) => api.get('/admin-panel/reports/', { params }),
  exportReports: (params = {}) => {
    const fmt = params.format || params.export_format || 'excel'
    return api.get('/admin-panel/reports/export/', {
      params: { ...params, format: fmt, export_format: fmt },
      responseType: 'blob',
      headers: {
        Accept: '*/*',
      },
    })
  },

  // Site settings
  getSiteSettings: () => api.get('/admin-panel/site-settings/'),
  updateSiteSettings: (data) => api.patch('/admin-panel/site-settings/', data),

  // Banners
  getBanners: () => api.get('/admin-panel/banners/'),
  createBanner: (data) => api.post('/admin-panel/banners/', data, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  updateBanner: (id, data) => api.patch(`/admin-panel/banners/${id}/`, data),
  deleteBanner: (id) => api.delete(`/admin-panel/banners/${id}/`),
}
