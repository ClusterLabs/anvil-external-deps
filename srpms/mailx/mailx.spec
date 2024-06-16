Name:                   mailx
Version:                1
Release:                1
Epoch:                  99
Vendor:                 dummy
Group:                  dummy
Summary:                Provides %{name}
License:                %{vendor}
# in Provides: you add whatever you want to fool the system
Buildroot:              %{_tmppath}/%{name}-%{version}-root
Provides:               %{name} = %{version}
Requires:               s-nail
%description
%{summary}
%files
