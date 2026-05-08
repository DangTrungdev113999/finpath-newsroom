import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { IndexPage } from './pages/IndexPage';
import { ArticlePage } from './pages/ArticlePage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<IndexPage />} />
        <Route path="/article/:id" element={<ArticlePage />} />
      </Routes>
    </BrowserRouter>
  );
}
