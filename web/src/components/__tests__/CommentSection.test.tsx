// web/src/components/__tests__/CommentSection.test.tsx
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CommentSection } from '../CommentSection';
import * as client from '../../lib/feedbackClient';
import { resetStorage, saveName, appendComment } from '../../lib/feedbackStorage';

beforeEach(() => {
  resetStorage();
  vi.spyOn(client, 'isFeedbackEnabled').mockReturnValue(true);
});

describe('CommentSection', () => {
  it('renders nothing when isFeedbackEnabled() is false', () => {
    vi.spyOn(client, 'isFeedbackEnabled').mockReturnValue(false);
    const { container } = render(
      <CommentSection articleId="x" articleTitle="t" ticker="VCB" />,
    );
    expect(container.firstChild).toBeNull();
  });

  it('renders collapsed CTA initially', () => {
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    expect(screen.getByText(/Góp ý cho bài này/)).toBeInTheDocument();
  });

  it('expands to show form on click', () => {
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.getByPlaceholderText(/Nhập góp ý/)).toBeInTheDocument();
  });

  it('shows name field on first use, hides after saved', () => {
    const { rerender } = render(
      <CommentSection articleId="x" articleTitle="t" ticker="VCB" />,
    );
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.getByPlaceholderText(/Tên/)).toBeInTheDocument();

    saveName('Trung');
    rerender(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    expect(screen.queryByPlaceholderText(/Tên/)).toBeNull();
  });

  it('disables submit when comment too short', () => {
    saveName('Trung');
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/);
    fireEvent.change(ta, { target: { value: 'hi' } });
    expect(screen.getByRole('button', { name: /Gửi/ })).toBeDisabled();
  });

  it('submits payload then clears textarea on success', async () => {
    saveName('Trung');
    const submitSpy = vi
      .spyOn(client, 'submitFeedback')
      .mockResolvedValue({ ok: true, telegram_message_id: 999 });
    render(<CommentSection articleId="vcb-1" articleTitle="VCB" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/) as HTMLTextAreaElement;
    fireEvent.change(ta, { target: { value: 'câu opening hơi lủng' } });
    fireEvent.click(screen.getByRole('button', { name: /Gửi/ }));

    await waitFor(() => expect(submitSpy).toHaveBeenCalled());
    const payload = submitSpy.mock.calls[0][0];
    expect(payload.name).toBe('Trung');
    expect(payload.comment).toBe('câu opening hơi lủng');
    expect(payload.article_id).toBe('vcb-1');
    expect(payload.ticker).toBe('VCB');

    await waitFor(() => expect(ta.value).toBe(''));
  });

  it('keeps textarea on rate-limit error', async () => {
    saveName('Trung');
    vi.spyOn(client, 'submitFeedback').mockResolvedValue({
      ok: false,
      error: 'rate_limited',
      retry_after: 240,
    });
    render(<CommentSection articleId="x" articleTitle="t" ticker="VCB" />);
    fireEvent.click(screen.getByText(/Góp ý cho bài này/));
    const ta = screen.getByPlaceholderText(/Nhập góp ý/) as HTMLTextAreaElement;
    fireEvent.change(ta, { target: { value: 'thử submit khi rate limit' } });
    fireEvent.click(screen.getByRole('button', { name: /Gửi/ }));

    await waitFor(() => expect(screen.getByText(/đợi vài phút/i)).toBeInTheDocument());
    expect(ta.value).toBe('thử submit khi rate limit');
  });

  it('shows local history badge when comments exist', () => {
    saveName('Trung');
    // simulate prior comment (use top-level import — plan's require() is CJS, not ESM)
    appendComment('vcb-1', { comment: 'cũ', timestamp: '2026-05-11T00:00:00Z' });
    render(<CommentSection articleId="vcb-1" articleTitle="t" ticker="VCB" />);
    expect(screen.getByText(/1/)).toBeInTheDocument(); // badge count
  });
});
