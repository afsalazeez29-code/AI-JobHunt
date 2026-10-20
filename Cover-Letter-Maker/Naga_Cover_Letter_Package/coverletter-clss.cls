% -----------------------------------------------------------------------------
% coverletter.cls — Large-text, full-page Times-style cover letter
% Keep this file in the same folder as your cover-letter .tex file.
% -----------------------------------------------------------------------------

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{coverletter}[2026/10/19 v1.4 Large professional cover-letter class]

\LoadClass[12pt,a4paper]{article}

% -----------------------------------------------------------------------------
% PAGE LAYOUT — generous writing area
% -----------------------------------------------------------------------------

\RequirePackage[
    a4paper,
    left=0.55in,
    right=0.55in,
    top=0.50in,
    bottom=0.50in
]{geometry}

\RequirePackage[T1]{fontenc}
\RequirePackage{newtxtext}
\RequirePackage{newtxmath}
\RequirePackage{microtype}
\RequirePackage{hyperref}
\RequirePackage{xcolor}

% -----------------------------------------------------------------------------
% GLOBAL TYPOGRAPHY
% -----------------------------------------------------------------------------

\renewcommand{\familydefault}{\rmdefault}

\hypersetup{
    hidelinks,
    pdfborder={0 0 0}
}

\urlstyle{same}
\pagestyle{empty}

\setlength{\parindent}{0pt}
\setlength{\parskip}{11pt plus 2pt minus 1pt}
\setlength{\emergencystretch}{3em}

% -----------------------------------------------------------------------------
% BODY TEXT — larger, clearer, and more readable
% -----------------------------------------------------------------------------

\renewcommand{\normalsize}{%
    \@setfontsize\normalsize{14pt}{19pt}%
}

\normalsize
\linespread{1.15}

\frenchspacing
% -----------------------------------------------------------------------------
% COVER LETTER DATA COMMANDS
% -----------------------------------------------------------------------------

\makeatletter

\def\cl@name{}
\def\cl@role{}
\def\cl@contact{}
\def\cl@date{}
\def\cl@subject{}
\def\cl@recipient{}


\newcommand{\clname}[1]{\gdef\cl@name{#1}}
\newcommand{\clrole}[1]{\gdef\cl@role{#1}}
\newcommand{\clcontact}[1]{\gdef\cl@contact{#1}}
\newcommand{\cldate}[1]{\gdef\cl@date{#1}}
\newcommand{\clrecipient}[1]{\gdef\cl@recipient{#1}}
\newcommand{\clsubject}[1]{\gdef\cl@subject{#1}}

% -----------------------------------------------------------------------------
% HEADER — large name, role and readable contact information
% -----------------------------------------------------------------------------
\newcommand{\makecoverletterhead}{%
    \noindent
    \begin{minipage}[t]{0.56\textwidth}
        \vspace{0pt}%
        {\fontsize{23}{27}\selectfont
         \bfseries\MakeUppercase{\cl@name}\par}
        \vspace{10pt}%
        {\fontsize{17}{17}\selectfont
         \cl@role\par}
    \end{minipage}%
    \hfill
    \begin{minipage}[t]{0.42\textwidth}
        \vspace{3pt}%
        \raggedleft
        {\fontsize{13}{13}\selectfont
         \cl@contact\par}
    \end{minipage}%
    \par
    \vspace{10pt}%
    \noindent\rule{\textwidth}{0.65pt}\par
    \vspace{0pt}%
}
% -----------------------------------------------------------------------------
% LETTER DETAILS — date, recipient and subject
% -----------------------------------------------------------------------------
\newcommand{\makecoverletterdetails}{%
    \noindent
    \hfill
    {\fontsize{13}{15}\selectfont\cl@date}\par
    \vspace{0pt}%
    {\fontsize{14}{14}\selectfont
     \bfseries\MakeUppercase{\cl@subject}\par}
    \vspace{0pt}%
    {\fontsize{16}{16}\selectfont
     \cl@recipient\par}
    \vspace{10pt}%
}

\makeatother
% -----------------------------------------------------------------------------
% END OF CLASS FILE
% -----------------------------------------------------------------------------