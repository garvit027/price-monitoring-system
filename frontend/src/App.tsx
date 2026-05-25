import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { RefreshCw, Package, Activity, DollarSign, ExternalLink, Bell, AlertCircle, CheckCircle, LogOut, Plus, User, Mail, Calendar, Shield, Key, TrendingUp, DownloadCloud, Sun, Moon } from 'lucide-react';
import './style.css';

const API_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api'
  : 'https://price-monitoring-system.onrender.com/api';

export const getCurrencySymbol = (source: string) => {
  if (!source) return '$';
  const rsSources = ['Flipkart', 'Myntra', 'Amazon India'];
  if (rsSources.includes(source)) return '₹';
  return '$';
};

// --- Axios Interceptor ---
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// --- Toast System ---
function Toast({ message, type, onClose }: { message: string, type: 'success' | 'error', onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(() => onClose(), 4000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast ${type}`}>
      {type === 'success' ? <CheckCircle color="var(--accent-primary)" /> : <AlertCircle color="#ff0055" />}
      {message}
    </div>
  );
}

function useToast() {
  const [toasts, setToasts] = useState<any[]>([]);
  const addToast = (msg: string, type: 'success' | 'error' = 'success') => {
    setToasts(prev => [...prev, { id: Date.now(), msg, type }]);
  };
  const removeToast = (id: number) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };
  return { toasts, addToast, removeToast };
}

// --- Auth Component ---
function AuthPage({ addToast, onLogin }: any) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (isLogin) {
        const res = await axios.post(`${API_URL}/auth/login`, { email, password });
        localStorage.setItem('token', res.data.access_token);
        onLogin();
        addToast('Authentication successful', 'success');
      } else {
        const res = await axios.post(`${API_URL}/auth/register`, { email, username, password });
        localStorage.setItem('token', res.data.access_token);
        onLogin();
        addToast('Registration successful', 'success');
      }
    } catch (err: any) {
      addToast(err.response?.data?.detail || 'Authentication failed', 'error');
    }
  };

  return (
    <div className="auth-container animate-fade">
      <div className="auth-card">
        <h1 className="logo-text" style={{ justifyContent: 'center', marginBottom: 32 }}>
          <Activity size={28} /> PriceMonitor
        </h1>
        <h2 style={{ textAlign: 'center', marginBottom: 24, color: 'var(--accent-primary)' }}>
          {isLogin ? 'SYSTEM ACCESS' : 'INITIALIZE AGENT'}
        </h2>
        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="email"
            placeholder="Identity Matrix (Email)"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="auth-input"
          />
          {!isLogin && (
            <input
              type="text"
              placeholder="Alias (Username)"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="auth-input"
            />
          )}
          <input
            type="password"
            placeholder="Security Key (Password)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="auth-input"
          />
          <button type="submit" className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: 16 }}>
            {isLogin ? 'DECRYPT & ENTER' : 'REGISTER SIGNATURE'}
          </button>
        </form>
        <p style={{ textAlign: 'center', marginTop: 24, color: 'var(--text-muted)' }}>
          {isLogin ? "No access signature?" : "Already registered?"}
          <button
            type="button"
            onClick={() => setIsLogin(!isLogin)}
            style={{ background: 'none', border: 'none', color: 'var(--accent-secondary)', marginLeft: 8, cursor: 'pointer', textDecoration: 'underline' }}
          >
            {isLogin ? "Initialize here" : "Authenticate here"}
          </button>
        </p>
      </div>
    </div>
  );
}

// --- Dashboard Component ---
function Dashboard({ addToast }: any) {
  const [stats, setStats] = useState<any>({ total_products: 0, average_price: 0, by_source: {}, by_category: {}, purchases_by_source: {} });
  const [events, setEvents] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      const res = await axios.get(`${API_URL}/analytics`);
      setStats(res.data);
      const evRes = await axios.get(`${API_URL}/events`);
      setEvents(evRes.data.slice(-5).reverse());
    } catch (e: any) {
      if (e.response?.status !== 401) {
        addToast(`Error loading data: ${e.message}`, 'error');
      }
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  const handleExportCSV = async () => {
    try {
      const res = await axios.get(`${API_URL}/export`, { responseType: 'blob' });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'price_monitoring_data.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      addToast('Data exported successfully', 'success');
    } catch (e: any) {
      addToast('Failed to export CSV', 'error');
    }
  };

  return (
    <div className="animate-fade">
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
        <h1 className="page-title">Datacenter Control</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button onClick={handleExportCSV} className="btn-primary" style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: 'white' }}>
            <DownloadCloud size={16} /> Export CSV
          </button>
          <div style={{ color: 'var(--text-muted)', fontSize: '14px', display: 'flex', alignItems: 'center' }}>
            <Activity size={14} className="animate-pulse" style={{ marginRight: 8, color: 'var(--accent-primary)' }} />
            Autonomous Sync Active
          </div>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div>
            <p className="stat-label">Indexed Entities</p>
            <p className="stat-value">{stats.total_products}</p>
          </div>
          <div className="stat-icon">
            <Package size={28} />
          </div>
        </div>

        <div className="stat-card">
          <div>
            <p className="stat-label">Market Baseline</p>
            <p className="stat-value">{stats.average_price}</p>
          </div>
          <div className="stat-icon pink">
            <DollarSign size={28} />
          </div>
        </div>

        <div className="stat-card">
          <div>
            <p className="stat-label">Active Anomalies</p>
            <p className="stat-value">{stats.active_anomalies || 0}</p>
          </div>
          <div className="stat-icon purple">
            <Bell size={28} />
          </div>
        </div>
      </div>

      <div className="dashboard-content-grid">
        <div className="notifications-panel">
          <h2 className="section-title"><Package className="text-accent-primary" /> Category Averages</h2>
          <div className="notification-list">
            {Object.entries(stats.by_category || {}).length === 0 ? <span style={{ color: 'var(--text-muted)' }}>No aggregate data</span> : Object.entries(stats.by_category).map(([cat, avg]: any) => (
              <div key={cat} className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', borderLeftColor: 'var(--accent-primary)' }}>
                <span>{cat}</span>
                <span style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>{avg}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="notifications-panel">
          <h2 className="section-title"><Activity className="text-accent-primary" /> Purchase / Track Activity</h2>
          <div className="notification-list">
            {Object.entries(stats.purchases_by_source || {}).length === 0 ? <span style={{ color: 'var(--text-muted)' }}>No mass volume data</span> : Object.entries(stats.purchases_by_source).map(([src, count]: any) => (
              <div key={src} className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', borderLeftColor: 'var(--neon-purple)' }}>
                <span>{src}</span>
                <span style={{ color: 'var(--neon-purple)', fontWeight: 'bold' }}>{count} Interactions</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="notifications-panel">
        <h2 className="section-title"><Bell className="text-accent-primary" /> System Event Log</h2>
        <div className="notification-list">
          {events.length === 0 ? (
            <p style={{ color: "var(--text-muted)", fontStyle: 'italic' }}>No network anomalies detected.</p>
          ) : (
            events.map((e: any) => (
              e.product_id ? (
                <Link to={`/products/${e.product_id}`} key={e.id} style={{ textDecoration: 'none' }}>
                  <div className="notification-item" style={{ cursor: 'pointer' }}>
                    <span style={{ color: 'var(--accent-secondary)', marginRight: 10, fontWeight: 'bold' }}>&gt;_</span>
                    {e.message}
                  </div>
                </Link>
              ) : (
                <div key={e.id} className="notification-item">
                  <span style={{ color: 'var(--accent-secondary)', marginRight: 10, fontWeight: 'bold' }}>&gt;_</span>
                  {e.message}
                </div>
              )
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// --- Product List Component ---
function ProductList({ addToast }: any) {
  const [products, setProducts] = useState<any[]>([]);
  const [selectedSource, setSelectedSource] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [trackUrl, setTrackUrl] = useState("");
  const [isTracking, setIsTracking] = useState(false);
  const [collections, setCollections] = useState<any[]>([]);
  const [selectedFolder, setSelectedFolder] = useState<number | null>(null);
  const [newFolderName, setNewFolderName] = useState('');
  const navigate = useNavigate();

  const fetchProducts = () => {
    axios.get(`${API_URL}/products?limit=1000`)
      .then(res => setProducts(res.data))
      .catch((e: any) => addToast(`Failed fetching directory: ${e.message}`, 'error'));
  };

  const fetchCollections = () => {
    axios.get(`${API_URL}/collections`)
      .then(res => setCollections(res.data))
      .catch(() => {});
  };

  useEffect(() => {
    fetchProducts();
    fetchCollections();
  }, [addToast]);

  const handleCreateFolder = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newFolderName) return;
    try {
      await axios.post(`${API_URL}/collections`, { name: newFolderName });
      setNewFolderName('');
      fetchCollections();
      addToast('Folder created', 'success');
    } catch (e) {
      addToast('Failed to create folder', 'error');
    }
  };

  const handleTrackUrl = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!trackUrl) return;
    setIsTracking(true);
    try {
      const res = await axios.post(`${API_URL}/track`, { url: trackUrl });
      addToast(`Tracking successful: ${res.data.product.name}`, 'success');
      setTrackUrl("");
      fetchProducts();
      navigate(`/products/${res.data.product_id}`);
    } catch (e: any) {
      addToast(e.response?.data?.detail || 'Tracking failed', 'error');
    } finally {
      setIsTracking(false);
    }
  };

  const sources = Array.from(new Set(products.map(p => p.source)));
  const filteredProducts = products.filter(p => {
    let filtered = products;
    if (selectedSource) {
      filtered = filtered.filter(p => p.source === selectedSource);
    }
    if (selectedFolder !== null) {
      filtered = filtered.filter(p => p.collection_id === selectedFolder);
    }
    const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.brand?.toLowerCase().includes(searchQuery.toLowerCase());
    return filtered.includes(p) && matchSearch;
  });

  return (
    <div className="animate-fade" style={{ display: 'flex', gap: '24px', flexDirection: 'row' }}>
      
      {/* Folders Sidebar */}
      <div style={{ width: '250px', flexShrink: 0, display: 'flex', flexDirection: 'column', gap: 16 }}>
        <div className="notifications-panel">
          <h2 className="section-title"><Package size={18} className="text-accent-primary" /> Folders</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            <button 
              className={selectedFolder === null ? 'btn-primary' : 'btn-black'} 
              style={{ width: '100%', justifyContent: 'flex-start' }}
              onClick={() => setSelectedFolder(null)}
            >
              All Items
            </button>
            {collections.map(c => (
              <button 
                key={c.id} 
                className={selectedFolder === c.id ? 'btn-primary' : 'btn-black'} 
                style={{ width: '100%', justifyContent: 'flex-start' }}
                onClick={() => setSelectedFolder(c.id)}
              >
                {c.name}
              </button>
            ))}
          </div>
          <form onSubmit={handleCreateFolder} style={{ marginTop: 16, display: 'flex', gap: 8 }}>
            <input 
              className="auth-input" 
              placeholder="New folder..." 
              value={newFolderName}
              onChange={e => setNewFolderName(e.target.value)}
              style={{ flex: 1, padding: '4px 8px' }}
            />
            <button type="submit" className="btn-primary" style={{ padding: '4px 8px' }}><Plus size={16}/></button>
          </form>
        </div>
      </div>

      <div style={{ flex: 1 }}>
        <div className="page-header" style={{ marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="page-title">Global Directory</h1>

        <input
          type="text"
          placeholder="Query network assets..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="notifications-panel" style={{ marginBottom: 48 }}>
        <h2 className="section-title" style={{ marginBottom: 16 }}><Activity className="text-accent-primary" /> New Asset Tracking</h2>
        <form onSubmit={handleTrackUrl} style={{ display: 'flex', gap: 16 }}>
          <input
            type="url"
            placeholder="Enter product URL from any site..."
            value={trackUrl}
            onChange={e => setTrackUrl(e.target.value)}
            className="search-input"
            style={{ flex: 1, width: 'auto' }}
            required
          />
          <button type="submit" className="btn-primary" disabled={isTracking}>
            {isTracking ? <span className="animate-spin"><RefreshCw size={20} /></span> : <Plus size={20} />}
            {isTracking ? 'SCANNING...' : 'TRACK'}
          </button>
        </form>
      </div>

      {/* Marketplace Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 48, overflowX: 'auto', paddingBottom: 8 }}>
        <button
          onClick={() => setSelectedSource(null)}
          className="btn-black"
          style={{ background: selectedSource === null ? 'var(--accent-primary)' : undefined, color: selectedSource === null ? '#000' : undefined, borderColor: selectedSource === null ? 'var(--accent-primary)' : undefined }}
        >
          All Marketplaces
        </button>
        {sources.map(src => (
          <button
            key={src}
            onClick={() => setSelectedSource(src)}
            className="btn-black"
            style={{ background: selectedSource === src ? 'var(--accent-primary)' : undefined, color: selectedSource === src ? '#000' : undefined, borderColor: selectedSource === src ? 'var(--accent-primary)' : undefined }}
          >
            {src}
          </button>
        ))}
      </div>

      <div className="products-grid">
        {filteredProducts.map((p: any) => (
          <Link key={p.id} to={`/products/${p.id}`}>
            <div className="product-card">
              <div className="product-image-wrap">
                <img src={p.image || "https://placehold.co/200x200"} alt={p.name} className="product-image" />
              </div>
              <div className="product-info">
                <div className="product-meta">
                  <span className="product-brand">{p.brand}</span>
                  <span className="product-source">{p.source}</span>
                </div>
                <h3 className="product-name" title={p.name}>{p.name}</h3>
                <p className="product-price">{getCurrencySymbol(p.source)}{p.price}</p>
              </div>
            </div>
          </Link>
        ))}
        </div>
      </div>
    </div>
  );
}

// --- Product Detail Component ---
function ProductDetail({ addToast }: any) {
  const [product, setProduct] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [collections, setCollections] = useState<any[]>([]);
  const [alertPriceInput, setAlertPriceInput] = useState("");
  const [updatingAlert, setUpdatingAlert] = useState(false);
  const id = window.location.pathname.split('/').pop();
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_URL}/collections`).then(res => setCollections(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    axios.get(`${API_URL}/products/${id}`)
      .then(res => {
        setProduct(res.data);
        if (res.data.alert_price) {
          setAlertPriceInput(res.data.alert_price.toString());
        }
      })
      .catch((e: any) => addToast(`Asset retrieval issue: ${e.message}`, 'error'));

    axios.get(`${API_URL}/products/${id}/history`)
      .then(res => {
        if (Array.isArray(res.data)) {
          let parsedHistory = res.data.map((h: any) => ({
            timestamp: new Date(h.timestamp).getTime(),
            price: h.price
          }));

          parsedHistory.sort((a: any, b: any) => a.timestamp - b.timestamp);

          if (parsedHistory.length === 1) {
            parsedHistory.unshift({
              timestamp: parsedHistory[0].timestamp - 86400000,
              price: parsedHistory[0].price
            });
          }

          setHistory(parsedHistory);
        }
      })
      .catch((e: any) => console.error('Tracking failure:', e));
  }, [id, addToast]);

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to stop tracking this product and delete its history?")) {
      try {
        await axios.delete(`${API_URL}/products/${id}`);
        addToast("Product successfully removed from monitoring.", "success");
        navigate("/products");
      } catch (e: any) {
        addToast(`Failed to stop tracking: ${e.message}`, "error");
      }
    }
  };

  const handleSetAlert = async (e: React.FormEvent) => {
    e.preventDefault();
    setUpdatingAlert(true);
    try {
      const val = alertPriceInput ? parseFloat(alertPriceInput) : null;
      await axios.post(`${API_URL}/products/${id}/alert`, { alert_price: val });
      addToast(val ? `Alert set below ${getCurrencySymbol(product?.source)}${val}` : "Alert cleared", "success");
      const res = await axios.get(`${API_URL}/products/${id}`);
      setProduct(res.data);
    } catch (e: any) {
      addToast(`Failed to configure alert: ${e.message}`, "error");
    } finally {
      setUpdatingAlert(false);
    }
  };

  const handleClearAlert = async () => {
    setUpdatingAlert(true);
    try {
      await axios.post(`${API_URL}/products/${id}/alert`, { alert_price: null });
      addToast("Alert cleared successfully", "success");
      setAlertPriceInput("");
      const res = await axios.get(`${API_URL}/products/${id}`);
      setProduct(res.data);
    } catch (e: any) {
      addToast(`Failed to clear alert: ${e.message}`, "error");
    } finally {
      setUpdatingAlert(false);
    }
  };

  const handleAssignFolder = async (collectionId: string) => {
    if (!collectionId) return;
    try {
      await axios.post(`${API_URL}/collections/${collectionId}/products/${id}`);
      addToast('Added to folder successfully', 'success');
      const res = await axios.get(`${API_URL}/products/${id}`);
      setProduct(res.data);
    } catch (e: any) {
      addToast('Failed to add to folder', 'error');
    }
  };

  if (!product) return <div className="animate-fade" style={{ fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--accent-primary)' }}>Decrypting asset signatures...</div>;

  const lowestPrice = history.length > 0 ? Math.min(...history.map(h => h.price)) : product.price;
  const highestPrice = history.length > 0 ? Math.max(...history.map(h => h.price)) : product.price;
  const priceDropPercent = highestPrice > 0 ? ((highestPrice - product.price) / highestPrice * 100).toFixed(0) : "0";

  return (
    <div className="detail-container animate-fade">
      <div className="detail-header" style={{ marginBottom: '32px' }}>
        <div className="detail-image-box">
          <img src={product.image || "https://placehold.co/400x400"} alt={product.name} className="detail-image" />
        </div>
        <div className="detail-info">
          <p className="detail-brand">{product.brand}</p>
          <h1 className="detail-title">{product.name}</h1>
          <div className="detail-price-box" style={{ marginBottom: '24px' }}>
            <span className="detail-price">{getCurrencySymbol(product.source)}{product.price}</span>
            {history.length > 0 && Math.max(...history.map(h => h.price)) > product.price && (
              <span className="detail-old-price">{getCurrencySymbol(product.source)}{Math.max(...history.map(h => h.price)).toFixed(2)}</span>
            )}
          </div>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
            <a href={product.url} target="_blank" rel="noopener noreferrer" className="btn-black" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '10px 20px' }}>
              Access Origin Matrix <ExternalLink size={20} />
            </a>
            <button onClick={handleDelete} className="btn-primary" style={{ background: '#ff0055', borderColor: '#ff0055', color: '#fff', padding: '10px 20px' }}>
              Stop Tracking
            </button>
            <select 
              className="auth-input" 
              style={{ width: 'auto', padding: '10px 20px' }}
              value={product.collection_id || ''}
              onChange={(e) => handleAssignFolder(e.target.value)}
            >
              <option value="">No Folder</option>
              {collections.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
          </div>

          {/* Phase 4: Competitor Search */}
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
            <p style={{ width: '100%', color: 'var(--text-muted)', fontSize: 14, marginBottom: 4 }}>Compare Prices Across Web:</p>
            <a href={`https://www.amazon.in/s?k=${encodeURIComponent(product.name)}`} target="_blank" rel="noopener noreferrer" className="btn-black" style={{ background: '#232f3e', color: 'white' }}>Search Amazon</a>
            <a href={`https://www.flipkart.com/search?q=${encodeURIComponent(product.name)}`} target="_blank" rel="noopener noreferrer" className="btn-black" style={{ background: '#2874f0', color: 'white' }}>Search Flipkart</a>
            <a href={`https://www.myntra.com/${encodeURIComponent(product.name)}`} target="_blank" rel="noopener noreferrer" className="btn-black" style={{ background: '#ff3f6c', color: 'white' }}>Search Myntra</a>
          </div>

          {/* Price Alert Configuration Card */}
          <div className="notifications-panel" style={{ background: 'rgba(10, 10, 22, 0.4)', border: '1px solid rgba(255, 0, 85, 0.15)', padding: '20px', borderRadius: '12px' }}>
            <h3 className="section-title" style={{ fontSize: '18px', color: 'var(--accent-secondary)', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
              <Bell size={18} style={{ color: 'var(--accent-secondary)' }} /> Configure Price Drop Alert
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '13px', marginBottom: '16px' }}>
              Get flagged in the System Event Log when this item drops below your target price.
            </p>
            <form onSubmit={handleSetAlert} style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <div style={{ position: 'relative', flex: 1 }}>
                <span style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)', fontWeight: 'bold' }}>{getCurrencySymbol(product.source)}</span>
                <input
                  type="number"
                  placeholder="Target price threshold..."
                  value={alertPriceInput}
                  onChange={e => setAlertPriceInput(e.target.value)}
                  className="search-input"
                  style={{ width: '100%', paddingLeft: '28px', boxSizing: 'border-box' }}
                />
              </div>
              <button type="submit" className="btn-primary" disabled={updatingAlert}>
                {updatingAlert ? 'SAVING...' : 'SET ALERT'}
              </button>
              {product.alert_price && (
                <button type="button" onClick={handleClearAlert} className="btn-black" style={{ border: '1px solid rgba(255,255,255,0.1)' }}>
                  CLEAR
                </button>
              )}
            </form>
            {product.alert_price && (
              <p style={{ color: 'var(--accent-primary)', fontSize: '13px', marginTop: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <CheckCircle size={14} color="var(--accent-primary)" /> Active Alert: Trigger when price drops below {getCurrencySymbol(product.source)}{product.alert_price}
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Trajectory Metrics Grid */}
      <div className="stats-grid" style={{ marginBottom: '32px' }}>
        <div className="stat-card">
          <div>
            <p className="stat-label">Lowest Tracked Price</p>
            <p className="stat-value">{getCurrencySymbol(product.source)}{lowestPrice}</p>
          </div>
          <div className="stat-icon"><DollarSign size={28} /></div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-label">Highest Tracked Price</p>
            <p className="stat-value">{getCurrencySymbol(product.source)}{highestPrice}</p>
          </div>
          <div className="stat-icon purple"><TrendingUp size={28} /></div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-label">Discount From Peak</p>
            <p className="stat-value">{priceDropPercent}%</p>
          </div>
          <div className="stat-icon pink"><Activity size={28} /></div>
        </div>
      </div>

      <div>
        <h2 className="section-title">
          <Activity size={24} style={{ color: 'var(--accent-secondary)' }} /> Trajectory Analytics
        </h2>

        {history.length > 0 ? (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history} margin={{ top: 20, right: 20, left: 0, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(99, 102, 241, 0.05)" />
                <XAxis
                  dataKey="timestamp"
                  type="number"
                  domain={['auto', 'auto']}
                  tickFormatter={(unixTime) => new Date(unixTime).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#8b8b99', fontSize: 12 }}
                  dy={15}
                />
                <YAxis
                  axisLine={false}
                  tickLine={false}
                  tick={{ fill: '#8b8b99', fontSize: 12 }}
                  tickFormatter={(value) => `${getCurrencySymbol(product.source)}${value}`}
                  dx={-15}
                  domain={['dataMin - (dataMin * 0.05)', 'dataMax + (dataMax * 0.05)']}
                />
                <Tooltip
                  cursor={{ stroke: 'rgba(99, 102, 241, 0.2)', strokeWidth: 2, strokeDasharray: '4 4' }}
                  contentStyle={{ background: 'rgba(10, 10, 22, 0.95)', backdropFilter: 'blur(10px)', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '12px', padding: '16px', boxShadow: '0 8px 32px rgba(0, 0, 0, 0.5)', color: '#fff' }}
                  labelFormatter={(unixTime) => new Date(unixTime).toLocaleString([], { weekday: 'short', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                  itemStyle={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}
                />
                <Area
                  type="monotone"
                  dataKey="price"
                  stroke="var(--accent-primary)"
                  strokeWidth={4}
                  fillOpacity={1}
                  fill="url(#colorPrice)"
                  dot={{ r: 5, fill: '#0a0a16', strokeWidth: 2, stroke: 'var(--accent-primary)' }}
                  activeDot={{ r: 8, fill: 'var(--accent-secondary)', stroke: '#fff', strokeWidth: 3, style: { filter: 'drop-shadow(0px 0px 8px rgba(255,0,85,0.8))' } }}
                  animationDuration={1500}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p style={{ color: 'var(--text-muted)', fontStyle: 'italic' }}>Awaiting sufficient temporal data to compile chart.</p>
        )}
      </div>
    </div>
  );
}

// --- Profile Dashboard Component ---
function ProfileDashboard({ addToast }: any) {
  const [user, setUser] = useState<any>(null);
  const [stats, setStats] = useState<any>({ total_products: 0, by_source: {} });
  const [loading, setLoading] = useState(true);
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [pwForm, setPwForm] = useState({ current: '', newPw: '', confirm: '' });
  const [telegramId, setTelegramId] = useState('');

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [userRes, statsRes] = await Promise.all([
          axios.get(`${API_URL}/auth/me`),
          axios.get(`${API_URL}/analytics`),
        ]);
        setUser(userRes.data);
        if (userRes.data.telegram_chat_id) setTelegramId(userRes.data.telegram_chat_id);
        setStats(statsRes.data);
      } catch (e: any) {
        if (e.response?.status !== 401) addToast('Failed to load profile', 'error');
      } finally {
        setLoading(false);
      }
    };
    fetchAll();
  }, []);

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    if (pwForm.newPw !== pwForm.confirm) {
      addToast('Passwords do not match', 'error');
      return;
    }
    addToast('Password update coming soon', 'success');
    setShowPasswordForm(false);
    setPwForm({ current: '', newPw: '', confirm: '' });
  };

  const avatarLetter = user?.username?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || '?';
  const joinedDate = user?.created_at
    ? new Date(user.created_at).toLocaleDateString([], { year: 'numeric', month: 'long', day: 'numeric' })
    : 'N/A';
  const sourceCount = Object.keys(stats.by_source || {}).length;

  const handleSaveTelegram = async () => {
    try {
      await axios.patch(`${API_URL}/auth/profile`, { telegram_chat_id: telegramId });
      addToast('Telegram ID saved successfully', 'success');
    } catch (e: any) {
      addToast('Failed to save Telegram ID', 'error');
    }
  };

  if (loading) return <div className="animate-fade" style={{ fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--accent-primary)' }}>Loading profile...</div>;

  return (
    <div className="animate-fade">
      <div className="page-header">
        <h1 className="page-title">Agent Profile</h1>
        <div style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
          <Shield size={14} style={{ marginRight: 8, color: 'var(--accent-primary)', display: 'inline' }} />
          Authenticated Session
        </div>
      </div>

      {/* Profile Hero Card */}
      <div className="profile-hero-card" style={{ marginBottom: 32 }}>
        <div className="profile-avatar">{avatarLetter}</div>
        <div className="profile-hero-info">
          <h2 className="profile-username">{user?.username || 'Unknown Agent'}</h2>
          <div className="profile-detail-row">
            <Mail size={15} style={{ color: 'var(--accent-primary)' }} />
            <span>{user?.email}</span>
          </div>
          <div className="profile-detail-row">
            <Calendar size={15} style={{ color: 'var(--accent-secondary)' }} />
            <span>Member since {joinedDate}</span>
          </div>
        </div>
        <div className="profile-badge">ACTIVE AGENT</div>
      </div>

      {/* Stats Row */}
      <div className="stats-grid" style={{ marginBottom: 32 }}>
        <div className="stat-card">
          <div>
            <p className="stat-label">Tracked Products</p>
            <p className="stat-value">{stats.total_products}</p>
          </div>
          <div className="stat-icon"><Package size={28} /></div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-label">Market Baseline</p>
            <p className="stat-value">{stats.average_price ?? 0}</p>
          </div>
          <div className="stat-icon pink"><TrendingUp size={28} /></div>
        </div>
        <div className="stat-card">
          <div>
            <p className="stat-label">Sources Monitored</p>
            <p className="stat-value">{sourceCount}</p>
          </div>
          <div className="stat-icon purple"><Activity size={28} /></div>
        </div>
      </div>

      {/* Details + Password */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32 }}>
        {/* Account Info */}
        <div className="notifications-panel">
          <h2 className="section-title"><User className="text-accent-primary" /> Account Details</h2>
          <div className="notification-list">
            <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Username</span>
              <span style={{ color: 'var(--accent-primary)', fontWeight: 600 }}>{user?.username}</span>
            </div>
            <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Email</span>
              <span style={{ color: '#fff' }}>{user?.email}</span>
            </div>
            <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>User ID</span>
              <span style={{ color: 'var(--text-muted)', fontFamily: 'monospace' }}>#{user?.id}</span>
            </div>
            <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ color: 'var(--text-muted)' }}>Joined</span>
              <span style={{ color: '#fff' }}>{joinedDate}</span>
            </div>
          </div>
        </div>

        {/* Security */}
        <div className="notifications-panel">
          <h2 className="section-title"><Key className="text-accent-primary" /> Security</h2>
          {!showPasswordForm ? (
            <div className="notification-list">
              <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: 'var(--text-muted)' }}>Password</span>
                <span style={{ letterSpacing: 4 }}>••••••••</span>
              </div>
              <div className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: 'var(--text-muted)' }}>Session Token</span>
                <span style={{ color: 'var(--accent-primary)', fontSize: 12, fontFamily: 'monospace' }}>VALID</span>
              </div>
              <button
                onClick={() => setShowPasswordForm(true)}
                className="btn-primary"
                style={{ marginTop: 16, width: '100%', justifyContent: 'center' }}
              >
                <Key size={16} /> Change Password
              </button>
            </div>
          ) : (
            <form onSubmit={handlePasswordChange} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <input className="auth-input" type="password" placeholder="Current password" value={pwForm.current} onChange={e => setPwForm(p => ({ ...p, current: e.target.value }))} required />
              <input className="auth-input" type="password" placeholder="New password" value={pwForm.newPw} onChange={e => setPwForm(p => ({ ...p, newPw: e.target.value }))} required />
              <input className="auth-input" type="password" placeholder="Confirm new password" value={pwForm.confirm} onChange={e => setPwForm(p => ({ ...p, confirm: e.target.value }))} required />
              <div style={{ display: 'flex', gap: 12 }}>
                <button type="submit" className="btn-primary" style={{ flex: 1, justifyContent: 'center' }}>Update</button>
                <button type="button" onClick={() => setShowPasswordForm(false)} className="btn-black" style={{ flex: 1, justifyContent: 'center' }}>Cancel</button>
              </div>
            </form>
          )}
        </div>

        {/* External Integrations */}
        <div className="notifications-panel">
          <h2 className="section-title"><Bell className="text-accent-primary" /> Integrations</h2>
          <div className="notification-list">
            <div style={{ marginBottom: 16 }}>
              <label style={{ display: 'block', color: 'var(--text-muted)', marginBottom: 8 }}>Telegram Chat ID</label>
              <div style={{ display: 'flex', gap: 12 }}>
                <input
                  className="auth-input"
                  style={{ flex: 1 }}
                  placeholder="e.g. 123456789"
                  value={telegramId}
                  onChange={e => setTelegramId(e.target.value)}
                />
                <button onClick={handleSaveTelegram} className="btn-primary">Save</button>
              </div>
              <p style={{ color: 'var(--text-muted)', fontSize: 12, marginTop: 8 }}>Find this by messaging @userinfobot on Telegram. You will receive price drops instantly on Telegram.</p>
            </div>
          </div>
        </div>
      </div>

      {/* Source Breakdown */}
      {sourceCount > 0 && (
        <div className="notifications-panel" style={{ marginTop: 32 }}>
          <h2 className="section-title"><Activity className="text-accent-primary" /> Marketplace Coverage</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 12 }}>
            {Object.entries(stats.by_source || {}).map(([src, count]: any) => (
              <div key={src} className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ textTransform: 'capitalize' }}>{src}</span>
                <span className="product-source">{count} items</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// --- Main App Setup ---
export default function App() {
  const { toasts, addToast, removeToast } = useToast();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');


  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    addToast('Disconnected from terminal', 'success');
  };

  if (!isAuthenticated) {
    return (
      <div className="app-container">
        <div className="toast-container">
          {toasts.map(t => (
            <Toast key={t.id} message={t.msg} type={t.type} onClose={() => removeToast(t.id)} />
          ))}
        </div>
        <AuthPage addToast={addToast} onLogin={() => setIsAuthenticated(true)} />
      </div>
    );
  }

  return (
    <Router>
      <div className="app-container">
        <div className="toast-container">
          {toasts.map(t => (
            <Toast key={t.id} message={t.msg} type={t.type} onClose={() => removeToast(t.id)} />
          ))}
        </div>

        <aside className="sidebar">
          <div className="sidebar-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 className="logo-text">
              <Activity size={28} /> PriceMonitor
            </h1>
            <button onClick={toggleTheme} className="nav-item" style={{ width: 'auto', background: 'transparent', padding: '8px', cursor: 'pointer' }}>
              {theme === 'dark' ? <Sun size={20} color="var(--text-muted)" /> : <Moon size={20} color="var(--text-muted)" />}
            </button>
          </div>
          <nav className="nav-links">
            <Link to="/" className="nav-item">
              <Activity size={20} /> Dashboard
            </Link>
            <Link to="/products" className="nav-item">
              <Package size={20} /> Directory
            </Link>
            <Link to="/profile" className="nav-item">
              <User size={20} /> Profile
            </Link>
          </nav>
          <div style={{ marginTop: 'auto', padding: '24px 16px' }}>
            <button onClick={handleLogout} className="nav-item" style={{ width: '100%', background: 'transparent', cursor: 'pointer', textAlign: 'left', color: '#ff0055' }}>
              <LogOut size={20} /> Terminate Session
            </button>
          </div>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard addToast={addToast} />} />
            <Route path="/products" element={<ProductList addToast={addToast} />} />
            <Route path="/products/:id" element={<ProductDetail addToast={addToast} />} />
            <Route path="/profile" element={<ProfileDashboard addToast={addToast} />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
