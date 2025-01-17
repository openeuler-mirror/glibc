%global __filter_GLIBC_PRIVATE 1

%define rpm_ver_major %(eval "echo `rpm -q rpm |cut -d '-' -f2 |cut -d. -f1`")
%define rpm_ver_minor %(eval "echo `rpm -q rpm |cut -d '-' -f2 |cut -d. -f2`")
%define rpm_version_ge_412 %(eval "if [ %{rpm_ver_major} -gt 4 -o %{rpm_ver_major} -eq 4 -a %{rpm_ver_minor} -ge 12 ]; then echo 1; else echo 0; fi")
%define gcc_version %(eval "echo `gcc --version |head -1 |awk '{print $3}' |awk -F '.' '{print $1}'`")
##############################################################################
# We support the following options:
# --with/--without,
# * testsuite
#  - Running the testsuite. It must run for production builds.
#  - Default: Always run the testsuite.
# * benchtests
#  - Running and building benchmark subpackage.
#  - Default: Always build the benchtests.
# * bootstrap
#  - Bootstrapping the package.
#  - Default: Not bootstrapping.
# * werror
#  - Build with -Werror
#  - Default: Enable using -Werror
# * docs
#  - Build with documentation and the required dependencies.
#  - Default: Always build documentation.
# * valgrind
#  - Run smoke tests with valgrind to verify dynamic loader.
#  - Default: Always run valgrind tests if there is architecture support.
##############################################################################
%bcond_without testsuite
%bcond_with benchtests
%bcond_with bootstrap
%bcond_with werror
%bcond_without docs
%ifarch x86_64 aarch64
%bcond_with compat_2_17
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%if %{with bootstrap}
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif

# Only some architectures have static PIE support
%define pie_arches %{ix86} x86_64 aarch64

%define enablekernel 3.2
%define target %{_target_cpu}-%{_vendor}-linux
%ifarch %{arm}
%define target %{_target_cpu}-%{_vendor}-linuxeabi
%endif
%define x86_arches %{ix86} x86_64
%define all_license LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL
%define GCC gcc
%define GXX g++
##############################################################################
# glibc - The GNU C Library (glibc) core package.
##############################################################################
Name: 	 	glibc
Version: 	2.35
Release: 	4
Summary: 	The GNU libc libraries
License:	%{all_license}
URL: 		http://www.gnu.org/software/glibc/

Source0:   https://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Source2:   nsswitch.conf
Source3:   bench.mk
Source4:   glibc-bench-compare
Source5:   LanguageList
Source6:   LicenseList
Source7:   replace_same_file_to_hard_link.py

%if %{with testsuite}
Source8:   testsuite_whitelist.%{_target_cpu}
%endif

#Patch9000: turn-default-value-of-x86_rep_stosb_threshold_form_2K_to_1M.patch
#Patch9001: delete-no-hard-link-to-avoid-all_language-package-to.patch 
#Patch9002: 0001-add-base-files-for-libphtread-condition-family.patch
#Patch9003: 0002-add-header-files-for-libphtread_2_17_so.patch
#Patch9004: 0003-add-build-script-and-files-of-libpthread_2_17_so.patch
#Patch9005: 0004-add-two-header-files-with-some-deleted-macros.patch
#Patch9006: 0005-add-pthread-functions_h.patch
#Patch9007: 0006-add-elsion-function-which-moved-to-libc-in-glibc-2.34.patch
#Patch9008: 0007-add-lowlevellock_2_17_c.patch
#Patch9009: 0008-add-pause_nocancel_2_17.patch
#Patch9010: 0009-add-unwind-with-longjmp.patch
Patch9011: use-region-to-instead-of-country-for-extract-timezon.patch

Obsoletes: nscd < 2.35
Provides: ldconfig rtld(GNU_HASH) bundled(gnulib)

BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
BuildRequires: procps-ng, util-linux, gawk, systemtap-sdt-devel, systemd, python3
BuildRequires: make >= 4.0, bison >= 2.7, binutils >= 2.30-17, gcc >= 7.2.1-6
BuildRequires: m4 gcc_secure

%if %{without bootstrap}
BuildRequires: gd-devel libpng-devel zlib-devel
%endif

%if %{with docs}
BuildRequires: texinfo >= 5.0
%endif

%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
%endif

%if %{with valgrind}
BuildRequires: valgrind
%endif

%if 0%{?_enable_debug_packages}
BuildRequires: elfutils >= 0.72 rpm >= 4.2-0.56
%endif

%if %{without bootstrap}
%if %{with testsuite}
BuildRequires: gcc-c++ libstdc++-static glibc-devel libidn2
%endif
%endif

Requires: glibc-common = %{version}-%{release}
Requires: glibc-langpack = %{version}-%{release}
Requires: basesystem

%description
The GNU C Library project provides the core libraries for the GNU system and
GNU/Linux systems, as well as many other systems that use Linux as the kernel.
These libraries provide critical APIs including ISO C11, POSIX.1-2008, BSD,
OS-specific APIs and more. These APIs include such foundational facilities as
open, read, write, malloc, printf, getaddrinfo, dlopen, pthread_create, crypt,
 login, exit and more.

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Provides: glibc-langpack = %{version}-%{release}

Provides: glibc-langpack-en = %{version}-%{release}
Provides: glibc-langpack-en%{?_isa} = %{version}-%{release}
Provides: glibc-langpack-zh = %{version}-%{release}
Provides: glibc-langpack-zh%{?_isa} = %{version}-%{release}

Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a

%description common
The glibc-common package includes common binaries for the GNU libc
libraries and national language (locale) support. Besides, zh_CN and
en_US are included.

%transfiletriggerin common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

%transfiletriggerpostun common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

%undefine __brp_ldconfig

##############################################################################
# glibc "all-langpacks" sub-package
##############################################################################
%package all-langpacks
Summary: All language packs for %{name}.
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
Obsoletes: %{name}-minimal-langpack = 2.28

%{lua:
-- List the Symbol provided by all-langpacks
lang_provides = {}
for line in io.lines(rpm.expand("%{SOURCE5}")) do
    print(rpm.expand([[
Provides:]]..line..[[ = %{version}-%{release} 
Obsoletes:]]..line..[[ = 2.28 
]]))
end
}

%description all-langpacks
The glibc-all-langpacks provides all the glibc-langpacks. Every entry
includes the basic information required to support the corresponding
language in your applications.

##############################################################################
# glibc "locale-source" sub-package
##############################################################################
%package locale-source
Summary: The sources package of locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description locale-source
The locale-source package contains all language packs which are built custom
locales

##############################################################################
# glibc "locale-archive" sub-package
##############################################################################
%package locale-archive
Summary: The locale-archive of glibc
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description locale-archive
The locale-archive sub package contains the locale-archive. In the past,
this file is provided in "glibc-common".Now, we provide basic language support
in "glibc-common", but if you need a customized language, you can extract
it from the "local-archive".

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary:  The devel for %{name}
Requires: %{name} = %{version}-%{release}
Requires: libgcc%{_isa}
Requires(pre): info
Requires(pre): kernel-headers
Requires(pre): coreutils
Requires: kernel-headers >= 3.2
%if 0%{rpm_version_ge_412}
Requires: libxcrypt-devel%{_isa} >= 4.0.0
Requires: libxcrypt-static%{?_isa} >= 4.0.0
%endif
BuildRequires: kernel-headers >= 3.2

Provides: %{name}-static = %{version}-%{release}
Provides: %{name}-static%{_isa} = %{version}-%{release}
Provides: %{name}-headers = %{version}-%{release}
Provides: %{name}-headers(%{_target_cpu})
Provides: %{name}-headers%{_isa} = %{version}-%{release}

Obsoletes: %{name}-static = 2.28
Obsoletes: %{name}-headers = 2.28

%description devel
The glibc-devel package contains the object files necessary for developing
programs which use the standard C libraries. Besides, it contains the
headers. Thus, it is necessory to install glibc-devel if you ned develop programs.

##############################################################################
# nss modules sub-package
##############################################################################
%package -n nss_modules
Summary: Name Service Switch module using hash-indexed files and Hesiod
Requires: %{name}%{_isa} = %{version}-%{release}
Provides: nss_db = %{version}-%{release}
Provides: nss_db%{_isa} = %{version}-%{release}
Provides: nss_hesiod = %{version}-%{release}
Provides: nss_hesiod%{_isa} = %{version}-%{release}
Obsoletes: nss_db = 2.28, nss_hesiod = 2.28

%description -n nss_modules
This package contains nss_db and nss_hesiod. The former uses hash-indexed files
to speed up user, group, service, host name, and other NSS-based lookups.The
latter uses the Domain Name System (DNS) as a source for user, group, and service
information to follow the Hesiod convention of Project Athena.

##############################################################################
# nss-devel sub-package
##############################################################################
%package nss-devel
Summary:  The devel for directly linking NSS service modules
Requires: nss_db%{_isa} = %{version}-%{release}
Requires: nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
This package contains the necessary devel files to compile applications and
libraries which directly link against NSS modules supplied by glibc. This
package is rarely used, and in most cases use the glibc-devel package instead.

##############################################################################
# libnsl subpackage
##############################################################################
%package -n libnsl
Summary: 	Public client interface for NIS(YP) and NIS+
Requires: 	%{name}%{_isa} = %{version}-%{release}

%description -n libnsl
The libnsl package contains the public client interface for NIS(YP) and NIS+.
It replaces the NIS library that used to be in glibc.

##############################################################################
# glibc benchtests sub-package
##############################################################################
%if %{with benchtests}

%package benchtests
Summary: Build benchmarking binaries and scripts for %{name}

%description benchtests
This package provides built benchmark binaries and scripts which will be used
to run microbenchmark tests on the system.
%endif

##############################################################################
# glibc debugutils sub-package
##############################################################################
%package debugutils
Summary: debug files for %{name}
Requires: %{name} = %{version}-%{release}
Provides: %{name}-utils = %{version}-%{release}
Provides: %{name}-utils%{_isa} = %{version}-%{release}

Obsoletes: %{name}-utils = 2.28

%description debugutils
This package provides memusage, a memory usage profiler, mtrace, a memory leak
tracer and xtrace, a function call tracer, all of which is not necessory for you.

##############################################################################
# glibc help sub-package
##############################################################################
%package help
Summary: The doc and man for %{name}
Buildarch: noarch
Requires: man info

%description help
This package provides al doc and man files of %{name}

##############################################################################
# glibc compat-2.17 sub-package
##############################################################################
%if %{with compat_2_17}
%package compat-2.17
Summary: provides pthread library with glibc-2.17

%description compat-2.17
This subpackage to provide the function of the glibc-2.17 pthread library.
Currently, provide pthread_condition function..
%endif

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%autosetup -n %{name}-%{version} -p1

chmod +x benchtests/scripts/*.py scripts/pylint

find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

touch `find . -name configure`

touch locale/programs/*-kw.h

##############################################################################
# Build glibc...
##############################################################################
%build

BuildFlags="-O2 -g"
BuildFlags="$BuildFlags -DNDEBUG"
reference=" \
        "-Wp,-D_GLIBCXX_ASSERTIONS" \
        "-fasynchronous-unwind-tables" \
        "-fstack-clash-protection" \
        "-funwind-tables" \
        "-m31" \
        "-m32" \
        "-m64" \
        "-march=haswell" \
        "-march=i686" \
        "-march=x86-64" \
        "-march=z13" \
        "-march=z14" \
        "-march=zEC12" \
        "-mfpmath=sse" \
        "-msse2" \
        "-mstackrealign" \
        "-mtune=generic" \
        "-mtune=z13" \
        "-mtune=z14" \
        "-mtune=zEC12" \
        "-specs=/usr/lib/rpm/%{_vendor}/%{_vendor}-annobin-cc1" "

for flag in $RPM_OPT_FLAGS $RPM_LD_FLAGS ; do
        if echo "$reference" | grep -q -F " $flag " ; then
                BuildFlags="$BuildFlags $flag"
        fi
done

%define glibc_make_flags_as ASFLAGS="-g -Wa,--generate-missing-build-notes=yes"
%define glibc_make_flags %{glibc_make_flags_as}

EnableKernel="--enable-kernel=%{enablekernel}"

builddir=build-%{target}
rm -rf $builddir
mkdir $builddir
pushd $builddir
../configure CC="%GCC" CXX="%GXX" CFLAGS="$BuildFlags" \
	--prefix=%{_prefix} \
	--with-headers=%{_prefix}/include $EnableKernel \
	--with-nonshared-cflags=-Wp,-D_FORTIFY_SOURCE=2 \
	--enable-bind-now \
	--build=%{target} \
	--enable-stack-protector=strong \
%ifarch %{pie_arches}
%if 0%{?gcc_version} >= 8
	--enable-static-pie \
%endif
%endif
%ifarch %{x86_arches}
%if 0%{?gcc_version} >= 8
	--enable-cet \
%endif
%endif
	--enable-tunables \
	--enable-systemtap \
%ifarch %{ix86}
	--disable-multi-arch \
%endif
%if %{without werror}
	--disable-werror \
%endif
	--disable-profile \
%if %{with bootstrap}
	--without-selinux \
%endif
%if 0%{rpm_version_ge_412}
	--disable-crypt \
%endif
        --disable-build-nscd \
        --disable-nscd ||
	{ cat config.log; false; }

make %{?_smp_mflags} -O -r %{glibc_make_flags}
popd

##############################################################################
# Build libpthread-2.17.so
##############################################################################
%if %{with compat_2_17}
	cd nptl_2_17
	sh build_libpthread-2.17.so.sh %{_target_cpu} $builddir
	cd ..
%endif

##############################################################################
# Install glibc...
##############################################################################
%install
%ifarch riscv64
for d in $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT/%{_lib}; do
	mkdir -p $d
	(cd $d && ln -sf . lp64d)
done
%endif

make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT install -C build-%{target}

pushd build-%{target}

make %{?_smp_mflags} install_root=$RPM_BUILD_ROOT \
	install-locale-files -C ../localedata objdir=`pwd`
popd

python3 %{SOURCE7} $RPM_BUILD_ROOT/usr/lib/locale

rm -f $RPM_BUILD_ROOT/%{_libdir}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libNoVersion*
rm -f $RPM_BUILD_ROOT/%{_lib}/libnss1-*
rm -f $RPM_BUILD_ROOT/%{_lib}/libnss-*.so.1
rm -f $RPM_BUILD_ROOT/{usr/,}sbin/sln

mkdir -p $RPM_BUILD_ROOT/var/cache/ldconfig
truncate -s 0 $RPM_BUILD_ROOT/var/cache/ldconfig/aux-cache

$RPM_BUILD_ROOT/sbin/ldconfig -N -r $RPM_BUILD_ROOT

# Install info files
%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d $RPM_BUILD_ROOT%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p $RPM_BUILD_ROOT%{_infodir}
  mv -f $RPM_BUILD_ROOT%{_prefix}/info/* $RPM_BUILD_ROOT%{_infodir}
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf $RPM_BUILD_ROOT%{_infodir}/libc*

%else
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_infodir}/libc.info*
%endif

# Create all-packages libc.lang
olddir=`pwd`
pushd $RPM_BUILD_ROOT%{_prefix}/lib/locale
rm -f locale-archive
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
        --alias-file=$olddir/intl/locale.alias	\
        --prefix $RPM_BUILD_ROOT --add-to-archive \
        eo *_*
%{find_lang} libc
# In the past, locale-archive is provided by common.
# In the current version, locale-archive is provided by locale-archive.
# Due to the change of the packing mode, the locale-archive fails to be
# replaced during the upgrade. Therefore, a backup file is required to
# replace the locale-archive.
ln locale-archive locale-archive.update
popd
mv  $RPM_BUILD_ROOT%{_prefix}/lib/locale/libc.lang .

# Install configuration files for services
install -p -m 644 %{SOURCE2} $RPM_BUILD_ROOT/etc/nsswitch.conf

# This is for compat-2.17
%if %{with compat_2_17}
install -p -m 755  build-%{target}/nptl/libpthread-2.17.so $RPM_BUILD_ROOT%{_libdir}
%endif

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
truncate -s 0 $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
truncate -s 0 $RPM_BUILD_ROOT/etc/gai.conf

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

touch -r %{SOURCE0} $RPM_BUILD_ROOT/etc/ld.so.conf
touch -r inet/etc.rpc $RPM_BUILD_ROOT/etc/rpc

# Lastly copy some additional documentation for the packages.
rm -rf documentation
mkdir documentation
cp timezone/README documentation/README.timezone
cp posix/gai.conf documentation/

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/

#makefile.
for b in %{SOURCE3} %{SOURCE4}; do
	cp $b $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
done

#comparison scripts.
for i in benchout.schema.json compare_bench.py import_bench.py validate_benchout.py; do
	cp benchtests/scripts/$i $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
done
%endif

pushd locale
ln -s programs/*.gperf .
popd

pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

%if %{with docs}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%endif

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so \
	$RPM_BUILD_ROOT%{_libdir}

# Strip all of the installed object files.
strip -g $RPM_BUILD_ROOT%{_libdir}/*.o

# create a null libpthread static link for compatibility.
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
rm libpthread.a
ar rc libpthread.a
popd

for i in $RPM_BUILD_ROOT%{_prefix}/bin/{xtrace,memusage}; do
%if %{with bootstrap}
  test -w $i || continue
%endif
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

touch master.filelist
touch glibc.filelist
touch common.filelist
touch devel.filelist
touch nss_modules.filelist
touch nss-devel.filelist
touch libnsl.filelist
touch debugutils.filelist
touch benchtests.filelist
%if %{with compat_2_17}
touch compat-2.17.filelist
%endif

{
  find $RPM_BUILD_ROOT \( -type f -o -type l \) \
       \( \
     -name etc -printf "%%%%config " -o \
     -name gconv-modules \
     -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " -o \
     -name gconv-modules.cache \
     -printf "%%%%verify(not md5 size mtime) " \
     , \
     ! -path "*/lib/debug/*" -printf "/%%P\n" \)

  find $RPM_BUILD_ROOT -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' \
%if %{with docs}
    ! -path '*%{_infodir}' -o \
%endif
      -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e '\,.*/share/i18n/locales/.*,d' \
      -e '\,.*/share/i18n/charmaps/.*,d' \
      -e '\,.*/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,.*%{_libdir}/lib\(pcprofile\|memusage\)\.so,d' \
%if %{with compat_2_17}
      -e '\,.*%{_libdir}/libpthread-2.17.so,d' \
%endif
      -e '\,.*/bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > master.filelist

chmod 0444 master.filelist

##############################################################################
# glibc - The GNU C Library (glibc) core package.
##############################################################################
cat master.filelist \
    | grep -v \
    -e '%{_infodir}' \
    -e '%{_libdir}/lib.*_p.a' \
    -e '%{_prefix}/include' \
    -e '%{_libdir}/lib.*\.a' \
        -e '%{_libdir}/.*\.o' \
    -e '%{_libdir}/lib.*\.so' \
    -e '%{_prefix}/bin' \
    -e '%{_prefix}/lib/locale' \
    -e '%{_prefix}/sbin/[^i]' \
    -e '%{_prefix}/share' \
    -e '/var/db/Makefile' \
    -e '/libnss_.*\.so[0-9.]*$' \
    -e '/libnsl' \
    -e 'glibc-benchtests' \
    -e 'aux-cache' \
    > glibc.filelist

for module in compat files dns; do
    cat master.filelist \
    | grep -E \
    -e "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    >> glibc.filelist
done

echo  '%{_libdir}/libmemusage.so' >> glibc.filelist
echo  '%{_libdir}/libpcprofile.so' >> glibc.filelist

##############################################################################
# glibc "common" sub-package
##############################################################################
grep '%{_prefix}/bin' master.filelist > common.filelist
grep '%{_prefix}/sbin' master.filelist \
       | grep -v '%{_prefix}/sbin/iconvconfig'  >> common.filelist

grep '%{_prefix}/share' master.filelist \
	| grep -v \
	-e '%{_prefix}/share/info/libc.info.*' \
	-e '%%dir %{prefix}/share/info' \
	-e '%%dir %{prefix}/share' \
	>> common.filelist

###############################################################################
# glibc "devel" sub-package
###############################################################################
%if %{with docs}
grep '%{_infodir}' master.filelist | grep -v '%{_infodir}/dir' > devel.filelist
%endif

grep '%{_libdir}/lib.*\.a' master.filelist \
  | grep '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\)\.a$' \
  >> devel.filelist

grep '%{_libdir}/.*\.o' < master.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < master.filelist >> devel.filelist

sed -i -e '\,/libnss_[a-z]*\.so$,d' devel.filelist

grep '%{_prefix}/include' < master.filelist >> devel.filelist

grep '%{_libdir}/lib.*\.a' < master.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\)\.a$' \
  >> devel.filelist


##############################################################################
# nss modules sub-package
##############################################################################
grep -E "/libnss_(db|hesiod)(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
master.filelist > nss_modules.filelist

##############################################################################
# nss-devel sub-package
##############################################################################
grep '/libnss_[a-z]*\.so$' master.filelist > nss-devel.filelist

##############################################################################
# libnsl subpackage
##############################################################################
grep -E '/libnsl\.so\.[0-9]+$' master.filelist > libnsl.filelist
test $(wc -l < libnsl.filelist) -eq 1

##############################################################################
# glibc debugutils sub-package
##############################################################################
cat > debugutils.filelist <<EOF
%if %{without bootstrap}
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%endif
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

%if %{with benchtests}
##############################################################################
# glibc benchtests sub-package
##############################################################################
find build-%{target}/benchtests -type f -executable | while read b; do
    echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done > benchtests.filelist
# ... and the makefile.
for b in %{SOURCE3} %{SOURCE4}; do
    echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done
# ... and finally, the comparison scripts.
echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif

%if %{with compat_2_17}
##############################################################################
# glibc compat-2.17 sub-package
##############################################################################
        echo "%{_libdir}/libpthread-2.17.so" >> compat-2.17.filelist
%endif

reliantlib=""

function findReliantLib()
{
        local library=$1
        reliantlib=$(readelf -d $library | grep "(NEEDED)" | awk -F "Shared library" '{print $2}')$reliantlib
}

# remove gconv rpath/runpath
function removeLoadPath()
{
        local file=$1
        local rpathInfo=$(chrpath -l $file | grep "RPATH=")
        local runpathInfo=$(chrpath -l $file | grep "RUNPATH=")

        local currPath=""
        if [ x"$rpathInfo" != x"" ]; then
                currPath=$(echo $rpathInfo | awk -F "RPATH=" '{print $2}')
        fi

        if [ x"$runpathInfo" != x"" ]; then
                currPath=$(echo $runpathInfo | awk -F "RUNPATH=" '{print $2}')
        fi

        if [ x"$currPath" == x"\$ORIGIN" ]; then
                chrpath -d $file

                findReliantLib $file
        fi
}

set +e

# find and remove RPATH/RUNPATH
for file in $(find $RPM_BUILD_ROOT%{_libdir}/gconv/ -name "*.so" -exec file {} ';' | grep "\<ELF\>" | awk -F ':' '{print $1}')
do
        removeLoadPath $file
done

function createSoftLink()
{
        # pick up the dynamic libraries and create softlink for them
        local tmplib=$(echo $reliantlib | sed 's/://g' | sed 's/ //g' | sed 's/\[//g' | sed 's/]/\n/g' | sort | uniq)

        for temp in $tmplib
        do
                if [ -f "$RPM_BUILD_ROOT%{_libdir}/gconv/$temp" ]; then
                        ln -sf %{_libdir}/gconv/$temp $RPM_BUILD_ROOT%{_libdir}/$temp
                        echo %{_libdir}/$temp >> glibc.filelist
                fi
        done
}

# create soft link for the reliant libraries
createSoftLink
set -e

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

omit_testsuite() {
  whitelist=$1
  sed -i '/^#/d' $whitelist
  sed -i '/^[\s]*$/d' $whitelist
  while read testsuite; do
    testsuite_escape=$(echo "$testsuite" | \
                       sed 's/\([.+?^$\/\\|()\[]\|\]\)/\\\0/g')
    sed -i "/${testsuite_escape}/d" rpmbuild.tests.sum.not-passing
  done < "$whitelist"
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
make %{?_smp_mflags} -O check |& tee rpmbuild.check.log >&2
test -s tests.sum

# This hides a test suite build failure, which should be fatal.  We
# check "Summary of test results:" below to verify that all tests
# were built and run.
if ! grep -q '^Summary of test results:$' rpmbuild.check.log ; then
  echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
  exit 1
fi
grep -v ^PASS: tests.sum | grep -v ^UNSUPPORTED > rpmbuild.tests.sum.not-passing || true

# Delete the testsuite from the whitelist
#cp %{SOURCE8} testsuite_whitelist
#omit_testsuite testsuite_whitelist
#rm -rf testsuite_whitelist

set +x
if test -s rpmbuild.tests.sum.not-passing ; then
  echo ===================FAILED TESTS===================== >&2
  echo "Target: $(basename "$(pwd)")" >& 2
  cat rpmbuild.tests.sum.not-passing >&2
  while read failed_code failed_test ; do
    for suffix in out test-result ; do
      if test -e "$failed_test.$suffix"; then
        echo >&2
        echo "=====$failed_code $failed_test.$suffix=====" >&2
        cat -- "$failed_test.$suffix" >&2
        echo >&2
      fi
    done
  done <rpmbuild.tests.sum.not-passing
  #exit 1
fi

# Unconditonally dump differences in the system call list.
echo "* System call consistency checks:" >&2
cat misc/tst-syscall-list.out >&2
set -x
popd

echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr $RPM_BUILD_ROOT/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

pushd build-%{target}
LD_SHOW_AUXV=1 elf/ld.so --library-path .:elf:nptl:dlfcn /bin/true

%if %{with valgrind}
elf/ld.so --library-path .:elf:nptl:dlfcn \
	/usr/bin/valgrind --error-exitcode=1 \
	elf/ld.so --library-path .:elf:nptl:dlfcn /usr/bin/true
%endif
popd

%endif # %{run_glibc_tests}

##############################################################################
# Install and uninstall scripts
##############################################################################
%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

%post -p <lua>
-- We use lua's posix.exec because there may be no shell that we can
-- run during glibc upgrade.
function post_exec (program, ...)
  local pid = posix.fork ()
  if pid == 0 then
    assert (posix.exec (program, ...))
  elseif pid > 0 then
    posix.wait (pid)
  end
end

-- (1) Remove multilib libraries from previous installs.
-- In order to support in-place upgrades, we must immediately remove
-- obsolete platform directories after installing a new glibc
-- version.  RPM only deletes files removed by updates near the end
-- of the transaction.  If we did not remove the obsolete platform
-- directories here, they may be preferred by the dynamic linker
-- during the execution of subsequent RPM scriptlets, likely
-- resulting in process startup failures.

-- Full set of libraries glibc may install.
install_libs = { "anl", "BrokenLocale", "c", "dl", "m", "mvec",
                "nss_compat", "nss_db", "nss_dns", "nss_files",
                "nss_hesiod", "pthread", "resolv", "rt", "SegFault",
                "thread_db", "util" }

-- We are going to remove these libraries. Generally speaking we remove
-- all core libraries in the multilib directory.
-- We employ a tight match where X.Y is in [2.0,9.9*], so we would 
-- match "libc-2.0.so" and so on up to "libc-9.9*".
remove_regexps = {}
for i = 1, #install_libs do
  remove_regexps[i] = ("lib" .. install_libs[i]
                       .. "%%-[2-9]%%.[0-9]+%%.so$")
end

-- Two exceptions:
remove_regexps[#install_libs + 1] = "libthread_db%%-1%%.0%%.so"
remove_regexps[#install_libs + 2] = "libSegFault%%.so"

-- We are going to search these directories.
local remove_dirs = { "%{_libdir}/i686",
                     "%{_libdir}/i686/nosegneg" }

-- Walk all the directories with files we need to remove...
for _, rdir in ipairs (remove_dirs) do
  if posix.access (rdir) then
    -- If the directory exists we look at all the files...
    local remove_files = posix.files (rdir)
    for rfile in remove_files do
      for _, rregexp in ipairs (remove_regexps) do
       -- Does it match the regexp?
       local dso = string.match (rfile, rregexp)
        if (dso ~= nil) then
         -- Removing file...
         os.remove (rdir .. '/' .. rfile)
       end
      end
    end
  end
end

-- (2) Update /etc/ld.so.conf
-- Next we update /etc/ld.so.conf to ensure that it starts with
-- a literal "include ld.so.conf.d/*.conf".

local ldsoconf = "/etc/ld.so.conf"
local ldsoconf_tmp = "/etc/glibc_post_upgrade.ld.so.conf"

if posix.access (ldsoconf) then

  -- We must have a "include ld.so.conf.d/*.conf" line.
  local have_include = false
  for line in io.lines (ldsoconf) do
    -- This must match, and we don't ignore whitespace.
    if string.match (line, "^include ld.so.conf.d/%%*%%.conf$") ~= nil then
      have_include = true
    end
  end

  if not have_include then
    -- Insert "include ld.so.conf.d/*.conf" line at the start of the
    -- file. We only support one of these post upgrades running at
    -- a time (temporary file name is fixed).
    local tmp_fd = io.open (ldsoconf_tmp, "w")
    if tmp_fd ~= nil then
      tmp_fd:write ("include ld.so.conf.d/*.conf\n")
      for line in io.lines (ldsoconf) do
        tmp_fd:write (line .. "\n")
      end
      tmp_fd:close ()
      local res = os.rename (ldsoconf_tmp, ldsoconf)
      if res == nil then
        io.stdout:write ("Error: Unable to update configuration file (rename).\n")
      end
    else
      io.stdout:write ("Error: Unable to update configuration file (open).\n")
    end
  end
end

-- (3) Rebuild ld.so.cache early.
-- If the format of the cache changes then we need to rebuild
-- the cache early to avoid any problems running binaries with
-- the new glibc.

-- Note: We use _prefix because Fedora's UsrMove says so.
post_exec ("%{_prefix}/sbin/ldconfig")

-- (4) Update gconv modules cache.
-- If the /usr/lib/gconv/gconv-modules.cache exists, then update it
-- with the latest set of modules that were just installed.
-- We assume that the cache is in _libdir/gconv and called
-- "gconv-modules.cache".
local iconv_dir = "%{_libdir}/gconv"
local iconv_cache = iconv_dir .. "/gconv-modules.cache"
if (posix.utime (iconv_cache) == 0) then
  post_exec ("%{_prefix}/sbin/iconvconfig",
            "-o", iconv_cache,
            "--nostdlib",
            iconv_dir)
else
  io.stdout:write ("Error: Missing " .. iconv_cache .. " file.\n")
end

%posttrans locale-archive
archive_path="%{_prefix}/lib/locale/locale-archive"
update_path="%{_prefix}/lib/locale/locale-archive.update"
save_path="%{_prefix}/lib/locale/locale-archive.rpmsave"
archive_stat=`stat --format="%D %i" "$archive_path" 2>/dev/null || echo "null"`
update_stat=`stat --format="%D %i" "$update_path" || echo "null"`
# When the hard link does not match, use locale-archive.update
if [ "$archive_stat" != "null" ] &&
   [ "$update_stat" != "null" ] &&
   [ "$archive_stat" != "$update_stat" ];then
    unlink $archive_path
    archive_stat="null"
fi
# Regenerate a file if it does not exist
if [ "$archive_stat" == "null" ];then
   ln "$update_path" "$archive_path"
fi
# Delete the .rpmsave
if [ -f "$save_path" ];then
    unlink $save_path
fi

%pre devel
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

##############################################################################
# Files list
##############################################################################
%files -f glibc.filelist
%dir %{_prefix}/%{_lib}/audit
%verify(not md5 size mtime) %config(noreplace) /etc/nsswitch.conf
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%files -f common.filelist common
%dir %{_prefix}/lib/locale
%dir %{_prefix}/lib/locale/C.utf8
%{_prefix}/lib/locale/C.utf8/*
%{_prefix}/lib/locale/zh*
%{_prefix}/lib/locale/en*
%{_prefix}/share/locale/zh*
%{_prefix}/share/locale/en*

%files -f libc.lang all-langpacks
%{_prefix}/lib/locale
%exclude %{_prefix}/lib/locale/locale-archive
%exclude %{_prefix}/lib/locale/locale-archive.update
%exclude %{_prefix}/lib/locale/C.utf8
%exclude %{_prefix}/lib/locale/zh*
%exclude %{_prefix}/lib/locale/en*
%exclude %{_prefix}/share/locale/zh*
%exclude %{_prefix}/share/locale/en*

%files locale-source
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files locale-archive
%attr(0644,root,root) %{_prefix}/lib/locale/locale-archive
%attr(0644,root,root) %{_prefix}/lib/locale/locale-archive.update

%files -f devel.filelist devel

%files -f nss_modules.filelist -n nss_modules
/var/db/Makefile

%files -f nss-devel.filelist nss-devel

%files -f libnsl.filelist -n libnsl
/%{_lib}/libnsl.so.1

%files -f debugutils.filelist debugutils

%if %{with benchtests}
%files -f benchtests.filelist benchtests
%endif

#Doc of glibc package
%doc README NEWS INSTALL elf/rtld-debugger-interface.txt
#Doc of common sub-package
%doc documentation/README.timezone
%doc documentation/gai.conf
#Doc of nss_modules sub-package
%doc hesiod/README.hesiod

%if %{with compat_2_17}
%files -f compat-2.17.filelist compat-2.17
%endif

%changelog
* Tue Mar 1 2022 Qingqing Li <liqingqing3@huawei.com> - 2.35-4
- remove shared library's RPATH/RUNPATH for security

* Tue Feb 22 2022 Qingqing Li <liqingqing3@huawei.com> - 2.35-3
- tzselect: use region to select timezone

* Thu Feb 10 2022 jiangheng12 <jiangheng12@huawei.com> - 2.35-2
- remove nscd; The functionality nscd currently provides can be
  achieved by using systemd-resolved for DNS caching and the sssd
  daemon for everything else

* Tue Feb 8 2022 Qingqing Li <liqingqing3@huawei.com> - 2.35-1
- upgrade to 2.35

* Fri Jan 28 2022 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-39
- refactor the generation mode of the debug package and
  add correct files to the glibc-debugsource sync form 22.03-LTS

* Tue Jan 4 2022 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-38
- testsuit: delete check-installed-headers-c and check-installed-headers-cxx
            which are checked in CI to improves the compilation speed.
- testsuit: delete glibc-benchtest

* Sat Dec 25 2021 liusirui <liusirui@huawei.com> - 2.34-37
- ld.so: Don't fill the DT_DEBUG entry in ld.so [BZ #28129]

* Fri Dec 24 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-36
- do not define tgmath.h fmaxmag, fminmag macros for C2X (BZ #28397)

* Fri Dec 24 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-35
- io: Fix ftw internal realloc buffer (BZ #28126)

* Tue Dec 21 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-34
- tst: fix failing nss/tst-nss-files-hosts-long with local resolver
       use support_open_dev_null_range io/tst-closefrom, mise/tst-close_range, and posix/tst-spawn5(BZ#28260)
       nptl: add one more barrier to nptl/tst-create1

* Wed Dec 15 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-33
- pthread/tst-cancel28: Fix barrier re-init race condition

* Thu Dec 9 2021 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-32
- Deleted some unnecessary command when make master.filelist

* Thu Dec 9 2021 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-31
- support all Chinese and English by default
  add zh_* and en_* to glibc-common
  the size of glibc-common is increased from 1.8MB to 3.5MB

* Fri Dec 3 2021 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-30
- turn the default value of x86_rep_stosb_threshold from 2k to 1M

* Thu Dec 2 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-29
- revert the use of sched_getaffinity [BZ #28310]

* Tue Nov 30 2021 Bin Wang <wangbin224@huawei.com> - 2.34-28
- Linux: Simplify __opensock and fix race condition [BZ #28353]

* Wed Nov 24 2021 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-27
- Refactor the libpthread-2.17.so code and pass all test cases.
  delete libpthread-2.17.so from glibc-devel

* Fri Nov 19 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-26
- revert supress -Wcast-qual warnings in bsearch

* Mon Nov 15 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-25
- fix attribute access mode on getcwd [BZ #27476]
- supress -Wcast-qual warnings in bsearch

* Mon Nov 15 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-24
- elf: fix ld.so crash while loading a DSO with a read-only dynamic section
  https://sourceware.org/bugzilla/show_bug.cgi?id=28340

* Wed Nov 10 2021 Qingqing Li <liqingqing3@huawei.com> - 2.34-23
- gconv: Do not emit spurious NUL character in ISO-2022-JP-3,
	this also fix CVE-2021-43396.
  uplink: https://sourceware.org/bugzilla/show_bug.cgi?id=28524

* Tue Nov 9 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-22
- iconvconfig: Fix behaviour with --prefix
  uplink: https://sourceware.org/bugzilla/show_bug.cgi?id=28199

* Mon Nov 8 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-21
- nptl: pthread_kill race condition issues fixed.
  uplink: https://sourceware.org/bugzilla/show_bug.cgi?id=19193
	  https://sourceware.org/bugzilla/show_bug.cgi?id=12889
	  https://sourceware.org/bugzilla/show_bug.cgi?id=28036
	  https://sourceware.org/bugzilla/show_bug.cgi?id=28363
	  https://sourceware.org/bugzilla/show_bug.cgi?id=28407

* Thu Nov 4 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-20
- nptl: pthread_kill and pthread_cancel return success
        for satisfy posix standard.
  uplink: https://sourceware.org/bugzilla/show_bug.cgi?id=19193

* Fri Oct 29 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-19
- aarch64: update a64fx memset not to degrade at 16KB

* Thu Oct 28 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-18
- use testl instead of andl to check __x86_string_control to
  avoid updating __x86_string_control

* Tue Oct 26 2021 Yang Yanchao<yangyanchao6@huawei.com> - 2.34-17
- Show more debugging information during testsuite

* Tue Oct 26 2021 Chuangchuang Fang<fangchuangchuang@huawei.com> - 2.34-16
- Use __executable_start as the lowest address for profiling

* Tue Oct 26 2021 Yang Yanchao<yangyanchao6@huawei.com> - 2.34-15
- add glibc-compat-2.17 subpackage to provide the function of 
  the glibc-2.17 pthread library.
  Currently, provide pthread_condition function.

* Mon Oct 25 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-14
- mtrace fix output with PIE and ASLR.
- elf: rtld copy terminating null in tunables strdup.

* Mon Oct 25 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-13
- fpu: x86-64 optimize load of all bits set into ZMM register.

* Tue Oct 19 2021 Yang Yanchao <yangyanchao6@huawei.com> - 2.34-12
- Add locale-archive sub packages to support more languages
  and reduce memory usage.

* Tue Oct 12 2021 Yang Yanchao<yangyanchao6@huawei.com> - 2.34-11
- Add the testsuite whitelist.
  If a test case out of the trustlist fails, the compilation is interrupted.

* Mon Oct 11 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-10
- update test memmove.c to cover 16KB.

* Wed Sep 29 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-9
- elf: drop elf/tls-macros.h in favor of thread tls_mode attribute.
- use __ehdr_start for __GLOBAL_OFFSET_TABLE[0]

* Wed Sep 29 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-8
- fix overflow ittimer tests on 32 bit system

* Mon Sep 27 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-7
- mtrace: use a static buffer for printing, fix memory leak.
  upstream link: https://sourceware.org/bugzilla/show_bug.cgi?id=25947

* Sun Sep 26 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-6
- elf: Unconditionally use __ehdr_start.
- aarch64: Make elf_machine_{load_addr,dynamic} robust [BZ #28203].
  upstream link: https://sourceware.org/bugzilla/show_bug.cgi?id=28203

* Fri Sep 17 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-5
- aarch64: optimize memset performance.

* Fri Sep 17 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-4
- backport upstream patches to fix some memory leak and double free bugs

* Tue Sep 14 2021 Yang Yanchao<yangyanchao6@huawei.com> - 2.34-3
- add --enable-static-pie in aarch64

* Wed Aug 25 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-2
- fix CVE-2021-38604
  https://sourceware.org/bugzilla/show_bug.cgi?id=28213

* Thu Aug 5 2021 Qingqing Li<liqingqing3@huawei.com> - 2.34-1
- upgrade to 2.34.

* Fri Jul 23 2021 zhouwenpei<zhouwenpei1@huawei.com> - 2.33-7
- remove unnecessary build require.

* Sat Jul 3 2021 Qingqing Li<liqingqing3@huawei.com> - 2.33-6
- malloc: tcache shutdown sequence does not work if the thread never allocated anything. (bug 28028)
  https://sourceware.org/bugzilla/show_bug.cgi?id=28028

* Thu Jul 1 2021 Qingqing Li<liqingqing3@huawei.com> - 2.33-5
- wordexp: Use strtoul instead of atoi so that overflow can be detected. (bug 28011)
  https://sourceware.org/bugzilla/show_bug.cgi?id=28011

* Fri Jun 18 2021 Qingqing Li<liqingqing3@huawei.com> - 2.33-4
- fix CVE-2021-33574(bug 27896)
  https://sourceware.org/bugzilla/show_bug.cgi?id=27896

* Tue Apr 27 2021 xuhuijie<xuhujie@huawei.com> - 2.33-3
- Fix locales BEP inconsistence, use python to replace same file
  to hard link

* Wed Apr 7 2021 xieliuhua<xieliuhua@huawei.com> - 2.33-2
- Fix-the-inaccuracy-of-j0f-j1f-y0f-y1f-BZ.patch

* Fri Mar 5 2021 Wang Shuo<wangshuo_1994@foxmail.com> - 2.33-1
- upgrade glibc to 2.33-1

* Tue Jan 26 2021 shanzhikun <shanzhikun@huawei.com> - 2.31-9
- elf: Allow dlopen of filter object to work [BZ #16272]
  https://sourceware.org/bugzilla/show_bug.cgi?id=16272

* Fri Jan 8 2021 Wang Shuo<wangshuo_1994@foxmail.com> - 2.31-8
- Replace "openEuler" by %{_vendor} for versatility

* Tue Nov 10 2020 liusirui <liusirui@huawei.com> - 2.31-7
- Fix CVE-2020-27618, iconv accept redundant shift sequences in IBM1364 [BZ #26224]
  https://sourceware.org/bugzilla/show_bug.cgi?id=26224

* Tue Sep 15 2020 shanzhikun<shanzhikun@huawei.com> - 2.31-6
- rtld: Avoid using up static TLS surplus for optimizations [BZ #25051].
  https://sourceware.org/git/?p=glibc.git;a=commit;h=ffb17e7ba3a5ba9632cee97330b325072fbe41dd

* Fri Sep 4 2020 MarsChan<chenmingmin@huawei.com> - 2.31-5
- For political reasons, remove country selection from tzselect.ksh

* Fri Aug 14 2020 Xu Huijie<546391727@qq.com> - 2.31-4
- since the new version of the pthread_cond_wait() 
  function has performance degradation in multi-core 
  scenarios, here is an extra libpthreadcond.so using 
  old version of the function. you can use it by adding 
  LD_PRELOAD=./libpthreadcond.so in front of your program
  (eg: LD_PRELOAD=./libpthreadcond.so ./test). 
  use with-libpthreadcond to compile it.
  warning:2.17 version pthread_cond_wait() does not meet
  the posix standard, you should pay attention when using
  it. 

* Fri Jul 24 2020 Wang Shuo<wangshuo_1994@foxmail.com> - 2.31-3
- backport patch to disable warnings due to deprecated libselinux
- symbols used by nss and nscd

* Fri Jul 24 2020 Wang Shuo<wangshuo_1994@foxmail.com> - 2.31-2
- fix CVE-2020-6096
- fix bugzilla 26137, 26214 and 26215

* Thu Jul 9 2020 wuxu<wuxu.wu@hotmail.com> - 2.31-1
- upgrade glibc to 2.31-1 
- delete build-locale-archive command
- delete nsswitch.conf file
- replace glibc_post_upgrade function with lua
- remove sys/sysctl.h header file
- delete stime, ftime function

* Tue Jul 7 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-45
- disable rpc, it has been splited to libnss and libtirpc
- disable parallel compilation

* Tue Jul 7 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-44
- backup to version 40

* Mon Jul 6 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-43
- disable rpc, it has been splited to libnss and libtirpc
- disable parallel compilation

* Mon Jul 6 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-42
- add zh and en to LanguageList

* Thu Jul 2 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-41
- add filelist to improve the scalability
- backport many patch for bugfix

* Sat May 30 2020 liqingqing<liqignqing3@huawei.com> - 2.28-40
- Fix array overflow in backtrace on PowerPC (bug 25423) 

* Thu May 28 2020 jdkboy<guoge1@huawei.com> - 2.28-39
- Disable compilation warnings temporarily

* Tue Apr 28 2020 liqingqing<liqignqing3@huawei.com> - 2.28-38
- Avoid ldbl-96 stack corruption from range reduction of pseudo-zero (bug 25487)

* Thu Apr 16 2020 wangbin<wangbin224@huawei.com> - 2.28-37
- backport Kunpeng patches

* Thu Mar 19 2020 yuxiangyang<yuxiangyang4@huawei.com> - 2.28-36
- fix build src.rpm error

* Fri Mar 13 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-35
- exclude conflict files about rpc

* Fri Mar 13 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-34
- enable obsolete rpc

* Tue Mar 10 2020 liqingqing<liqingqing3@huawei.com> - 2.28-33
- fix use after free in glob when expanding user bug

* Wed Feb 26 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-32
- remove aditional require for debugutils package

* Tue Jan 7 2020 Wang Shuo <wangshuo47@huawei.com> - 2.28-31
- Fix compile macro

* Mon Jan 6 2020 Wang Shuo <wangshuo47@huawei.com> - 2.28-30
- add obsoletes symbol for language

* Fri Dec 20 2019 liqingqing <liqingqing3@huawei.com> - 2.28-29
- remove country selection from tzselect
- fix some bugs https://sourceware.org/git/?p=glibc.git;a=commit;h=1df872fd74f730bcae3df201a229195445d2e18a
                https://sourceware.org/git/?p=glibc.git;a=commit;h=823624bdc47f1f80109c9c52dee7939b9386d708
                https://sourceware.org/git/?p=glibc.git;a=commit;h=bc10e22c90e42613bd5dafb77b80a9ea1759dd1b
                https://sourceware.org/git/?p=glibc.git;a=commit;h=6c29942cbf059aca47fd4bbd852ea42c9d46b71f
                https://sourceware.org/git/?p=glibc.git;a=commit;h=31effacee2fc1b327bedc9a5fcb4b83f227c6539
                https://sourceware.org/git/?p=glibc.git;a=commit;h=5b06f538c5aee0389ed034f60d90a8884d6d54de
                https://sourceware.org/git/?p=glibc.git;a=commit;h=57ada43c905eec7ba28fe60a08b93a52d88e26c1
                https://sourceware.org/git/?p=glibc.git;a=commit;h=e0e4c321c3145b6ac0e8f6e894f87790cf9437ce
                https://sourceware.org/git/?p=glibc.git;a=commit;h=182a3746b8cc28784718c8ea27346e97d1423945
                https://sourceware.org/git/?p=glibc.git;a=commit;h=02d8b5ab1c89bcef2627d2b621bfb35b573852c2
                https://sourceware.org/git/?p=glibc.git;a=commit;h=f59a54ab0c2dcaf9ee946df2bfee9d4be81f09b8
                https://sourceware.org/git/?p=glibc.git;a=commit;h=fefa21790b5081e5d04662a240e2efd18603ef86
                https://sourceware.org/git/?p=glibc.git;a=commit;h=2bd81b60d6ffdf7e0d22006d69f4b812b1c80513
                https://sourceware.org/git/?p=glibc.git;a=commit;h=a55541fd1c4774d483c2d2b4bd17bcb9faac62e7
                https://sourceware.org/git/?p=glibc.git;a=commit;h=b6d2c4475d5abc05dd009575b90556bdd3c78ad0
                https://sourceware.org/git/?p=glibc.git;a=commit;h=8a80ee5e2bab17a1f8e1e78fab5c33ac7efa8b29
                https://sourceware.org/git/?p=glibc.git;a=commit;h=c0fd3244e71db39cef1e2d1d8ba12bb8b7375ce4
- fix CVE-2016-10739 CVE-2019-19126 CVE-2019-6488
- add pie compile option for debug/Makefile and remove -static for build-locale-archive

* Fri Dec 20 2019 liusirui <liusirui@huawei.com> - 2.28-28
- Fix null pointer in mtrace

* Thu Nov 21 2019 mengxian <mengxian@huawei.com> - 2.28-27
- In x86, configure static pie and cet only with gcc 8 or above

* Wed Nov 13 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.28-26
- Optimized instructions for Kunpeng processor

* Fri Jan 18 2019 openEuler Buildteam <buildteam@openeuler.org> - 2.28-25
- Package init
