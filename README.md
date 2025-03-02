# ![](docs/img/bookmark_border-24px.svg) pdf-yaml-bookmark
A command line tool that adds a bookmark (table of contents, or outline) to PDF files.

### Prerequisites

Make sure you have `ghostscript` installed. In Mac, you can use `homebrew`:

```
brew install ghostscript
```

`ghostscript` for windows can be installed from [the official website](https://www.ghostscript.com/releases/gsdnld.html)

### Installation
```
$ pip install pdf-yaml-bookmark
```

### Sample output

<img src="docs/img/demo-output.png" width="300" style="margin:auto">


### Sample bookmark file: `sample.bkm`

```
# This is a comment
First Chapter 1
    first section 1
        first subsection 1
    second section 4
    third section 5

# An offset to fix a gap between pdf pages and content pages
+10

Second Chapter 10
    some entry 10
    some entry 11
```

### Usage
```
$ pdf-yaml-bookmark sample.pdf sample.bkm -o sample-out.pdf --show-progress
 |██████████████████████----------------------------| 118/263
```

optionally, the ghost script executable can be specified as well

```
$ pdf-yaml-bookmark sample.pdf sample.bkm -o sample-out.pdf --gs-path 'C:\Program Files\gs\gs9.55.0\bin\gswin64.exe' --show-progress

```

It also supports for bookmark in YAML format:
```
$ pdf-yaml-bookmark sample.pdf sample.yaml --format='yaml' -o sample-out.pdf
```
where a YAML file looks like:
```
# This is a comment
-
 heading: First Chapter
 page: 1
 children:
    -
     heading: First section
     page: 1
     children:
        -
         heading: Second section
         page: 1
         children:
-
 heading: First Chapter
 page: 1
 children:
    -
     heading: First section
     page: 1
     children:
    -
     heading: Second section
     page: 1
     children:
```
