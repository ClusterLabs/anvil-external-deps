# Run extra test
# Break lines according to Unicode rules
%if ! (0%{?rhel})
%bcond_without perl_Test2_Suite_enables_extra_test
%bcond_without perl_Test2_Suite_enables_unicode
%else
%bcond_with perl_Test2_Suite_enables_extra_test
%bcond_with perl_Test2_Suite_enables_unicode
%endif

Name:           perl-Test2-Suite
Version:        0.000155
Release:        3%{?dist}
Summary:        Set of tools built upon the Test2 framework
License:        GPL-1.0-or-later OR Artistic-1.0-Perl
URL:            https://metacpan.org/release/Test2-Suite
Source0:        https://cpan.metacpan.org/authors/id/E/EX/EXODIST/Test2-Suite-%{version}.tar.gz
Patch0:         Test2-Suite-0.000140-add_perl.patch
BuildArch:      noarch
BuildRequires:  coreutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Term::Table) >= 0.013
BuildRequires:  perl(Term::Table::Cell)
BuildRequires:  perl(Term::Table::LineBreak)
BuildRequires:  perl(Term::Table::Util)
BuildRequires:  perl(Test2::API) >= 1.302176
BuildRequires:  perl(Test2::API::Context)
BuildRequires:  perl(Test2::Event)
BuildRequires:  perl(Test2::Event::Exception)
# Test2::Event::Note loaded by send_event()
BuildRequires:  perl(Test2::Event::Note)
# Test2::Event::Skip loaded by send_event()
BuildRequires:  perl(Test2::Event::Skip)
BuildRequires:  perl(Test2::EventFacet)
BuildRequires:  perl(Test2::EventFacet::Info::Table)
BuildRequires:  perl(Test2::EventFacet::Trace)
BuildRequires:  perl(Test2::Hub::Interceptor)
BuildRequires:  perl(Test2::Hub::Subtest)
BuildRequires:  perl(Test2::IPC)
BuildRequires:  perl(Test2::Tools::Tiny)
BuildRequires:  perl(Test2::Util)
BuildRequires:  perl(Test2::Util::HashBase)
BuildRequires:  perl(Test2::Util::Trace)
BuildRequires:  perl(threads)
BuildRequires:  perl(Time::HiRes)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
# Optional run-time:
# Sub::Util
BuildRequires:  perl(Sub::Util)
%if %{with perl_Test2_Suite_enables_unicode}
BuildRequires:  perl(Unicode::GCString)
%endif
# Tests:
BuildRequires:  perl(IO::Handle)
%if %{with perl_Test2_Suite_enables_extra_test}
BuildRequires:  perl(JSON::MaybeXS)
%endif
BuildRequires:  perl(PerlIO)
BuildRequires:  perl(Test2::EventFacet::Assert)
BuildRequires:  perl(Test2::Formatter::TAP)
Requires:       perl(Data::Dumper)
# Sub::Util
Suggests:       perl(Sub::Util)
Requires:       perl(Term::Table) >= 0.013
Requires:       perl(Test2::API) >= 1.302176
Requires:       perl(Test2::Event)
# Test2::Event::Note loaded by send_event()
Requires:       perl(Test2::Event::Note)
# Test2::Event::Skip loaded by send_event()
Requires:       perl(Test2::Event::Skip)
Requires:       perl(Test2::EventFacet)
Requires:       perl(threads)
Requires:       perl(utf8)
Recommends:     perl(Module::Pluggable) >= 2.7
%if %{with perl_Test2_Suite_enables_unicode}
# Unicode::GCString for formating double-width strings
Recommends:     perl(Unicode::GCString)
%endif
# perl-Test2-AsyncSubtest-0:0.000020-1.fc28 merged
Provides:       perl-Test2-AsyncSubtest = %{version}-%{release}
Obsoletes:      perl-Test2-AsyncSubtest < 0.000020-2
# perl-Test2-Workflow-0:0.000018-4.fc27 merged
Provides:       perl-Test2-Workflow = %{version}-%{release}
Obsoletes:      perl-Test2-Workflow < 0.000018-5
# 3 inlined modules for future Perl Core
Provides:       bundled(Importer) = 0.026
Provides:       bundled(Scope::Guard) = 0.21
Provides:       bundled(Sub::Info) = 0.002

# Remove under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%{__requires_exclude}|}^perl\\((Term::Table|Test2::API)\\)$
# Remove private modules
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(MyTest::Target\\)$
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_libexecdir}

%description
Rich set of tools, plugins, bundles, etc. built upon the Test2 testing
library. If you are interested in writing Perl tests this is the distribution
for you.

%package tests
Summary:        Tests for %{name}
Requires:       %{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       perl-Test-Harness
Requires:       perl(JSON::MaybeXS)
Requires:       perl(Test::Compile) >= 1.1.0
Recommends:     perl(Module::Pluggable) >= 2.7
Recommends:     perl(Unicode::GCString)

%description tests
Tests from %{name}. Execute them
with "%{_libexecdir}/%{name}/test".

%prep
%setup -q -n Test2-Suite-%{version}
%patch0 -p1
# Help generators to recognize Perl scripts
for F in `find . -type f -name '*.t'`; do
    perl -i -MConfig -ple 'print $Config{startperl} if $. == 1 && !s{\A#!\s*perl}{$Config{startperl}}' "$F"
    chmod +x "$F"
done

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1
%{make_build}

%install
%{make_install}
%{_fixperms} %{buildroot}/*
# Install tests
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a t %{buildroot}%{_libexecdir}/%{name}
cat > %{buildroot}%{_libexecdir}/%{name}/test << 'EOF'
#!/bin/sh
cd %{_libexecdir}/%{name} && exec prove -r -I . -j "$(getconf _NPROCESSORS_ONLN)"
EOF
chmod +x %{buildroot}%{_libexecdir}/%{name}/test

%check
unset AUTHOR_TESTING
make test

%files
%license LICENSE
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*

%files tests
%{_libexecdir}/%{name}

%changelog
* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.000155-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000155-2
- Add conditional which could disable integration tests

* Tue May 02 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000155-1
- Add information about inlined modules
- 0.000155 bump

* Fri Apr 28 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000153-1
- Add some recommends to tests package
- 0.000153 bump

* Thu Apr 27 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000152-1
- 0.000152 bump

* Thu Mar 23 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000150-1
- 0.000150 bump

* Tue Mar 21 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000149-1
- 0.000149 bump
- Fix usage of patch macro

* Mon Mar 06 2023 Michal Josef Špaček <mspacek@redhat.com> - 0.000148-1
- 0.000148 bump

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.000145-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.000145-5
- Fix requires packages in *-tests package

* Wed Dec 07 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.000145-4
- Remove provided packages from *-tests package
- Update license to SPDX format

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.000145-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 01 2022 Jitka Plesnikova <jplesnik@redhat.com> - 0.000145-2
- Perl 5.36 rebuild

* Tue Mar 08 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.000145-1
- 0.000145 bump

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.000144-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Michal Josef Špaček <mspacek@redhat.com> - 0.000144-1
- 0.000144 bump

* Tue Nov 16 2021 Michal Josef Špaček <mspacek@redhat.com> - 0.000142-1
- 0.000142 bump

* Tue Jul 27 2021 Michal Josef Špaček <mspacek@redhat.com> - 0.000141-1
- 0.000141 bump

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.000140-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Michal Josef Špaček <mspacek@redhat.com> - 0.000140-1
- 0.000140 bump
- Package tests

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 0.000139-3
- Perl 5.34 rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.000139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 16 2020 Petr Pisar <ppisar@redhat.com> - 0.000139-1
- 0.000139 bump

* Thu Oct 22 2020 Petr Pisar <ppisar@redhat.com> - 0.000138-1
- 0.000138 bump

* Tue Oct 06 2020 Petr Pisar <ppisar@redhat.com> - 0.000136-1
- 0.000136 bump

* Wed Aug 19 2020 Petr Pisar <ppisar@redhat.com> - 0.000135-1
- 0.000135 bump

* Fri Aug 07 2020 Petr Pisar <ppisar@redhat.com> - 0.000132-1
- 0.000132 bump

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.000130-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Jitka Plesnikova <jplesnik@redhat.com> - 0.000130-2
- Perl 5.32 rebuild

* Mon Jun 01 2020 Petr Pisar <ppisar@redhat.com> - 0.000130-1
- 0.000130 bump

* Fri Jan 31 2020 Petr Pisar <ppisar@redhat.com> - 0.000129-1
- 0.000129 bump

* Fri Jan 31 2020 Petr Pisar <ppisar@redhat.com> - 0.000128-1
- 0.000128 bump

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.000127-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Petr Pisar <ppisar@redhat.com> - 0.000127-1
- 0.000127 bump

* Thu Aug 29 2019 Petr Pisar <ppisar@redhat.com> - 0.000126-1
- 0.000126 bump

* Tue Aug 20 2019 Petr Pisar <ppisar@redhat.com> - 0.000125-1
- 0.000125 bump

* Mon Aug 19 2019 Petr Pisar <ppisar@redhat.com> - 0.000124-1
- 0.000124 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.000122-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.000122-2
- Perl 5.30 rebuild

* Mon May 20 2019 Petr Pisar <ppisar@redhat.com> - 0.000122-1
- 0.000122 bump

* Thu May 09 2019 Petr Pisar <ppisar@redhat.com> - 0.000121-1
- 0.000121 bump

* Mon Apr 29 2019 Petr Pisar <ppisar@redhat.com> - 0.000120-1
- 0.000120 bump

* Mon Mar 18 2019 Petr Pisar <ppisar@redhat.com> - 0.000119-1
- 0.000119 bump

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.000118-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Petr Pisar <ppisar@redhat.com> - 0.000118-1
- 0.000118 bump

* Wed Dec 05 2018 Petr Pisar <ppisar@redhat.com> - 0.000117-1
- 0.000117 bump

* Thu Nov 29 2018 Petr Pisar <ppisar@redhat.com> - 0.000116-1
- 0.000116 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.000115-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Petr Pisar <ppisar@redhat.com> - 0.000115-1
- 0.000115 bump

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.000114-2
- Perl 5.28 rebuild

* Fri Apr 20 2018 Petr Pisar <ppisar@redhat.com> - 0.000114-1
- 0.000114 bump

* Thu Mar 15 2018 Petr Pisar <ppisar@redhat.com> - 0.000111-1
- 0.000111 bump

* Mon Mar 12 2018 Petr Pisar <ppisar@redhat.com> - 0.000108-1
- 0.000108 bump

* Wed Mar 07 2018 Petr Pisar <ppisar@redhat.com> - 0.000106-1
- 0.000106 bump

* Tue Mar 06 2018 Petr Pisar <ppisar@redhat.com> - 0.000104-1
- 0.000104 bump

* Mon Mar 05 2018 Petr Pisar <ppisar@redhat.com> - 0.000102-1
- 0.000102 bump

* Wed Feb 14 2018 Petr Pisar <ppisar@redhat.com> - 0.000100-1
- 0.000100 bump

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.000097-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Petr Pisar <ppisar@redhat.com> - 0.000097-1
- 0.000097 bump

* Fri Dec 08 2017 Petr Pisar <ppisar@redhat.com> - 0.000094-2
- Remove unused dependency on Term::ReadKey

* Tue Dec 05 2017 Petr Pisar <ppisar@redhat.com> - 0.000094-1
- 0.000094 bump

* Mon Nov 20 2017 Petr Pisar <ppisar@redhat.com> - 0.000084-1
- 0.000084 bump

* Fri Oct 27 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.000083-1
- 0.000083 bump

* Mon Oct 23 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.000082-1
- 0.000082 bump

* Tue Oct 17 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.000080-1
- 0.000080 bump

* Thu Sep 14 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.000077-1
- 0.000077 bump

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.000072-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Petr Pisar <ppisar@redhat.com> - 0.000072-1
- 0.000072 bump

* Mon Jun 05 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.000070-2
- Perl 5.26 rebuild

* Mon Mar 20 2017 Petr Pisar <ppisar@redhat.com> - 0.000070-1
- 0.000070 bump

* Fri Mar 17 2017 Petr Pisar <ppisar@redhat.com> - 0.000069-1
- 0.000069 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.000067-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Petr Pisar <ppisar@redhat.com> - 0.000067-1
- 0.000067 bump

* Tue Dec 20 2016 Petr Pisar <ppisar@redhat.com> - 0.000065-1
- 0.000065 bump

* Mon Dec 19 2016 Petr Pisar <ppisar@redhat.com> - 0.000063-1
- 0.000063 bump

* Thu Sep 29 2016 Petr Pisar <ppisar@redhat.com> - 0.000060-1
- 0.000060 bump

* Fri Sep 02 2016 Petr Pisar <ppisar@redhat.com> - 0.000058-1
- 0.000058 bump

* Mon Aug 01 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.000055-1
- 0.000055 bump

* Fri Jul 29 2016 Petr Pisar <ppisar@redhat.com> - 0.000054-1
- 0.000054 bump

* Tue Jul 19 2016 Petr Pisar <ppisar@redhat.com> - 0.000052-1
- 0.000052 bump

* Mon Jul 11 2016 Petr Pisar <ppisar@redhat.com> - 0.000050-1
- 0.000050 bump

* Mon Jul 04 2016 Petr Pisar <ppisar@redhat.com> - 0.000048-1
- 0.000048 bump

* Tue Jun 28 2016 Petr Pisar <ppisar@redhat.com> - 0.000042-1
- 0.000042 bump

* Mon Jun 27 2016 Petr Pisar <ppisar@redhat.com> - 0.000038-1
- 0.000038 bump

* Mon Jun 20 2016 Petr Pisar <ppisar@redhat.com> - 0.000032-1
- 0.000032 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.000030-2
- Perl 5.24 rebuild

* Wed May 11 2016 Petr Pisar <ppisar@redhat.com> - 0.000030-1
- 0.000030 bump

* Mon May 02 2016 Petr Pisar <ppisar@redhat.com> - 0.000029-1
- 0.000029 bump

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 0.000028-1
- 0.000028 bump

* Thu Apr 14 2016 Petr Pisar <ppisar@redhat.com> - 0.000027-1
- 0.000027 bump

* Mon Apr 11 2016 Petr Pisar <ppisar@redhat.com> - 0.000026-1
- 0.000026 bump

* Tue Apr 05 2016 Petr Pisar <ppisar@redhat.com> - 0.000025-1
- 0.000025 bump

* Mon Mar 21 2016 Petr Pisar <ppisar@redhat.com> - 0.000024-1
- 0.000024 bump

* Fri Mar 18 2016 Petr Pisar <ppisar@redhat.com> - 0.000023-1
- 0.000023 bump

* Tue Mar 08 2016 Petr Pisar <ppisar@redhat.com> - 0.000022-1
- 0.000022 bump

* Mon Mar 07 2016 Petr Pisar <ppisar@redhat.com> - 0.000021-1
- 0.000021 bump

* Thu Feb 11 2016 Petr Pisar <ppisar@redhat.com> 0.000020-1
- Specfile autogenerated by cpanspec 1.78.
