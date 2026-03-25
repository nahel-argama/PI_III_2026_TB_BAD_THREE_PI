import { defineConfig, globalIgnores } from 'eslint/config';
import globals from 'globals';
import js from '@eslint/js';
import pluginVue from 'eslint-plugin-vue';
import pluginOxlint from 'eslint-plugin-oxlint';
import unusedImports from 'eslint-plugin-unused-imports';
import skipFormatting from 'eslint-config-prettier/flat';

export default defineConfig([
  {
    name: 'app/files-to-lint',
    files: ['**/*.{vue,js,mjs,jsx}'],
  },

  globalIgnores(['**/dist/**', '**/dist-ssr/**', '**/coverage/**']),

  {
    languageOptions: {
      globals: {
        ...globals.browser,
      },
    },
  },

  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],

  {
    name: 'app/base-rules',
    plugins: {
      vue: pluginVue,
      'unused-imports': unusedImports,
    },
    rules: {
      /*
       * Base JS
       */
      'no-var': 'warn',
      'prefer-const': 'warn',
      'no-console': 'warn',
      'no-debugger': 'warn',

      /*
       * Unused code
       * - desliga a regra nativa para evitar duplicidade
       * - usa plugin específico para imports não usados
       */
      'no-unused-vars': 'off',
      'unused-imports/no-unused-imports': 'warn',
      'unused-imports/no-unused-vars': [
        'warn',
        {
          vars: 'all',
          varsIgnorePattern: '^$',
          args: 'after-used',
          argsIgnorePattern: '^$',
        },
      ],

      /*
       * Vue SFC structure
       */
      'vue/block-order': [
        'warn',
        {
          order: ['template', 'script', 'style'],
        },
      ],

      /*
       * Vue template organization
       */
      'vue/attributes-order': 'warn',
      'vue/max-attributes-per-line': [
        'warn',
        {
          singleline: 1,
          multiline: 1,
        },
      ],
      'vue/first-attribute-linebreak': [
        'warn',
        {
          singleline: 'ignore',
          multiline: 'below',
        },
      ],
      'vue/html-self-closing': [
        'warn',
        {
          html: {
            void: 'always',
            normal: 'never',
            component: 'always',
          },
          svg: 'always',
          math: 'always',
        },
      ],

      /*
       * Vue props / emits
       */
      'vue/require-explicit-emits': 'warn',
      'vue/require-valid-default-prop': 'error',
      'vue/no-required-prop-with-default': 'error',
      'vue/no-mutating-props': 'error',

      /*
       * Vue Composition API / script setup
       * Evita alguns problemas comuns com props no setup.
       */
      'vue/no-setup-props-reactivity-loss': 'error',

      /*
       * Ordem simplificada para casos onde ainda existir export default
       * sem ficar rígido demais para Composition API.
       */
      'vue/order-in-components': [
        'warn',
        {
          order: [
            'name',
            ['components', 'directives'],
            ['props', 'propsData'],
            'emits',
            'setup',
            'computed',
            'watch',
            'methods',
            ['template', 'render'],
          ],
        },
      ],
    },
  },

  ...pluginOxlint.buildFromOxlintConfigFile('.oxlintrc.json'),

  skipFormatting,
]);
