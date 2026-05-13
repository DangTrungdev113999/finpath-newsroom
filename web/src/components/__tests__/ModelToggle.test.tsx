import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { ModelToggle } from '../ModelToggle';

describe('ModelToggle', () => {
  it('renders Claude active and Gemini disabled when gemini unavailable', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle selected="claude" onChange={onChange} geminiAvailable={false} />,
    );
    const claude = screen.getByRole('radio', { name: 'Bài Claude' });
    const gemini = screen.getByRole('radio', { name: /Bài Gemini không khả dụng/ });
    expect(claude.getAttribute('aria-checked')).toBe('true');
    expect(gemini.getAttribute('aria-checked')).toBe('false');
    expect(gemini.getAttribute('aria-disabled')).toBe('true');
  });

  it('switches to Gemini on click when available', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle selected="claude" onChange={onChange} geminiAvailable={true} />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Gemini' }));
    expect(onChange).toHaveBeenCalledWith('gemini');
  });

  it('does not fire onChange when Gemini is disabled', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle selected="claude" onChange={onChange} geminiAvailable={false} />,
    );
    fireEvent.click(
      screen.getByRole('radio', { name: /Bài Gemini không khả dụng/ }),
    );
    expect(onChange).not.toHaveBeenCalled();
  });

  it('does not fire onChange when clicking the already-active button', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle selected="gemini" onChange={onChange} geminiAvailable={true} />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Gemini' }));
    expect(onChange).not.toHaveBeenCalled();
  });

  it('switches back to Claude on click from Gemini', () => {
    const onChange = vi.fn();
    render(
      <ModelToggle selected="gemini" onChange={onChange} geminiAvailable={true} />,
    );
    fireEvent.click(screen.getByRole('radio', { name: 'Bài Claude' }));
    expect(onChange).toHaveBeenCalledWith('claude');
  });
});
