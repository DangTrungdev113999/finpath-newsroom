import { useEffect, useMemo, useState } from 'react';
import { Navigate, useLocation, useParams, useSearchParams } from 'react-router-dom';
import { Menu } from 'lucide-react';
import { docsForSector } from '../lib/kbLoader';
import { isSector, type Sector } from '../lib/kbTypes';
import { KbContent, KbContentNotFound } from '../components/kb/KbContent';
import { KbSidebar } from '../components/kb/KbSidebar';

export function KbPage() {
  const { slug } = useParams<{ slug?: string }>();
  const [params] = useSearchParams();
  const location = useLocation();

  const sectorParam = params.get('sector');
  const sector: Sector = isSector(sectorParam) ? sectorParam : 'bds';

  const docs = useMemo(() => docsForSector(sector), [sector]);

  const [drawerOpen, setDrawerOpen] = useState(false);

  useEffect(() => {
    setDrawerOpen(false);
  }, [location.pathname, location.search]);

  useEffect(() => {
    if (!location.hash) {
      window.scrollTo({ top: 0 });
      return;
    }
    const id = location.hash.slice(1);
    const t = setTimeout(() => {
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 50);
    return () => clearTimeout(t);
  }, [location.hash, location.pathname]);

  if (!slug) {
    if (docs.length === 0) {
      return (
        <PageShell
          sector={sector}
          docs={docs}
          drawerOpen={drawerOpen}
          setDrawerOpen={setDrawerOpen}
        >
          <div className="mx-auto max-w-[760px] px-6 py-12 text-fg-2">
            Sector này chưa có KB.
          </div>
        </PageShell>
      );
    }
    // Find master reference or first doc
    const masterDoc = docs.find((d) => d.slug.includes('master-reference') || d.slug.includes('industry-master'));
    const firstSlug = masterDoc?.slug ?? docs[0].slug;
    const qs = sector === 'bds' ? '' : `?sector=${sector}`;
    return <Navigate to={`/tai-lieu/${firstSlug}${qs}`} replace />;
  }

  const doc = docs.find((d) => d.slug === slug);

  return (
    <PageShell
      sector={sector}
      docs={docs}
      drawerOpen={drawerOpen}
      setDrawerOpen={setDrawerOpen}
    >
      {doc ? <KbContent doc={doc} /> : <KbContentNotFound slug={slug} />}
    </PageShell>
  );
}

function PageShell({
  sector,
  docs,
  drawerOpen,
  setDrawerOpen,
  children,
}: {
  sector: Sector;
  docs: ReturnType<typeof docsForSector>;
  drawerOpen: boolean;
  setDrawerOpen: (v: boolean) => void;
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-[calc(100vh-56px)]">
      <KbSidebar
        sector={sector}
        docs={docs}
        isDrawerOpen={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      />
      <main className="min-w-0 flex-1">
        <div className="flex items-center justify-between border-b border-fg-4/40 px-3 py-2 lg:hidden">
          <button
            type="button"
            onClick={() => setDrawerOpen(true)}
            className="flex items-center gap-2 rounded-md px-2 py-1.5 font-sans text-[12.5px] text-fg-2 hover:bg-bg-2 hover:text-fg-0"
            aria-label="Mở phụ lục"
          >
            <Menu className="h-4 w-4" strokeWidth={2.2} aria-hidden />
            Phụ lục
          </button>
        </div>
        {children}
      </main>
    </div>
  );
}
