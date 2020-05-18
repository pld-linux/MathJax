# TODO: unbundle fonts (eot, otf, woff formats)
Summary:	JavaScript display engine for mathematics
Summary(pl.UTF-8):	Oparty na JavaScripcie silnik wyświetlania wzorów matematycznych
Name:		MathJax
Version:	2.7.8
Release:	1
License:	Apache v2.0
Group:		Applications/WWW
#Source0Download: https://github.com/mathjax/MathJax/releases
Source0:	https://github.com/mathjax/MathJax/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6cea1e2445ba7ab478be07463bca539c
URL:		https://www.mathjax.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	%{name}-base = %{version}-%{release}
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(alias)
Conflicts:	apache-base < 2.4.0-1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
MathJax is an open source JavaScript display engine for mathematics
that works in all modern browsers.

This package exposes MathJax via web server.

%description -l pl.UTF-8
MathJax to mający otwarte źródła, oparty na JavaScripcie silnik
wyświetlania wzorów matematycznych, działający we wszystkich
współczesnych przeglądarkach.

Ten pakiet udostępnia MathJax przez serwer WWW.

%package base
Summary:	JavaScript display engine for mathematics - local installation
Summary(pl.UTF-8):	Oparty na JavaScripcie silnik wyświetlania wzorów matematycznych - instalacja lokalna
Group:		Applications/WWW

%description base
MathJax is an open source JavaScript display engine for mathematics
that works in all modern browsers.

This package allows to use MathJax through local files.

%description base -l pl.UTF-8
MathJax to mający otwarte źródła, oparty na JavaScripcie silnik
wyświetlania wzorów matematycznych, działający we wszystkich
współczesnych przeglądarkach.

Ten pakiet pozwala używać silnika przez pliki lokalne.

%package source
Summary:	Unpacked source code of MathJax engine
Summary(pl.UTF-8):	Rozpakowany kod źródłowy silnika MathJax
Group:		Documentation

%description source
Unpacked source code of MathJax engine.

%description source -l pl.UTF-8
Rozpakowany kod źródłowy silnika MathJax.

%prep
%setup -q

# fixup separation of unpacked .js files
install -d unpacked/fonts/HTML-CSS/TeX
%{__mv} fonts/HTML-CSS/TeX/png/unpacked unpacked/fonts/HTML-CSS/TeX/png

cat > apache.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Allow from all
</Directory>
EOF

cat > httpd.conf <<'EOF'
Alias /%{name} %{_appdir}
<Directory %{_appdir}>
	Require all granted
</Directory>
EOF

cat > lighttpd.conf <<'EOF'
alias.url += (
    "/%{name}" => "%{_appdir}",
)
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

cp -pr MathJax.js config extensions fonts jax localization $RPM_BUILD_ROOT%{_appdir}
# drop messages documentation
%{__rm} -r $RPM_BUILD_ROOT%{_appdir}/localization/qqq

cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf

install -d $RPM_BUILD_ROOT%{_examplesdir}
cp -pr unpacked $RPM_BUILD_ROOT%{_prefix}/src/%{name}
cp -pr test $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf

%files base
%defattr(644,root,root,755)
%dir %{_appdir}
%{_appdir}/MathJax.js
%{_appdir}/config
%{_appdir}/extensions
%dir %{_appdir}/fonts
%dir %{_appdir}/fonts/HTML-CSS
%{_appdir}/fonts/HTML-CSS/Asana-Math
%{_appdir}/fonts/HTML-CSS/Gyre-Pagella
%{_appdir}/fonts/HTML-CSS/Gyre-Termes
%{_appdir}/fonts/HTML-CSS/Latin-Modern
%{_appdir}/fonts/HTML-CSS/Neo-Euler
%{_appdir}/fonts/HTML-CSS/STIX-Web
%dir %{_appdir}/fonts/HTML-CSS/TeX
# MathJax_{AMS,Caligraphic,Fraktur,Main,Math,SansSerif,Script,Size1,Size2,Size4,Typewriter,Vector,WinIE6}
%{_appdir}/fonts/HTML-CSS/TeX/eot
%{_appdir}/fonts/HTML-CSS/TeX/otf
%{_appdir}/fonts/HTML-CSS/TeX/png
%{_appdir}/fonts/HTML-CSS/TeX/svg
%{_appdir}/fonts/HTML-CSS/TeX/woff
%{_appdir}/jax
%dir %{_appdir}/localization
%lang(ar) %{_appdir}/localization/ar
%lang(ast) %{_appdir}/localization/ast
%lang(bcc) %{_appdir}/localization/bcc
%lang(bg) %{_appdir}/localization/bg
%lang(br) %{_appdir}/localization/br
%lang(ca) %{_appdir}/localization/ca
%lang(cdo) %{_appdir}/localization/cdo
%lang(ce) %{_appdir}/localization/ce
%lang(cs) %{_appdir}/localization/cs
%lang(cy) %{_appdir}/localization/cy
%lang(da) %{_appdir}/localization/da
%lang(de) %{_appdir}/localization/de
%lang(diq) %{_appdir}/localization/diq
%{_appdir}/localization/en
%lang(eo) %{_appdir}/localization/eo
%lang(es) %{_appdir}/localization/es
%lang(fa) %{_appdir}/localization/fa
%lang(fi) %{_appdir}/localization/fi
%lang(fr) %{_appdir}/localization/fr
%lang(gl) %{_appdir}/localization/gl
%lang(he) %{_appdir}/localization/he
%lang(ia) %{_appdir}/localization/ia
%lang(it) %{_appdir}/localization/it
%lang(ja) %{_appdir}/localization/ja
%lang(kn) %{_appdir}/localization/kn
%lang(ko) %{_appdir}/localization/ko
%lang(lb) %{_appdir}/localization/lb
%lang(lki) %{_appdir}/localization/lki
%lang(lt) %{_appdir}/localization/lt
%lang(mk) %{_appdir}/localization/mk
%lang(nl) %{_appdir}/localization/nl
%lang(oc) %{_appdir}/localization/oc
%lang(pl) %{_appdir}/localization/pl
%lang(pt) %{_appdir}/localization/pt
%lang(pt_BR) %{_appdir}/localization/pt-br
%lang(ru) %{_appdir}/localization/ru
%lang(scn) %{_appdir}/localization/scn
%lang(sco) %{_appdir}/localization/sco
%lang(sk) %{_appdir}/localization/sk
%lang(sl) %{_appdir}/localization/sl
%lang(sv) %{_appdir}/localization/sv
%lang(th) %{_appdir}/localization/th
%lang(tr) %{_appdir}/localization/tr
%lang(uk) %{_appdir}/localization/uk
%lang(vi) %{_appdir}/localization/vi
%lang(zh_CN) %{_appdir}/localization/zh-hans
%lang(zh_TW) %{_appdir}/localization/zh-hant
%{_examplesdir}/%{name}-%{version}

%files source
%defattr(644,root,root,755)
# move to some common "unpacked" or "js-unpacked", "javascript-unpacked" subdir?
%{_prefix}/src/%{name}
