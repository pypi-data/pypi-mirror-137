<div id="top"></div>

<div align="center">

  <h3 align="center">cloudos-webdav-server</h3>
  <p align="center">
    An easy-to-use webdav server written in python.
</p>
</div>




## About The Project

A webdav server that can be mounted as local drive. It can be accessed from remote client, eg. a javascript client in frontend webpage.
          
### Built With

* [wsgidav](https://github.com/mar10/wsgidav)
* [sqlitedict](https://github.com/RaRe-Technologies/sqlitedict)
* [fire](https://github.com/google/python-fire)
* [pkman](https://gitee.com/peiiii/pkman)


## Getting Started

1. Install this package `pip install cloudos-webdav-server`
2. Run command `cws run --host=127.0.0.1 --port=8004 --root=./ --dc_data_source=./data.db`, 
where dc_data_source is the auto-created sqlite file path for data storage.
3. To visit users' files in browser, open `http://localhost:8004/u1` in your browser, login with default test user (username:`u1`,password:`u1`), this page is for serving files on web page.
4. You can mount user's file storage as local operating system. For example, on windows' file explorer,
you can mount user `u1`'s storage(with url: `http://localhost/u1`,username:`u1`, password:`u1`). Just google it if you don't know how to mount a webdav on your operating system.
5. To add more users: 
   1. Create a new folder inside root path with the username as folder name.
   2. Add access information into the sqlite db file for data storage.
       ```python
       import sqlitedict
       db=sqlitedict.SqliteDict("./data.db")
       db.update({
           "/u1":{
               "u1":{
                   "password":"u1"
               },
               "you-can-add-another-user":{
                   "password":"123"
               }
           },
           "/another-public-realm":True
       })
       ```


### Prerequisites

* python>=3.5

### Installation
```shell
pip install cloudos-webdav-server
```

## Usage
see chapter [Getting Started](#Getting Started)


## Roadmap

- [ ] Add Additional Templates w/ Examples

See the [open issues](https://gitee.com/peiiii/cloudos-webdav-server/issues) for a full list of proposed features (and known issues).

## Contributing


1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License.

## Contact
Wang Pei - 1535376447@qq.com
Project Link: [https://gitee.com/peiiii/cloudos-webdav-server](https://gitee.com/peiiii/cloudos-webdav-server)

## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [wsgidav](https://github.com/mar10/wsgidav)
* [fire](https://github.com/google/python-fire)

<p align="right">(<a href="#top">back to top</a>)</p>



