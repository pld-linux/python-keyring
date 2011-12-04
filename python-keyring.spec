%define 	module	keyring
Summary:	Python library to access the system keyring service
Name:		python-%{module}
Version:	0.5.1
Release:	1
Source0:	http://pypi.python.org/packages/source/k/keyring/%{module}-%{version}.tar.gz
# Source0-md5:	a2f0dcea7185580c163ef2db1f4fbe0c
License:	Python
Group:		Development/Libraries
URL:		http://pypi.python.org/pypi/keyring
BuildRequires:	python-devel
BuildRequires:	rpmbuild(macros) >= 1.219
Obsoletes:	python-keyring-gnome < 0.5.1
Obsoletes:	python-keyring-kwallet < 0.5.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python keyring lib provides a easy way to access the system
keyring service from python. It can be used in any application that
needs safe password storage.

This package only provides file-based pseudo-keyrings. To interface
with gnome-keyring or KWallet, please install one of
python-keyring-gnome or python-keyring-kwallet.

%prep
%setup -q -n %{module}-%{version}

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/%{module}/tests

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a demo/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{module}-*.egg-info
%{_examplesdir}/%{name}-%{version}
