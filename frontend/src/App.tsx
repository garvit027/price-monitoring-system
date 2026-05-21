import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { RefreshCw, Package, Activity, DollarSign, ExternalLink, Bell, AlertCircle, CheckCircle, LogOut, Plus, User, Mail, Calendar, Shield, Key, TrendingUp } from 'lucide-react';
import './style.css';

const API_URL = 'https://price-monitoring-system.onrender.com/api';

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
  const [loading, setLoading] = useState(true);
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
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="animate-fade">
      <div className="page-header">
        <h1 className="page-title">Datacenter Control</h1>
        <div style={{ color: 'var(--text-muted)', fontSize: '14px' }}>
          <Activity size={14} className="animate-pulse" style={{ marginRight: 8, color: 'var(--accent-primary)' }} />
          Autonomous Sync Active
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
            <p className="stat-value">₹{stats.average_price}</p>
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
          <h2 className="section-title"><Package className="text-accent-primary" /> Category Averages</h2>
          <div className="notification-list">
            {Object.entries(stats.by_category || {}).length === 0 ? <span style={{ color: 'var(--text-muted)' }}>No aggregate data</span> : Object.entries(stats.by_category).map(([cat, avg]: any) => (
              <div key={cat} className="notification-item" style={{ display: 'flex', justifyContent: 'space-between', borderLeftColor: 'var(--accent-primary)' }}>
                <span>{cat}</span>
                <span style={{ color: 'var(--accent-primary)', fontWeight: 'bold' }}>₹{avg}</span>
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
  const navigate = useNavigate();

  const fetchProducts = () => {
    axios.get(`${API_URL}/products?limit=100`)
      .then(res => setProducts(res.data))
      .catch((e: any) => addToast(`Failed fetching directory: ${e.message}`, 'error'));
  };

  useEffect(() => {
    fetchProducts();
  }, [addToast]);

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
                <p className="product-price">₹{p.price}</p>
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
    axios.get(`${API_URL}/products/${id}`)
      .then(res => setProduct(res.data))
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

  if (!product) return <div className="animate-fade" style={{ fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--accent-primary)' }}>Decrypting asset signatures...</div>;

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
            <span className="detail-price">₹{product.price}</span>
            {history.length > 0 && Math.max(...history.map(h => h.price)) > product.price && (
              <span className="detail-old-price">₹{Math.max(...history.map(h => h.price)).toFixed(2)}</span>
            )}
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
                  tickFormatter={(value) => `₹${value}`}
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

  useEffect(() => {
    const fetchAll = async () => {
      try {
        const [userRes, statsRes] = await Promise.all([
          axios.get(`${API_URL}/auth/me`),
          axios.get(`${API_URL}/analytics`),
        ]);
        setUser(userRes.data);
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
            <p className="stat-value">₹{stats.average_price ?? 0}</p>
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
          <div className="sidebar-header">
            <h1 className="logo-text">
              <Activity size={28} /> PriceMonitor
            </h1>
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
