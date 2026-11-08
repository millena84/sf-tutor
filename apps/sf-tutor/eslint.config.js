import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist', 'node_modules', 'public', 'playwright-report', 'test-results'] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    languageOptions: { ecmaVersion: 2022, sourceType: 'module' },
    rules: {
      // conteúdo dos dados nunca vai para innerHTML/outerHTML/insertAdjacentHTML/document.write
      'no-restricted-properties': ['error',
        { property: 'innerHTML', message: 'Use h()/textContent: conteúdo dos dados não pode virar HTML.' },
        { property: 'outerHTML', message: 'Use h()/textContent.' },
        { property: 'insertAdjacentHTML', message: 'Use h()/textContent.' },
      ],
      'no-restricted-syntax': ['error', { selector: "CallExpression[callee.object.name='document'][callee.property.name='write']", message: 'Sem document.write.' }],
      'no-eval': 'error',
      'no-implied-eval': 'error',
      'no-new-func': 'error',
    },
  },
);
