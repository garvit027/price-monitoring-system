import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { RefreshCw, Package, Activity, DollarSign, ExternalLink, Bell, AlertCircle, CheckCircle } from 'lucide-react';
import './style.css';

const API_URL = 'http://localhost:8000/api';

// --- Toast System ---
function Toast({ message, type, onClose }: { message: string, type: 'success'|'error', onClose: () => void }) {
  useEffect(() => {
    const timer = setTimeout(() => onClose(), 4000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div className={`toast ${type}`}>
      {type === 'success' ? <CheckCircle color="var(--neon-cyan)" /> : <AlertCircle color="#ff0055" />}
      {message}
    </div>
  );
}

function useToast() {
  const [toasts, setToasts] = useState<any[]>([]);
  const addToast = (msg: string, type: 'success'|'error' = 'success') => {
    setToasts(prev => [...prev, { id: Date.now(), msg, type }]);
  };
  const removeToast = (id: number) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  };
  return { toasts, addToast, removeToast };
}

// --- Dashboard Component ---
function Dashboard({ addToast }: any) {
  const [stats, setStats] = useState({ total_products: 0, average_price: 0, by_source: {}, by_category: {} });
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState<any[]>([]);

  const fetchData = async () => {
    try {
      console.log('Fetching initial analytics data...');
      const res = await axios.get(`${API_URL}/analytics`);
      setStats(res.data);
      console.log('Analytics response:', res.data);

      const evRes = await axios.get(`${API_URL}/events`);
      setEvents(evRes.data.slice(-5).reverse());
      console.log('Events response:', evRes.data);
    } catch (e: any) {
      console.error('Error fetching dashboard data:', e);
      addToast(`Error loading data: ${e.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleRefresh = async () => {
    setLoading(true);
    console.log('Initiating dataset sync...');
    try {
      const res = await axios.post(`${API_URL}/refresh`);
      console.log('Sync complete!', res.data);
      addToast(`Sync successful! Inserted: ${res.data.inserted}`);
      fetchData();
    } catch (e: any) {
      console.error('Sync failed with error:', e);
      addToast(`Sync failed: ${e.message}`, 'error');
      setLoading(false);
    }
  };

  return (
    <div className="animate-fade">
      <div className="page-header">
        <h1 className="page-title">Datacenter Control</h1>
        <button onClick={handleRefresh} className="btn-primary">
          <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
          Sync Datastreams
        </button>
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
            <p className="stat-value">${stats.average_price}</p>
          </div>
          <div className="stat-icon pink">
            <DollarSign size={28} />
          </div>
        </div>

        <div className="stat-card">
          <div>
            <p className="stat-label">Active Anomalies</p>
            <p className="stat-value">{events.length}</p>
          </div>
          <div className="stat-icon purple">
            <Bell size={28} />
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0,1fr) minmax(0,1fr)', gap: '32px', marginBottom: '48px' }}>
        <div className="notifications-panel">
          <h2 className="section-title"><Package className="text-neon-cyan" /> Category Averages</h2>
          <div className="notification-list">
            {Object.entries(stats.by_category || {}).length === 0 ? <span style={{color: 'var(--text-muted)'}}>No aggregate data</span> : Object.entries(stats.by_category).map(([cat, avg]: any) => (
              <div key={cat} className="notification-item" style={{display: 'flex', justifyContent: 'space-between', borderLeftColor: 'var(--neon-cyan)'}}>
                <span>{cat}</span>
                <span style={{color: 'var(--neon-cyan)', fontWeight: 'bold'}}>${avg}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="notifications-panel">
          <h2 className="section-title"><Activity className="text-neon-cyan" /> Source Volumes</h2>
          <div className="notification-list">
            {Object.entries(stats.by_source || {}).length === 0 ? <span style={{color: 'var(--text-muted)'}}>No mass volume data</span> : Object.entries(stats.by_source).map(([src, count]: any) => (
              <div key={src} className="notification-item" style={{display: 'flex', justifyContent: 'space-between', borderLeftColor: 'var(--neon-purple)'}}>
                <span>{src}</span>
                <span style={{color: 'var(--neon-purple)', fontWeight: 'bold'}}>{count} Items</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="notifications-panel">
        <h2 className="section-title"><Bell className="text-neon-cyan" /> System Event Log</h2>
        <div className="notification-list">
          {events.length === 0 ? (
            <p style={{color: "var(--text-muted)", fontStyle: 'italic'}}>No network anomalies detected.</p>
          ) : (
            events.map((e: any) => (
              e.product_id ? (
                <Link to={`/products/${e.product_id}`} key={e.id} style={{textDecoration: 'none'}}>
                  <div className="notification-item" style={{cursor: 'pointer'}}>
                    <span style={{color: 'var(--neon-pink)', marginRight: 10, fontWeight: 'bold'}}>&gt;_</span>
                    {e.message}
                  </div>
                </Link>
              ) : (
                <div key={e.id} className="notification-item">
                  <span style={{color: 'var(--neon-pink)', marginRight: 10, fontWeight: 'bold'}}>&gt;_</span>
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

  useEffect(() => {
    console.log('Fetching directory listings...');
    axios.get(`${API_URL}/products?limit=100`)
      .then(res => {
        setProducts(res.data);
        console.log('Directory payload:', res.data);
      })
      .catch((e: any) => {
        console.error('Failed fetching directory:', e);
        addToast(`Failed fetching directory: ${e.message}`, 'error');
      });
  }, [addToast]);

  const sources = Array.from(new Set(products.map(p => p.source)));
  const filteredProducts = products.filter(p => {
    const matchSource = selectedSource ? p.source === selectedSource : true;
    const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.brand?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchSource && matchSearch;
  });

  return (
    <div className="animate-fade">
      <div className="page-header" style={{ marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 className="page-title">Global Directory</h1>
        
        <input 
          type="text" 
          placeholder="Query network assets..." 
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          style={{
            background: 'rgba(255,255,255,0.05)',
            border: '1px solid rgba(0,243,255,0.3)',
            color: '#fff',
            padding: '12px 24px',
            borderRadius: '8px',
            fontSize: '15px',
            width: '300px',
            outline: 'none',
            boxShadow: '0 0 10px rgba(0, 243, 255, 0.05)'
          }}
        />
      </div>
      
      {/* Marketplace Filters */}
      <div style={{ display: 'flex', gap: 12, marginBottom: 48, overflowX: 'auto', paddingBottom: 8 }}>
        <button 
          onClick={() => setSelectedSource(null)}
          className="btn-black"
          style={{ background: selectedSource === null ? 'var(--neon-cyan)' : undefined, color: selectedSource === null ? '#000' : undefined, borderColor: selectedSource === null ? 'var(--neon-cyan)' : undefined }}
        >
          All Marketplaces
        </button>
        {sources.map(src => (
          <button 
            key={src}
            onClick={() => setSelectedSource(src)}
            className="btn-black"
            style={{ background: selectedSource === src ? 'var(--neon-cyan)' : undefined, color: selectedSource === src ? '#000' : undefined, borderColor: selectedSource === src ? 'var(--neon-cyan)' : undefined }}
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
                <p className="product-price">${p.price}</p>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}

// --- Product Detail Component ---
function ProductDetail({ addToast }: any) {
  const [product, setProduct] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const id = window.location.pathname.split('/').pop();

  useEffect(() => {
    console.log(`Fetching specific intelligence on ID: ${id}`);
    axios.get(`${API_URL}/products/${id}`)
      .then(res => setProduct(res.data))
      .catch((e: any) => {
        console.error(`Failed to load product ${id}:`, e);
        addToast(`Asset retrieval issue: ${e.message}`, 'error');
      });

    axios.get(`${API_URL}/products/${id}/history`)
      .then(res => {
        if (Array.isArray(res.data)) {
          console.log(`Historical tracking points:`, res.data);
          setHistory(res.data.map((h: any) => ({
            date: new Date(h.timestamp).toLocaleDateString(),
            price: h.price
          })));
        }
      })
      .catch((e: any) => console.error('Tracking failure:', e));
  }, [id, addToast]);

  if (!product) return <div className="animate-fade" style={{fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--neon-cyan)'}}>Decrypting asset signatures...</div>;

  return (
    <div className="detail-container animate-fade">
      <div className="detail-header">
        <div className="detail-image-box">
          <img src={product.image || "https://placehold.co/400x400"} alt={product.name} className="detail-image" />
        </div>
        <div className="detail-info">
          <p className="detail-brand">{product.brand}</p>
          <h1 className="detail-title">{product.name}</h1>
          <div className="detail-price-box">
            <span className="detail-price">${product.price}</span>
            <span className="detail-old-price">${(product.price * 1.15).toFixed(2)}</span> 
          </div>
          <div>
             <a href={product.url} target="_blank" rel="noopener noreferrer" className="btn-black">
               Access Origin Matrix <ExternalLink size={20} />
             </a>
          </div>
        </div>
      </div>
      
      <div>
        <h2 className="section-title">
          <Activity size={24} style={{color: 'var(--neon-pink)'}} /> Trajectory Analytics
        </h2>
        
        {history.length > 0 ? (
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={history}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(0, 243, 255, 0.1)" />
                <XAxis dataKey="date" axisLine={false} tickLine={false} tick={{fill: '#8b8b99'}} dy={15} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#8b8b99'}} tickFormatter={(value) => `$${value}`} dx={-15} domain={['dataMin - 50', 'dataMax + 50']} />
                <Tooltip cursor={{fill: 'rgba(0, 243, 255, 0.05)'}} contentStyle={{background: 'rgba(10, 10, 22, 0.9)', backdropFilter: 'blur(10px)', border: '1px solid var(--neon-cyan)', borderRadius: '12px', padding: '16px', boxShadow: '0 0 20px rgba(0, 243, 255, 0.2)', color: '#fff'}} />
                <Line type="monotone" dataKey="price" stroke="var(--neon-cyan)" strokeWidth={4} dot={{r: 6, fill: '#0a0a16', strokeWidth: 3, stroke: 'var(--neon-cyan)'}} activeDot={{r: 8, fill: 'var(--neon-pink)', stroke: '#fff', strokeWidth: 2}} animationDuration={2000} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p style={{color: 'var(--text-muted)', fontStyle: 'italic'}}>Awaiting sufficient temporal data to compile chart.</p>
        )}
      </div>
    </div>
  );
}

// --- Main App Setup ---
export default function App() {
  const { toasts, addToast, removeToast } = useToast();

  return (
    <Router>
      <div className="app-container">
        
        {/* Global Toast Drawer */}
        <div className="toast-container">
          {toasts.map(t => (
            <Toast key={t.id} message={t.msg} type={t.type} onClose={() => removeToast(t.id)} />
          ))}
        </div>

        <aside className="sidebar">
          <div className="sidebar-header">
            <h1 className="logo-text">
              <Activity size={28} /> ENTPrice
            </h1>
          </div>
          <nav className="nav-links">
            <Link to="/" className="nav-item">
              <Activity size={20} /> Dashboard
            </Link>
            <Link to="/products" className="nav-item">
              <Package size={20} /> Directory
            </Link>
          </nav>
        </aside>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard addToast={addToast} />} />
            <Route path="/products" element={<ProductList addToast={addToast} />} />
            <Route path="/products/:id" element={<ProductDetail addToast={addToast} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
