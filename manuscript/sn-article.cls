\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{sn-article}[2026/08/20 v1.0 Springer Nature simplified class]

\LoadClass[twocolumn,10pt,letterpaper]{article}

\RequirePackage{graphicx}
\RequirePackage{amsmath,amssymb,amsfonts}
\RequirePackage{booktabs}
\RequirePackage{xcolor}
\RequirePackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
\RequirePackage{siunitx}
\RequirePackage[numbers,sort&compress]{natbib}
\RequirePackage{lineno}
\RequirePackage{newtxtext,newtxmath}
\RequirePackage[margin=2.5cm]{geometry}
\RequirePackage{authblk}

\newcommand{\abstract}[1]{\def\@abstract{#1}}
\newcommand{\keywords}[1]{\def\@keywords{#1}}

\renewcommand{\maketitle}{%
  \twocolumn[%
  \begin{center}%
    {\LARGE \bfseries \@title \par}%
    \vskip 1.5em%
    {\large \@author \par}%
    \vskip 1.5em%
  \end{center}%
  \@ifundefined{@abstract}{}{%
    \begin{quotation}
    \noindent\textbf{Abstract}\par\noindent\@abstract
    \vskip 1em
    \@ifundefined{@keywords}{}{%
      \noindent\textbf{Keywords: } \@keywords
    }
    \end{quotation}
  }
  \vskip 2em%
  ]%
}
