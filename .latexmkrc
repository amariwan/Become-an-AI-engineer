# Use LuaLaTeX for the main book build to support tagpdf/PDF-UA workflows
$pdf_mode = 1;
$ENV{'LC_ALL'} = 'C.UTF-8';
$ENV{'LANG'} = 'C.UTF-8';
$pdflatex = 'lualatex --interaction=nonstopmode %O %S';
$bibtex = 'bibtex %O %B';
$makeindex = 'makeindex %O %S';
$clean_ext .= ' %R.out %R.fls %R.fdb_latexmk %R.xdv';
