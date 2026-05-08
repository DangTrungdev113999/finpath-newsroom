import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

export function Markdown({ children }: { children: string }) {
  return (
    <div className="prose-content">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          strong: ({ children }) => (
            <strong className="font-semibold text-gray-900">{children}</strong>
          ),
        }}
      >
        {children}
      </ReactMarkdown>
    </div>
  );
}
