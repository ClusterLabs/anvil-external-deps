# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%global buildforkernels akmod
%global debug_package %{nil}

Name:    drbd-kmod
Summary: Kernel module (kmod) for drbd9
Version: 9.1.10
Release: 1%{?dist}
License: GPLv2
URL:     http://www.drbd.org/
Source0: https://pkg.linbit.com//downloads/drbd/9/drbd-%{version}.tar.gz

BuildRequires:    %{_bindir}/kmodtool
%{!?kernels:BuildRequires: gcc, elfutils-libelf-devel, kernel-devel}

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
DRBD is a distributed replicated block device. It mirrors a
block device over the network to another machine. Think of it
as networked raid 1. It is a building block for setting up
high availability (HA) clusters.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu} --repo rpmfusion --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c -T -a 0 -p 0
ls
for kernel_version in %{?kernel_versions} ; do
    cp -a drbd-%{version} _kmod_build_${kernel_version%%___*}
done


%build
for kernel_version  in %{?kernel_versions} ; do
    %{__make} %{?_smp_mflags} V=1 -C "_kmod_build_${kernel_version%%___*}" \
	KVER="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" \
	module
done


%install
for kernel_version  in %{?kernel_versions} ; do
    %{__make} %{?_smp_mflags} V=1 -C "_kmod_build_${kernel_version%%___*}" \
	KVER="${kernel_version%%___*}" KSRC="${kernel_version##*___}" KBUILD="${kernel_version##*___}" \
	MODSUBDIR="%{kmodinstdir_postfix}" DESTDIR=%{buildroot}/ \
	install
done
%{?akmod_install}

%changelog
* Thu Sep 01 2022 Madison Kelly <mkelly@alteeve.ca> - 9.1.10-1.el8
- Updated source to 9.1.10.

* Tue Aug 30 2022 Madison Kelly <mkelly@alteeve.ca> - 9.1.9-1.el8
- Updated source to 9.1.9.

* Tue Jul 26 2022 Madison Kelly <mkelly@alteeve.ca> - 9.1.8-1.el8
- Updated source to 9.1.8.

* Fri May 06 2022 Madison Kelly <mkelly@alteeve.ca> - 9.1.7-1.el8
- Updated source to 9.1.7.

* Mon Dec 20 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.5-2.el8
- Updated source to 9.1.5.
- Revert workaround for https://bugzilla.redhat.com/show_bug.cgi?id=2034193

* Mon Dec 20 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.5-1.el8
- Updated source to 9.1.5.
- Add workaround for https://bugzilla.redhat.com/show_bug.cgi?id=2034193

* Sun Aug 15 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.3-1.el8
- Updated source to 9.1.3.

* Sat Jun 26 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.2-2.el8
- Move to akmod infrastructure

* Fri May 07 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.2-1.el8
- Updated source to 9.1.2.

* Sat Mar 27 2021 Madison Kelly <mkelly@alteeve.ca> - 9.1.1-1.el8
- Updated source to 9.1.1.

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
