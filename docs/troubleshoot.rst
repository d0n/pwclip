Troubleshoot
------------

There are currently no known issues

Obsolete:

When using the yubikey challenge-response mode there is a bug in the usb_hid
interface. This is because of python2 => 3 transition most likely and can be
fixed by executing the following command:

``sudo vi +':107s/\(.* =\).*/\1 response[0]/' +':wq' /usr/local/lib/python3.5/dist-packages/yubico/yubikey_4_usb_hid.py``

Explained:

In line 107 of the file

``/usr/local/lib/python3.5/dist-packages/yubico/yubikey_4_usb_hid.py``

the ord() coversion of the response:

``r_len = ord(response[0])``

needs to be replaced by:

``r_len = response[0]``**
