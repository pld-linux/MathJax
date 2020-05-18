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

%description -l pl.UTF-8
MathJax to mający otwarte źródła, oparty na JavaScripcie silnik
wyświetlania wzorów matematycznych, działający we wszystkich
współczesnych przeglądarkach.

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

cp -pr MathJax.js config extensions fonts jax $RPM_BUILD_ROOT%{_appdir}

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
%doc README.*
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%{_appdir}
%{_examplesdir}/%{name}-%{version}

%files source
%defattr(644,root,root,755)
# move to some common "unpacked" or "js-unpacked", "javascript-unpacked" subdir?
%{_prefix}/src/%{name}
