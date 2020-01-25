#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	Lexical
%define		pnam	Persistence
Summary:	Lexical::Persistence - Persistent lexical variable values for arbitrary calls.
Name:		perl-Lexical-Persistence
Version:	1.020
Release:	1
License:	GPL v1+ or Artistic
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/Lexical/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	22fc0a2486c6746bdd1a635f42889809
URL:		http://search.cpan.org/dist/Lexical-Persistence/
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
%if %{with tests}
BuildRequires:	perl-Devel-LexAlias >= 0.04
BuildRequires:	perl-PadWalker >= 1.1
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Lexical::Persistence does a few things, all related.  Note that all
the behaviors listed here are the defaults.  Subclasses can override
nearly every aspect of Lexical::Persistence's behavior.

Lexical::Persistence lets your code access persistent data through
lexical variables.  This example prints "some value" because the value
of $x perists in the $lp object between setter() and getter().

	use Lexical::Persistence;

	my $lp = Lexical::Persistence->new();
	$lp->call(\&setter);
	$lp->call(\&getter);

	sub setter { my $x = "some value" }
	sub getter { print my $x, "\n" }

Lexicals with leading underscores are not persistent.

By default, Lexical::Persistence supports accessing data from multiple
sources through the use of variable prefixes.  The set_context()
member sets each data source.  It takes a prefix name and a hash of
key/value pairs.  By default, the keys must have sigils representing
their variable types.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} pure_install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a eg $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README
%dir %{perl_vendorlib}/Lexical
%{perl_vendorlib}/Lexical/*.pm
%{_mandir}/man3/*
%{_examplesdir}/%{name}-%{version}
