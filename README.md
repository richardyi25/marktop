# Marktop

Marktop is a single-purpose "lightweight" parser that converts Marktop code to HTML code.

In other words, it's a single 300-line Python file that parses some Markdown-like code to HTML just so I don't have to directly write the HTML for my website.

The usage is currently extremely limited so there's no real point in using it right now unless you want your websites to look and be structured exactly like mine.

## Installation (Linux and similar)


```
git clone https://github.com/richardyi25/marktop.git
cd marktop
cp marktop.py marktop
chmod +x marktop
sudo mv marktop /usr/bin
```

You must also include `style.css`, `prism.css`, and `prism.js` in your project folder.

## Usage

```
marktop in.mt out.html
```

Note that the file extension is not important. `in.mt` represents the Marktop file, `out.html` represents the output HTML file.

## Documentation

[Documentation, demos, etc.](https://richardyi25.github.io/marktop)

## Vim Support (Linux and similar)

For syntax highlighting, copy `marktop.vim` to `~/.vim/syntax`. If it doesn't exist, create it. Then add
```
autocmd BufRead,BufNewFile *.mt set filetype=marktop
```
to your `.vimrc`.

For automatic Marktop on filesave, add

```
autocmd BufWritePost *.mt silent !marktop %:r.mt %:r.html
```

Marktop must be installed. This will automatically convert to `[filename].html` if you save while editing `[filename].mt`
