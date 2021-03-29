# Define the kmod package name here.
%define kmod_name drbd90
%define real_name drbd

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion %(rpm -q kernel-devel | /usr/lib/rpm/redhat/rpmsort -r | head -n 1 | sed -e 's#kernel-devel-##g')}

Name:    %{kmod_name}-kmod
Version: 9.0.28
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: Distributed Redundant Block Device driver for Linux
URL:     http://www.drbd.org/

BuildRequires: kernel-devel make kernel-rpm-macros
BuildRequires: perl-interpreter
BuildRequires: redhat-rpm-config
BuildRequires: elfutils-libelf-devel

ExclusiveArch: x86_64

Source0:  https://www.linbit.com/downloads/drbd/9.0/drbd-%{version}-1.tar.gz
Source10: kmodtool-%{kmod_name}-el8.sh

# Magic hidden here.
%{expand:%(sh %{SOURCE10} rpmtemplate %{kmod_name} %{kversion} "")}

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
DRBD is a distributed replicated block device. It mirrors a
block device over the network to another machine. Think of it
as networked raid 1. It is a building block for setting up
high availability (HA) clusters.

%prep
%setup -n %{real_name}-%{version}-1
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
KSRC=%{_usrsrc}/kernels/%{kversion}
%{__make} %{?_smp_mflags} module KDIR=${KSRC} KVER=%{kversion}

%install
%{__install} -d %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} drbd/*.ko %{buildroot}/lib/modules/%{kversion}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
for file in ChangeLog COPYING README.md; do
    %{__install} -Dp -m0644 $file %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/$file
done

# strip the modules(s)
find %{buildroot} -type f -name \*.ko -exec %{__strip} --strip-debug \{\} \;

# Sign the modules(s)
%if %{?_with_modsign:1}%{!?_with_modsign:0}
# If the module signing keys are not defined, define them here.
%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
for module in $(find %{buildroot} -type f -name \*.ko);
do %{__perl} /usr/src/kernels/%{kversion}/scripts/sign-file \
sha256 %{privkey} %{pubkey} $module;
done
%endif

%clean
%{__rm} -rf %{buildroot}

%changelog
* Fri Feb 26 2021 Madison Kelly <mkelly@alteeve.ca> - 9.0.28-1.el8
- Updated source to 9.0.28.

* Thu Dec 24 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.27-1.el8
- Updated source to 9.0.27.

* Tue Dec 22 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.26-1.el8
- Updated source to 9.0.26.

* Sat Nov 28 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.25-3.el8
- Added kernel development packages are install requirements.

* Mon Nov 16 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.25-2.el8
- Rebuilt to resolve kmod issue.

* Thu Sep 24 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.25-1.el8
- Updated source to 9.0.25.

* Wed Aug 12 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.24-1.el8
- Updated source to 9.0.24.

* Mon Jun 08 2020 Madison Kelly <mkelly@alteeve.ca> - 9.0.23-1.el8
- Updated source to 9.0.23.

* Tue Nov 12 2019 Madison Kelly <mkelly@alteeve.ca> - 9.0.21-1.el8
- Updated source to 9.0.21.

* Fri Nov 01 2019 Madison Kelly <mkelly@alteeve.ca> - 9.0.20-1.el8
- Updated source to 9.0.20.

* Mon Jul 08 2019 Madison Kelly <mkelly@alteeve.ca> - 9.0.19-1.el8
- Updated source to 9.0.19.

* Wed Jun 26 2019 Madison Kelly <mkelly@alteeve.ca> - 9.0.18-1.el8
- Rebuild for RHEL 8 final.
- Updated source to 9.0.18.

* Tue Jan 15 2019 Madison Kelly <mkelly@alteeve.ca> - 9.0.16-1.el8
- Rebuild for RHEL 8 beta.
- Updated the auto-definition of kversion to use 'uname -r'.
- Updated the perl dependency (not a meta package) to perl-interpreter.
- Renamed kmodtool-drbd90-el7.sh to kmodtool-drbd90-el8.sh

* Sat Nov 03 2018 Akemi Yagi <toracat@elrepo.org> - 9.0.16-1.el7_6
- Updated to 9.0.16
- Rebuild against RHEL 7.6 kernel

* Thu May 03 2018 Akemi Yagi <toracat@elrepo.org> - 9.0.14-1.el7_5
- Updated to 9.0.14

* Wed Apr 18 2018 Akemi Yagi <toracat@elrepo.org> - 9.0.13-1.el7_5
- Updated to 9.0.13
- Rebuild against RHEL 7.5 kernel

* Thu Sep 14 2017 Akemi Yagi <toracat@elrepo.org> - 9.0.9-1
- Updated to 9.0.9
- Built against EL7.4 kernel

* Fri Jun 30 2017 Philip J Perry <phil@elrepo.org> - 9.0.8-1
- Updated to 9.0.8

* Sat Jun 10 2017 Akemi Yagi <toracat@elrepo.org> - 9.0.7-1
- Updated to 9.0.7

* Wed Jun 24 2015 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 9.0.0-1
- Initial el7 build of the kmod package.
