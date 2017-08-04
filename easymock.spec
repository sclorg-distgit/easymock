%{?scl:%scl_package easymock}
%{!?scl:%global pkg_name %{name}}

Name:           %{?scl_prefix}easymock
Version:        3.4
Release:        4.2%{?dist}
Summary:        Easy mock objects
License:        ASL 2.0
URL:            http://www.easymock.org

Source0:        https://github.com/%{pkg_name}/%{pkg_name}/archive/%{pkg_name}-%{version}.tar.gz

Patch1:         0001-Port-to-maven-jar-plugin-3.0.0.patch
Patch2:         0002-Disable-android-support.patch
Patch3:         0003-Unshade-cglib-and-asm.patch
Patch4:         0004-Fix-OSGi-manifest.patch

BuildArch:      noarch

BuildRequires:  %{?scl_prefix}maven-local
BuildRequires:  %{?scl_prefix}mvn(cglib:cglib)
BuildRequires:  %{?scl_prefix}mvn(junit:junit)
BuildRequires:  %{?scl_prefix}mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.apache.maven.plugins:maven-remote-resources-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.codehaus.mojo:build-helper-maven-plugin)
BuildRequires:  %{?scl_prefix}mvn(org.objenesis:objenesis)
BuildRequires:  %{?scl_prefix}mvn(org.ow2.asm:asm)
# xmvn-builddep misses this:
BuildRequires:  %{?scl_prefix}mvn(org.apache:apache-jar-resource-bundle)

Provides:       %{name}3 = %{version}-%{release}

%description
EasyMock provides Mock Objects for interfaces in JUnit tests by generating
them on the fly using Java's proxy mechanism. Due to EasyMock's unique style
of recording expectations, most refactorings will not affect the Mock Objects.
So EasyMock is a perfect fit for Test-Driven Development.

%package javadoc
Summary:        Javadoc for %{pkg_name}

%description javadoc
Javadoc for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%pom_remove_plugin :maven-license-plugin

# remove android support
rm core/src/main/java/org/easymock/internal/Android*.java
rm core/src/test/java/org/easymock/tests2/ClassExtensionHelperTest.java
%pom_disable_module test-android
%pom_remove_dep :dexmaker core

# unbundle asm and cglib
%pom_disable_module test-nodeps
%pom_remove_plugin :maven-shade-plugin core

# missing test deps
%pom_disable_module test-integration
%pom_disable_module test-osgi

# remove some warning caused by unavailable plugin
%pom_remove_plugin org.codehaus.mojo:versions-maven-plugin

# retired
%pom_remove_plugin :maven-timestamp-plugin

# For compatibility reasons
%mvn_file ":easymock{*}" easymock@1 easymock3@1

# ssh not needed during our builds
%pom_xpath_remove pom:extensions

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%license core/LICENSE.txt

%files javadoc -f .mfiles-javadoc
%license core/LICENSE.txt

%changelog
* Thu Jun 22 2017 Michael Simacek <msimacek@redhat.com> - 3.4-4.2
- Mass rebuild 2017-06-22

* Wed Jun 21 2017 Java Maintainers <java-maint@redhat.com> - 3.4-4.1
- Automated package import and SCL-ization

* Thu Feb 23 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-4
- Add missing BR on apache-resource-bundles

* Tue Feb 07 2017 Michael Simacek <msimacek@redhat.com> - 3.4-3
- Remove useless license-plugin

* Wed Jun  1 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.4-2
- Fix OSGi manifest
- Resolves: rhbz#1341052

* Mon May 30 2016 Michael Simacek <msimacek@redhat.com> - 3.4-1
- Update to upstream version 3.4

* Mon May 30 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-5
- Port to maven-jar-plugin 3.0.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3.1-3
- Obsolete easymock2
- Resolves: rhbz#1172958

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 5 2015 Alexander Kurtakov <akurtako@redhat.com> 3.3.1-1
- Update to upstream 3.3.1 release.

* Sat Mar 07 2015 Michael Simacek <msimacek@redhat.com> - 3.3-2
- Remove retired maven-timestamp-plugin

* Tue Nov 25 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 3.3-1
- Update to upstream version 3.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 3.2-2
- Use Requires: java-headless rebuild (#1067528)

* Fri Aug 30 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:3.2-1
- Update to upstream version 3.2

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

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
