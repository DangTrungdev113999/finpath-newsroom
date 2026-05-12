import { describe, it, expect, vi, beforeEach } from 'vitest';
import { loadPipelineRuns } from './pipelineRunsLoader';

describe('loadPipelineRuns', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('fetches pipeline-runs.json and returns sessions', async () => {
    const mockManifest = {
      built_at: '2026-05-12T15:30:00Z',
      sessions: [
        {
          session_id: 'abc',
          trigger_type: 'tin',
          trigger_args: 'VHM',
          started_at: '2026-05-12T14:30:00Z',
          ended_at: '2026-05-12T14:35:00Z',
          fetched_total: 10,
          chosen_total: 3,
          rejected_total: 7,
          batches: [],
        },
      ],
    };
    vi.spyOn(global, 'fetch').mockResolvedValue(
      new Response(JSON.stringify(mockManifest), {
        status: 200,
        headers: { 'content-type': 'application/json' },
      }),
    );

    const result = await loadPipelineRuns();
    expect(result.sessions).toHaveLength(1);
    expect(result.sessions[0].session_id).toBe('abc');
  });

  it('returns empty manifest when 404 (first deploy, no pipeline runs yet)', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(
      new Response('Not found', { status: 404 }),
    );
    const result = await loadPipelineRuns();
    expect(result.sessions).toEqual([]);
    expect(result.built_at).toMatch(/^\d{4}-\d{2}-\d{2}T/);
  });

  it('returns empty manifest when Vite SPA fallback returns index.html', async () => {
    // Dev/preview without prior pipeline runs: missing JSON file falls through
    // to SPA index.html with HTTP 200 + text/html content-type.
    vi.spyOn(global, 'fetch').mockResolvedValue(
      new Response('<!doctype html><html>...</html>', {
        status: 200,
        headers: { 'content-type': 'text/html' },
      }),
    );
    const result = await loadPipelineRuns();
    expect(result.sessions).toEqual([]);
  });

  it('throws when manifest fetch fails (non-404)', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(
      new Response('Server error', { status: 500 }),
    );
    await expect(loadPipelineRuns()).rejects.toThrow();
  });
});
