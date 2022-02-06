# ![](img/bookmark_border-24px.svg) pdfoutline

A command line tool for adding an outline (a bookmark, or table of contents) to pdf files

### Prerequisites

Make sure you have `ghostscript` installed. In Mac, you can use `homebrew`:

```
brew install ghostscript
```

`ghostscript` for windows can be installed from [the official website](https://www.ghostscript.com/releases/gsdnld.html)

### Sample output

<img src="img/demo-output.png" width="300" style="margin:auto">


### Sample Table of contents file: `sample.toc`

```
# this is a comment
First Chapter 1
    first section 1
        first subsection 1
    second section 4
    third section 5

# a command to fix a gap between pdf pages and content pages
+10

Second Chapter 10
    some entry 10
    some entry 11
```

### Usage

```
$ ./pdfoutline.py sample.pdf sample.toc sample-out.pdf
 |██████████████████████----------------------------| 118/263
```

optionally, the ghost script executable can be specified as well

```
$ ./pdfoutline.py sample.pdf sample.toc sample-out.pdf --gs_path 'C:\Program Files\gs\gs9.55.0\bin\gswin64.exe'
```
