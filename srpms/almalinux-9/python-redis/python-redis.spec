# Enable tests by default.
%bcond_without tests

%global upstream_name redis

Name:           python-%{upstream_name}
Version:        5.0.5
Release:        %autorelease
Summary:        Python interface to the Redis key-value store
License:        MIT
URL:            https://github.com/redis/redis-py
Source0:        https://github.com/redis/redis-py/archive/v%{version}/redis-py-%{version}.tar.gz
BuildArch:      noarch
Patch0:         testrequires.patch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  redis
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(async-timeout)
BuildRequires:  python3dist(pytest-timeout)
%endif

%global _description\
This is a Python interface to the Redis key-value store.

%description %_description

%package -n     python3-%{upstream_name}
Summary:        Python 3 interface to the Redis key-value store
%{?python_provide:%python_provide python3-%{upstream_name}}

%description -n python3-%{upstream_name}
This is a Python 3 interface to the Redis key-value store.

%prep
%autosetup -n redis-py-%{version} -p1

# This test passes locally but fails in koji...
rm tests/test_commands.py*
rm tests/test_asyncio/test_commands.py

# Times out
rm tests/test_asyncio/test_connect.py
rm tests/test_asyncio/test_cwe_404.py

# The Fedora redis json and bloom packages are out of date, ts and graph are missing in the repos
rm tests/test_bloom.py
rm tests/test_graph.py
rm tests/test_json.py
rm tests/test_timeseries.py
rm tests/test_asyncio/test_bloom.py
rm tests/test_asyncio/test_graph.py
rm tests/test_asyncio/test_json.py
rm tests/test_asyncio/test_timeseries.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{upstream_name}

%if %{with tests}
%check
%if 0%{?fedora} >= 37 || 0%{?rhel} > 9
# redis 7+
redis-server --enable-debug-command yes &
%else
redis-server &
%endif
%pytest -m 'not onlycluster and not redismod and not ssl'
kill %1
%endif

%files -n python3-%{upstream_name} -f %{pyproject_files}
%doc CHANGES README.md

%changelog
%autochangelog
