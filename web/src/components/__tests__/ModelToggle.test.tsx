import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ModelToggle } from '../ModelToggle';

describe('ModelToggle', () => {
  it('renders Claude active and parallel sides disabled when unavailable', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="claude"
        onChange={onChange}
        geminiAvailable={false}
        grokAvailable={false}
      />,
    );
    const claude = screen.getByRole('radio', { name: 'Bài Claude' });
    const gemini = screen.getByRole('radio', { name: /Bài Gemini không khả dụng/ });
    const grok = screen.getByRole('radio', { name: /Bài Grok không khả dụng/ });
    expect(claude.getAttribute('aria-checked')).toBe('true');
    expect(gemini.getAttribute('aria-checked')).toBe('false');
    expect(grok.getAttribute('aria-checked')).toBe('false');
    expect(gemini.getAttribute('aria-disabled')).toBe('true');
    expect(grok.getAttribute('aria-disabled')).toBe('true');
  });

  it('switches to Gemini on click when available', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="claude"
        onChange={onChange}
        geminiAvailable={true}
        grokAvailable={false}
      />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Gemini' }));
    expect(onChange).toHaveBeenCalledWith('gemini');
  });

  it('switches to Grok on click when available', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="claude"
        onChange={onChange}
        geminiAvailable={false}
        grokAvailable={true}
      />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Grok' }));
    expect(onChange).toHaveBeenCalledWith('grok');
  });

  it('does not fire onChange when Gemini is disabled', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="claude"
        onChange={onChange}
        geminiAvailable={false}
        grokAvailable={true}
      />,
    );
    fireEvent.click(
      screen.getByRole('radio', { name: /Bài Gemini không khả dụng/ }),
    );
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not fire onChange when Grok is disabled', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="claude"
        onChange={onChange}
        geminiAvailable={true}
        grokAvailable={false}
      />,
    );
    fireEvent.click(
      screen.getByRole('radio', { name: /Bài Grok không khả dụng/ }),
    );
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not fire onChange when clicking the already-active button', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="gemini"
        onChange={onChange}
        geminiAvailable={true}
        grokAvailable={true}
      />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Gemini' }));
    expect(onChange).not.toHaveBeenCalled();
  });

  it('switches back to Claude on click from Gemini', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="gemini"
        onChange={onChange}
        geminiAvailable={true}
        grokAvailable={true}
      />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Claude' }));
    expect(onChange).toHaveBeenCalledWith('claude');
  });

  it('switches from Grok back to Claude', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle
        selected="grok"
        onChange={onChange}
        geminiAvailable={true}
        grokAvailable={true}
      />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Claude' }));
    expect(onChange).toHaveBeenCalledWith('claude');
  });

  it('Grok button has aria-checked when grok is selected', () => {
    render(
      <ModelToggle
        selected="grok"
        onChange={vi.fn()}
        geminiAvailable={true}
        grokAvailable={true}
      />,
    );
    expect(
      screen.getByRole('radio', { name: 'Bài Grok' }).getAttribute('aria-checked'),
    ).toBe('true');
  });
});
