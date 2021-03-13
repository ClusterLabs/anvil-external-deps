Name:		alteeve-el8-repo
Version:	0.1
Release:	1
Summary:	fake rpm for Anvil CI

Group:		server
License:	GPL
URL:		https://alteeve.com

BuildArch:	noarch

%description
fake rpm for Anvil CI

%prep

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/yum.repos.d/
touch %{buildroot}/etc/yum.repos.d/alteeve-el8.repo

%clean
rm -rf rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/alteeve-el8.repo

%changelog
* Sat Mar 13 2021 Fabio M. Di Nitto <fabbione@fabbione.net> 0.1-1
- Mock up release
