%define     _disable_lto    1
%define     debug_package   %{nil}

%define     tslanguage  lua
%define     libname %mklibname tree-sitter-lua 
%define     devname %mklibname tree-sitter-lua 

Name:       %{libname} 
Version:    0.2.0 
Release:    1
SOURCE0:    https://github.com/tree-sitter-grammars/tree-sitter-lua/archive/v%{version}.tar.gz
Summary:    Tree-sitter LUA parser library   
URL:        https://github.com/tree-sitter-grammars/tree-sitter-lua
License:    MIT 
Group:      System/Libraries/C_C++

Provides:   %{libname} = %{EVRD}

%description
Tree-sitter LUA parser library

# ───────────────────────────────────────────────────────────────────────────── #
%package    static 

Summary:    Tree-sitter LUA parser static library 

%description static
Tree-sitter LUA parser static library

# ───────────────────────────────────────────────────────────────────────────── #

%package    devel
Summary:    Development files for %{name}
Requires:   %{libname} = %{EVRD}

%description devel
Development files (Headers etc.) for %{name}

# ───────────────────────────────────────────────────────────────────────────── #

%prep
%autosetup -C

# ───────────────────────────────────────────────────────────────────────────── #

%build
%make_build \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 


# ───────────────────────────────────────────────────────────────────────────── #

%install
%make_install \
        CC="%{__cc}" \
        CFLAGS="%{optflags}" \
        LDFLAGS="%{build_ldflags}" \
        PREFIX="%{_prefix}" \
        LIBDIR="%{_libdir}" 

install -d %{buildroot}%{_libdir}/tree_sitter


libs=$(ls "%{buildroot}%{_libdir}" | \
    sed "/libtree-sitter-%{tslanguage}[^.]*\.so\.[0-9][0-9]*$/!d")

# Create symlink in tree_sitter directory to be used by Neovim  
for lib in $libs; do
    shortname=$(echo "$lib" | sed "s/libtree-sitter-\(%{tslanguage}[^.]*\).*$/\1/")
    ln -s -r "%{buildroot}%{_libdir}/${lib}" \
        "%{buildroot}%{_libdir}/tree_sitter/${shortname}.so"
done



# ───────────────────────────────────────────────────────────────────────────── #

%files 
%{_libdir}/*.so.*
%{_libdir}/tree_sitter/*.so
%license  LICENSE*
%doc README*

# ───────────────────────────────────────────────────────────────────────────── #

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%license  LICENSE*
%doc    README*

# ───────────────────────────────────────────────────────────────────────────── #

%files static
%{_libdir}/libtree-sitter-lua*.a


