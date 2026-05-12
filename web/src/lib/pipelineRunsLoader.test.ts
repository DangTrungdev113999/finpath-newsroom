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
      new Response(JSON.stringify(mockManifest), { status: 200 }),
    );

    const result = await loadPipelineRuns();
    expect(result.sessions).toHaveLength(1);
    expect(result.sessions[0].session_id).toBe('abc');
  });

  it('throws when manifest fetch fails', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue(
      new Response('Not found', { status: 404 }),
    );
    await expect(loadPipelineRuns()).rejects.toThrow();
  });
});
