<img src="https://1.bp.blogspot.com/-N-XwxleEyOo/WYQEtqUZGnI/AAAAAAAAwRI/Klh5vIblR_EzyXjHsm1zh5WP3hWZMaciACLcBGAs/s1600/SRM%2BLogo.png" height=70>

# QR Code Generator

This is a simple QR code generator built using Flask. This project is for my PPS(Programming for Problem Solving).

## Table of Contents

* [Screenshots](#screenshots)
* [API](#api)
* [Installation](#installation)
* [Authors](#authors)

## Screenshots

![Screenshot 1](./screenshots/screenshots-1.png)

## API

Example: `http://localhost:5000?url=https://mbarde.de&boxsize=50`

Expected parameters:

* `url`: URL to "qr-encode"
* `size` (optional): Size (width & height) of resulting QR code image
* `boxsize` (optional): Size of single box of the QR code (when `size` is set as well, this is the size of each box *before* image gets resized)
* `fill` (optional): Hex code for fill color (without `#`)
* `back` (optional): Hex code for background color (without `#`)

## Installation

```bash
git clone https://github.com/mantreshkhurana/qr-code-geneartor-mini-project-sem-1.git
cd qr-code-geneartor-mini-project-sem-1
pip install -r requirements.txt
python app.py
```

## Authors

* [Mantresh Kumar | RA2311003011417](https://github.com/mantreshkhurana)
* Arpit Mohan Saxena | RA2311003011378
