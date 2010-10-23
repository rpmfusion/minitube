Name:           minitube
Version:        1.2
Release:        2%{?dist}
Summary:        A YouTube desktop client

Group:          Applications/Multimedia

# License info:
###
# LGPLv2.1 with exceptions or GPLv3:
# src/iconloader/qticonloader.h
# src/iconloader/qticonloader.cpp
# src/searchlineedit.h
# src/searchlineedit.cpp
#
# LGPLv2 with exceptions or GPLv3:
# src/urllineedit.h 
# src/urllineedit.cpp
#
# GPLv2 or GPLv3:
# src/flickcharm.cpp 
# src/flickcharm.h
#
# LGPLv2.1:
# src/minisplitter.h 
# src/minisplitter.cpp
#
# All other files are GPLv3+ as per INSTALL file
###
# End Of License info.

# The source files combined together into minitube binary are GPLv3, and the .qm files are GPLv3+
License:        GPLv3 and GPLv3+
URL:            http://flavio.tordini.org/minitube
Source0:        http://flavio.tordini.org/files/%{name}/%{name}-%{version}.tar.gz

# fixes requirement on bundled qtsingleapplication
Patch0:         minitube-qtsingleapp.patch

# fix breakage caused by qtsingleapplication-add-api.patch
# Patch1:         minitube-QString.patch
# name the lang files
Patch2:         minitube-lang.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%{?_qt4_version:Requires: qt4 >= %{_qt4_version}}

BuildRequires:  qt4-devel
BuildRequires:  desktop-file-utils
BuildRequires:  phonon-devel
BuildRequires:  qtsingleapplication-devel
Requires:       hicolor-icon-theme
Requires:       xine-lib-extras-freeworld


%description
Minitube is a YouTube desktop client.
With it you can watch YouTube videos in a new way:
you type a keyword, Minitube gives you an endless video stream.
Minitube is not about cloning the original YouTube web interface,
it aims to create a new TV-like experience.

%prep
%setup -q -n %{name}

# Fix spurious-executable-perm
chmod -x src/*{h,cpp}

# remove bundled copy of qtsingleapplication
rm -rf src/qtsingleapplication

# rename latvian language code
mv locale/lat.ts locale/lv.ts


%patch0 -p 1

#%%patch1 -p 0

%patch2 -p1 -b .lang

%build
%{_qt4_qmake} PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install INSTALL_ROOT=%{buildroot}

desktop-file-install \
  --dir=%{buildroot}%{_datadir}/applications/ \
  --delete-original \
        %{buildroot}%{_datadir}/applications/%{name}.desktop


# find_lang magic:
%find_lang %{name} --all-name --with-qt

%clean
rm -rf %{buildroot}

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING LICENSE.LGPL CHANGES TODO INSTALL
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/locale

%changelog
* Sat Oct 23 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.2-2
- rebuild

* Sun Oct 13 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.2-1
- version 1.2
- QString patch dropped

* Sat Aug 21 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.1-8
- rebuilt

* Sun Aug 15 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-7
- drop minitube-QString.patch

* Wed Aug 11 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-6
- add BR qt4-devel
- use better naming for patches
- own directories
- sort license information

* Wed Aug 11 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-5
- add lang patch by Leigh Scott
- rename locale/lat.ts to locale/lv.ts

* Mon Aug 09 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-4
- add Req: xine-lib-extras-freeworld
- add license information
- add INSTALL file
- use %%find_lang + magic on locale files
- patch to use system qtsingleapplication
- del bundled qtsingleapplication

* Wed Aug 04 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-3
- add %%post %%postun %%posttrans as suggested by Leigh Scott
- validate desktop file
- remove Req: xine-lib-extras-freeworld
- add Req: desktop-file-utils

* Wed Aug 04 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-2
- add Req: xine-lib-extras-freeworld

* Sun Aug 01 2010 Magnus Tuominen <magnus.tuominen@gmail.com> - 1.1-1
- initial build
