import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          strong: ({ children }) => (
            <strong className="font-semibold text-fg-0">{children}</strong>
          ),
          h2: ({ children }) => (
            <h2 className="!mt-6 !mb-5 px-4 py-2.5 rounded-r-xl bg-bg-2 border-l-[3px] border-fg-4 text-base font-semibold text-fg-0">
              {children}
            </h2>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
