import { describe, expect, it } from 'vitest';
import { h } from '../../src/ui/dom';

describe('h() não interpreta HTML vindo dos dados', () => {
  it('texto com tags vira texto', () => {
    const el = h('p', null, '<img src=x onerror=alert(1)>');
    expect(el.querySelector('img')).toBeNull();
    expect(el.textContent).toBe('<img src=x onerror=alert(1)>');
  });
  it('href só aceita http(s), ? e #', () => {
    expect(h('a', { href: 'javascript:alert(1)' }).getAttribute('href')).toBeNull();
    expect(h('a', { href: 'https://developer.salesforce.com/' }).getAttribute('href')).toBe('https://developer.salesforce.com/');
    expect(h('a', { href: '?n=obj:User' }).getAttribute('href')).toBe('?n=obj:User');
  });
});
