# FDsploit [![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/chrispetrou/FDsploit/blob/master/LICENSE) [![](https://img.shields.io/badge/Made%20with-python-yellow.svg)](https://www.python.org/)

`FDsploit` is a File inclusion & Directory Traversal fuzzer, enumeration & exploitation tool.

<img src="images/FDsploit.png" width="70%">

`FDsploit` can be used to discover Local/Remote File Inclusion and directory traversal vulnerabilities automatically. In case an LFI vulnerability is found, `--lfishell` option can be used to exploit it. For now, __3__ different types of LFI shells are supported:

*   `simple`: This type of shell allows user to read files easily without having to type the url everytime. __Also__ it only provides the output of the file and __not__ the whole html-source code of the page which makes it very useful.
*   `expect`: This type of shell is a semi-interactive shell which allows user to execute commands through PHP's `expect://` wrapper.
*   `input`: This type of shell is a semi-interactive shell which also allows user to execute commands through PHP's `php://input` stream.

So far, there are only two lfi-shell built-in commands:
*   `clear` and
*   `exit`.

### Features

*   The LFI-shell interface provides only the output of the file readed or the command issued and __not__ all the html code.
*   __3__ different types of LFI-shells can be specified.
*   Both GET/POST requests are supported.
*   Automatic detection of GET parameters.
*   Certain parameters can be specified for testing using wildcards (`*`).
*   Optional session cookies can be specified and used.
*   Automatic check for RCE using PHP functions can be performed.
*   Additional use of sha-256 hash is used to identify the potential vulnerabilities.
*   base64/urlencoding support.

### Some Examples

#### 1. Directory traversal vulnerability discovery:

From the below output it seems that the `directory` parameter is probably vulnerable to directory traversal vulnerability since every request with `../` as payload produces a different _sha-256_ hash. Also the content-length is different for every request:

```python
./fdsploit.py -u 'http://127.0.0.1:8888/test/bWAPP/bWAPP/rlfi.php?language=fsd&action=go' -c 'PHPSESSID=a55475b0abccbf3b32fab4c95a98c3ab; security_level=0' -d 7
```
<img src="images/directory_traversal.png" width="70%">

#### 2. LFI vulnerability discovery:

Again, the language parameter seems vulnerable to LFI since every request being colored with green produces a different hash, a different content-length from the initial, and the keyword specified is found in the response:

```python
./fdsploit.py -u 'http://127.0.0.1:8888/test/bWAPP/bWAPP/rlfi.php?language=fsd&action=go' -c 'PHPSESSID=a55475b0abccbf3b32fab4c95a98c3ab; security_level=0' -d 7 -k root -p /etc/passwd
```
<img src="images/lfi.png" width="70%">

#### 3. LFI simple shell:

Exploiting the above LFI using `simple` shell:

<img src="images/simpleshell.png" width="70%">

### Notes

1.  When `POST` verb is used, `--params` option must also be specified.
2.  To test for _Directory Traversal_ vulnerability the `--payload` option must be left to default value (_None_).
3.  When `--file` options is used for multiple-urls testing, then only GET request is supported.
4.  When __both__ `--file` & `--cookie` options are set then since only one cookie can be specified each time the urls must refer on the same domain or be accessible without a cookie (_that's is going to be fixed in a future update_).
5.  `input` shell is not compatible with `POST` verb.

### Requirements:

**Note:** To install the requirements:

`pip install -r requirements.txt --upgrade --user`

### TODO
- [ ] Fix _note 4_ from above and make `--file` also work with POST parameters and cookies, using probably a `json` etc... file as input.
- [ ] Add more built-in commands to `--lfishell` e.g. history etc...

### Contributions & Feedback

Feedback and contributions are welcome. If you find any bug or have a feature request feel free to open an issue, and as soon as I review it I'll try to fix it!

### Disclaimer
>This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software in general.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details