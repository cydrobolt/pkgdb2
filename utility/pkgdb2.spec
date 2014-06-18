%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from
%distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:           pkgdb2
Version:        1.11.1
Release:        2%{?dist}
Summary:        The Fedora package database

License:        GPLv2+
URL:            http://fedorahosted.org/pkgdb2/
Source0:        https://fedorahosted.org/releases/p/k/pkgdb2/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-flask
BuildRequires:  python-flask-wtf
BuildRequires:  python-wtforms
BuildRequires:  python-kitchen
BuildRequires:  python-fedora >= 0.3.33
BuildRequires:  python-fedora-flask >= 0.3.33
BuildRequires:  python-openid-teams
BuildRequires:  python-openid-cla
BuildRequires:  python-docutils
BuildRequires:  python-dateutil
BuildRequires:  python-dogpile-cache
BuildRequires:  python-mock
BuildRequires:  python-bugzilla
BuildRequires:  python-memcached
BuildRequires:  python-setuptools
BuildRequires:  python-blinker

# EPEL6
%if ( 0%{?rhel} && 0%{?rhel} == 6 )
BuildRequires:  python-sqlalchemy0.8
Requires:  python-sqlalchemy0.8
%else
BuildRequires:  python-sqlalchemy > 0.8
Requires:  python-sqlalchemy > 0.8
%endif

Requires:  python-alembic
Requires:  python-flask
Requires:  python-flask-wtf
Requires:  python-wtforms
Requires:  python-kitchen
Requires:  python-fedora >= 0.3.32.3-3
Requires:  python-fedora-flask
Requires:  python-docutils
Requires:  python-dateutil
Requires:  python-dogpile-cache
Requires:  python-bugzilla >= 1.1.0
Requires:  python-memcached
Requires:  python-setuptools
Requires:  mod_wsgi

%description
PackageDB is the package database for Fedora. It is the application handling who
is allowed to commit on the git of the Fedora packages, it also handles who is
the person getting the bugs on the Bugzilla and who get the notifications
for changes in the git, builds or bugs.

%prep
%setup -q

%build
%{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Install apache configuration file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/
install -m 644 utility/pkgdb2.conf $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/conf.d/pkgdb2.conf

# Install configuration file
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/pkgdb2
install -m 644 utility/pkgdb2.cfg.sample $RPM_BUILD_ROOT/%{_sysconfdir}/pkgdb2/pkgdb2.cfg

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/pkgdb2

# Install WSGI file
install -m 644 utility/pkgdb2.wsgi $RPM_BUILD_ROOT/%{_datadir}/pkgdb2/pkgdb2.wsgi

# Install the createdb script
install -m 644 createdb.py $RPM_BUILD_ROOT/%{_datadir}/pkgdb2/pkgdb2_createdb.py

# Install the pkgdb2_branch script
install -m 644 utility/pkgdb2_branch.py $RPM_BUILD_ROOT/%{_datadir}/pkgdb2/pkgdb2_branch.py

# Install the alembic files
cp -r alembic $RPM_BUILD_ROOT/%{_datadir}/pkgdb2/
install -m 644 utility/alembic.ini $RPM_BUILD_ROOT/%{_sysconfdir}/pkgdb2/alembic.ini

## Running the tests would require having flask >= 0.10 which is not present in
## epel6
#%check
#./runtests.sh

%files
%doc README.rst COPYING doc/
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pkgdb2.conf
%config(noreplace) %{_sysconfdir}/pkgdb2/pkgdb2.cfg
%config(noreplace) %{_sysconfdir}/pkgdb2/alembic.ini
%dir %{_sysconfdir}/pkgdb2/
%{_datadir}/pkgdb2/
%{python_sitelib}/pkgdb2/
%{python_sitelib}/%{name}*.egg-info


%changelog
* Wed Jun 18 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.11.1-2
- Test running the unit-tests at build time but doesn't work with EPEL6
- Bump requirement to python-sqlalchemy 0.8+

* Tue Jun 10 2014  Pierre-Yves Chibon <pingou@pingoured.fr> - 1.11.1-1
- Update to 1.11.1
- Fix the search to search all packages by default, including orphaned onces
- Fix bugzilla interaction
- Fix bugzilla notifications to not notify is the bug is assigned to someone
  else or to the new point of contact
- Hide the `Take package` button if the user is not logged in
- Mention /api/version in the API documentation
- Catch problem when interacting with bugzilla
- Fix searching pseudo-user while searching packagers
- Fix display in the package's page

* Wed Jun 04 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.11-1
- Update to 1.11
- DB change to the log table to allow deleting packages
- Add a button to completely delete a package from the database, admins only
- Fix displaying the action buttons on the package's page
- Keep the filtering parameters when browsing multiple pages
- Enhance unit-tests
- Add new api endpoint /api/packager/package/ which lists the packages related
  to the specified packager (just like the packager's page does)

* Fri May 30 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.10.1-1
- Update to 1.10.1
- CSS fixes on the package's page (min resolution: 1024x768)

* Fri May 30 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.10-1
- Update to 1.10
- Search for all packages on /api/packages just like it is in the UI
- Always include `acls` on the package representation even if the list is
  empty
- Redirect the user trying to take a package if no branches are orphaned
- Redirect the user that tries to drop some ACLs if that user does not have
  this acl on this branch or any branch
- Prevent anyone except pkgdb admins to retire a non-orphaned package
- Show packagers that are only watching packages (ie: pseudo-user)
- Fix the admins table in the package's page

* Tue May 27 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.9.2-1
- Update to 1.9.2
- Fix displaying the most recent package in the front page

* Tue May 27 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.9.1-1
- Update to 1.9.1
- Fix displaying the branches in the front page

* Tue May 27 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.9-1
- Update to 1.9
- Fix ordering of the branches in the packager view
- Fix ordering of the branches in the list packages view/search
- When updating multiple ACLs, do not fail the whole transaction if one fails
- Do not show the ``Manage the admins`` button if you are not an admin
- Do not show the ``Request Commit ACLs`` button if you are not logged in
- Split up the approved and pending admins
- Put the most recent packages added on the front page of the application
- Update the status_change field upon entry update
- Ensure there are no: user X change ACL Y from Z to Z
- Remove watchcommits and commit ACL owners from the bugzilla CC list
- Add possibility to see someone's ACL on EOL'd releases
- Adjust the title of the email sent

* Thu May 22 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.8.2-1
- Update to 1.8.2
- Fix redirection if someone calls an opensearch endpoints that does not exist
- Fix the link in the email sent

* Wed May 21 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.8.1-1
- Update 1.8.1
- Fix the reverse proxy

* Wed May 21 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.8-1
- Update to 1.8
- Return the critpath status of a package in a collection in the API
- Drop the version from the front page
- Search all packages by default and set a drop-down list to filter by their
  status
- Fix the https redirection by setting pkgdb2 as a reverse proxied application
- Add browser opensearch extension
- Restrict retiring package from the UI to pkgdb admins
- Do not show the pagination block if there is only one page
  (Thanks to Michael Haynes)
- Improve the subject of the emails sent
- Do not update ACL if the ACL already has this status
- Add link to the package's page at the bottom of the emails sent
- Adjust the label of the 'Manage the committers' per person

* Mon May 19 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.7-1
- Update to 1.7
- Fix the pagination in the log viewer
- Allow to filters the logs per user/packager
- Update the logic for the API/bugzilla endpoint
- Allow admin to retire package on multiple branches
- Only show the branches people are allowed to retire package in in the UI
- Have a pop-up for the main buttons (Watch/Unwatch, Request/Drop) for
  confirmation
- Use forms/POST requests for the main buttons allowing CSRF protection
  fixes https://fedorahosted.org/fedora-infrastructure/ticket/4368
- Only give up commit ACL on branches where the user had them
- Add python-alembic as Requires
- Make sure the page is always greater than 0, otherwise we end up with a
  negative offset

* Fri May 16 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.6-1
- Bump to 1.6
- Layout fixes
- When giving a package only allow existing branches
- Typo in the API doc
- Link to upstream website and the packages application
- Fix the category settings when doing a search
- Default search is '*' (instead of 'a*')
- Rewrite the get_pending_acl and order the results

* Fri May 16 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.5-1
- Bump to 1.5
- Drop the shouldopen field of the Package table
- Fix the message in the logs/emails to say to whom the acl was updated for
- s/poc/point of contact in the logs/emails
- Ensure that page and limit cannot be negative
- Make the 'Give Up Commit Access' link working
- Add alembic to get DB schema change working

* Thu May 15 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.4-1
- Bump to 1.4
- Fix http link when editing ACLs
  https://fedorahosted.org/fedora-infrastructure/ticket/4362
- Fix ordering the branches in the ACL overview and editing page
  https://github.com/fedora-infra/pkgdb2/issues/36
- Speed up Package.search should reflect a bit everywhere including the API
- Enhance the critpath API to allow restricting for only one or more branches
  and let it return only Approved package
- More unit-tests
- Code cleaning

* Wed May 14 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.3-1
- Bump to 1.3
- Add the possibility to Cc one or more email addresses to every emails sent

* Wed May 14 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.2-1
- Bump to 1.2
- Fix the API to return provenpackagers where needed (should allow
  provenpackagers to create update for packages they do not own)
- Few layout bug and typos fixes
- Allow to not check the SSL cert for FAS
- Fix updating ACLs for @kevin
- Add koji_tag and dist_tag to the jsoin output of the Collections
- Let pkgdb admin review ACLs
- Show package status per branch

* Wed May 14 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.1-1
- Bump to 1.1
- Add a critpath filter in the list packages method of the API (for bodhi
  consumption)
- Fix bug in the pending ACLs to return them only on non-EOL collections

* Wed May 14 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.0-1
- Bump to release 1.0
- Add helping queries in the upgrade script
- Adjust the forms to show the mandatory fields

* Sat May 03 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.8-1
- Update to 0.8
- Rewrite of the ACL overview page
- Rewrite of the update ACL mechanism
- Fix redirect issue

* Tue Apr 22 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.7-1
- Update to 0.7
- Distinguish the two notify api endpoint
- Add script to do branching in pkgdb2 (from one collection to another)
- Fix the /api/bugzilla json output to be fully backward compatible
- Install that script in /usr/share/pkgdb2

* Tue Apr 08 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.6-1
- Update to 0.6
- Update the api endpoint /api/notify to list only people with commit and
  approveacls ACL
- Fix the backward compatibility for this endpoint
- Add api endpoint /api/notify/all to list all people having at least one ACLs
  for each package
- Change the branchname format from F-x to fx
- Getride of the git_branch_name option in the collection table
- Add `eol` argument in the api endpoint /api/vcs use to include as well data
  for eol'd release
- Document the extras api endpoints in the api documentation

* Tue Mar 18 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.5-1
- Update to 0.5
- Add support for the ``poc`` argument in the packager endpoint of the API
- Improved unit-tests
- Make sure the total_page if always returned on all pages that are paginated

* Thu Mar 13 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.4-1
- Update to 0.4
- Add support for the ``eol`` argument in the API, this argument allows
  retrieving information for all collections (including EOL'd ones) in
  the API.

* Thu Mar 13 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.3-1
- Update to 0.3
- The packager API now allows to filter for some ACLs only

* Tue Mar 11 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.2.1-1
- Update to 0.2.1
- Fix documentation for /api/package/

* Tue Mar 11 2014 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.2-1
- Update to 0.2
- Let /api/package/ allow filter for multiple branches

* Wed Nov 27 2013 Pierre-Yves Chibon <pingou@pingoured.fr> - 0.1.0-1
- Initial packaging work for Fedora
