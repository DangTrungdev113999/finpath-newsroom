import { Link } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';

// KB-specific markdown renderer. Separate from <Markdown> (article-specific)
// to avoid coupling article styling to KB styling.
//
// - rehype-slug emits id="<slug>" on h2/h3 so search result clicks can
//   scroll to anchors (KbSearch uses location.hash).
// - h1 hidden (title rendered in KbContent header strip).
// - Internal link [text](./other.md) or [text](other.md) → React Router Link.
// - External link → new tab.
export function KbMarkdown({ children }: { children: string }) {
  return (
    <div className="prose-content max-w-none">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSlug]}
        components={{
          h1: () => null,
          h2: ({ id, children }) => (
            <h2
              id={id}
              className="!mt-6 !mb-5 px-4 py-2.5 rounded-r-xl bg-bg-2 border-l-[3px] border-fg-4 text-base font-semibold text-fg-0 scroll-mt-20"
            >
              {children}
            </h2>
          ),
          h3: ({ id, children }) => (
            <h3
              id={id}
              className="mt-5 mb-3 text-[14px] font-semibold text-fg-0 scroll-mt-20"
            >
              {children}
            </h3>
          ),
          strong: ({ children }) => (
            <strong className="font-semibold text-fg-0">{children}</strong>
          ),
          blockquote: ({ children }) => (
            <blockquote className="my-4 border-l-4 border-brand bg-brand/5 pl-4 py-2 text-fg-1">
              {children}
            </blockquote>
          ),
          table: ({ children }) => (
            <div className="my-4 overflow-x-auto">
              <table className="w-full border-collapse text-sm">{children}</table>
            </div>
          ),
          th: ({ children }) => (
            <th className="border border-fg-4/40 bg-bg-2 px-3 py-2 text-left font-semibold">
              {children}
            </th>
          ),
          td: ({ children }) => (
            <td className="border border-fg-4/40 px-3 py-2 align-top">{children}</td>
          ),
          a: ({ href, children }) => {
            if (href && /^[a-z0-9-]+\.md$|^\.\/[a-z0-9-]+\.md$/i.test(href)) {
              const slug = href.replace(/^\.\//, '').replace(/\.md$/i, '');
              return (
                <Link to={`/tai-lieu/${slug}`} className="text-brand hover:underline">
                  {children}
                </Link>
              );
            }
            return (
              <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-brand hover:underline"
              >
                {children}
              </a>
            );
          },
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
