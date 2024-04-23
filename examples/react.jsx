// Author: https://github.com/mauroreisvieira/github-sublime-theme/
import { useState } from 'react';

export function Counter({ name }) {
    const [count, setCount] = useState(0);

    function onClick() {
        setCount(count => count + 1);
    }

    return (
        <div>
            <h2
                style={{
                    color: 'red',
                    fontSize: 24,
                }}
            >
                {name}'s count: {count}
            </h2>
            <button onClick={onClick}>+</button>
        </div>
    );
}

import { MonacoEditor } from 'solid-monaco';

import Editor from './Editor';
import './main.css'

const root = document.getElementById('root');

if (import.meta.env.DEV && !(root instanceof HTMLElement)) {
  throw new Error(
    'Root element not found. Did you forget to add it to your index.html? Or maybe the id attribute got misspelled?',
  );
}

render(() => <Editor />, root);