# Marktop

Marktop is a single-purpose "lightweight" parser that converts Marktop code to HTML code.

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

Marktop must be installed. This will automatically write Marktop output to `[filename].html` if you save while editing `[filename].mt`.
