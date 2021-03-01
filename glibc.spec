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
%bcond_without benchtests
%bcond_with bootstrap
%bcond_without werror
%bcond_without docs

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

%define enablekernel 3.2
%define target %{_target_cpu}-openEuler-linux
%ifarch %{arm}
%define target %{_target_cpu}-openEuler-linuxeabi
%endif
%define x86_arches %{ix86} x86_64
%define all_license LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL
%define GCC gcc
%define GXX g++
##############################################################################
# glibc - The GNU C Library (glibc) core package.
##############################################################################
Name: 	 	glibc
Version: 	2.28
Release: 	53
Summary: 	The GNU libc libraries
License:	%{all_license}
URL: 		http://www.gnu.org/software/glibc/

Source0:   https://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Source1:   build-locale-archive.c
Source2:   nscd.conf
Source3:   nsswitch.conf
Source4:   bench.mk
Source5:   glibc-bench-compare
Source6:   LicenseList
Source7:   LanguageList

Patch0: Fix-use-after-free-in-glob-when-expanding-user-bug-2.patch
Patch1: backport-Kunpeng-patches.patch
Patch2: Avoid-ldbl-96-stack-corruption-from-range-reduction-.patch 
Patch3: backport-CVE-2020-1751-Fix-array-overflow-in-backtrace-on-PowerPC-bug-25423.patch  
Patch4: Do-not-use-gettimeofday-in-random-id.patch
Patch5: Reset-converter-state-after-second-wchar_t-output-Bu.patch
Patch6: Fix-avx2-strncmp-offset-compare-condition-check-BZ-2.patch
Patch7: nptl-wait-for-pending-setxid-request-also-in-detache.patch
Patch8: x86-64-Use-RDX_LP-on-__x86_shared_non_temporal_thres.patch
Patch9: x86_64-Use-xmmN-with-vpxor-to-clear-a-vector-registe.patch
Patch10: nptl-Don-t-madvise-user-provided-stack.patch
Patch11: turn-REP_STOSB_THRESHOLD-from-2k-to-1M.patch
Patch12: Fix-strtod-multiple-precision-division-bug-bug-26137.patch
Patch13: Fix-double-free-in-__printf_fp_l-bug-26214.patch
Patch14: Fix-memory-leak-in-__printf_fp_l-bug-26215.patch
Patch15: Fix-CVE-2020-6096-001.patch
Patch16: Fix-CVE-2020-6096-002.patch
Patch17: backport-Correct-locking-and-cancellation-cleanup-in-syslog-functions.patch
Patch18: makedb-fix-build-with-libselinux-3.1.patch
Patch19: Workaround-deprecation-warnings-introduced-in-libselinux-3.1.patch
Patch20: backport-0001-Fix-handling-of-collating-symbols-in-fnmatch-bug-266.patch
Patch21: backport-sysvipc-Fix-SEM_STAT_ANY-kernel-argument-pass-BZ-26637.patch
Patch22: backport-i686-tst-strftime3-fix-printf-warning.patch
Patch23: Fix-CVE-2020-27618-iconv-Accept-redundant-shift-sequences.patch
Patch24: backport-x86-Use-one-ldbl2mpn.c-file-for-both-i386-and-x86_64.patch
Patch25: backport-Fix-CVE-2020-29573-x86-Harden-printf-against-non-normal-long-double-val.patch
Patch26: backport-Fix-iconv-buffer-handling-with-IGNORE-error-handler-.patch
Patch27: backport-CVE-2020-29562-iconv-Fix-incorrect-UCS4-inner-loop-bounds-BZ-26923.patch
Patch28: backport-aarch64-fix-stack-missing-after-sp-is-updated.patch
Patch29: backport-aarch64-push-the-set-of-rules-before-falling-into-sl.patch
Patch30: backport-Fix-buffer-overrun-in-EUC-KR-conversion-module-bz-24.patch
Patch31: backport-addmntent-Remove-unbounded-alloca-usage-from-getmnte.patch
Patch32: backport-Use-O_CLOEXEC-in-sysconf-BZ-26791.patch
Patch33: backport-aarch64-Add-unwind-information-to-_start-bug-26853.patch
Patch34: disable-threads-in-Intel-vm-environment.patch
Patch35: backport-aarch64-revert-memcpy-optimze-for-kunpeng-to-avoid-p.patch

Provides: ldconfig rtld(GNU_HASH) bundled(gnulib)

BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
BuildRequires: procps-ng, util-linux, gawk, systemtap-sdt-devel, systemd, python3
BuildRequires: make >= 4.0, bison >= 2.7, binutils >= 2.30-17, gcc >= 7.2.1-6
BuildRequires: m4 gcc_secure gdb

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
Requires(pre): basesystem

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
for line in io.lines(rpm.expand("%{SOURCE7}")) do
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
# glibc "devel" sub-package
##############################################################################
%package devel
Summary:  The devel for %{name}
Requires: %{name} = %{version}-%{release}
Requires: libgcc%{_isa}
Requires(pre): info
Requires(pre): kernel-headers
Requires: kernel-headers >= 2.2.1
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
# glibc "nscd" sub-package
##############################################################################
%package -n nscd
Summary:  Name caching service daemon.
Requires: %{name} = %{version}-%{release}
%if %{without bootstrap}
Requires: libselinux >= 1.17.10-1
%endif
Requires: audit-libs >= 1.1.3
Requires(pre): shadow-utils, coreutils
Requires: systemd
Requires(postun): shadow-utils

%description -n nscd
The nscd package is able to daemon caches name service lookups and improve
the performance with LDAP.

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
# glibc debuginfo sub-package
##############################################################################
%if 0%{?_enable_debug_packages}
%define debug_package %{nil}
%define __debug_install_post %{nil}
%global __debug_package 1

%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%undefine _unique_debug_names
%undefine _unique_debug_srcs

%package debuginfo
Summary: Debug information for %{name}
AutoReqProv: no

%description debuginfo
This package provides debug information for package %{name}.
Debug information is useful when developing applications that use this
package or when debugging this package.

%package debugsource
Summary: Debug source for %{name}
AutoReqProv: no

%description debugsource
This package provides debug sources for package %{name}.
Debug sources are useful when developing applications that use this
package or when debugging this package.

%endif # 0%{?_enable_debug_packages}

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
%ifarch %{x86_arches}
%if 0%{?gcc_version} >= 8
	--enable-static-pie \
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
	||
	{ cat config.log; false; }

make %{?_smp_mflags} -O -r %{glibc_make_flags}
popd

##############################################################################
# Install glibc...
##############################################################################
%install
chmod 644 sysdeps/gnu/errlist.c

%ifarch riscv64
for d in $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT/%{_lib}; do
	mkdir -p $d
	(cd $d && ln -sf . lp64d)
done
%endif

make -j1 install_root=$RPM_BUILD_ROOT install -C build-%{target}

pushd build-%{target}

# notice: we can't use parallel compilation because the localedata will use "localedef" command
# to create locales such as LC_CTYPE, LC_TIME etc, and this command will create a file,
# or create a hard link if there already has a output file who's input is the same,
# so when we use parallel compilation, it will lead to different results, and this will cause BEP inconsistence.
make -j1 install_root=$RPM_BUILD_ROOT \
	install-locales -C ../localedata objdir=`pwd`
popd

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
        --prefix $RPM_BUILD_ROOT --add-to-archive \
        *_*
# Setup the locale-archive template for use by glibc-all-langpacks.
mv locale-archive{,.tmpl}
%{find_lang} libc
popd
mv  $RPM_BUILD_ROOT%{_prefix}/lib/locale/libc.lang .

# Install configuration files for services
install -p -m 644 %{SOURCE3} $RPM_BUILD_ROOT/etc/nsswitch.conf

mkdir -p $RPM_BUILD_ROOT/etc/default
install -p -m 644 nis/nss $RPM_BUILD_ROOT/etc/default/nss

# This is for ncsd - in glibc 2.2
install -m 644 nscd/nscd.conf $RPM_BUILD_ROOT/etc
mkdir -p $RPM_BUILD_ROOT%{_tmpfilesdir}
install -m 644 %{SOURCE2} %{buildroot}%{_tmpfilesdir}
mkdir -p $RPM_BUILD_ROOT/lib/systemd/system
install -m 644 nscd/nscd.service nscd/nscd.socket $RPM_BUILD_ROOT/lib/systemd/system

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > $RPM_BUILD_ROOT/etc/ld.so.conf
truncate -s 0 $RPM_BUILD_ROOT/etc/ld.so.cache
chmod 644 $RPM_BUILD_ROOT/etc/ld.so.conf
mkdir -p $RPM_BUILD_ROOT/etc/ld.so.conf.d
mkdir -p $RPM_BUILD_ROOT/etc/sysconfig
truncate -s 0 $RPM_BUILD_ROOT/etc/sysconfig/nscd
truncate -s 0 $RPM_BUILD_ROOT/etc/gai.conf

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache
chmod 644 $RPM_BUILD_ROOT%{_libdir}/gconv/gconv-modules.cache

# Install the upgrade program
install -m 700 build-%{target}/elf/glibc_post_upgrade \
  $RPM_BUILD_ROOT%{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

# Install debug copies of unstripped static libraries
%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}
cp -a $RPM_BUILD_ROOT%{_libdir}/*.a \
	$RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/
rm -f $RPM_BUILD_ROOT%{_prefix}/lib/debug%{_libdir}/*_p.a
%endif

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/zoneinfo

touch -r %{SOURCE0} $RPM_BUILD_ROOT/etc/ld.so.conf
touch -r sunrpc/etc.rpc $RPM_BUILD_ROOT/etc/rpc

pushd build-%{target}
%GCC -Os -g -o build-locale-archive %{SOURCE1} \
    ../build-%{target}/locale/locarchive.o \
    ../build-%{target}/locale/md5.o \
    ../build-%{target}/locale/record-status.o \
    -I. -DDATADIR=\"%{_datadir}\" -DPREFIX=\"%{_prefix}\" \
    -L../build-%{target} \
    -B../build-%{target}/csu/ -lc -lc_nonshared \
    -Wl,-dynamic-linker=/lib64/ld-%{version}.so \
    -Wl,-rpath-link=.:./math:./elf:./dlfcn:./nss:./rt:./resolv:./mathvec:./support:./nptl libc.so.6 libc_nonshared.a \
    -Wl,--as-needed $olddir/build-%{target}/elf/ld.so
install -m 700 build-locale-archive $RPM_BUILD_ROOT%{_prefix}/sbin/build-locale-archive
popd

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
for b in %{SOURCE4} %{SOURCE5}; do
	cp $b $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
done

#comparison scripts.
for i in benchout.schema.json compare_bench.py import_bench.py validate_benchout.py; do
	cp benchtests/scripts/$i $RPM_BUILD_ROOT%{_prefix}/libexec/glibc-benchtests/
done

%if 0%{?_enable_debug_packages}
pushd locale
ln -s programs/*.gperf .
popd

pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

%if %{with docs}
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%endif

truncate -s 0 $RPM_BUILD_ROOT/%{_prefix}/lib/locale/locale-archive
mkdir -p $RPM_BUILD_ROOT/var/{db,run}/nscd
touch $RPM_BUILD_ROOT/var/{db,run}/nscd/{passwd,group,hosts,services}
touch $RPM_BUILD_ROOT/var/run/nscd/{socket,nscd.pid}

mkdir -p $RPM_BUILD_ROOT%{_libdir}
mv -f $RPM_BUILD_ROOT/%{_lib}/lib{pcprofile,memusage}.so \
	$RPM_BUILD_ROOT%{_libdir}

# Strip all of the installed object files.
strip -g $RPM_BUILD_ROOT%{_libdir}/*.o

# Rebuild libpthread.a using --whole-archive to ensure all of libpthread
# is included in a static link.
pushd $RPM_BUILD_ROOT%{_prefix}/%{_lib}/
%GCC -r -nostdlib -o libpthread.o -Wl,--whole-archive ./libpthread.a
rm libpthread.a
ar rcs libpthread.a libpthread.o
rm libpthread.o
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
touch nscd.filelist
touch nss_modules.filelist
touch nss-devel.filelist
touch libnsl.filelist
touch debugutils.filelist
touch benchtests.filelist
touch debuginfo.filelist

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
      -e '\,.*/%{_libdir}/lib\(pcprofile\|memusage\)\.so,d' \
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
    -e 'nscd' \
    -e '%{_prefix}/bin' \
    -e '%{_prefix}/lib/locale' \
    -e '%{_prefix}/sbin/[^gi]' \
    -e '%{_prefix}/share' \
    -e '/var/db/Makefile' \
    -e '/libnss_.*\.so[0-9.]*$' \
    -e '/libnsl' \
    -e 'glibc-benchtests' \
    -e 'aux-cache' \
    -e 'build-locale-archive' \
    > glibc.filelist

for module in compat files dns; do
    cat master.filelist \
    | grep -E \
    -e "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    >> glibc.filelist
done
grep -e "libmemusage.so" -e "libpcprofile.so" master.filelist >> glibc.filelist

##############################################################################
# glibc "common" sub-package
##############################################################################
grep '%{_prefix}/bin' master.filelist > common.filelist
grep '%{_prefix}/sbin/[^gi]' master.filelist \
	| grep -v 'nscd' >> common.filelist

grep '%{_prefix}/share' master.filelist \
	| grep -v \
	-e '%{_prefix}/share/info/libc.info.*' \
	-e '%%dir %{prefix}/share/info' \
	-e '%%dir %{prefix}/share' \
	>> common.filelist

echo '%{_prefix}/sbin/build-locale-archive' >> common.filelist

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

sed -i -e '\,libmemusage.so,d' \
    -e '\,libpcprofile.so,d' \
    -e '\,/libnss_[a-z]*\.so$,d' \
    devel.filelist

grep '%{_prefix}/include' < master.filelist >> devel.filelist

grep '%{_libdir}/lib.*\.a' < master.filelist \
  | grep -v '/lib\(\(c\|pthread\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\)\.a$' \
  >> devel.filelist


##############################################################################
# glibc "nscd" sub-package
##############################################################################
echo '%{_prefix}/sbin/nscd' > nscd.filelist

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
grep '/libnsl-[0-9.]*.so$' master.filelist > libnsl.filelist
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

##############################################################################
# glibc benchtests sub-package
##############################################################################
find build-%{target}/benchtests -type f -executable | while read b; do
    echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done > benchtests.filelist
# ... and the makefile.
for b in %{SOURCE4} %{SOURCE5}; do
    echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done
# ... and finally, the comparison scripts.
echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif # 0%{?_enable_debug_packages}

##############################################################################
# glibc debuginfo sub-package
##############################################################################
touch debuginfo_additional.filelist
find_debuginfo_args='--strict-build-id -i'
%ifarch %{x86_arches}
find_debuginfo_args="$find_debuginfo_args \
    -l common.filelist \
    -l debugutils.filelist \
    -l nscd.filelist \
    -p '.*/(sbin|libexec)/.*' \
    -o debuginfo_additional.filelist \
    -l nss_modules.filelist \
    -l libnsl.filelist \
    -l glibc.filelist \
%if %{with benchtests}
    -l benchtests.filelist
%endif
    "
%endif

/usr/lib/rpm/find-debuginfo.sh $find_debuginfo_args -o debuginfo.filelist

%ifarch %{x86_arches}
sed -i '\#^$RPM_BUILD_ROOT%{_prefix}/src/debug/#d' debuginfo_additional.filelist
cat debuginfo_additional.filelist >> debuginfo.filelist
find $RPM_BUILD_ROOT%{_prefix}/src/debug \
     \( -type d -printf '%%%%dir ' \) , \
     -printf '%{_prefix}/src/debug/%%P\n' >> debuginfo.filelist

add_dir=%{_prefix}/lib/debug%{_libdir}
find $RPM_BUILD_ROOT$add_dir -name "*.a" -printf "$add_dir/%%P\n" >> debuginfo.filelist
%endif # %{x86_arches}

remove_dir="%{_prefix}/src/debug"
remove_dir="$remove_dir $(echo %{_prefix}/lib/debug{,/%{_lib},/bin,/sbin})"
remove_dir="$remove_dir $(echo %{_prefix}/lib/debug%{_prefix}{,/%{_lib},/libexec,/bin,/sbin})"

for d in $(echo $remove_dir | sed 's/ /\n/g'); do
    sed -i "\|^%%dir $d/\?$|d" debuginfo.filelist
done
%endif # %{with benchtests}
##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}
# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
make %{?_smp_mflags} -O check |& tee rpmbuild.check.log >&2
test -n tests.sum
if ! grep -q '^Summary of test results:$' rpmbuild.check.log ; then
  echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
  exit 1
fi
set +x
grep -v ^PASS: tests.sum > rpmbuild.tests.sum.not-passing || true
if test -n rpmbuild.tests.sum.not-passing ; then
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

%post -p %{_prefix}/sbin/glibc_post_upgrade.%{_target_cpu}

%posttrans common -e -p <lua>
if posix.stat("%{_prefix}/lib/locale/locale-archive.tmpl", "size") > 0 then
  pid = posix.fork()
  if pid == 0 then
    posix.exec("%{_prefix}/sbin/build-locale-archive", "--install-langs", "%%{_install_langs}")
  elseif pid > 0 then
    posix.wait(pid)
  end
end

%postun common -p <lua>
os.remove("%{_prefix}/lib/locale/locale-archive")

%pre devel
# this used to be a link and it is causing nightmares now
if [ -L %{_prefix}/include/scsi ] ; then
  rm -f %{_prefix}/include/scsi
fi

%if %{with docs}
%post devel
/sbin/install-info %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :

%preun devel
if [ "$1" = 0 ]; then
  /sbin/install-info --delete %{_infodir}/libc.info.gz %{_infodir}/dir > /dev/null 2>&1 || :
fi
%endif

%pre -n nscd
getent group nscd >/dev/null || /usr/sbin/groupadd -g 28 -r nscd
getent passwd nscd >/dev/null ||
  /usr/sbin/useradd -M -o -r -d / -s /sbin/nologin \
		    -c "NSCD Daemon" -u 28 -g nscd nscd

%post -n nscd
%systemd_post nscd.service

%preun -n nscd
%systemd_preun nscd.service

%postun -n nscd
if test $1 = 0; then
  /usr/sbin/userdel nscd > /dev/null 2>&1 || :
fi
%systemd_postun_with_restart nscd.service

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
%attr(0644,root,root) %verify(not md5 size mtime) %{_prefix}/lib/locale/locale-archive.tmpl
%attr(0644,root,root) %verify(not md5 size mtime mode) %ghost %config(missingok,noreplace) %{_prefix}/lib/locale/locale-archive
%dir %{_prefix}/lib/locale
%dir %{_prefix}/lib/locale/C.utf8
%{_prefix}/lib/locale/C.utf8/*
%{_prefix}/lib/locale/zh_CN.utf8
%{_prefix}/lib/locale/en_US.utf8
%{_prefix}/share/locale/zh_CN
%{_prefix}/share/locale/en_GB
%dir %attr(755,root,root) /etc/default
%verify(not md5 size mtime) %config(noreplace) /etc/default/nss

%files -f libc.lang all-langpacks
%{_prefix}/lib/locale
%exclude %{_prefix}/lib/locale/locale-archive
%exclude %{_prefix}/lib/locale/locale-archive.tmpl
%exclude %{_prefix}/lib/locale/C.utf8
%exclude %{_prefix}/lib/locale/zh_CN.utf8
%exclude %{_prefix}/lib/locale/en_US.utf8
%exclude %{_prefix}/share/locale/zh_CN
%exclude %{_prefix}/share/locale/en_GB

%files locale-source
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files -f devel.filelist devel

%files -f nscd.filelist -n nscd
%config(noreplace) /etc/nscd.conf
%dir %attr(0755,root,root) /var/run/nscd
%dir %attr(0755,root,root) /var/db/nscd
/lib/systemd/system/nscd.service
/lib/systemd/system/nscd.socket
%{_tmpfilesdir}/nscd.conf
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/nscd.pid
%attr(0666,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/socket
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/run/nscd/services
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/passwd
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/group
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/hosts
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/db/nscd/services
%ghost %config(missingok,noreplace) /etc/sysconfig/nscd

%files -f nss_modules.filelist -n nss_modules
/var/db/Makefile

%files -f nss-devel.filelist nss-devel

%files -f libnsl.filelist -n libnsl
/%{_lib}/libnsl.so.1

%files -f debugutils.filelist debugutils

%if %{with benchtests}
%files -f benchtests.filelist benchtests
%endif

%if 0%{?_enable_debug_packages}
%files -f debuginfo.filelist debuginfo

%files debugsource
%endif

%files help
#Doc of glibc package
%doc README NEWS INSTALL elf/rtld-debugger-interface.txt
#Doc of common sub-package
%doc documentation/README.timezone
%doc documentation/gai.conf
#Doc of nss_modules sub-package
%doc hesiod/README.hesiod

%changelog
* Fri Jan 22 2021 Qingqing Li<liqingqing3@huawei.com> - 2.28-53
- revert memcpy optimze for kunpeng to avoid performance regression when input large than kbyte. 

* Thu Jan 21 2021 Wang Shuo<wangshuo_1994@foxmail.com> - 2.28-52
- Disable threads in Intel vm environment to avoid performance degradation

* Thu Jan 7 2021 Qingqing Li<liqingqing3@huawei.com> - 2.28-51
- Fix bug 26791: Use O_CLOEXEC in sysconf
  bugzilla link: https://sourceware.org/bugzilla/show_bug.cgi?id=26791
- Fix bug 26853: aarch64: Add unwind information to _start
  bugzilla link: https://sourceware.org/bugzilla/show_bug.cgi?id=26853

* Wed Jan 6 2021 Wang Shuo<wangshuo_1994@foxmail.com> - 2.28-50
- Fix stack missing in _dl_tlsdesc_dynamic
  Fix buffer overrun in EUC-KR conversion module (bz #24973)
  Remove unbounded alloca usage from getmntent [BZ#27083]
  https://sourceware.org/pipermail/libc-alpha/2021-January/121272.html
  https://sourceware.org/pipermail/libc-alpha/2021-January/121330.html
  https://sourceware.org/bugzilla/show_bug.cgi?id=24973
  https://sourceware.org/bugzilla/show_bug.cgi?id=27083

* Mon Dec 21 2020 Wang Shuo<wangshuo_1994@foxmail.com> - 2.28-49
- Fix CVE-2020-29562, Fix incorrect UCS4 inner loop bounds (BZ#26923)
  https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-29562
  https://sourceware.org/bugzilla/show_bug.cgi?id=26923

* Thu Dec 17 2020 Wang Shuo <wangshuo_1994@foxmail.com> - 2.28-48
- Fix CVE-2020-29573, Harden printf against non-normal long double values
  https://cve.mitre.org/cgi-bin/cvename.cgi?name=2020-29573
  https://sourceware.org/bugzilla/show_bug.cgi?id=26649

* Tue Nov 10 2020 liusirui<liusirui@huawei.com> - 2.28-47
- Fix CVE-2020-27618, iconv accept redundant shift sequences in IBM1364 [BZ #26224]
  https://sourceware.org/bugzilla/show_bug.cgi?id=26224

* Tue Oct 27 2020 Qingqing Li <liqingqing3@huawei.com> - 2.28-46
- fix handling of collating symbols in fnmatch.
  upstream link is: https://sourceware.org/bugzilla/show_bug.cgi?id=26620
- fix SEM_STAT_ANY kernel argument pass.
  upstream link is: https://sourceware.org/bugzilla/show_bug.cgi?26637
- fix i686 test-strftime3.c compile warning.

* Tue Sep 22 2020 zhaowei<zhaowei23@huawei.com> - 2.28-45
- fix bug 965941: fix build with libselinux >= 3.1 
- origin bugzilla link is https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=965941

* Tue Sep 12 2020 liqingqing_1229<liqingqing3@huawei.com> - 2.28-44
- fix bug 26100: correct locking and cancellation cleanup in syslog functions. 
- origin bugzilla link is https://sourceware.org/bugzilla/show_bug.cgi?id=26100

* Mon Jul 20 2020 liqingqing<liqingqing3@huawei.com> - 2.28-43
- fix CVE-2020-6096
- fix bugzilla 26137, 26214, 26215

* Mon Jul 6 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-42
- disable rpc, it has been splited to libnss and libtirpc

* Mon Jul 6 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-41
- add zh and en to LanguageList

* Fri Jul 3 2020 Wang Shuo<wangshuo47@huawei.com> - 2.28-40
- add filelist to improve the scalability
- disable DEBUG for performence
- disable parallel compilation for locale
- backport many patch for bugfix:
- User provided stack should not be released nor madvised at thread exit
- removes the HP_TIMING_BITS usage for fast random bits
- reset the state a-vector-registe fter outputting the second whcar_t characte(Bug 25734)
- implement avx2 offset check condition for strncmp function[BZ #25933]
- bugfix for __nptl_setxid and exiting detached thread(bug 25942)
- use RDX_LP to compare against __x86_shared_non_temporal_threshold in assembly code[BZ #25966]
- Since "vpxor %xmmN, %xmmN, %xmmN" clears the whole vector register
- To improve the performance of memset

* Sat May 30 2020 liqingqing<liqignqing3@huawei.com> - 2.28-39
- Fix array overflow in backtrace on PowerPC (bug 25423) 

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
