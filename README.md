# reMarkable template

A python3 script to upload a template to the reMarkable. It will ask for the reMarkable ssh password.

By default it uses the "usb" ssh IP 10.11.99.1 meaning that you need to connect the reMarkable through usb. You can change this to use network ssh IP by declaring the variable ```rm_ip``` in

## Installation
Run ```pip install -r requirements.txt ``` 

## Usage
```
python3 add_template <path_to_template>
```