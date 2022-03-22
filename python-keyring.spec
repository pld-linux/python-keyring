#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# py.test tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	keyring
Summary:	Python 2 library to access the system keyring service
Summary(pl.UTF-8):	Biblioteka Pythona 2 do dostępu do systemowego pęku kluczy
Name:		python-%{module}
# keep 18.x here for python2 support
Version:	18.0.1
Release:	1
License:	MIT, PSF
Group:		Libraries/Python
#Source0Download: https://pypi.python.org/simple/keyring
Source0:	https://files.pythonhosted.org/packages/source/k/keyring/%{module}-%{version}.tar.gz
# Source0-md5:	00cdec34da9c15ad804441979b70830b
URL:		https://pypi.python.org/pypi/keyring
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python-entrypoints
BuildRequires:	python-pytest >= 2.8
BuildRequires:	python-pytest-flake8
BuildRequires:	python-secretstorage
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15.0
%if %{with tests}
BuildRequires:	python3-entrypoints
BuildRequires:	python3-pytest >= 2.8
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-secretstorage
%endif
%endif
%if %{with doc}
BuildRequires:	python-Sphinx
BuildRequires:	python-jaraco.packaging >= 3.2
BuildRequires:	python-rst.linker >= 1.9
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
# kwalletd5 through dbus
Suggests:	python-dbus
Obsoletes:	python-keyring-gnome < 0.5.1
Obsoletes:	python-keyring-kwallet < 0.5.1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Python keyring library provides a easy way to access the system
keyring service from Python. It can be used in any application that
needs safe password storage.

%description -l pl.UTF-8
Biblioteka Pythona keyring udostępnia prosty sposób dostępu do usługi
systemowego pęku kluczy z poziomu Pythona. Może być używana w dowolnej
aplikacji wymagającej bezpiecznego przechowywania haseł.

%package -n python3-%{module}
Summary:	Python 3 library to access the system keyring service
Summary(pl.UTF-8):	Biblioteka Pythona 3 do dostępu do systemowego pęku kluczy
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3
# kwalletd5 through dbus
Suggests:	python-dbus

%description -n python3-%{module}
The Python keyring lib provides a easy way to access the system
keyring service from Python. It can be used in any application that
needs safe password storage.

%description -n python3-%{module} -l pl.UTF-8
Biblioteka Pythona keyring udostępnia prosty sposób dostępu do usługi
systemowego pęku kluczy z poziomu Pythona. Może być używana w dowolnej
aplikacji wymagającej bezpiecznego przechowywania haseł.

%package apidocs
Summary:	API documentation for Python keyring library
Summary(pl.UTF-8):	Dokumentacja API biblioteki Pythona keyring
Group:		Documentation

%description apidocs
API documentation for Python keyring library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki Pythona keyring.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
%py_build %{?with_doc:build_sphinx}

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
PYTHONPATH=$(pwd)/build-2/lib \
%{__python} -m pytest tests keyring/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_flake8" \
PYTHONPATH=$(pwd)/build-3/lib \
%{__python3} -m pytest tests keyring/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python3}
%py3_install

# keep base tests classes (for e.g. python-keyrings.alt tests), remove just backends unit tests
%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/keyring/tests/backends
# "keyring" name is too generic, add -py[version] suffix
%{__mv} $RPM_BUILD_ROOT%{_bindir}/keyring{,-py3}
%endif

%if %{with python2}
%py_install

%py_postclean

# keep base tests classes (for e.g. python-keyrings.alt tests), remove just backends unit tests
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/keyring/tests/backends
# "keyring" name is too generic, add -py[version] suffix
%{__mv} $RPM_BUILD_ROOT%{_bindir}/keyring{,-py2}
ln -sf keyring-py2 $RPM_BUILD_ROOT%{_bindir}/keyring-py
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/keyring-py
%attr(755,root,root) %{_bindir}/keyring-py2
%{py_sitescriptdir}/keyring
%{py_sitescriptdir}/keyring-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/keyring-py3
%{py3_sitescriptdir}/keyring
%{py3_sitescriptdir}/keyring-%{version}-py*.egg-info
%endif

%if %{with python2} && %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc build-2/sphinx/html/{_static,*.html,*.js}
%endif
