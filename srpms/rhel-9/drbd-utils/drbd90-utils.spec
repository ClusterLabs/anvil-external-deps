%define real_name drbd-utils

%global selinuxtype             targeted
%global selinuxmodulename       drbd

Name:    drbd90-utils
Version: 9.29.0
Release: 2%{?dist}
License: GPLv2+
Summary: Management utilities for DRBD
URL:     http://www.drbd.org/

Source0: https://pkg.linbit.com//downloads/drbd/utils/drbd-utils-%{version}.tar.gz
Patch1:  elrepo-selinux-bug695.patch
Patch2:  selinux-permit-module-load.patch

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: docbook-style-xsl
BuildRequires: flex
BuildRequires: libxslt
BuildRequires: po4a
BuildRequires: udev
BuildRequires: systemd
BuildRequires: gcc gcc-c++
BuildRequires: keyutils-libs-devel
BuildRequires: selinux-policy-devel

Requires: udev
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units
Requires: selinux-policy >= %{_selinux_policy_version}
Requires: drbd-kmod >= 9.1.2
Conflicts: drbd91-kmod

### Virtual provides that people may use
Provides: drbd = %{version}-%{release}
Provides: drbd90 = %{version}-%{release}
Provides: drbd-utils = %{version}-%{release}
Provides: drbd-kmod-common = 9.2.12

### Conflict with older Linbit packages
Conflicts: drbd < 9.0
Conflicts: drbd-utils < 9.0

### Conflict with older CentOS packages
Conflicts: drbd82 <= %{version}-%{release}
Conflicts: drbd82-utils <= %{version}-%{release}
Conflicts: drbd83 <= %{version}-%{release}
Conflicts: drbd83-utils <= %{version}-%{release}
Conflicts: drbd84 <= %{version}-%{release}
Conflicts: drbd84-utils <= %{version}-%{release}

%description
DRBD mirrors a block device over the network to another machine.
Think of it as networked raid 1. It is a building block for
setting up high availability (HA) clusters.

This packages includes the DRBD administration tools and integration
scripts for heartbeat, pacemaker, rgmanager and xen.

%prep
%setup -n %{real_name}-%{version}
%patch1 -p1
%patch2 -p2

%build
### Overriding standard configure call because it breaks C++11
### detection in configure script.
./configure \
    --prefix=/usr \
    --localstatedir=/var \
    --sysconfdir=/etc \
    --without-rgmanager \
    --without-xen \
    --without-windrbd \
    --without-heartbeat \
    --without-84support \
    --with-udev \
    --with-pacemaker \
    --with-drbdmon \
    --with-prebuiltman \
    --with-initscripttype=systemd
%{__make} %{?_smp_mflags}
%{__make} -C selinux %{?_smp_mflags}

%pre
%selinux_relabel_pre -s %{selinuxtype}

%install
%{__rm} -rf %{buildroot}
%{__make} install DESTDIR="%{buildroot}"
%{__make} -C selinux install DESTDIR="%{buildroot}"

%clean
%{__rm} -rf %{buildroot}

%post
%selinux_modules_install -s %{selinuxtype} -p 200 %{_datadir}/selinux/packages/%{selinuxtype}/%{selinuxmodulename}.pp.bz2

%systemd_post drbd.service

if /usr/bin/getent group | grep -q ^haclient; then
    chgrp haclient /usr/sbin/drbdadm
    chgrp haclient /usr/sbin/drbdmeta
    chgrp haclient /usr/sbin/drbdmon
    chgrp haclient /usr/sbin/drbdsetup
fi

%preun
%systemd_preun drbd.service

%postun
%systemd_postun_with_restart drbd.service

if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} -p 200 %{selinuxmodulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%doc ChangeLog COPYING README.md scripts/drbd.conf.example
%doc %{_mandir}/man7/*.7*
%doc %{_mandir}/man5/drbd.conf.5*
%doc %{_mandir}/man5/drbd.conf-*
%doc %{_mandir}/man8/drbd*
%doc %{_mandir}/ja/man5/drbd.conf.5*
%doc %{_mandir}/ja/man5/drbd.conf-*
%doc %{_mandir}/ja/man8/drbd*
%config %{_sysconfdir}/bash_completion.d/drbdadm
%config %{_prefix}/lib/udev/rules.d/65-drbd.rules
%config(noreplace) %{_sysconfdir}/drbd.conf
%config(noreplace) %{_sysconfdir}/multipath/conf.d/drbd.conf
%dir %{_sysconfdir}/drbd.d/
%config(noreplace) %{_sysconfdir}/drbd.d/global_common.conf
%config %{_unitdir}/*
%dir %{_localstatedir}/lib/drbd/
%dir %{_prefix}/lib/drbd/scripts
%attr(755, root, root) %{_prefix}/lib/drbd/scripts/*
%attr(755, root, root) %{_sbindir}/drbdadm
%attr(755, root, root) %{_sbindir}/drbdmeta
%attr(755, root, root) %{_sbindir}/drbdsetup
%attr(755, root, root) %{_sbindir}/drbdmon
%dir %{_prefix}/lib/drbd/
%{_prefix}/lib/drbd/notify-out-of-sync.sh
%{_prefix}/lib/drbd/notify-split-brain.sh
%{_prefix}/lib/drbd/notify-emergency-reboot.sh
%{_prefix}/lib/drbd/notify-emergency-shutdown.sh
%{_prefix}/lib/drbd/notify-io-error.sh
%{_prefix}/lib/drbd/notify-pri-lost-after-sb.sh
%{_prefix}/lib/drbd/notify-pri-lost.sh
%{_prefix}/lib/drbd/notify-pri-on-incon-degr.sh
%{_prefix}/lib/drbd/notify.sh
%{_prefix}/lib/drbd/outdate-peer.sh
%{_prefix}/lib/drbd/snapshot-resync-target-lvm.sh
%{_prefix}/lib/drbd/stonith_admin-fence-peer.sh
%{_prefix}/lib/drbd/unsnapshot-resync-target-lvm.sh
%{_prefix}/lib/tmpfiles.d/drbd.conf

### pacemaker
%{_prefix}/lib/drbd/crm-fence-peer.sh
%{_prefix}/lib/drbd/crm-unfence-peer.sh
%{_prefix}/lib/ocf/resource.d/linbit/drbd
%{_prefix}/lib/ocf/resource.d/linbit/drbd-attr
%{_prefix}/lib/drbd/crm-fence-peer.9.sh
%{_prefix}/lib/drbd/crm-unfence-peer.9.sh
%{_prefix}/lib/ocf/resource.d/linbit/drbd.shellfuncs.sh

### selinux
%attr(0644, root, root) %{_datadir}/selinux/packages/%{selinuxtype}/%{selinuxmodulename}.pp.bz2
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{selinuxmodulename}

%changelog
* Fri Jan 03 2025 Yanhao Lei <yanhao.lei@alteeve.com> - 9.29.0-2
- Bump version
- Add selinux rules to allow module_load

* Mon Dec 02 2024 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.29.0-1
- Updated to 9.29.0.
- Update for new drbd-kmod

* Sat Aug 17 2024 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.28.0-1
- Updated to 9.28.0.
- Update for new drbd-kmod

* Thu Mar 28 2024 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.27.0-3
- bump version
- include selinux rules from Yan

* Wed Mar 06 2024 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.27.0-2
- Update for new drbd-kmod

* Sat Jan 13 2024 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.27.0-1
- Updated to 9.25.0.
- Update for new drbd-kmod

* Sat Aug 26 2023 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.25.0-1
- Updated to 9.25.0.
- Update for new drbd-kmod

* Fri Jun 16 2023 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.24.0-1
- Updated to 9.24.0.
- Update for new drbd-kmod

* Wed Apr 05 2023 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.23.1-2
- Update for new drbd-kmod

* Wed Mar 15 2023 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.23.1-1
- Updated to 9.23.1.
- Update for new drbd-kmod

* Thu Mar 02 2023 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.23.0-1
- Updated to 9.23.0.
- Update for new drbd-kmod

* Wed Nov 16 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.22.0-2
- Update for new drbd-kmod

* Tue Nov 15 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.22.0-1
- Updated to 9.22.0.
- Update for new drbd-kmod

* Wed Sep 07 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.4-4
- Update for new drbd-kmod

* Thu Sep 01 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.4-3
- Update for new drbd-kmod

* Tue Aug 30 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.4-2
- Update for new drbd-kmod
- Update Provides: drbd-utils for drbd-proxy

* Tue Jul 26 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.4-1
- Updated to 9.21.4.

* Fri May 20 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.1-2
- Fix c9s BRs

* Fri May 06 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.21.1-1
- Updated to 9.21.1.

* Sun Feb 06 2022 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.20.2-1
- Updated to 9.20.2.

* Mon Dec 20 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.19.1-1
- Updated to 9.19.1.

* Wed Aug 25 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.18.2-3
- Fix drbd-kmod-common Provides

* Sun Aug 15 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.18.2-2
- Fix up packaging after 9.18.2 update

* Sun Aug 15 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.18.2-1
- Updated to 9.18.2

* Mon Jun 28 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.17.0-2
- Switch to akmods

* Mon Apr 26 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.17.0-1
- Updated to 9.17.0.

* Sun Feb 21 2021 Fabio M. Di Nitto <fabbione@fabbione.net> - 9.16.0-2
- Fix upstream tarball download url
- Fix drbdmon build
- Remove support for all distros and compat layers
- Cleanup spec file a bit

* Tue Feb 09 2021 Madison Kelly <mkelly@alteeve.ca> - 9.16.0-1
- Updated to 9.16.0.

* Mon Sep 28 2020 Madison Kelly <mkelly@alteeve.ca> - 9.15.0-1
- Updated to 9.15.0.

* Mon Sep 21 2020 Madison Kelly <mkelly@alteeve.ca> - 9.14.1-1
- Updated to 9.14.1.

* Thu Sep 10 2020 Madison Kelly <mkelly@alteeve.ca> - 9.14.0-1
- Updated to 9.14.0.

* Tue Jul 14 2020 Madison Kelly <mkelly@alteeve.ca> - 9.13.1-2
- Removed the mode set on drbdsetup and drbdmeta.

* Mon Jun 08 2020 Madison Kelly <mkelly@alteeve.ca> - 9.13.1-1
- Updated to 9.13.1.

* Fri Nov 01 2019 Madison Kelly <mkelly@alteeve.ca> - 9.11.0-1
- Updated to 9.11.0.

* Wed Jun 26 2019 Madison Kelly <mkelly@alteeve.ca> - 9.10.0-1
- Built for RHEL 8 final.
- Updated to 9.10.0.

* Wed Jan 16 2019 Madison Kelly <mkelly@alteeve.ca> - 9.8.0-1
- Updated to 9.8.0.
- Added po4a to build dependencies.

* Tue Jan 15 2019 Madison Kelly <mkelly@alteeve.ca> - 9.6.0-1
- Rebuild for RHEL8.

* Sat Nov 03 2018 Akemi Yagi <toracat@elrepo.org> - 9.6.0-1
- Updated to 9.6.0

* Wed Apr 18 2018 Akemi Yagi <toracat@elrepo.org> - 9.3.1-1
- Updated to 9.3.1

* Thu Sep 14 2017 Akemi Yagi <toracat@elrepo.org> - 9.1.0-1
- Updated to 9.1.0

* Mon Jun 12 2017 Akemi Yagi <toracat@elrepo.org> - 9.0.0-1
- Updated to 9.0.0
- xmlto replaced with docbook-style-xsl

* Sat Dec  3 2016 Akemi Yagi <toracat@elrepo.org> - 8.9.8-1
- update to version 8.9.8.
- Bug fix (elrepo bug #695)

* Wed Oct  5 2016 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.6-1
- Update to version 8.9.6.
- BuildRequires: xmlto added by A. Yagi for building in mock.

* Mon Jan  4 2016 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.5-1
- Update to version 8.9.5.

* Sat Aug 15 2015 Akemi Yagi <toracat@elrepo.org> - 8.9.3-1.1
- Patch drbd.ocf to the version from 8.9.3-2 (bugs #578 and #589)

* Wed Jun 24 2015 Hiroshi Fujishima <h-fujishima@sakura.ad.jp> - 8.9.3-1
- Initial package for RHEL7.
