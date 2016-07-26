%global pkg_name easymock
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2009, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.2
Release:        22.7%{?dist}
Epoch:          0
Summary:        Easy mock objects
License:        MIT
URL:            http://www.easymock.org/
# cvs -d:pserver:anonymous@easymock.cvs.sourceforge.net:/cvsroot/easymock login
# cvs -z3 -d:pserver:anonymous@easymock.cvs.sourceforge.net:/cvsroot/easymock export -r EasyMock1_2_Java1_3 easymock
# tar czf easymock-1.2-src.tar.gz easymock
Source0:        easymock-1.2-src.tar.gz
Source1:        http://repo1.maven.org/maven2/easymock/easymock/1.2_Java1.5/easymock-1.2_Java1.5.pom
Source2:        easymock-component-info.xml
# Starting with version 2.5.1, EasyMock changed its license to Apache 2.
# Older versions are still available under MIT License
# See http://www.easymock.org/License.html
Source3:        LICENSE
Patch0:         easymock-1.2-build_xml.patch
Patch1:         %{pkg_name}-removed-test.patch
Patch2:         %{pkg_name}-removed-alltests.patch
BuildRequires:  %{?scl_prefix}javapackages-tools
BuildRequires:  %{?scl_prefix}ant >= 0:1.6
BuildRequires:  %{?scl_prefix}ant-junit >= 0:1.6
BuildRequires:  %{?scl_prefix}junit >= 0:3.8.1
BuildArch:      noarch

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style
of recording expectations, most refactorings will not affect the Mock Objects.
So EasyMock is a perfect fit for Test-Driven Development.

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p0
%patch1 -p1
%patch2 -p1
cp %{SOURCE3} .
mkdir lib
pushd lib
ln -sf $(build-classpath junit) .
popd

# We no longer ship a 1.3/1.4 VM, Set it to generic javahome
rm easymockbuild.properties
echo "java\ 1.3=%{java}" >> easymockbuild.properties
echo "java\ 1.4=%{java}" >> easymockbuild.properties
echo "java\ 1.5=%{java}" >> easymockbuild.properties
echo "java\ compiler=%{javac}" >> easymockbuild.properties
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export OPT_JAR_LIST="ant/ant-junit junit"
export CLASSPATH=
%{ant} -Dbuild.sysclasspath=first
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
unzip -qq %{pkg_name}%{version}_Java1.3.zip
install -dm 755 $RPM_BUILD_ROOT%{_javadir}

install -pm 644 %{pkg_name}%{version}_Java1.3/%{pkg_name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr %{pkg_name}%{version}_Java1.3/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# pom
install -dm 755 $RPM_BUILD_ROOT%{_mavenpomdir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_mavenpomdir}/JPP-%{pkg_name}.pom
%add_maven_depmap
%{?scl:EOF}


%files
%doc LICENSE
%doc %{pkg_name}%{version}_Java1.3/{Documentation,License}.html
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*
%{_javadir}/%{pkg_name}.jar

%files javadoc
%doc LICENSE
%{_javadocdir}/%{name}

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:1.2-22.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-22.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.2-22
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-21
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Mon Feb 18 2013 Tomas Radej <tradej@redhat.com> - 0:1.2-20
- Fixed sources (bz #905973)

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 27 2012 Tomas Radej <tradej@redhat.com> - 0:1.2-18
- Removed ownership of _mavenpomdir

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.2-17
- Add LICENSE file
- Remove rpm bug workaround
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Tomas Radej <tradej@redhat.com> - 0:1.2-15
- Removed test

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 0:1.2-12
- Fix pom filename (Resolves rhbz#655795)
- Remove clean section and buildroot declaration
- Remove versioned jars and pom files

* Thu Aug 20 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-11
- Bump release for rebuild.

* Thu Aug 20 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.2-10
- Disable tests.

* Mon May 18 2009 Fernando Nasser <fnasser@redhat.com> 0:1.2-9
- Update instructions for obtaining source tar ball

* Mon May 04 2009 Yong Yang <yyang@redhat.com> 0:1.2-8
- Rebuild with maven2-2.0.8 built in non-bootstrap mode

* Wed Mar 18 2009 Yong Yang <yyang@redhat.com>  0:1.2-7
- merge from JPP-6
- rebuild with new maven2 2.0.8 built in bootstrap mode

* Mon Feb 02 2009 David Walluck <dwalluck@redhat.com> 0:1.2-6
- fix component-info.xml

* Mon Feb 02 2009 David Walluck <dwalluck@redhat.com> 0:1.2-5
- remove unneeded maven flag

* Mon Feb 02 2009 David Walluck <dwalluck@redhat.com> 0:1.2-4
- add repolib

* Fri Jan 30 2009 Will Tatam <will.tatam@red61.com> 1.2-3.jpp5
- Inital JPP-5 Build

* Fri Jan 09 2009 Yong Yang <yyang@redhat.com> 1.2-2jpp.1
- Imported from dbhole's maven 2.0.8 packages, initial building on jpp6

* Fri Apr 11 2008 Deepak Bhole <dbhole@redhat.com> 1.2-1jpp.1
- Import from JPackage
- Add pom file

* Fri Feb 24 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.2-1jpp
- Update to 1.2 keeping only java 1.4 requirement

* Fri Feb 24 2006 Ralph Apel <r.apel at r-apel.de> - 0:1.1-3jpp
- drop java-1.3.1 requirement

* Mon Oct 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1-2jpp
- Fixed Url, Summary, Description and License

* Mon Oct 04 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.1-1jpp
- First JPackage release
