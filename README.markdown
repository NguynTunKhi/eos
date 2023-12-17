## Ghi chú khi clone về thì để run được
1. Tải về thư mục gluon/* server hoặc copy từ web2py 2.17.2 down từ trang chủ
2. Sửa applications/eos/private_default/ thành applications/eos/private/
3. Chỉnh lại các biến user:pass:ip, ... trong applications/eos/private/appconfig.ini
4. Run by pthon web2py
5. Chạy lệnh để run các schedule:
- su web2py
- /usr/bin/python /var/www/web2py/web2py.py -K eos &
- Code thì ở /applications/eos/models/scheduler.py
-

## Readme

web2py is a free open source full-stack framework for rapid development of fast, scalable, secure and portable database-driven web-based applications.

It is written and programmable in Python. LGPLv3 License

Learn more at http://web2py.com

## Google App Engine deployment

    cp examples/app.yaml ./
    cp handlers/gaehandler.py ./

Then edit ./app.yaml and replace "yourappname" with yourappname.

## Important reminder about this GIT repo

An important part of web2py is the Database Abstraction Layer (DAL). In early 2015 this was decoupled into a separate code-base (PyDAL). In terms of git, it is a sub-module of the main repository.

The use of a sub-module requires a one-time use of the --recursive flag for git clone if you are cloning web2py from scratch.

    git clone --recursive https://github.com/web2py/web2py.git

If you have an existing repository, the commands below need to be executed at least once:

    git submodule update --init --recursive

If you have a folder gluon/dal you must remove it:

    rm -r gluon/dal

PyDAL uses a separate stable release cycle to the rest of web2py. PyDAL releases will use a date-naming scheme similar to Ubuntu. Issues related to PyDAL should be reported to its separate repository.


## Documentation (readthedocs.org)

[![Docs Status](https://readthedocs.org/projects/web2py/badge/?version=latest&style=flat-square)](http://web2py.rtfd.org/)

## Tests

[![Build Status](https://img.shields.io/travis/web2py/web2py/master.svg?style=flat-square&label=Travis-CI)](https://travis-ci.org/web2py/web2py)
[![MS Build Status](https://img.shields.io/appveyor/ci/web2py/web2py/master.svg?style=flat-square&label=Appveyor-CI)](https://ci.appveyor.com/project/web2py/web2py)
[![Coverage Status](https://img.shields.io/codecov/c/github/web2py/web2py.svg?style=flat-square)](https://codecov.io/github/web2py/web2py)


## Installation Instructions

To start web2py there is NO NEED to install it. Just unzip and do:

    python web2py.py

That's it!!!

## web2py directory structure

    project/
        README
        LICENSE
        VERSION                    > this web2py version
        web2py.py                  > the startup script
        anyserver.py               > to run with third party servers
        ...                        > other handlers and example files
        gluon/                     > the core libraries
            packages/              > web2py submodules
              dal/
            contrib/               > third party libraries
            tests/                 > unittests
        applications/              > are the apps
            admin/                 > web based IDE
                ...
            examples/              > examples, docs, links
                ...
            welcome/               > the scaffolding app (they all copy it)
                ABOUT
                LICENSE
                models/
                views/
                controllers/
                sessions/
                errors/
                cache/
                static/
                uploads/
                modules/
                cron/
                tests/
            ...                    > your own apps
        examples/                  > example config files, mv .. and customize
        extras/                    > other files which are required for building web2py
        scripts/                   > utility and installation scripts
        handlers/
            wsgihandler.py         > handler to connect to WSGI
            ...                    > handlers for Fast-CGI, SCGI, Gevent, etc
        site-packages/             > additional optional modules
        logs/                      > log files will go in there
        deposit/                   > a place where web2py stores apps temporarily

## Issues?

Report issues at https://github.com/web2py/web2py/issues

# ENV:
* `APP_SIDE`=`TW`/`LOCAL_DP`
* `ENV_PASSWORD_BASIC_AUTH_API` env for password basic auth internal api
* `ENV_USER_BASIC_AUTH_API` env for password basic auth internal api
* `ENV_MONGO_DB_NAME` eos db name

# How To
## Manage separate function TW and local_dp:
Manage by env `APP_SIDE`:
* `LOCAL_DP`: for deploy app on local(địa phương)
* `TW`: for deploy app on TW(trung ương)

Feature only for TW, not for LocalDP:
* View all and Approve request indicator

## How to add more feature permissions
In file `applications/eos/modules/const.py`:
* Step 1: Add new feature to `SYS_PERMISSION`. Example:
    ```python
        # QuanLyYeuCauTaoThongSo
        "request_indicators": {'name': 'Request indicators', 'rules': RULES_ACTION['SETTING']['REQUEST_INDICATOR'],
                               'seq': 61},
    ```
* Step 2: Add new permissions to `RULES_ACTION`. Example:
  ```python
          'REQUEST_INDICATOR': {
              'VIEW': {'value': 'view', 'name': 'Permission_View', 'seq': 1},
              'APPROVE': {'value': 'approve', 'name': 'Permission_Approve', 'seq': 3},
          },
  ```
* Step 3: Go to `http://localhost:8000/eos/permissions/index?group_id=30971739552335706296452950778` to check new feature permissions

## reset du lieu 
db.getCollection("last_data_files").updateMany({} , {$set : {lasttime: ISODate("2019-05-16T21:11:00.000+0000")} })
db.getCollection("stations").updateMany({} , {$set : {last_time: ISODate("2019-05-16T21:11:00.000+0000") , last_file_name :"" , status : 4} })
db.getCollection("latest_time_data_import").updateMany({station_id :{$in : ["31068514952546253133648148424" , "31069608475534942635867948574" , "31069611703715155535039481425" , "31069636256331517642452682827"]}} , {$set :{latest_time : ISODate("2022-05-17T03:05:00.000+0000")}})


## Run EOS Workers:
**Can create many workers**
```shell
  web2py.py -K eos
```
