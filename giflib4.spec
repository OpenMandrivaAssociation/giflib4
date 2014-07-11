%define major 4
%define	libname	%mklibname gif %{major}
%define	libungif %mklibname ungif %{major}
%define	devname	%mklibname -d gif

Summary:	Compatibility library for applications using an older version of giflib
Name:		giflib4
Version:	4.2.1
Release:	8
Group:		System/Libraries
License:	BSD like
Url:		http://giflib.sourceforge.net/
Source0:	http://switch.dl.sourceforge.net/project/giflib/giflib-4.x/giflib-%{version}.tar.bz2
Patch1:		giflib-4.1.6-fix-link.patch
Patch2:		giflib-4.2.1-automake-1.13.patch
BuildRequires:	pkgconfig(x11)
BuildRequires:	xmlto

%track
prog %{name} = {
	url = http://sourceforge.net/projects/giflib/files/giflib-4.x/
	regex = %{name}-(__VER__)\.tar\.bz2
	version = %{version}
}

%description
giflib is a library for reading and writing gif images. It is API and
ABI compatible with libungif which was in wide use while the LZW
compression algorithm was patented.

This package provides an older version of giflib for compatibility.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Library for reading and writing gif images (old version)

%description -n	%{libname}
giflib is a library for reading and writing gif images. It is API and
ABI compatible with libungif which was in wide use while the LZW
compression algorithm was patented.

This package provides an older version of giflib for compatibility.

%package -n	%{libungif}
Group:		System/Libraries
Summary:	Library for reading and writing gif images (old version)
Conflicts:	%{_lib}gif4 < 4.1.6-12

%description -n	%{libungif}
giflib is a library for reading and writing gif images. It is API and
ABI compatible with libungif which was in wide use while the LZW
compression algorithm was patented.

This package provides an older version of giflib for compatibility.

%prep
%setup -q -n giflib-%{version}
%patch1 -p0
%patch2 -p1 -b .am13~
autoreconf -fi

%build
%configure2_5x \
	--disable-static

%make

# Handling of libungif compatibility
MAJOR=`echo '%{version}' | sed -e 's/\([0-9]\+\)\..*/\1/'`
%{__cc} %{ldflags} %{optflags} -shared -Wl,-soname,libungif.so.$MAJOR -Llib/.libs -lgif -o libungif.so.%{version}

%install
%makeinstall_std

# Handling of libungif compatibility
install -p -m 755 libungif.so.%{version} %{buildroot}%{_libdir}
ln -sf libungif.so.%{version} %{buildroot}%{_libdir}/libungif.so.4
ln -sf libungif.so.4 %{buildroot}%{_libdir}/libungif.so

# Remove anything but the library - people should get the tools and development
# files from giflib 5.x
rm -rf %{buildroot}%{_bindir} %{buildroot}%{_includedir} %{buildroot}%{_libdir}/*.so

%files -n %{libname}
%{_libdir}/libgif.so.%{major}*

%files -n %{libungif}
%{_libdir}/libungif.so.%{major}*

