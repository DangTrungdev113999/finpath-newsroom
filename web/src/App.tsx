import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { IndexPage } from './pages/IndexPage';
import { ArticlePage } from './pages/ArticlePage';
import { FeedPage } from './pages/FeedPage';
import { Header } from './components/Header';

// Phase G GitHub Pages: BASE_URL = '/finpath-newsroom/' (build) hoặc '/' (dev).
// React Router basename phải khớp Vite base để deep-link work trên Pages.
const BASENAME = import.meta.env.BASE_URL.replace(/\/$/, '') || '/';

export default function App() {
  return (
    <BrowserRouter basename={BASENAME}>
      <Header />
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/feed" element={<FeedPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
      </Routes>
    </BrowserRouter>
  );
}
