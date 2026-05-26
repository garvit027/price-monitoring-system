import os

path = "/Users/garvitjuneja27/price-monitoring-system copy/frontend/src/App.tsx"

with open(path, "r") as f:
    content = f.read()

# Phase 1: Icons
content = content.replace(
    "import { RefreshCw, Package, Activity, DollarSign, ExternalLink, Bell, AlertCircle, CheckCircle, LogOut, Plus, User, Mail, Calendar, Shield, Key, TrendingUp } from 'lucide-react';",
    "import { RefreshCw, Package, Activity, DollarSign, ExternalLink, Bell, AlertCircle, CheckCircle, LogOut, Plus, User, Mail, Calendar, Shield, Key, TrendingUp, DownloadCloud, Sun, Moon } from 'lucide-react';"
)

# Phase 1: Export CSV in Dashboard
export_csv_func = """  const handleExportCSV = async () => {
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
"""
content = content.replace("  return (\n    <div className=\"animate-fade\">\n      <div className=\"page-header\" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>", export_csv_func + "    <div className=\"animate-fade\">\n      <div className=\"page-header\" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>")

export_btn = """        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <button onClick={handleExportCSV} className="btn-primary" style={{ padding: '8px 16px', background: 'var(--accent-primary)', color: 'white' }}>
            <DownloadCloud size={16} /> Export CSV
          </button>
"""
content = content.replace("""        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>\n""", export_btn, 1)

# Phase 1: Theme Toggle
theme_state = """  const { toasts, addToast, removeToast } = useToast();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [theme, setTheme] = useState(localStorage.getItem('theme') || 'dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === 'dark' ? 'light' : 'dark');
"""
content = content.replace("""  const { toasts, addToast, removeToast } = useToast();\n  const [isAuthenticated, setIsAuthenticated] = useState(false);""", theme_state)

theme_btn = """          <div className="sidebar-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h1 className="logo-text">
              <Activity size={28} /> PriceMonitor
            </h1>
            <button onClick={toggleTheme} className="nav-item" style={{ width: 'auto', background: 'transparent', padding: '8px', cursor: 'pointer' }}>
              {theme === 'dark' ? <Sun size={20} color="var(--text-muted)" /> : <Moon size={20} color="var(--text-muted)" />}
            </button>
          </div>"""
content = content.replace("""          <div className="sidebar-header">\n            <h1 className="logo-text">\n              <Activity size={28} /> PriceMonitor\n            </h1>\n          </div>""", theme_btn)

# Phase 2: Telegram
profile_state = """  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [pwForm, setPwForm] = useState({ current: '', newPw: '', confirm: '' });
  const [telegramId, setTelegramId] = useState('');"""
content = content.replace("""  const [showPasswordForm, setShowPasswordForm] = useState(false);\n  const [pwForm, setPwForm] = useState({ current: '', newPw: '', confirm: '' });""", profile_state)

profile_fetch = """        setUser(userRes.data);
        if (userRes.data.telegram_chat_id) setTelegramId(userRes.data.telegram_chat_id);
        setStats(statsRes.data);"""
content = content.replace("""        setUser(userRes.data);\n        setStats(statsRes.data);""", profile_fetch)

telegram_save = """  const handleSaveTelegram = async () => {
    try {
      await axios.patch(`${API_URL}/auth/profile`, { telegram_chat_id: telegramId });
      addToast('Telegram ID saved successfully', 'success');
    } catch (e: any) {
      addToast('Failed to save Telegram ID', 'error');
    }
  };

  if (loading) return <div className="animate-fade" style={{ fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--accent-primary)' }}>Loading profile...</div>;"""
content = content.replace("""  if (loading) return <div className="animate-fade" style={{ fontSize: 24, textAlign: 'center', marginTop: 100, color: 'var(--accent-primary)' }}>Loading profile...</div>;""", telegram_save, 1)

telegram_ui = """            </form>
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
      </div>"""
content = content.replace("""            </form>\n          )}\n        </div>\n      </div>""", telegram_ui)


# Phase 3: Folders in ProductList
pl_state = """  const [trackUrl, setTrackUrl] = useState("");
  const [isTracking, setIsTracking] = useState(false);
  const [collections, setCollections] = useState<any[]>([]);
  const [selectedFolder, setSelectedFolder] = useState<number | null>(null);
  const [newFolderName, setNewFolderName] = useState('');"""
content = content.replace("""  const [trackUrl, setTrackUrl] = useState("");\n  const [isTracking, setIsTracking] = useState(false);""", pl_state)

pl_fetch = """  const fetchProducts = () => {
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
  };"""
content = content.replace("""  const fetchProducts = () => {
    axios.get(`${API_URL}/products?limit=1000`)
      .then(res => setProducts(res.data))
      .catch((e: any) => addToast(`Failed fetching directory: ${e.message}`, 'error'));
  };

  useEffect(() => {
    fetchProducts();
  }, [addToast]);""", pl_fetch)

pl_filter = """  const filteredProducts = products.filter(p => {
    let filtered = products;
    if (selectedSource) {
      filtered = filtered.filter(p => p.source === selectedSource);
    }
    if (selectedFolder !== null) {
      filtered = filtered.filter(p => p.collection_id === selectedFolder);
    }
    const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.brand?.toLowerCase().includes(searchQuery.toLowerCase());
    return filtered.includes(p) && matchSearch;
  });"""
content = content.replace("""  const filteredProducts = products.filter(p => {
    const matchSource = selectedSource ? p.source === selectedSource : true;
    const matchSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase()) || p.brand?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchSource && matchSearch;
  });""", pl_filter)

pl_render_start = """  return (
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
        <div className="page-header" style={{ marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'space-between', alignItems: 'center' }}>"""
content = content.replace("""  return (
    <div className="animate-fade">
      <div className="page-header" style={{ marginBottom: 24, display: 'flex', flexWrap: 'wrap', gap: 24, justifyContent: 'space-between', alignItems: 'center' }}>""", pl_render_start)

pl_render_end = """        </div>
      </div>
    </div>
  );
}

// --- Product Detail Component ---"""
content = content.replace("""      </div>\n    </div>\n  );\n}\n\n// --- Product Detail Component ---""", pl_render_end)

# Phase 3 & 4: Folders and Search in ProductDetail
pd_state = """  const [product, setProduct] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [collections, setCollections] = useState<any[]>([]);
  const [alertPriceInput, setAlertPriceInput] = useState("");
  const [updatingAlert, setUpdatingAlert] = useState(false);
  const id = window.location.pathname.split('/').pop();
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`${API_URL}/collections`).then(res => setCollections(res.data)).catch(() => {});
  }, []);"""
content = content.replace("""  const [product, setProduct] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [alertPriceInput, setAlertPriceInput] = useState("");
  const [updatingAlert, setUpdatingAlert] = useState(false);
  const id = window.location.pathname.split('/').pop();
  const navigate = useNavigate();""", pd_state)

pd_funcs = """  const handleClearAlert = async () => {
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
  };"""
content = content.replace("""  const handleClearAlert = async () => {
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
  };""", pd_funcs)

pd_ui = """          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
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
          </div>"""
content = content.replace("""          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginBottom: '24px' }}>
            <a href={product.url} target="_blank" rel="noopener noreferrer" className="btn-black" style={{ textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '10px 20px' }}>
              Access Origin Matrix <ExternalLink size={20} />
            </a>
            <button onClick={handleDelete} className="btn-primary" style={{ background: '#ff0055', borderColor: '#ff0055', color: '#fff', padding: '10px 20px' }}>
              Stop Tracking
            </button>
          </div>""", pd_ui)

with open(path, "w") as f:
    f.write(content)
print("SUCCESS!")
