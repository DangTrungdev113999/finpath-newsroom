import type { PipelineRunsManifest } from '../types';

// Phase H GitHub Pages: prepend Vite BASE_URL, mirror articleLoader pattern.
// web/public/articles is a symlink to output/compare-feed/, so pipeline-runs.json
// is served from ${BASE_URL}articles/pipeline-runs.json.
const MANIFEST_URL = `${import.meta.env.BASE_URL.replace(/\/$/, '')}/articles/pipeline-runs.json`;

export async function loadPipelineRuns(): Promise<PipelineRunsManifest> {
  const response = await fetch(MANIFEST_URL, { cache: 'no-store' });

  // First-deploy graceful: file missing OR Vite SPA fallback returns index.html
  // (dev/preview without prior pipeline runs). Return empty manifest both cases.
  if (response.status === 404) {
    return { built_at: new Date().toISOString(), sessions: [] };
  }
  if (!response.ok) {
    throw new Error(
      `Lỗi load pipeline-runs.json: ${response.status} ${response.statusText}`,
    );
  }

  const contentType = response.headers.get('content-type') ?? '';
  if (!contentType.includes('json')) {
    return { built_at: new Date().toISOString(), sessions: [] };
  }

  return response.json();
}
