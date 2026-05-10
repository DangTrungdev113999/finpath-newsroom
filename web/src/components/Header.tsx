import { Link, useLocation } from 'react-router-dom';

export function Header() {
  const { pathname } = useLocation();
  const isCards = pathname === '/' || pathname.startsWith('/article/');
  const isFeed = pathname === '/feed';

  return (
    <header className="sticky top-0 z-10 border-b border-gray-200 bg-white px-6 py-3">
      <div className="mx-auto flex max-w-7xl items-center justify-between">
        <Link to="/" className="text-base font-semibold text-gray-900">
          📰 Finpath Newsroom
        </Link>
        <nav className="flex gap-1 text-sm">
          <Link
            to="/"
            className={`rounded-md px-3 py-1.5 ${isCards ? 'bg-gray-900 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Cards
          </Link>
          <Link
            to="/feed"
            className={`rounded-md px-3 py-1.5 ${isFeed ? 'bg-gray-900 text-white' : 'text-gray-600 hover:bg-gray-100'}`}
          >
            Feed
          </Link>
        </nav>
      </div>
    </header>
  );
}
