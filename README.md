SRS milter plugin for postfix and sendmail
==========================================

This milter implemets SRS (Sender Rewriting Scheme) that can be used to fix envelope MAIL FROM for forwarded mails protected by SPF. It can be configured in two modes for:

* Incoming mail - rewrite RCPT TO addresses in SRS format back
* Outgoing mail - rewrite MAIL FROM address to SRS format

SRS secrets can be provided securely inside a file. For quick testing and backwards compatibility with old configurations, they can still be provided insecurely on the command line.

Dependencies
------------

* postfix 2.5 or sendmail 8.14 -- supports SMFIF_CHGFROM
* libmilter -- compatible with sendmail 8.14.0 and higher
* libspf2 -- to be able to rewrite only outgoing addresses that can be rejected by SPF checks on final MTA
* libsrs2 -- for SRS address rewriting

Both libraries contain several patches that are not part of official source code but comes from different distributions (debian, freebsd).

Installation
------------

### Building srs-milter from sources

* clone github srs-milter repository
  ```
  git clone https://github.com/vokac/srs-milter
  ```
* instlall libspf2, libsrs2 and libmilter devel packages
* compile sources with `cmake` in base directory (or just `make` in source directory)
* startup script/unit available in `dist` subdirectory

### RPM packages

Source and binary packages for RHEL/CentOS/Fedora available in repositories at http://copr.fedoraproject.org/coprs/vokac/srs-milter/

Configuration
-------------

### Command line arguments and configuration file

You can specify configuration options as command line arguments or in a configuration file. List of all available parameters can be obtained executing `srs-filter --help`. Configuration files supports only long version of the command line arguments and these commands starts `srs-filter` daemon with same configuration:

```
# use command line arguments to configure srs-filter
srs-filter --verbose --daemon --socket=inet:1234@localhost --reverse --forward \
      --local-domain=example.com --srs-domain=srs.example.com --srs-secret=secret
```

```
# use config file to configure srs-filter
srs-filter --config=/etc/srs-milter.conf
# content of the configuration file /etc/srs-milter.conf
verbose
daemon
socket=inet:1234@localhost
reverse
forward
local-domain=example.com
srs-domain=srs.example.com
srs-secret=secret
```



### Incomming mail:

* Start srs-milter in reverse mode
  ```
  srs-filter --socket=inet:10044@localhost --reverse \
      --local-domain=example.com --local-domain=.allsubdomain.example.com \
      --srs-domain=srs.example.com --srs-secret-file=/etc/srs-secrets \
      -P /var/run/srs-filter1.pid
  ```

* Configure Postfix to use the milter in main.cf
  ```
  smtpd_milters = inet:localhost:10044
  ```

* NOTE: You should also add new hash entry to your `local_recipient_maps` directive to ensure Postfix treats SRS address as valid addresses. Without this, SRS addresses will never reach srs-milter for decoding because Postfix will immediately reject the address as non-existent. Your new directive might look something like this (this is actually the Postfix default with the new hash added):
  ```
  local_recipient_maps = proxy:unix:passwd.byname $alias_maps hash:/etc/postfix/srsdomain
  ```
  And `/etc/postfix/srsdomain` would contain your full SRS domain - the second value after the entry is ignored for `local_recipient_maps` so a hyphen is fine:
  ```
  @srsdomain.com -
  ```

* Configure sendmail to use the milter in your mc file
  ```
  INPUT_MAIL_FILTER(`milter-srs', `S=inet:10044@localhost, F=T, T=S:360s;R:360s;E:15m')dnl
  ```

* NOTE: you don't need any other configuration in sendmail if you use the milter in forward mode.

### Outgoing mail:

* Start srs-milter in forward mode
  ```
  srs-filter --socket=inet:10043@localhost --forward \
      --local-domain=example.com --local-domain=.allsubdomain.example.com \
      --srs-domain=srs.example.com --srs-secret-file=/etc/srs-secrets \
      --spf-check \
      -P /var/run/srs-filter0.pid
  ```

* Configure Postfix to use the milter in main.cf
  ```
  smtpd_milters = inet:localhost:10044
  ```

* NOTE: If you use virtual_alias_maps for outgoing mails to change recipient address you can't use same smtpd with srs-milter (it doesn't see changes from rewriting virtual aliases). In main.cf you can define new smtpd that listens on different port and forward all outgoing mails throught this smtpd configured with srs-milter.

* Configure sendmail to use the milter in your mc file
  ```
  INPUT_MAIL_FILTER(`milter-srs', `S=inet:10044@localhost, F=T, T=S:360s;R:360s;E:15m')dnl
  ```

* NOTE: You need to make sure sendmail accepts the SRS address as a valid address. You can achieve this by
  allowing relay access to your SRS domain in /etc/mail/access for example.

Service startup
---------------

SysV initscript (service configuration via /etc/sysconfig/srs-milter):
  ```
  # enable srs-milter service
  /sbin/chkconfig srs-milter on
  # start srs-milter service
  /sbin/service srs-milter start
  ```

Systemd (service configuration via /etc/srs-milter.*.conf files):
  ```
  # enable srs-milter service
  systemctl enable srs-milter@default
  # start srs-milter service
  systemctl start srs-milter@default
  ```

Other notes
-----------

Unfortunatelly it is neccessary to have some basic understanding how SPF/SRS works to be able to configure and plug this milter in your mailserver configuration.

Althought original code was just quick hack to fix mail forwarding to sites that started to force SPF validation and the source code is not always perfectly readable it seems to be pretty stable.

Contributors
------------

[vokac](https://github.com/vokac) ([Original author](http://kmlinux.fjfi.cvut.cz/~vokacpet/activities/srs-milter/))<br>
[emsearcy](https://github.com/emsearcy)<br>
[Driskell](https://github.com/driskell) &lt;packages at jasonwoods me uk&gt;
